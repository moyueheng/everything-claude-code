# LangChain 自定义 Middleware 开发详解

## Hook 类型对比

### Node-Style Hooks

**特点**: 顺序执行，用于日志、验证、状态更新

**可用 hooks**:
- `before_agent` - Agent 启动前（每调用一次）
- `before_model` - 每次模型调用前
- `after_model` - 每次模型响应后
- `after_agent` - Agent 完成后（每调用一次）

**函数签名**:

```python
def hook_name(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """
    Args:
        state: 当前 agent 状态，包含 messages 等
        runtime: 运行时上下文

    Returns:
        状态更新字典，或 None 表示无更新
        可包含 "jump_to" 键控制执行流程
    """
    return {"messages": [...], "custom_field": value}
```

### Wrap-Style Hooks

**特点**: 包裹执行，可控制 handler 调用次数（0/1/N次）

**可用 hooks**:
- `wrap_model_call` - 包裹每次模型调用
- `wrap_tool_call` - 包裹每次工具调用

**函数签名**:

```python
def wrap_hook(
    request: ModelRequest | ToolCallRequest,
    handler: Callable[[Request], Response],
) -> Response:
    """
    Args:
        request: 请求对象
        handler: 实际执行函数

    Returns:
        响应对象
    """
    # 可调用 0 次（短路）、1 次（正常）、N 次（重试）
    return handler(request)
```

---

## 实现方式详解

### 装饰器方式

适合快速原型和简单场景。

#### 基础示例

```python
from langchain.agents.middleware import (
    before_model, after_model,
    wrap_model_call, wrap_tool_call,
    AgentState, ModelRequest, ModelResponse,
)
from langgraph.runtime import Runtime
from typing import Any, Callable

@before_model
def log_before(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"About to call model with {len(state['messages'])} messages")
    return None

@after_model
def log_after(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"Model returned: {state['messages'][-1].content}")
    return None

@wrap_model_call
def retry_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    for attempt in range(3):
        try:
            return handler(request)
        except Exception as e:
            if attempt == 2:
                raise
            print(f"Retry {attempt + 1}/3 after error: {e}")

agent = create_agent(
    model="gpt-4.1",
    middleware=[log_before, log_after, retry_model],
    tools=[...],
)
```

#### 带配置的 Hook

```python
from langchain.agents.middleware import hook_config

@before_model
@hook_config(can_jump_to=["end"])
def check_limit(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    if len(state["messages"]) >= 50:
        return {
            "messages": [AIMessage("Conversation limit reached.")],
            "jump_to": "end"
        }
    return None
```

---

### 类方式

适合生产环境、复杂配置、多 hook 组合。

#### 基础示例

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

agent = create_agent(
    model="gpt-4.1",
    middleware=[LoggingMiddleware()],
    tools=[...],
)
```

#### 带配置的 Middleware

```python
class MessageLimitMiddleware(AgentMiddleware):
    def __init__(self, max_messages: int = 50):
        super().__init__()
        self.max_messages = max_messages

    @hook_config(can_jump_to=["end"])
    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        if len(state["messages"]) >= self.max_messages:
            return {
                "messages": [AIMessage("Limit reached.")],
                "jump_to": "end"
            }
        return None

# 使用
middleware = MessageLimitMiddleware(max_messages=100)
```

#### Wrap-Style 类实现

```python
from langchain.agents.middleware import ModelRequest, ModelResponse
from typing import Callable

class RetryMiddleware(AgentMiddleware):
    def __init__(self, max_retries: int = 3):
        super().__init__()
        self.max_retries = max_retries

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        for attempt in range(self.max_retries):
            try:
                return handler(request)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                print(f"Retry {attempt + 1}/{self.max_retries}: {e}")
```

---

## 自定义状态

### 定义状态 Schema

```python
from typing_extensions import NotRequired
from langchain.agents.middleware import AgentState

class CustomState(AgentState):
    call_count: NotRequired[int]
    user_id: NotRequired[str]
    request_start_time: NotRequired[float]
```

### 装饰器方式使用自定义状态

```python
from langchain.agents.middleware import before_model, after_model

