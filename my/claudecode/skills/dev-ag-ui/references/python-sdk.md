# Python SDK 参考

## 包结构

```
sdks/python/
├── ag_ui/
│   ├── core/
│   │   ├── events.py    # 16 种核心事件类型
│   │   └── types.py     # 消息类型、工具定义
│   └── encoder/
│       └── encoder.py   # SSE 编码器
└── tests/
```

## 核心事件类型

```python
from ag_ui.core import (
    EventType,
    TextMessageStartEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
)

# 事件使用 Pydantic 模型，自动 camelCase 序列化
event = TextMessageContentEvent(
    message_id="msg_123",
    delta="Hello!"
)

# 序列化为 JSON（自动转换为 camelCase）
json_str = event.model_dump_json(by_alias=True)
# 输出: {"type":"TEXT_MESSAGE_CONTENT","messageId":"msg_123","delta":"Hello!"}
```

## 消息类型

```python
from ag_ui.core import (
    UserMessage,
    AssistantMessage,
    ToolMessage,
    ActivityMessage,
)

# 创建用户消息（支持多模态）
user_msg = UserMessage(
    id="msg_123",
    content=[{
        "type": "text",
        "text": "Hello!"
    }]
)

# 创建助手消息（带工具调用）
assistant_msg = AssistantMessage(
    id="msg_124",
    content="I'll help you with that.",
    tool_calls=[{
        "id": "call_1",
        "type": "function",
        "function": {
            "name": "get_weather",
            "arguments": '{"city": "Beijing"}'
        }
    }]
)
```

## SSE 编码器

```python
from ag_ui.encoder import EventEncoder
from ag_ui.core import TextMessageContentEvent, EventType

encoder = EventEncoder()

event = TextMessageContentEvent(
    type=EventType.TEXT_MESSAGE_CONTENT,
    message_id="msg_123",
    delta="Hello!"
)

# 编码为 SSE 格式
sse_data = encoder.encode(event)
# 输出: data: {"type":"TEXT_MESSAGE_CONTENT","messageId":"msg_123","delta":"Hello!"}\n\n
```

## 测试

```bash
cd sdks/python
poetry run pytest tests/test_events.py -v

# 运行特定测试
poetry run pytest tests/test_events.py::TestEvents::test_text_message_start -v
```

## 自动 camelCase 转换

Python SDK 使用 `ConfiguredBaseModel` 自动将 snake_case 转换为 camelCase：

```python
# Python 中使用 snake_case
class TextMessageContentEvent(ConfiguredBaseModel):
    message_id: str
    delta: str

# JSON 序列化后为 camelCase
# {"messageId": "...", "delta": "..."}
```
