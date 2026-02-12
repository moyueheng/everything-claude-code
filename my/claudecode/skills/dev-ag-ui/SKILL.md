---
name: ag-ui
description: AG-UI 协议和 Python/TypeScript SDK 开发指南。当涉及 AG-UI (Agent-User Interaction Protocol) 相关任务时使用：(1) 理解或实现 AG-UI 事件类型（TEXT_MESSAGE_START/CONTENT/END、TOOL_CALL_*、STATE_*/DELTA 等），(2) 使用 Python SDK (Pydantic) 或 TypeScript SDK (Zod) 开发 agent 服务器，(3) 创建或修改 AG-UI 集成，(4) 实现 SSE 事件编码/解码，(5) 处理多模态消息或工具调用流式传输
---

# AG-UI 开发指南

AG-UI 是一个开放、轻量级、基于事件的协议，用于标准化 AI Agent 与用户应用的连接。

## 快速开始

### Python SDK

```python
from ag_ui.core import TextMessageContentEvent, EventType
from ag_ui.encoder import EventEncoder

# 创建事件（Python 使用 snake_case，自动转为 camelCase）
event = TextMessageContentEvent(
    message_id="msg_123",
    delta="Hello!"
)

# SSE 编码
encoder = EventEncoder()
sse_data = encoder.encode(event)
# 输出: data: {"type":"TEXT_MESSAGE_CONTENT","messageId":"msg_123","delta":"Hello!"}\n\n
```

### TypeScript SDK

```typescript
import { AGUIClient } from '@ag-ui/client';

const client = new AGUIClient({ url: 'http://localhost:3000/agent' });

const response = await client.run({
  messages: [{ role: 'user', content: 'Hello!' }]
});

for await (const event of response.events) {
  if (event.type === 'TEXT_MESSAGE_CONTENT') {
    console.log(event.delta);
  }
}
```

## 核心概念

### 16 种标准事件类型

**生命周期**: `RUN_STARTED`, `RUN_FINISHED`, `RUN_ERROR`, `STEP_STARTED`, `STEP_FINISHED`

**文本消息**: `TEXT_MESSAGE_START/CONTENT/END`, `THINKING_TEXT_MESSAGE_*`

**工具调用**: `TOOL_CALL_START/ARGS/END`, `TOOL_CALL_RESULT`

**状态管理**: `STATE_SNAPSHOT`, `STATE_DELTA` (JSON Patch), `MESSAGES_SNAPSHOT`

**活动**: `ACTIVITY_SNAPSHOT`, `ACTIVITY_DELTA`

**特殊**: `RAW` (外部透传), `CUSTOM` (自定义)

### Start-Content-End 流式模式

```
TEXT_MESSAGE_START (建立 messageId)
  ↓
TEXT_MESSAGE_CONTENT (多次，传递 delta)
  ↓
TEXT_MESSAGE_END (标记完成)
```

### 消息角色

- `developer` - 开发者指令
- `system` - 系统提示
- `assistant` - AI 回复（可含 tool_calls）
- `user` - 用户输入（支持多模态）
- `tool` - 工具执行结果
- `activity` - 进度更新

## 常见任务

### 发送流式文本 (Python)

```python
from ag_ui.core import TextMessageStartEvent, TextMessageContentEvent, TextMessageEndEvent
from ag_ui.encoder import EventEncoder

encoder = EventEncoder()
message_id = "msg_123"

# Start
yield encoder.encode(TextMessageStartEvent(
    type=EventType.TEXT_MESSAGE_START,
    message_id=message_id,
    role="assistant"
))

# Content (流式)
for chunk in stream_response():
    yield encoder.encode(TextMessageContentEvent(
        type=EventType.TEXT_MESSAGE_CONTENT,
        message_id=message_id,
        delta=chunk
    ))

# End
yield encoder.encode(TextMessageEndEvent(
    type=EventType.TEXT_MESSAGE_END,
    message_id=message_id
))
```

### 工具调用流式参数 (TypeScript)

```typescript
import { ToolCallStartEvent, ToolCallArgsEvent, ToolCallEndEvent } from '@ag-ui/core';

const toolCallId = 'call_123';

yield {
  type: 'TOOL_CALL_START',
  toolCallId,
  toolCallName: 'get_weather',
  parentMessageId: 'msg_123'
};

// 流式 JSON 参数
for (const chunk of streamJsonArgs()) {
  yield {
    type: 'TOOL_CALL_ARGS',
    toolCallId,
    delta: chunk
  };
}

yield { type: 'TOOL_CALL_END', toolCallId };
```

### 状态增量更新 (JSON Patch)

```python
from ag_ui.core import StateDeltaEvent

patch = [
    {"op": "replace", "path": "/status", "value": "running"},
    {"op": "add", "path": "/progress", "value": 0.5}
]

yield StateDeltaEvent(patch=patch)
```

## 参考资料

- **TypeScript SDK**: [typescript-sdk.md](typescript-sdk.md) - 包结构、客户端使用、测试
- **Python SDK**: [python-sdk.md](python-sdk.md) - 事件类型、SSE 编码、camelCase 转换
- **事件规范**: [event-types.md](event-types.md) - 完整事件类型列表、JSON Patch 格式



## 关键注意事项

1. **Python 自动 camelCase**: 使用 `by_alias=True` 或继承 `ConfiguredBaseModel`
2. **事件 ID 一致性**: `messageId`、`toolCallId` 必须在 Start/Content/End 事件中保持一致
3. **JSON Patch 路径**: 使用 RFC 6902 格式，路径如 `/items/-` (append)
4. **测试位置**: TypeScript 在 `__tests__/`，Python 在 `tests/`