@before_model(state_schema=CustomState, can_jump_to=["end"])
def check_call_limit(state: CustomState, runtime: Runtime) -> dict[str, Any] | None:
    count = state.get("call_count", 0)
    if count > 10:
        return {"jump_to": "end"}
    return None

@after_model(state_schema=CustomState)
def increment_counter(state: CustomState, runtime: Runtime) -> dict[str, Any] | None:
    return {"call_count": state.get("call_count", 0) + 1}

agent = create_agent(
    model="gpt-4.1",
    middleware=[check_call_limit, increment_counter],
    tools=[],
)

# 调用时传入自定义状态
result = agent.invoke({
    "messages": [HumanMessage("Hello")],
    "call_count": 0,
    "user_id": "user-123",
})
```

### 类方式使用自定义状态

```python
class CallCounterMiddleware(AgentMiddleware[CustomState]):
    state_schema = CustomState

    def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
        count = state.get("call_count", 0)
        if count > 10:
            return {"jump_to": "end"}
        return None

    def after_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
        return {"call_count": state.get("call_count", 0) + 1}
```

---

## Agent 跳转（Jumps）

### 可用跳转目标

- `"end"` - 跳到 agent 执行末尾
- `"tools"` - 跳到 tools 节点
- `"model"` - 跳到 model 节点（或第一个 before_model hook）

### 装饰器方式

```python
from langchain.agents.middleware import after_model, hook_config, AgentState
from langchain.messages import AIMessage
from typing import Any

