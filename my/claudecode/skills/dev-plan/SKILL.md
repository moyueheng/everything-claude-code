---
name: dev-plan
description: 重述需求、评估风险、创建分步实施计划。WAIT for user CONFIRM before touching any code.
---

# 开发规划 Skill

此 Skill 在编写任何代码之前创建全面的实施计划。

## Skill 作用

1. **重述需求** - 明确需要构建什么
2. **识别风险** - 揭示潜在问题和阻塞点
3. **创建步骤计划** - 将实施拆分为多个阶段
4. **等待确认** - 必须先获得用户批准才能继续

## 何时激活

在以下情况使用此 Skill：
- 开始新功能开发
- 进行重大架构变更
- 处理复杂重构
- 多个文件/组件会受到影响
- 需求不清晰或模棱两可

## 工作原理

此 Skill 将：

1. **分析请求** 并用清晰的术语重述需求
2. **积极提问** - 使用 `AskUserQuestion` 工具澄清模糊需求、确认技术选型、询问实现偏好
3. **拆分为阶段** 并制定具体可执行的步骤
4. **识别依赖** 分析组件间的关系
5. **评估风险** 和潜在阻塞点
6. **估算复杂度** (High/Medium/Low)
7. **呈现计划** 并 WAIT for your explicit confirmation

## 积极提问原则

**规划过程中必须主动使用 `AskUserQuestion`：**

- 需求不清晰时 → 询问具体细节
- 有多种实现方案时 → 让用户选择
- 技术选型不确定时 → 确认用户偏好
- 优先级不明确时 → 询问哪些是 must-have vs nice-to-have
- 边界条件模糊时 → 确认行为

**提问示例：**
- "数据持久化方案？(Redis / PostgreSQL / SQLite)"
- "是否需要支持批量操作？"
- "错误处理策略：静默失败 / 记录日志 / 抛出异常？"
- "实时性要求：WebSocket / Server-Sent Events / 轮询？"

## 计划文档结构

### Plan Header（必须包含）

每个计划必须以以下 Header 开头：

```markdown
# [功能名称] 实施计划

> **For Claude:** REQUIRED SUB-SKILL: 使用 dev-tdd-workflow 按任务实施此计划。

**Goal:** [一句话描述要构建什么]

**Architecture:** [2-3 句话描述实现方法]

**Tech Stack:** [关键技术/库]

---
```

### 任务结构

**每个任务一个动作（2-5 分钟）：**
- "编写失败的测试" - 一个步骤
- "运行测试确保它失败" - 一个步骤
- "编写最小实现让测试通过" - 一个步骤
- "运行测试确保通过" - 一个步骤
- "提交" - 一个步骤

### 任务详细格式

```markdown
### Task N: [组件名称]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: 编写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: 编写最小实现**

```python
def function(input):
    return expected
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: 提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## 完整计划示例

```markdown
# 实时市场结算通知 实施计划

> **For Claude:** REQUIRED SUB-SKILL: 使用 dev-tdd-workflow 按任务实施此计划。

**Goal:** 当市场结算时向用户发送实时通知

**Architecture:** 使用 BullMQ 队列处理通知发送，支持多渠道（应用内、邮件、Webhook）。前端使用 Supabase 订阅实现实时更新。

**Tech Stack:** TypeScript, Next.js, BullMQ, Redis, Supabase, Prisma

---

### Task 1: 数据库 Schema 设计

**Files:**
- Create: `prisma/migrations/20240101000000_add_notifications/migration.sql`
- Modify: `prisma/schema.prisma`
- Test: `tests/db/notifications.test.ts`

**Step 1: 编写迁移测试**
...

**Step 2: 添加 Prisma 模型**
...

**Step 3: 运行迁移**
...

**Step 4: 提交**
```

## 执行交接

计划完成后，提供两种执行选项：

**"计划已保存。两种执行方式：**

**1. Subagent-Driven（当前会话）** - 我分配子 Agent 按任务执行，任务间审查，快速迭代

**2. Parallel Session（独立会话）** - 开启新会话使用 dev-tdd-workflow Skill，批量执行并设置检查点

**选择哪种方式？"**

**如果选 Subagent-Driven：**
- 保持当前会话
- 每个任务使用新鲜子 Agent + 代码审查

**如果选 Parallel Session：**
- 引导用户在工作树中开启新会话
- 新会话使用 dev-tdd-workflow Skill

## 使用示例

```
用户: /dev-plan 我需要添加市场结算时的实时通知功能

Agent:
# 实施计划：实时市场结算通知

> **For Claude:** REQUIRED SUB-SKILL: 使用 dev-tdd-workflow 按任务实施此计划。

**Goal:** 当市场结算时向用户发送实时通知

**Architecture:** 使用 BullMQ 队列处理通知发送，支持多渠道（应用内、邮件、Webhook）

**Tech Stack:** TypeScript, Next.js, BullMQ, Redis, Supabase

---

## 需求重述
- 当用户关注的市场结算时发送通知
- 支持多种通知渠道（应用内、邮件、Webhook）
- 确保通知可靠送达
- 包含市场结果和用户仓位收益

## 实施任务

### Task 1: 数据库设计
**Files:**
- Create: `prisma/migrations/xxx_notifications/migration.sql`
- Modify: `prisma/schema.prisma`
- Test: `tests/db/notifications.test.ts`

**Steps:**
1. 编写 Schema 测试
2. 添加 notifications 表
3. 添加 user_notification_preferences 表
4. 创建索引
5. 提交

### Task 2: 通知服务
...

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
- 使用 `dev-tdd-workflow` 进行测试驱动开发（统一 TDD 流程）
- 遇到构建错误时修复
- 完成后使用 `dev-review-ts` 或 `dev-review-py` Skill 审查代码

## Related Agents

- `planner` Agent：负责输出可执行的实施计划

## 计划保存位置

计划保存到: `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 记住原则

- 始终使用精确文件路径
- 计划中包含完整代码（不是"添加验证"这种模糊描述）
- 包含精确命令和预期输出
- 使用 @ 语法引用相关 skills
- DRY, YAGNI, TDD, 频繁提交
