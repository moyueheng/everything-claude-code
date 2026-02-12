# LangChain 内置 Middleware 详解

## Provider-Agnostic Middleware（通用）

### SummarizationMiddleware

自动在接近 token 限制时总结对话历史。

**适用场景**:
- 长对话超出上下文窗口
- 多轮对话需要保留历史
- 需要压缩旧上下文同时保留最新消息

**配置参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `model` | str/BaseChatModel | 是 | - | 用于生成总结的模型 |
| `trigger` | ContextSize/list | 否 | None | 触发条件 |
| `keep` | ContextSize | 否 | ("messages", 20) | 保留的上下文量 |
| `token_count_method` | str | 否 | "approximate" | token 计数方法 |
| `summary_prompt` | str | 否 | 内置模板 | 自定义总结提示 |
| `max_summary_tokens` | int | 否 | - | 总结最大 token 数 |

**示例**:

```python
from langchain.agents.middleware import SummarizationMiddleware

# 单条件触发
SummarizationMiddleware(
    model="gpt-4.1-mini",
    trigger=("tokens", 4000),
    keep=("messages", 20),
)

# 多条件 OR 触发
SummarizationMiddleware(
    model="gpt-4.1-mini",
    trigger=[("tokens", 3000), ("messages", 6)],
    keep=("messages", 20),
)

# 使用比例
SummarizationMiddleware(
    model="gpt-4.1-mini",
    trigger=("fraction", 0.8),
    keep=("fraction", 0.3),
)
```

---

### HumanInTheLoopMiddleware

在工具调用执行前暂停等待人工审批。

**适用场景**:
- 高风险操作需要人工确认
- 合规要求人工监督
- 长对话需要人工反馈引导

**配置参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `interrupt_on` | dict | 是 | 工具名到中断配置的映射 |

**interrupt_on 格式**:

```python
{
    "tool_name": {
        "allowed_decisions": ["approve", "edit", "reject"],  # 可选
    },
    "safe_tool": False,  # 不中断
}
```

**完整示例**:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware

agent = create_agent(
    model="gpt-4.1",
    tools=[read_email, send_email],
    checkpointer=InMemorySaver(),  # 必需
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "read_email": False,  # 不中断
            }
        ),
    ],
)
```

---

### ModelCallLimitMiddleware

限制模型调用次数，防止无限循环或过高成本。

**适用场景**:
- 防止失控 agent 过度调用 API
- 生产环境成本控制
- 测试时限制调用预算

**配置参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `thread_limit` | int | 否 | None | 整个线程的最大调用数 |
| `run_limit` | int | 否 | None | 单次运行的最大调用数 |
| `exit_behavior` | str | 否 | "end" | 达到限制时的行为: "end" 或 "error" |

**注意**: `thread_limit` 需要 `checkpointer` 来保持状态。

**示例**:

```python
from langchain.agents.middleware import ModelCallLimitMiddleware

ModelCallLimitMiddleware(
    thread_limit=10,  # 整个会话最多 10 次
    run_limit=5,      # 单次调用最多 5 次
    exit_behavior="end",  # 优雅终止
)
```

---

### ToolCallLimitMiddleware

限制工具调用次数，可全局或针对特定工具。

**适用场景**:
- 限制昂贵外部 API 调用
- 限制搜索或数据库查询次数
- 防止工具调用循环

**配置参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `tool_name` | str | 否 | None | 特定工具名，None 表示全局 |
| `thread_limit` | int | 否 | None | 整个线程的最大调用数 |
| `run_limit` | int | 否 | None | 单次运行的最大调用数 |
| `exit_behavior` | str | 否 | "continue" | "continue" / "error" / "end" |

**exit_behavior 选项**:
- `"continue"` - 阻止超限调用并返回错误消息，agent 继续执行
- `"error"` - 立即抛出异常停止执行
- `"end"` - 立即停止并返回 ToolMessage + AI message（仅单工具场景）

**示例**:

```python
from langchain.agents.middleware import ToolCallLimitMiddleware

# 全局限制
global_limiter = ToolCallLimitMiddleware(thread_limit=20, run_limit=10)

# 特定工具限制
search_limiter = ToolCallLimitMiddleware(
    tool_name="search",
    thread_limit=5,
    run_limit=3,
)

# 严格限制（超限报错）
strict_limiter = ToolCallLimitMiddleware(
    tool_name="scrape_webpage",
    run_limit=2,
    exit_behavior="error",
)

agent = create_agent(
    model="gpt-4.1",
    tools=[search, database, scraper],
    middleware=[global_limiter, search_limiter, strict_limiter],
)
```

---

### ModelFallbackMiddleware

主模型失败时自动降级到备用模型。

**适用场景**:
- 构建容灾 agent 应对模型服务中断
- 成本优化（失败时降级到便宜模型）
- 跨提供商冗余

**配置参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `first_model` | str/BaseChatModel | 是 | 第一个备用模型 |
| `*additional_fallbacks` | str/BaseChatModel | 否 | 更多备用模型 |

**示例**:

```python
from langchain.agents.middleware import ModelFallbackMiddleware