@after_model
@hook_config(can_jump_to=["end"])
def check_blocked(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    last_message = state["messages"][-1]
    if "BLOCKED" in last_message.content:
        return {
            "messages": [AIMessage("I cannot respond to that request.")],
            "jump_to": "end"
        }
    return None
```

### 类方式

```python
from langchain.agents.middleware import AgentMiddleware, hook_config

class BlockedContentMiddleware(AgentMiddleware):
    @hook_config(can_jump_to=["end"])
    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        last_message = state["messages"][-1]
        if "BLOCKED" in last_message.content:
            return {
                "messages": [AIMessage("I cannot respond to that request.")],
                "jump_to": "end"
            }
        return None
```

---

## 高级示例

### 动态模型选择

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.chat_models import init_chat_model
from typing import Callable

complex_model = init_chat_model("gpt-4.1")
simple_model = init_chat_model("gpt-4.1-mini")

@wrap_model_call
def dynamic_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    # 根据对话长度选择模型
    model = complex_model if len(request.messages) > 10 else simple_model
    return handler(request.override(model=model))
```

### 工具调用监控

```python
from langchain.agents.middleware import wrap_tool_call
from langchain.tools.tool_node import ToolCallRequest
from langchain.messages import ToolMessage
from langgraph.types import Command
from typing import Callable

@wrap_tool_call
def monitor_tool(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    tool_name = request.tool_call['name']
    args = request.tool_call['args']

    print(f"Executing: {tool_name}")
    print(f"Arguments: {args}")

    try:
        result = handler(request)
        print(f"Success: {tool_name}")
        return result
    except Exception as e:
        print(f"Failed: {tool_name} - {e}")
        raise
```

### 动态工具选择

```python
from langchain.agents.middleware import wrap_model_call

def select_relevant_tools(state, runtime):
    """根据状态选择相关工具"""
    # 自定义选择逻辑
    return [tool for tool in all_tools if is_relevant(tool, state)]

@wrap_model_call
def filter_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    relevant = select_relevant_tools(request.state, request.runtime)
    return handler(request.override(tools=relevant))

agent = create_agent(
    model="gpt-4.1",
    tools=all_tools,  # 所有工具需预先注册
    middleware=[filter_tools],
)
```

### 系统消息修改（Anthropic 缓存）

```python
from langchain.messages import SystemMessage

@wrap_model_call
def add_cached_context(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    # 使用 content_blocks 处理
    new_content = list(request.system_message.content_blocks) + [{
        "type": "text",
        "text": "Here is a large document to analyze:\n\n<document>...</document>",
        "cache_control": {"type": "ephemeral"}  # 标记缓存点
    }]

    new_system_message = SystemMessage(content=new_content)
    return handler(request.override(system_message=new_system_message))
```

### 带计费的监控 Middleware

```python
from typing_extensions import NotRequired
import time

class BillingState(AgentState):
    total_tokens: NotRequired[int]
    total_cost: NotRequired[float]
    request_count: NotRequired[int]

class BillingMiddleware(AgentMiddleware[BillingState]):
    state_schema = BillingState

    def __init__(self, cost_per_1k_tokens: float = 0.002):
        super().__init__()
        self.cost_per_1k_tokens = cost_per_1k_tokens

    def before_model(self, state: BillingState, runtime) -> dict[str, Any] | None:
        return {"request_start_time": time.time()}

    def after_model(self, state: BillingState, runtime) -> dict[str, Any] | None:
        # 从响应中获取 token 使用量
        last_message = state["messages"][-1]
        usage = getattr(last_message, "usage_metadata", {})
        tokens = usage.get("total_tokens", 0)

        current_total = state.get("total_tokens", 0)
        current_cost = state.get("total_cost", 0)
        current_count = state.get("request_count", 0)

        return {
            "total_tokens": current_total + tokens,
            "total_cost": current_cost + (tokens / 1000) * self.cost_per_1k_tokens,
            "request_count": current_count + 1,
        }
```

---

## 执行顺序详解

```python
agent = create_agent(
    model="gpt-4.1",
    middleware=[middleware1, middleware2, middleware3],
    tools=[...],
)
```

### 执行流程

```
1. before_agent:  m1 → m2 → m3

2. Agent Loop 开始

3. before_model:  m1 → m2 → m3

4. wrap_model_call:
   m1.wrap_model_call(
       m2.wrap_model_call(
           m3.wrap_model_call(
               model_handler
           )
       )
   )

5. after_model:  m3 → m2 → m1  (逆序!)

6. [工具调用时]
   before_tool:  m1 → m2 → m3
   wrap_tool_call: m1(m2(m3(tool_handler)))
   after_tool:  m3 → m2 → m1

7. Agent Loop 结束

8. after_agent:  m3 → m2 → m1  (逆序!)
```

### 关键规则

- **before_***: 正序（列表顺序）
- **after_***: 逆序（列表逆序）
- **wrap_***: 嵌套（第一个包裹所有其他）

---

## 最佳实践

### 1. 保持专注

```python
# 好: 只做一件事
class RateLimitMiddleware(AgentMiddleware):
    def before_model(self, state, runtime):
        # 只处理限流
        ...

# 不好: 混合多个职责
class KitchenSinkMiddleware(AgentMiddleware):
    def before_model(self, state, runtime):
        # 限流 + 日志 + 验证
        ...
```

### 2. 优雅处理错误

```python
@before_model
def safe_validation(state, runtime):
    try:
        risky_operation()
    except Exception as e:
        # 记录但不中断
        logger.error(f"Validation error: {e}")
    return None
```

### 3. 选择合适的 Hook 类型

```python
# 日志/验证: Node-style
@after_model
def log_response(state, runtime):
    print(f"Response: {state['messages'][-1].content}")

# 重试/缓存: Wrap-style
@wrap_model_call
def with_retry(request, handler):
    for i in range(3):
        try:
            return handler(request)
        except TransientError:
            if i == 2:
                raise
```

### 4. 文档化自定义状态

```python
class MyState(AgentState):
    """
    自定义状态字段:
    - request_id: str, 当前请求唯一标识
    - start_time: float, 请求开始时间戳
    - retry_count: int, 当前重试次数
    """
    request_id: NotRequired[str]
    start_time: NotRequired[float]
    retry_count: NotRequired[int]
```

### 5. 独立测试

```python
def test_middleware():
    middleware = MyMiddleware(config="test")

    # 测试 before_model
    state = {"messages": [HumanMessage("test")]}
    result = middleware.before_model(state, mock_runtime)
    assert result is not None

    # 测试 wrap_model_call
    def mock_handler(request):
        return ModelResponse(...)

    result = middleware.wrap_model_call(mock_request, mock_handler)
    assert result is not None
```

### 6. 注意执行顺序

```python
# 关键 middleware 放前面
middleware=[
    auth_middleware,      # 先验证权限
    rate_limit_middleware, # 再检查限流
    logging_middleware,    # 最后记录日志
]
```
