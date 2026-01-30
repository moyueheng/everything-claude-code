#!/usr/bin/env python3
"""
Python 异步代码分析器
检测代码仓库中的异步反模式和低质量代码
"""

import ast
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
import json


@dataclass
class AsyncIssue:
    """异步代码问题"""

    file_path: str
    line_number: int
    issue_type: str
    severity: str  # critical, warning, info
    message: str
    suggestion: str
    original_code: str = ""


@dataclass
class AnalysisResult:
    """分析结果"""

    file_path: str
    issues: List[AsyncIssue] = field(default_factory=list)
    has_async_code: bool = False
    async_functions: List[str] = field(default_factory=list)
    sync_blocking_calls: List[Dict] = field(default_factory=list)


class AsyncCodeAnalyzer(ast.NodeVisitor):
    """AST 分析器，用于检测异步代码问题"""

    # 阻塞调用映射表
    BLOCKING_CALLS = {
        # 时间相关
        "time.sleep": {"replacement": "asyncio.sleep", "context": "async"},
        # HTTP 请求
        "requests.get": {
            "replacement": "aiohttp.ClientSession.get 或 httpx.AsyncClient.get",
            "context": "async",
        },
        "requests.post": {
            "replacement": "aiohttp.ClientSession.post 或 httpx.AsyncClient.post",
            "context": "async",
        },
        "requests.put": {
            "replacement": "aiohttp.ClientSession.put 或 httpx.AsyncClient.put",
            "context": "async",
        },
        "requests.delete": {
            "replacement": "aiohttp.ClientSession.delete 或 httpx.AsyncClient.delete",
            "context": "async",
        },
        "requests.request": {"replacement": "aiohttp 或 httpx", "context": "async"},
        # 文件 I/O
        "open": {"replacement": "aiofiles.open", "context": "async"},
        "file.read": {"replacement": "await f.read()", "context": "async"},
        "file.write": {"replacement": "await f.write()", "context": "async"},
        # 数据库 (常见同步驱动)
        "sqlite3.connect": {"replacement": "aiosqlite.connect", "context": "async"},
        "psycopg2.connect": {
            "replacement": "asyncpg.connect 或 psycopg (v3 async)",
            "context": "async",
        },
        "pymongo.MongoClient": {
            "replacement": "motor.motor_asyncio.AsyncIOMotorClient",
            "context": "async",
        },
        "redis.Redis": {"replacement": "redis.asyncio.Redis", "context": "async"},
        # 子进程
        "subprocess.run": {
            "replacement": "asyncio.create_subprocess_exec",
            "context": "async",
        },
        "subprocess.call": {
            "replacement": "asyncio.create_subprocess_exec",
            "context": "async",
        },
        "subprocess.check_output": {
            "replacement": "asyncio.create_subprocess_exec",
            "context": "async",
        },
        "os.system": {
            "replacement": "asyncio.create_subprocess_exec",
            "context": "async",
        },
        # SMTP
        "smtplib.SMTP": {"replacement": "aiosmtplib.SMTP", "context": "async"},
        # DNS 解析
        "socket.getaddrinfo": {
            "replacement": "asyncio.getaddrinfo",
            "context": "async",
        },
        "socket.gethostbyname": {
            "replacement": "asyncio.getaddrinfo",
            "context": "async",
        },
    }

    # 过时的 asyncio API
    DEPRECATED_APIS = {
        "asyncio.get_event_loop": {
            "replacement": "asyncio.get_running_loop() 或 asyncio.run()",
            "reason": "在 Python 3.10+ 中不推荐使用",
        },
        "asyncio.coroutine": {
            "replacement": "async def",
            "reason": "Python 3.5+ 使用 async/await 语法",
        },
        "asyncio.ensure_future": {
            "replacement": "asyncio.create_task",
            "reason": "create_task 更清晰且类型安全",
        },
    }

    def __init__(self, file_path: str, source: str):
        self.file_path = file_path
        self.source = source
        self.lines = source.split("\n")
        self.issues: List[AsyncIssue] = []
        self.async_functions: List[str] = []
        self.current_function: Optional[str] = None
        self.is_async_context: bool = False
        self.imported_names: Dict[str, str] = {}  # 别名映射

    def visit_Import(self, node: ast.Import):
        """记录导入"""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imported_names[name] = alias.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """记录 from import"""
        module = node.module or ""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imported_names[name] = f"{module}.{alias.name}"
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """访问异步函数定义"""
        self.current_function = node.name
        self.async_functions.append(node.name)
        self.is_async_context = True

        # 检查函数是否为空或只有 pass
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self._add_issue(
                node.lineno,
                "empty_async_function",
                "warning",
                f"异步函数 '{node.name}' 为空",
                "删除空函数或实现具体逻辑",
            )

        self.generic_visit(node)
        self.is_async_context = False
        self.current_function = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """访问同步函数定义"""
        prev_function = self.current_function
        prev_async = self.is_async_context
        self.current_function = node.name
        self.is_async_context = False

        # 检查函数是否返回协程但未标记为 async
        self.generic_visit(node)

        self.current_function = prev_function
        self.is_async_context = prev_async

    def visit_Call(self, node: ast.Call):
        """检测函数调用"""
        call_name = self._get_call_name(node)

        if not call_name:
            self.generic_visit(node)
            return

        # 检查是否在异步函数中使用了阻塞调用
        if self.is_async_context:
            self._check_blocking_call(node, call_name)

        # 检查过时的 asyncio API
        self._check_deprecated_api(node, call_name)

        # 检查 gather 的使用问题
        if "gather" in call_name:
            self._check_gather_usage(node)

        # 检查 create_task 问题
        if "create_task" in call_name:
            self._check_create_task_usage(node)

        self.generic_visit(node)

    def visit_Await(self, node: ast.Await):
        """检查 await 表达式"""
        # 检查 await 是否用于非协程
        if isinstance(node.value, ast.Call):
            call_name = self._get_call_name(node.value)
            if call_name and call_name in self.BLOCKING_CALLS:
                info = self.BLOCKING_CALLS[call_name]
                self._add_issue(
                    node.lineno,
                    "awaiting_blocking_call",
                    "critical",
                    f"await 了阻塞调用 '{call_name}'",
                    f"使用 {info['replacement']} 替代",
                )
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        """检查赋值语句"""
        # 检查是否创建了协程但未 await
        if isinstance(node.value, ast.Call):
            call_name = self._get_call_name(node.value)
            if call_name and self._is_coroutine_call(call_name):
                # 检查是否在异步上下文中
                if self.is_async_context:
                    self._add_issue(
                        node.lineno,
                        "unawaited_coroutine",
                        "critical",
                        f"协程 '{call_name}' 被创建但未 await",
                        f"添加 await 或使用 asyncio.create_task()",
                    )
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        """检查 for 循环"""
        if self.is_async_context:
            # 检查是否在异步函数中使用同步迭代
            if isinstance(node.iter, ast.Call):
                call_name = self._get_call_name(node.iter)
                if call_name and "async" not in call_name.lower():
                    # 可能是阻塞的迭代器
                    pass
        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr):
        """检查表达式语句"""
        # 检测裸协程调用（未 await）
        if isinstance(node.value, ast.Call):
            call_name = self._get_call_name(node.value)
            if call_name and self._is_coroutine_call(call_name):
                self._add_issue(
                    node.lineno,
                    "bare_coroutine_call",
                    "critical",
                    f"协程 '{call_name}' 被调用但未 await",
                    f"添加 await 前缀或使用 asyncio.create_task()",
                )
        self.generic_visit(node)

    def _get_call_name(self, node: ast.Call) -> Optional[str]:
        """获取函数调用的完整名称"""
        if isinstance(node.func, ast.Name):
            name = node.func.id
            return self.imported_names.get(name, name)
        elif isinstance(node.func, ast.Attribute):
            parts = []
            current = node.func
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
                full_name = ".".join(reversed(parts))
                # 检查是否有别名
                base = parts[-1]
                if base in self.imported_names:
                    return self.imported_names[base] + "." + ".".join(parts[:-1])
                return full_name
        return None

    def _is_coroutine_call(self, call_name: str) -> bool:
        """判断调用是否是协程"""
        coroutine_indicators = [
            "async",
            "fetch",
            "get",
            "post",
            "request",
            "query",
            "find",
            "load",
            "read",
            "write",
            "send",
            "recv",
            "connect",
            "close",
        ]
        return any(ind in call_name.lower() for ind in coroutine_indicators)

    def _check_blocking_call(self, node: ast.Call, call_name: str):
        """检查阻塞调用"""
        for pattern, info in self.BLOCKING_CALLS.items():
            if pattern in call_name or call_name.endswith(pattern.split(".")[-1]):
                self._add_issue(
                    node.lineno,
                    "blocking_call_in_async",
                    "critical",
                    f"在异步函数中使用了阻塞调用 '{call_name}'",
                    f"使用 {info['replacement']} 替代",
                    self._get_source_line(node.lineno),
                )
                return

    def _check_deprecated_api(self, node: ast.Call, call_name: str):
        """检查过时的 API"""
        for pattern, info in self.DEPRECATED_APIS.items():
            if pattern in call_name:
                self._add_issue(
                    node.lineno,
                    "deprecated_asyncio_api",
                    "warning",
                    f"使用了过时的 API '{call_name}'",
                    f"{info['reason']}，使用 {info['replacement']} 替代",
                )
                return

    def _check_gather_usage(self, node: ast.Call):
        """检查 gather 的使用"""
        # 检查是否使用了 return_exceptions
        has_return_exceptions = any(
            kw.arg == "return_exceptions"
            and isinstance(kw.value, ast.Constant)
            and kw.value.value is True
            for kw in node.keywords
        )

        if not has_return_exceptions:
            self._add_issue(
                node.lineno,
                "gather_without_exception_handling",
                "warning",
                "asyncio.gather() 没有设置 return_exceptions=True",
                "添加 return_exceptions=True 或使用 TaskGroup (Python 3.11+)",
            )

        # 建议升级到 TaskGroup
        self._add_issue(
            node.lineno,
            "consider_taskgroup",
            "info",
            "考虑使用 asyncio.TaskGroup 替代 gather",
            "TaskGroup 提供结构化并发和自动清理 (Python 3.11+)",
        )

    def _check_create_task_usage(self, node: ast.Call):
        """检查 create_task 的使用"""
        # 检查是否保存了任务引用
        # 这需要在父节点检查，简化处理
        pass

    def _add_issue(
        self,
        line: int,
        issue_type: str,
        severity: str,
        message: str,
        suggestion: str,
        original_code: str = "",
    ):
        """添加问题"""
        if not original_code and line > 0 and line <= len(self.lines):
            original_code = self.lines[line - 1].strip()

        self.issues.append(
            AsyncIssue(
                file_path=self.file_path,
                line_number=line,
                issue_type=issue_type,
                severity=severity,
                message=message,
                suggestion=suggestion,
                original_code=original_code,
            )
        )

    def _get_source_line(self, line: int) -> str:
        """获取源代码行"""
        if 0 < line <= len(self.lines):
            return self.lines[line - 1].strip()
        return ""