ModelFallbackMiddleware(
    "gpt-4.1-mini",
    "claude-3-5-sonnet-20241022",
)
```

---

### PIIMiddleware

检测和处理个人身份信息（PII）。

**适用场景**:
- 医疗/金融合规应用
- 客服 agent 需要清理日志
- 处理敏感用户数据

**配置参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `pii_type` | str | 是 | - | PII 类型名 |
| `strategy` | str | 是 | - | 处理策略 |
| `detector` | str/callable | 否 | 内置 | 自定义检测器 |
| `apply_to_input` | bool | 否 | True | 检查用户输入 |
| `apply_to_output` | bool | 否 | True | 检查 AI 输出 |
| `apply_to_tool_results` | bool | 否 | True | 检查工具结果 |

**内置 PII 类型**: `email`, `credit_card`, `ip`, `mac_address`, `url`

**strategy 选项**:
- `"block"` - 检测到抛出异常
- `"redact"` - 替换为 `[REDACTED_{TYPE}]`
- `"mask"` - 部分遮盖（如 `****-****-****-1234`）
- `"hash"` - 替换为确定性哈希

**自定义检测器示例**:

```python
import re

# 方法1: 正则字符串
PIIMiddleware("api_key", detector=r"sk-[a-zA-Z0-9]{32}", strategy="block")

# 方法2: 编译的正则
PIIMiddleware("phone", detector=re.compile(r"\+?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{4}"))

# 方法3: 自定义函数
def detect_ssn(content: str) -> list[dict[str, str | int]]:
    matches = []
    for match in re.finditer(r"\d{3}-\d{2}-\d{4}", content):
        ssn = match.group(0)
        first_three = int(ssn[:3])
        if first_three not in [0, 666] and not (900 <= first_three <= 999):
            matches.append({
                "text": ssn,
                "start": match.start(),
                "end": match.end(),
            })
    return matches

PIIMiddleware("ssn", detector=detect_ssn, strategy="hash")
```

---

### TodoListMiddleware

为 agent 提供任务规划和追踪能力。

**适用场景**:
- 复杂多步骤任务
- 长时运行操作需要进度可见性

**配置参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| `system_prompt` | str | 否 | 自定义 todo 使用提示 |
| `tool_description` | str | 否 | 自定义 write_todos 工具描述 |

**示例**:

```python
from langchain.agents.middleware import TodoListMiddleware

TodoListMiddleware(
    system_prompt="Use todos to track your progress...",
    tool_description="Write or update the todo list...",
)
```

---

### LLMToolSelectorMiddleware

使用 LLM 智能预选相关工具。

**适用场景**:
- Agent 有 10+ 工具但每查询只需少数几个
- 减少 token 使用
- 提高模型选择准确性

**配置参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `model` | str/BaseChatModel | 否 | agent 模型 | 选择用的模型 |
| `instructions` | str | 否 | 内置 | 选择提示 |
| `max_tools` | int | 否 | None | 最多选择工具数 |
| `always_include` | list[str] | 否 | [] | 始终包含的工具 |

**示例**:

```python
from langchain.agents.middleware import LLMToolSelectorMiddleware

LLMToolSelectorMiddleware(
    model="gpt-4.1-mini",
    max_tools=3,
    always_include=["search"],
)
```

---

### ToolRetryMiddleware

自动重试失败的工具调用。

**配置参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `max_retries` | int | 否 | 2 | 重试次数 |
| `tools` | list | 否 | None | 应用的工具，None=全部 |
| `retry_on` | tuple/callable | 否 | (Exception,) | 重试的异常类型 |
| `on_failure` | str/callable | 否 | "return_message" | 失败处理 |
| `backoff_factor` | float | 否 | 2.0 | 指数退避乘数 |
| `initial_delay` | float | 否 | 1.0 | 初始延迟（秒） |
| `max_delay` | float | 否 | 60.0 | 最大延迟（秒） |
| `jitter` | bool | 否 | True | 添加随机抖动 |

**on_failure 选项**:
- `"return_message"` - 返回 ToolMessage 让 LLM 处理
- `"raise"` - 重新抛出异常
- 自定义函数 - 返回字符串作为 ToolMessage 内容

**示例**:

```python
from langchain.agents.middleware import ToolRetryMiddleware

ToolRetryMiddleware(
    max_retries=3,
    backoff_factor=2.0,
    initial_delay=1.0,
    tools=["api_tool"],
    retry_on=(ConnectionError, TimeoutError),
    on_failure="return_message",
)
```

---

### ModelRetryMiddleware

自动重试失败的模型调用。

**配置参数**: 同 ToolRetryMiddleware，但 `on_failure` 默认是 `"continue"`。

**示例**:

```python
from langchain.agents.middleware import ModelRetryMiddleware

# 基础用法
ModelRetryMiddleware()

# 自定义异常过滤
def should_retry(error: Exception) -> bool:
    if hasattr(error, "status_code"):
        return error.status_code in (429, 503)
    return False

