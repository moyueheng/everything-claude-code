---
name: python-async-modernizer
description: 分析和现代化 Python 异步代码。当用户需要：(1) 检查代码仓库中的异步代码质量问题，(2) 将旧版 asyncio 代码迁移到现代模式 (Python 3.11+)，(3) 检测阻塞调用和异步反模式，(4) 重构代码使用 TaskGroup 和结构化并发，(5) 优化异步性能时使用此技能。
---

# Python Async Modernizer

分析和现代化 Python 异步代码的专业工具。

## 工作流程

```
1. 扫描分析 → 2. 问题识别 → 3. 生成方案 → 4. 执行重构
```

### 第一步：扫描分析

运行分析脚本检测代码质量问题：

```bash
python scripts/analyze_async.py <路径> -f markdown -o report.md
```

分析内容包括：
- 阻塞调用 (`time.sleep`, `requests`, 同步文件 I/O)
- 未 await 的协程
- 过时的 asyncio API (`get_event_loop`, `ensure_future`)
- 缺少异常处理的 `gather()`
- 无限制并发

### 第二步：问题识别

根据分析结果分类问题严重程度：

| 级别 | 问题类型 | 示例 |
|------|----------|------|
| 🔴 Critical | 阻塞事件循环 | `time.sleep()` 在 async 函数中 |
| 🔴 Critical | 未 await 协程 | `fetch_data()` 没有 await |
| 🟡 Warning | 过时 API | `asyncio.get_event_loop()` |
| 🟡 Warning | 异常处理不当 | `gather()` 无 `return_exceptions` |
| 🔵 Info | 可优化模式 | 使用 `TaskGroup` 替代 `gather` |

### 第三步：生成改造方案

针对检测到的问题生成具体改造方案：

**阻塞调用替换:**
- `time.sleep()` → `await asyncio.sleep()`
- `requests.get()` → `aiohttp.ClientSession.get()`
- `open()` → `aiofiles.open()`
- `sqlite3.connect()` → `aiosqlite.connect()`

**模式升级:**
- `asyncio.gather()` → `asyncio.TaskGroup` (Python 3.11+)
- `asyncio.wait_for()` → `asyncio.timeout()` (Python 3.11+)
- `try/except Exception` → `except* ExceptionGroup` (Python 3.11+)

### 第四步：执行重构

按照优先级执行代码重构：

1. **修复 Critical 问题** - 阻塞调用和未 await 协程
2. **更新过时 API** - 替换已弃用的 asyncio 函数
3. **现代化模式** - 采用 TaskGroup 和结构化并发
4. **添加类型注解** - 完善异步函数类型

## 核心能力

### 1. 检测阻塞调用

识别在异步函数中使用的同步阻塞操作：

```python
# 检测到的反模式
async def bad():
    time.sleep(1)  # 阻塞!
    requests.get(url)  # 阻塞!
    open('file.txt').read()  # 阻塞!
```

### 2. 协程管理检查

检测未正确管理的协程：

```python
# 未 await
async def bad():
    fetch_data()  # 协程被创建但从未执行

# 修复
async def good():
    await fetch_data()
```

### 3. 现代化重构

将旧模式升级到 Python 3.11+ 标准：

```python
# 旧模式
async def old():
    tasks = [asyncio.create_task(fetch(i)) for i in items]
    results = await asyncio.gather(*tasks, return_exceptions=True)

# 现代模式
async def modern():
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(i)) for i in items]
    results = [t.result() for t in tasks]
```

### 4. 异常处理改进

使用 ExceptionGroup 处理多个并发异常：

```python
# 旧模式
async def old():
    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        # 只能捕获第一个异常
        pass

# 现代模式
async def modern():
    try:
        async with asyncio.TaskGroup() as tg:
            for t in tasks:
                tg.create_task(t)
    except* ValueError as eg:
        for e in eg.exceptions:
            logger.error(f"Value error: {e}")
    except* TypeError as eg:
        for e in eg.exceptions:
            logger.error(f"Type error: {e}")
```

## 参考文档

- **反模式目录**: [references/anti-patterns.md](references/anti-patterns.md) - 完整的反模式列表和修复方案
- **现代模式指南**: [references/modern-patterns.md](references/modern-patterns.md) - Python 3.11+ 最佳实践

## 使用示例

### 分析整个项目

```bash
python scripts/analyze_async.py ./my_project -f markdown -o async_report.md
```

### 分析单个文件

```bash
python scripts/analyze_async.py ./my_project/api.py -f json
```

### 在代码中调用

```python
from scripts.analyze_async import analyze_directory, generate_report

results = analyze_directory(Path('./src'))
report = generate_report(results, 'markdown')
print(report)
```

## 输出格式

### JSON 格式

```json
{
  "summary": {
    "total_files": 42,
    "files_with_async": 15,
    "total_issues": 23,
    "critical_issues": 5,
    "warnings": 18
  },
  "files": [
    {
      "path": "src/api.py",
      "has_async_code": true,
      "async_functions": ["fetch_data", "process"],
      "issues": [
        {
          "line": 23,
          "type": "blocking_call_in_async",
          "severity": "critical",
          "message": "在异步函数中使用了阻塞调用 'time.sleep'",
          "suggestion": "使用 asyncio.sleep 替代"
        }
      ]
    }
  ]
}
```

### Markdown 格式

生成人类可读的报告，包含：
- 执行摘要
- 按文件分类的问题列表
- 具体修复建议
- 代码示例

## 注意事项

1. **Python 版本**: TaskGroup 和 ExceptionGroup 需要 Python 3.11+
2. **第三方库**: 某些修复需要安装异步库 (aiohttp, aiofiles, aiosqlite 等)
3. **测试**: 重构后务必运行测试验证功能正确性
4. **渐进式**: 建议分阶段重构，先修复 Critical 问题

## 相关工具

- **pyright**: 微软的 Python 类型检查器，对异步代码支持优秀
  ```bash
  # pyproject.toml
  [tool.pyright]
  typeCheckingMode = "strict"
  ```
- **ruff**: 启用 ASYNC 规则检测异步反模式
  ```bash
  # pyproject.toml
  [tool.ruff.lint]
  select = ["ASYNC"]
  ```
- **pytest-asyncio**: 测试异步代码
  ```toml
  # pyproject.toml
  [tool.pytest.ini_options]
  asyncio_mode = "strict"
  ```