def analyze_file(file_path: Path) -> AnalysisResult:
    """分析单个 Python 文件"""
    result = AnalysisResult(file_path=str(file_path))

    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        analyzer = AsyncCodeAnalyzer(str(file_path), source)
        analyzer.visit(tree)

        result.issues = analyzer.issues
        result.async_functions = analyzer.async_functions
        result.has_async_code = len(analyzer.async_functions) > 0

    except SyntaxError as e:
        result.issues.append(
            AsyncIssue(
                file_path=str(file_path),
                line_number=e.lineno or 0,
                issue_type="syntax_error",
                severity="critical",
                message=f"语法错误: {e.msg}",
                suggestion="修复语法错误后再分析",
            )
        )
    except Exception as e:
        result.issues.append(
            AsyncIssue(
                file_path=str(file_path),
                line_number=0,
                issue_type="analysis_error",
                severity="warning",
                message=f"分析失败: {e}",
                suggestion="检查文件是否可访问",
            )
        )

    return result


def analyze_directory(
    directory: Path, exclude_patterns: List[str] = None
) -> List[AnalysisResult]:
    """分析整个目录"""
    exclude_patterns = exclude_patterns or [
        "venv",
        ".venv",
        "__pycache__",
        ".git",
        ".tox",
        ".pytest_cache",
        "node_modules",
    ]
    results = []

    for py_file in directory.rglob("*.py"):
        # 检查是否应该排除
        if any(pattern in str(py_file) for pattern in exclude_patterns):
            continue

        result = analyze_file(py_file)
        results.append(result)

    return results


