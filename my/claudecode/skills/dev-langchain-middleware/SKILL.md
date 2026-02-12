---
name: dev-langchain-middleware
description: LangChain Agent Middleware 开发指南。当使用 LangChain Python 创建 Agent 并需要：(1) 添加日志/监控/调试，(2) 实现重试/降级/容错，(3) 限制 API 调用或工具执行，(4) 人机协作审批流程，(5) 自定义 Agent 执行行为，(6) 检测和处理敏感数据(PII)，(7) 动态选择工具或模型时使用
---

# LangChain Agent Middleware 开发指南

## 概述

LangChain Middleware 提供了一种在 Agent 执行流程的特定点介入控制的机制，类似于 Web 框架的中间件模式。通过 Middleware，你可以在不修改核心 Agent 逻辑的情况下添加横切关注点（cross-cutting concerns）。

## 快速开始

```python
from langchain.agents import create_agent
from langchain.agents.middleware import (
    SummarizationMiddleware,
    ToolRetryMiddleware,
    ModelCallLimitMiddleware,
)

agent = create_agent(
    model="gpt-4.1",
    tools=[your_tools],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4.1-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
        ToolRetryMiddleware(max_retries=3),
        ModelCallLimitMiddleware(thread_limit=10),
    ],
)
```

## Agent 循环与 Hook 时机

```
before_agent → [before_model → wrap_model_call → MODEL → after_model] →
[before_tool → wrap_tool_call → TOOL → after_tool] → ... → after_agent
```

- **before_***: 在节点执行前运行，用于验证/状态更新
- **wrap_***: 包裹执行，可控制调用次数（0/1/N次），用于重试/缓存/转换
- **after_***: 在节点执行后运行，用于日志/状态更新

## 内置 Middleware 速查表

| Middleware | 用途 | 关键参数 |
|-----------|------|---------|
| `SummarizationMiddleware` | 对话历史超限压缩 | `trigger`, `keep`, `model` |
| `HumanInTheLoopMiddleware` | 工具调用人工审批 | `interrupt_on` |
| `ModelCallLimitMiddleware` | 限制模型调用次数 | `thread_limit`, `run_limit` |
| `ToolCallLimitMiddleware` | 限制工具调用次数 | `thread_limit`, `run_limit`, `exit_behavior` |
| `ModelFallbackMiddleware` | 模型失败自动降级 | `first_model`, `additional_fallbacks` |
| `PIIMiddleware` | 敏感数据检测处理 | `pii_type`, `strategy` |
| `TodoListMiddleware` | 任务规划追踪 | 无 |
| `LLMToolSelectorMiddleware` | LLM 预选工具 | `model`, `max_tools`, `always_include` |
| `ToolRetryMiddleware` | 工具调用重试 | `max_retries`, `backoff_factor`, `on_failure` |
| `ModelRetryMiddleware` | 模型调用重试 | `max_retries`, `backoff_factor`, `on_failure` |
| `LLMToolEmulator` | LLM 模拟工具执行 | `tools`, `model` |
| `ContextEditingMiddleware` | 上下文编辑清理 | `edits` |
| `ShellToolMiddleware` | 持久 Shell 会话 | `workspace_root`, `execution_policy` |
| `FilesystemFileSearchMiddleware` | 文件系统搜索 | `root_path`, `use_ripgrep` |

### 上下文大小配置

所有涉及阈值配置的 middleware 使用统一的 `ContextSize` 格式：

```python
# 三种格式
("tokens", 4000)      # 绝对 token 数
("messages", 20)      # 消息数量
("fraction", 0.8)     # 模型上下文的比例 (0-1)

# 多条件 OR 逻辑
trigger=[("tokens", 3000), ("messages", 6)]  # 任一条件满足即触发
```

### PII 检测配置

```python
PIIMiddleware("email", strategy="redact")              # 内置类型
PIIMiddleware("api_key", detector=r"sk-\w{32}")        # 正则检测
PIIMiddleware("ssn", detector=custom_function)         # 函数检测

# strategy 选项: "block" | "redact" | "mask" | "hash"
# apply_to 选项: apply_to_input=True, apply_to_output=True
```

### Human-in-the-Loop 配置

需要 checkpointer：

```python
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="gpt-4.1",
    checkpointer=InMemorySaver(),  # 必需
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "dangerous_tool": {"allowed_decisions": ["approve", "edit", "reject"]},
                "safe_tool": False,  # 不中断
            }
        ),
    ],
)
```

