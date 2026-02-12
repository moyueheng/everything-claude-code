# TypeScript SDK 参考

## 包结构

```
sdks/typescript/packages/
├── core/        # 事件类型和 Zod schemas (@ag-ui/core)
├── client/      # HTTP 客户端 (@ag-ui/client)
├── encoder/     # SSE 编码器 (@ag-ui/encoder)
├── proto/       # 协议定义 (@ag-ui/proto)
└── cli/         # CLI 工具 (@ag-ui/cli)
```

## 核心事件类型

```typescript
import { EventType, TextMessageStartEventSchema } from '@ag-ui/core';

// 16 种标准事件类型
enum EventType {
  // 生命周期
  RUN_STARTED, RUN_FINISHED, RUN_ERROR,
  STEP_STARTED, STEP_FINISHED,

  // 文本消息
  TEXT_MESSAGE_START, TEXT_MESSAGE_CONTENT, TEXT_MESSAGE_END,
  TEXT_MESSAGE_CHUNK,
  THINKING_TEXT_MESSAGE_START, THINKING_TEXT_MESSAGE_CONTENT, THINKING_TEXT_MESSAGE_END,

  // 工具调用
  TOOL_CALL_START, TOOL_CALL_ARGS, TOOL_CALL_END,
  TOOL_CALL_CHUNK, TOOL_CALL_RESULT,

  // 状态管理
  STATE_SNAPSHOT, STATE_DELTA,
  MESSAGES_SNAPSHOT,
  ACTIVITY_SNAPSHOT, ACTIVITY_DELTA,

  // 特殊事件
  RAW, CUSTOM
}
```

## 消息类型

```typescript
import { MessageSchema, UserMessageSchema, AssistantMessageSchema } from '@ag-ui/core';

// 所有消息继承自 BaseMessage，使用 role 作为鉴别器
const message = {
  id: "msg_123",
  role: "assistant",  // "developer" | "system" | "assistant" | "user" | "tool" | "activity"
  content: "Hello!"
};
```

## 客户端使用

```typescript
import { AGUIClient } from '@ag-ui/client';

const client = new AGUIClient({
  url: 'http://localhost:3000/agent',
});

// 发送消息并接收事件流
const response = await client.run({
  messages: [{ role: 'user', content: 'Hello!' }]
});

// 处理事件流
for await (const event of response.events) {
  switch (event.type) {
    case 'TEXT_MESSAGE_CONTENT':
      console.log(event.delta);  // 文本增量
      break;
    case 'TOOL_CALL_START':
      console.log(event.toolCallName);
      break;
  }
}
```

## 测试

```bash
cd sdks/typescript/packages/core
pnpm test -- --reporter=verbose --run
```
