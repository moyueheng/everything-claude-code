---
name: dev-tdd-workflow
description: 通用 TDD 工作流（合并 command + skill）。用于新功能、修复 bug、重构时强制先写测试，覆盖率 80%+，包含单元/集成/E2E 测试。
---

# 测试驱动开发工作流

## 概述

用于在开发过程中强制执行先写测试、再实现、再重构的流程，并保证覆盖率达标。

## 何时启用

- 实现新功能或新增模块/组件
- 修复 bug 或问题（先写可复现的失败测试）
- 重构现有代码或关键业务逻辑
- 新增 API 端点或关键流程

## 快速流程（原 /tdd command 核心步骤）

1. **建立接口/类型骨架**（先定义输入/输出）
2. **先写失败测试**（RED）
3. **最小实现**（GREEN）
4. **重构**（REFACTOR）
5. **检查覆盖率**（至少 80%）

## TDD 循环

```
RED → GREEN → REFACTOR → REPEAT

RED:      编写失败的测试
GREEN:    实现最小代码让测试通过
REFACTOR: 改进代码并保持测试通过
REPEAT:   下一个场景/功能
```

## 详细步骤

### 步骤 1：编写用户旅程
```
作为 [角色]，我想要 [动作]，以便 [收益]
```

### 步骤 2：生成测试用例
- 为每个旅程覆盖：正常路径、边界值、错误路径
- 先写会失败的测试（验证失败原因正确）

### 步骤 3：运行测试并确认失败
- 失败原因必须与“尚未实现/逻辑缺失”一致

### 步骤 4：最小实现（GREEN）
- 只写足够通过测试的实现

### 步骤 5：运行测试并确认通过
- 所有测试必须变绿

### 步骤 6：重构（REFACTOR）
- 消除重复
- 改进命名与可读性
- 在测试保持绿色的前提下优化结构/性能

### 步骤 7：验证覆盖率
- 最低 80%
- 覆盖不足时补测试

## 测试类型

### 单元测试
- 单个函数/工具
- 组件逻辑
- 纯函数

### 集成测试
- API 端点
- 数据库操作
- 服务交互
- 外部 API 调用

### E2E 测试
- 关键用户流程
- 完整工作流
- UI 交互

## 覆盖率要求

- **全量最低 80%**
- **以下必须 100%**：
  - 金融计算
  - 认证逻辑
  - 安全关键代码
  - 核心业务逻辑

## 最佳实践（精简）

1. **测试先于代码**，绝不跳过 RED
2. **一条测试一个行为**，断言具体且有意义
3. **边界/错误路径必须覆盖**
4. **保持测试快速**，优先单元测试
5. **重构前后都要测试全绿**

## 计划同步更新

**当从 `dev-plan` 生成的计划执行 TDD 时，必须同步更新计划文件：**

### 计划文件位置
```
.plans/YYYY-MM-DD-<feature-name>.md
```

### 更新时机

每个 Task 完成后立即更新计划：

```markdown
### Task 1: 数据库 Schema 设计

**Status:** ✅ COMPLETED

**Files:**
- Create: `prisma/migrations/xxx_notifications/migration.sql` ✅
- Modify: `prisma/schema.prisma` ✅
- Test: `tests/db/notifications.test.ts` ✅

**实际变更:**
- 添加了 notifications 表，包含字段：id, user_id, market_id, type, status, created_at
- 添加了 user_notification_preferences 表存储渠道偏好
- 在 user_id 和 market_id 上创建了索引

**Notes:**
- 原计划使用 Prisma，实际实现时改用了原生 SQL（性能考虑）
```

### 计划调整

**TDD 过程中发现计划需要调整时，必须记录：**

```markdown
### Task 3: 通知服务集成

**Status:** 🔄 IN PROGRESS

**调整原因:** 发现 BullMQ 与现有 Redis 配置冲突

**新方案:** 改用内存队列 + 持久化到 PostgreSQL

**影响:** Task 4 的集成点需要相应调整
```

### 完成标记

- ✅ COMPLETED - 已完成且测试通过
- 🔄 IN PROGRESS - 正在进行
- ⏸️ BLOCKED - 被阻塞，记录阻塞原因
- ❌ SKIPPED - 跳过，记录跳过原因
- 📝 MODIFIED - 已修改，记录变更内容

### 进度跟踪

在计划文件顶部添加进度条：

```markdown
# [功能名称] 实施计划

> **For Claude:** REQUIRED SUB-SKILL: 使用 dev-tdd-workflow 按任务实施此计划。

**Progress:** [████████░░] 80% (4/5 tasks completed)

**Last Updated:** 2026-02-04 14:30
```

## 与 Agent/流程配合

- 需要执行型引导时可配合 `dev-tdd-guide-ts` 或 `dev-tdd-guide-py` Agent。
- 从 `dev-plan` 进入时，必须同步更新计划文件状态。
