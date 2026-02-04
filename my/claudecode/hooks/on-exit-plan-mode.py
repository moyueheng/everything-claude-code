#!/usr/bin/env python3
"""
ExitPlanMode hook - 当用户接受计划后自动触发 TDD 流程

上游 everything-claude-code 没有这个功能，这是一个创新的增强。
通过监听 ExitPlanMode 工具调用，在用户接受计划后自动注入 TDD 上下文。

环境变量控制：
- EXIT_PLAN_TDD_ENABLED=false  禁用此 hook
- EXIT_PLAN_TDD_MODE=strict      严格模式（默认）
- EXIT_PLAN_TDD_MODE=gentle      温和模式（仅提示）
"""

import json
import os
import sys
from pathlib import Path


def detect_project_type(cwd: str) -> str:
    """检测项目类型"""
    path = Path(cwd)

    # Python 项目
    if (
        (path / "pyproject.toml").exists()
        or (path / "requirements.txt").exists()
        or (path / "setup.py").exists()
    ):
        return "python"

    # Node/TypeScript 项目
    if (path / "package.json").exists():
        pkg = path / "package.json"
        if pkg.exists():
            content = pkg.read_text()
            if "typescript" in content.lower() or any(
                (path / "tsconfig.json").exists() for _ in [1]
            ):
                return "typescript"
        return "javascript"

    # Go 项目
    if (path / "go.mod").exists():
        return "go"

    return "unknown"


def get_tdd_context(project_type: str, mode: str = "strict") -> str:  # noqa: ARG001 - mode 参数保留用于未来扩展
    """根据项目类型生成 TDD 上下文"""

    base_context = """
【TDD 工作流已激活】

计划已被接受。现在必须严格按照以下 TDD 流程执行计划：

## TDD 执行流程 (RED → GREEN → REFACTOR)
"""

    if project_type == "python":
        test_framework = "pytest"
        coverage_cmd = "pytest --cov=src --cov-report=term-missing"
        test_file_pattern = "test_*.py"
    elif project_type == "typescript":
        test_framework = "vitest/jest"
        coverage_cmd = "npm test -- --coverage"
        test_file_pattern = "*.test.ts"
    elif project_type == "go":
        test_framework = "go test"
        coverage_cmd = "go test -cover ./..."
        test_file_pattern = "*_test.go"
    else:
        test_framework = "请手动配置"
        coverage_cmd = "请手动配置"
        test_file_pattern = "请手动配置"

    workflow = f"""
### 阶段 1: RED - 编写失败测试
1. 根据计划中的功能点，先建立接口/类型骨架
2. 为每个功能编写失败的测试用例：
   - 正常路径 (happy path)
   - 边界值 (edge cases)
   - 错误路径 (error cases)
3. 运行测试，确认失败原因正确（"尚未实现/逻辑缺失"）

测试框架: {test_framework}
测试文件模式: {test_file_pattern}

### 阶段 2: GREEN - 最小实现
1. 只写足够通过测试的最小代码
2. 不要过度设计，不要考虑未来需求
3. 运行测试，全部变绿

### 阶段 3: REFACTOR - 重构
1. 消除重复代码
2. 改进命名和可读性
3. 优化结构和性能
4. **确保测试保持绿色**

### 阶段 4: 覆盖率检查
- 运行: `{coverage_cmd}`
- 最低要求: 80% 覆盖率
- 核心逻辑/安全关键代码: 100% 覆盖率

## 执行规则

✅ **必须遵循**:
1. 先写测试，再写实现 - 绝不跳过 RED 阶段
2. 一次只实现一个功能点
3. 每个功能完成后立即运行测试
4. 重构前必须确保测试全绿
5. 覆盖率不达标时补充测试

❌ **禁止**:
- 一次性编写多个功能的实现
- 在测试失败时进行重构
- 跳过测试直接实现
- 编写没有对应测试的代码

## 开始执行

现在，请识别计划中的第一个最小功能点，开始 RED 阶段：编写失败测试。
"""

    return base_context + workflow


def main():
    # 从 stdin 读取 hook 输入
    input_data = json.load(sys.stdin)

    tool_name = input_data.get("tool_name", "")
    _ = input_data.get("tool_input", {})  # 保留用于未来扩展
    cwd = input_data.get("cwd", "")

    # 只处理 ExitPlanMode 工具
    if tool_name != "ExitPlanMode":
        print(json.dumps({}))
        return

    # 检查环境变量是否禁用
    if os.environ.get("EXIT_PLAN_TDD_ENABLED", "true").lower() == "false":
        print(json.dumps({}))
        return

    # 获取模式
    mode = os.environ.get("EXIT_PLAN_TDD_MODE", "strict")

    # 检测项目类型
    project_type = detect_project_type(cwd)

    # 生成 TDD 上下文
    tdd_context = get_tdd_context(project_type, mode)

    # 添加项目类型提示
    if project_type != "unknown":
        project_hint = f"\n[检测到项目类型: {project_type}]\n"
        tdd_context = project_hint + tdd_context

    # 构建 hook 输出
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": tdd_context,
        }
    }

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
