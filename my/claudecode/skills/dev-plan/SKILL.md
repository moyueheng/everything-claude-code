---
name: dev-plan
description: 重述需求、评估风险、创建分步实施计划。WAIT for user CONFIRM before touching any code.
---

# 开发规划 Skill

此 skill 在编写任何代码之前创建全面的实施计划。

## Skill 作用

1. **重述需求** - 明确需要构建什么
2. **识别风险** - 揭示潜在问题和阻塞点
3. **创建步骤计划** - 将实施拆分为多个阶段
4. **等待确认** - 必须先获得用户批准才能继续

## 何时激活

在以下情况使用此 skill：
- 开始新功能开发
- 进行重大架构变更
- 处理复杂重构
- 多个文件/组件会受到影响
- 需求不清晰或模棱两可

## 工作原理

此 skill 将：

1. **分析请求** 并用清晰的术语重述需求
2. **拆分为阶段** 并制定具体可执行的步骤
3. **识别依赖** 分析组件间的关系
4. **评估风险** 和潜在阻塞点
5. **估算复杂度** (High/Medium/Low)
6. **呈现计划** 并 WAIT for your explicit confirmation

## 使用示例

```
用户: /plan 我需要添加市场结算时的实时通知功能

Agent (planner):
# 实施计划：实时市场结算通知

## 需求重述
- 当用户关注的市场结算时发送通知
- 支持多种通知渠道（应用内、邮件、Webhook）
- 确保通知可靠送达
- 包含市场结果和用户仓位收益

## 实施阶段

### 阶段 1：数据库设计
- 添加 notifications 表，包含字段：id, user_id, market_id, type, status, created_at
- 添加 user_notification_preferences 表存储渠道偏好
- 在 user_id 和 market_id 上创建索引以提高性能

### 阶段 2：通知服务
- 在 lib/notifications.ts 中创建通知服务
- 使用 BullMQ/Redis 实现通知队列
- 添加失败重试逻辑
- 创建通知模板

### 阶段 3：集成点
- 接入市场结算逻辑（状态变为"已结算"时触发）
- 查询市场中所有有仓位的用户
- 为每个用户入队通知

### 阶段 4：前端组件
- 在头部创建 NotificationBell 组件
- 添加 NotificationList 弹窗
- 使用 Supabase 订阅实现实时更新
- 添加通知偏好设置页面

## 依赖关系
- Redis（队列使用）
- 邮件服务（SendGrid/Resend）
- Supabase 实时订阅

## 风险
- HIGH: 邮件送达率（需要 SPF/DKIM）
- MEDIUM: 单市场 1000+ 用户时的性能
- MEDIUM: 市场频繁结算导致的通知泛滥
- LOW: 实时订阅开销

## 预估复杂度: MEDIUM
- 后端：4-6 小时
- 前端：3-4 小时
- 测试：2-3 小时
- 总计：9-13 小时

**等待确认**: 是否继续执行此计划？(yes/no/modify)
```

## 重要说明

**关键**：在用户明确用 "yes" 或 "proceed" 或类似的肯定回答确认计划之前，**不会**编写任何代码。

如需修改，请回复：
- "modify: [你的修改内容]"
- "different approach: [替代方案]"
- "skip phase 2 and do phase 3 first"

## 与其他 Skills 配合

规划完成后：
- 使用 `dev-tdd-ts` 或 `dev-tdd-py` 进行测试驱动开发
- 遇到构建错误时修复
- 完成后使用 code-review agent 审查代码