ModelRetryMiddleware(
    max_retries=4,
    retry_on=should_retry,
    on_failure="continue",
)
```

---

### LLMToolEmulator

使用 LLM 模拟工具执行（测试用）。

**适用场景**:
- 不执行真实工具的测试
- 外部工具不可用或昂贵时开发
- 原型验证

**配置参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `tools` | list | 否 | None | 模拟的工具，None=全部 |
| `model` | str/BaseChatModel | 否 | agent 模型 | 模拟用的模型 |

**示例**:

```python
from langchain.agents.middleware import LLMToolEmulator

# 模拟所有工具
LLMToolEmulator()

# 只模拟特定工具
LLMToolEmulator(tools=["get_weather"])

# 使用特定模型模拟
LLMToolEmulator(model="claude-sonnet-4-5-20250929")
```

---

### ContextEditingMiddleware

管理对话上下文，清理旧的工具调用输出。

**适用场景**:
- 多工具调用的长对话
- 减少 token 成本
- 只保留最近 N 个工具结果

**配置参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `edits` | list[ContextEdit] | 否 | [ClearToolUsesEdit()] | 编辑策略 |
| `token_count_method` | str | 否 | "approximate" | token 计数方法 |

**ClearToolUsesEdit 参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `trigger` | int | 是 | - | 触发 token 阈值 |
| `reclaim` | int | 否 | 0 | 最少回收的 token 数 |
| `keep` | int | 否 | 3 | 保留的最近工具结果数 |
| `clear_tool_inputs` | bool | 否 | False | 是否清除工具调用参数 |
| `exclude_tools` | list[str] | 否 | [] | 不清除的工具 |
| `placeholder` | str | 否 | "[cleared]" | 替换文本 |

**示例**:

```python
from langchain.agents.middleware import (
    ContextEditingMiddleware,
    ClearToolUsesEdit,
)

ContextEditingMiddleware(
    edits=[
        ClearToolUsesEdit(
            trigger=2000,
            keep=3,
            clear_tool_inputs=False,
            exclude_tools=["critical_tool"],
            placeholder="[cleared]",
        ),
    ],
)
```

---

### ShellToolMiddleware

为 agent 提供持久 Shell 会话。

**适用场景**:
- 需要执行系统命令的 agent
- 开发部署自动化
- 文件系统操作

**配置参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `workspace_root` | str | 否 | 临时目录 | 工作目录 |
| `startup_commands` | list/str | 否 | None | 启动命令 |
| `shutdown_commands` | list/str | 否 | None | 关闭命令 |
| `execution_policy` | BaseExecutionPolicy | 否 | HostExecutionPolicy | 执行策略 |
| `redaction_rules` | list[RedactionRule] | 否 | None | 输出脱敏规则 |
| `shell_command` | str/list | 否 | "/bin/bash" | shell 可执行文件 |
| `env` | dict | 否 | None | 环境变量 |

**执行策略**:
- `HostExecutionPolicy()` - 完整主机访问（默认）
- `DockerExecutionPolicy(image="...", command_timeout=60.0)` - Docker 隔离
- `CodexSandboxExecutionPolicy()` - Codex CLI sandbox

**示例**:

```python
from langchain.agents.middleware import (
    ShellToolMiddleware,
    HostExecutionPolicy,
    DockerExecutionPolicy,
    RedactionRule,
)

# 基础用法
ShellToolMiddleware(
    workspace_root="/workspace",
    execution_policy=HostExecutionPolicy(),
)

# Docker 隔离
ShellToolMiddleware(
    workspace_root="/workspace",
    startup_commands=["pip install requests"],
    execution_policy=DockerExecutionPolicy(
        image="python:3.11-slim",
        command_timeout=60.0,
    ),
)

# 带输出脱敏
ShellToolMiddleware(
    workspace_root="/workspace",
    redaction_rules=[
        RedactionRule(pii_type="api_key", detector=r"sk-[a-zA-Z0-9]{32}"),
    ],
)
```

---

### FilesystemFileSearchMiddleware

提供 Glob 和 Grep 文件搜索工具。

**适用场景**:
- 代码探索分析
- 按文件名模式查找
- 正则搜索代码内容

**配置参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|-----|------|------|-------|------|
| `root_path` | str | 是 | - | 搜索根目录 |
| `use_ripgrep` | bool | 否 | True | 使用 ripgrep |
| `max_file_size_mb` | float | 否 | 10 | 最大文件大小（MB） |

**添加的工具**:
- `glob_search` - 文件模式匹配（如 `**/*.py`）
- `grep_search` - 内容正则搜索

**示例**:

```python
from langchain.agents.middleware import FilesystemFileSearchMiddleware

FilesystemFileSearchMiddleware(
    root_path="/workspace",
    use_ripgrep=True,
    max_file_size_mb=10,
)
```

---

## Provider-Specific Middleware

某些 middleware 针对特定 LLM 提供商优化，详见各提供商文档。