def generate_report(results: List[AnalysisResult], output_format: str = "json") -> str:
    """生成分析报告"""
    if output_format == "json":
        report = {
            "summary": {
                "total_files": len(results),
                "files_with_async": sum(1 for r in results if r.has_async_code),
                "total_issues": sum(len(r.issues) for r in results),
                "critical_issues": sum(
                    1 for r in results for i in r.issues if i.severity == "critical"
                ),
                "warnings": sum(
                    1 for r in results for i in r.issues if i.severity == "warning"
                ),
            },
            "files": [],
        }

        for result in results:
            if result.issues or result.has_async_code:
                file_report = {
                    "path": result.file_path,
                    "has_async_code": result.has_async_code,
                    "async_functions": result.async_functions,
                    "issues": [
                        {
                            "line": issue.line_number,
                            "type": issue.issue_type,
                            "severity": issue.severity,
                            "message": issue.message,
                            "suggestion": issue.suggestion,
                            "code": issue.original_code,
                        }
                        for issue in result.issues
                    ],
                }
                report["files"].append(file_report)

        return json.dumps(report, indent=2, ensure_ascii=False)

    elif output_format == "markdown":
        lines = ["# Python 异步代码分析报告\n"]

        critical_count = sum(
            1 for r in results for i in r.issues if i.severity == "critical"
        )
        warning_count = sum(
            1 for r in results for i in r.issues if i.severity == "warning"
        )

        lines.append(f"## 摘要\n")
        lines.append(f"- 分析文件数: {len(results)}")
        lines.append(
            f"- 包含异步代码的文件: {sum(1 for r in results if r.has_async_code)}"
        )
        lines.append(f"- 严重问题: {critical_count}")
        lines.append(f"- 警告: {warning_count}\n")

        for result in results:
            if result.issues:
                lines.append(f"## {result.file_path}\n")
                for issue in result.issues:
                    emoji = {"critical": "🔴", "warning": "🟡", "info": "🔵"}[
                        issue.severity
                    ]
                    lines.append(
                        f"{emoji} **{issue.issue_type}** (第 {issue.line_number} 行)"
                    )
                    lines.append(f"   - 问题: {issue.message}")
                    lines.append(f"   - 建议: {issue.suggestion}")
                    if issue.original_code:
                        lines.append(f"   - 代码: `{issue.original_code}`")
                    lines.append("")

        return "\n".join(lines)

    return ""


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="分析 Python 异步代码质量")
    parser.add_argument("path", help="要分析的 Python 文件或目录")
    parser.add_argument(
        "-f", "--format", choices=["json", "markdown"], default="json", help="输出格式"
    )
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--exclude", nargs="+", default=[], help="要排除的目录模式")

    args = parser.parse_args()

    target = Path(args.path)

    if target.is_file():
        results = [analyze_file(target)]
    elif target.is_dir():
        results = analyze_directory(target, args.exclude)
    else:
        print(f"错误: 路径不存在 {target}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(results, args.format)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"报告已保存到: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
