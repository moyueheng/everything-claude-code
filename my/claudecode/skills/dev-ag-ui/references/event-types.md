# AG-UI 事件类型规范

## 流式模式 (Start-Content-End)

大多数事件遵循 **Start-Content-End** 模式：

```
TEXT_MESSAGE_START
  ├── messageId: 唯一标识符
  └── role: 消息角色

TEXT_MESSAGE_CONTENT (可多次)
  ├── messageId: 关联的 ID
  └── delta: 文本增量

TEXT_MESSAGE_END
  └── messageId: 关联的 ID
```

## 生命周期事件

| 事件 | 描述 |
|------|------|
| `RUN_STARTED` | Agent 运行开始 |
| `RUN_FINISHED` | Agent 运行完成 |
| `RUN_ERROR` | Agent 运行出错 |
| `STEP_STARTED` | 步骤开始 |
| `STEP_FINISHED` | 步骤完成 |

## 文本消息事件

| 事件 | 描述 |
|------|------|
| `TEXT_MESSAGE_START` | 文本消息开始 |
| `TEXT_MESSAGE_CONTENT` | 文本内容增量 |
| `TEXT_MESSAGE_END` | 文本消息结束 |
| `TEXT_MESSAGE_CHUNK` | 便捷语法糖（合并事件）|
| `THINKING_TEXT_MESSAGE_START` | 思考过程开始 |
| `THINKING_TEXT_MESSAGE_CONTENT` | 思考内容增量 |
| `THINKING_TEXT_MESSAGE_END` | 思考过程结束 |

## 工具调用事件

| 事件 | 描述 |
|------|------|
| `TOOL_CALL_START` | 工具调用开始 |
| `TOOL_CALL_ARGS` | 工具参数增量（流式 JSON）|
| `TOOL_CALL_END` | 工具调用结束 |
| `TOOL_CALL_CHUNK` | 便捷语法糖 |
| `TOOL_CALL_RESULT` | 工具调用结果 |

## 状态管理事件

| 事件 | 描述 |
|------|------|
| `STATE_SNAPSHOT` | 完整状态快照 |
| `STATE_DELTA` | 状态增量（JSON Patch）|
| `MESSAGES_SNAPSHOT` | 消息列表快照 |
| `ACTIVITY_SNAPSHOT` | 活动状态快照 |
| `ACTIVITY_DELTA` | 活动状态增量 |

## 特殊事件

| 事件 | 描述 |
|------|------|
| `RAW` | 外部系统事件透传 |
| `CUSTOM` | 应用自定义事件 |

## JSON Patch (RFC 6902)

`STATE_DELTA` 和 `ACTIVITY_DELTA` 使用 JSON Patch 格式：

```json
{
  "type": "STATE_DELTA",
  "patch": [
    { "op": "replace", "path": "/count", "value": 42 },
    { "op": "add", "path": "/items/-", "value": "new item" }
  ]
}
```

操作类型：`add`, `remove`, `replace`, `move`, `copy`, `test`