## 自定义 Middleware

### 选择实现方式

| 场景 | 推荐方式 |
|------|---------|
| 单个简单 hook | 装饰器函数 |
| 多个 hooks 或需要配置 | 类继承 `AgentMiddleware` |
| 需要同时实现 sync/async | 类继承 |

### 装饰器方式（快速原型）

```python
from langchain.agents.middleware import before_model, after_model, AgentState
from langgraph.runtime import Runtime
from typing import Any

@before_model
def log_request(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"Calling with {len(state['messages'])} messages")
    return None  # 无状态修改

@after_model
def log_response(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"Response: {state['messages'][-1].content}")
    return None
```

### 类方式（生产推荐）

```python
from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime
from typing import Any

class LoggingMiddleware(AgentMiddleware):
    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"Before: {len(state['messages'])} messages")
        return None

    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"After: {state['messages'][-1].content}")
        return None
```

### Wrap-Style Hooks（控制流）

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call
def retry_with_backoff(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    for attempt in range(3):
        try:
            return handler(request)
        except Exception as e:
            if attempt == 2:
                raise
            print(f"Retry {attempt + 1}/3: {e}")
```

### 自定义状态

```python
from typing_extensions import NotRequired
from langchain.agents.middleware import AgentState

class CustomState(AgentState):
    call_count: NotRequired[int]
    user_id: NotRequired[str]

class CounterMiddleware(AgentMiddleware[CustomState]):
    state_schema = CustomState

    def after_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
        return {"call_count": state.get("call_count", 0) + 1}
```

### Agent 跳转（提前退出）

```python
from langchain.agents.middleware import hook_config, after_model, AgentState
from langchain.messages import AIMessage

@after_model
@hook_config(can_jump_to=["end"])
def check_blocked(state: AgentState, runtime) -> dict[str, Any] | None:
    if "BLOCKED" in state["messages"][-1].content:
        return {
            "messages": [AIMessage("Content blocked.")],
            "jump_to": "end"  # 跳转目标: "end" | "tools" | "model"
        }
    return None
```

## Hook 执行顺序

给定 `middleware=[m1, m2, m3]`：

```
before_agent:  m1 → m2 → m3
before_model:  m1 → m2 → m3
wrap_model:   m1(m2(m3(handler)))
after_model:  m3 → m2 → m1  (逆序)
after_agent:  m3 → m2 → m1  (逆序)
```

**规则**: `before_*` 正序，`after_*` 逆序，`wrap_*` 嵌套

## 高级场景

### 动态模型选择

```python
@wrap_model_call
def select_model(request: ModelRequest, handler) -> ModelResponse:
    model = complex_model if len(request.messages) > 10 else simple_model
    return handler(request.override(model=model))
```

### 动态工具选择

```python
@wrap_model_call
def filter_tools(request: ModelRequest, handler) -> ModelResponse:
    relevant = select_relevant(request.state)
    return handler(request.override(tools=relevant))
```

### 系统消息修改（Anthropic 缓存）

```python
from langchain.messages import SystemMessage

@wrap_model_call
def add_cached_context(request: ModelRequest, handler) -> ModelResponse:
    new_content = list(request.system_message.content_blocks) + [{
        "type": "text",
        "text": "<large_document>...</document>",
        "cache_control": {"type": "ephemeral"}
    }]
    new_system = SystemMessage(content=new_content)
    return handler(request.override(system_message=new_system))
```

## 最佳实践

1. **单一职责** - 每个 middleware 只做一件事
2. **优雅降级** - 不要让 middleware 错误导致整个 agent 崩溃
3. **选择合适的 hook 类型**:
   - Node-style 用于日志/验证（顺序执行）
   - Wrap-style 用于重试/缓存（控制调用次数）
4. **文档化自定义状态** - 清晰记录新增的状态字段
5. **独立测试** - 集成前先单独测试 middleware
6. **注意执行顺序** - 关键 middleware 放在列表前面

## 参考资源

- **内置 Middleware 详情**: 见 [references/builtin-middleware.md](references/builtin-middleware.md)
- **自定义开发示例**: 见 [references/custom-middleware.md](references/custom-middleware.md)
- **官方文档**: https://docs.langchain.com/oss/python/langchain/middleware/overview
