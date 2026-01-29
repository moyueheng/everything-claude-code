# My Claude Code 配置

个人 Claude Code 工作流配置，基于 [everything-claude-code](https://github.com/affaan-m/everything-claude-code) 改造。

---

## 推荐工作流程

### 1. 规划阶段 - `/plan`

**使用时机**: 新功能、复杂重构、架构变更

**流程**:
```
需求描述 → planner agent 分析 → 生成实施计划 → 用户确认 → 执行
```

**关键点**:
- 必须等待用户确认后才能写代码
- 包含风险识别和依赖分析
- 分阶段输出，每阶段可验证

---

### 2. 开发阶段 - `/tdd`

**使用时机**: 编写新功能、修复 Bug、重构

**TDD 循环** (RED → GREEN → IMPROVE):
```
1. 写 User Journey
2. 生成测试用例（先写测试）
3. 运行测试（应该失败）
4. 实现代码（使测试通过）
5. 重构代码
6. 验证覆盖率 ≥ 80%
```

**测试三层覆盖**:
- **单元测试**: 函数、组件、纯函数
- **集成测试**: API 端点、数据库操作
- **E2E 测试**: 关键用户流程 (Playwright)

---

### 3. 验证阶段 - `/verify`

**使用时机**: 代码完成后、提交 PR 前

**六阶段验证**:

| 阶段 | 检查项 | 命令 |
|------|--------|------|
| 1. Build | 项目能否构建 | `npm run build` |
| 2. Type | 类型检查 | `npx tsc --noEmit` |
| 3. Lint | 代码规范 | `npm run lint` |
| 4. Test | 测试覆盖 | `npm run test -- --coverage` |
| 5. Security | 密钥泄露/调试代码 | `grep -rn "sk-"` |
| 6. Diff | 变更审查 | `git diff --stat` |

**输出**: 验证报告，判断是否可进入 PR 阶段

---

### 4. 审查阶段 - `/code-review`

**使用时机**: 代码完成后

**并行审查**（多 agent 同时执行）:
- 代码质量和可维护性
- 安全漏洞检查
- 性能问题识别
- 一致性审查

---

### 5. 持续学习 - Continuous Learning v2

**核心概念**: 从会话中自动提取模式，形成"本能"

**工作流程**:
```
会话活动
    ↓
Pre/Post ToolUse Hooks 观察 (100% 可靠)
    ↓
observations.jsonl 存储
    ↓
Observer Agent 分析 (Haiku 后台运行)
    ↓
生成 instincts（带置信度 0.3-0.9）
    ↓
/evolve 聚类 → 生成 skill/command/agent
```

**常用命令**:
- `/instinct-status` - 查看已学习的本能
- `/evolve` - 聚类生成为 skill/command
- `/instinct-export` - 导出分享
- `/instinct-import <file>` - 导入他人的本能

---

## Agent 使用指南

### 立即使用的场景

| 场景 | 使用 Agent |
|------|-----------|
| 复杂功能需求 | `planner` - 先规划 |
| 刚写完代码 | `code-reviewer` - 代码审查 |
| Bug 修复/新功能 | `tdd-guide` - TDD 指导 |
| 架构决策 | `architect` - 系统设计 |
| 构建失败 | `build-error-resolver` - 修复构建 |
| 安全审查 | `security-reviewer` - 安全分析 |

### 并行执行原则

**正确做法**:
```
并行启动3个 agent:
1. Security analysis of auth.ts
2. Performance review of cache system
3. Type checking of utils.ts
```

**错误做法**:
```
先执行 agent 1, 完成后执行 agent 2, 再执行 agent 3
```

### 多视角分析

复杂问题使用分角色 agent:
- 事实审查员
- 高级工程师
- 安全专家
- 一致性审查员

---

## Iterative Retrieval 模式

解决子 agent 的上下文问题：

```
┌─────────────────────────────────────────┐
│                                         │
│   ┌──────────┐      ┌──────────┐        │
│   │ DISPATCH │─────▶│ EVALUATE │        │
│   └──────────┘      └──────────┘        │
│        ▲                  │             │
│        │                  ▼             │
│   ┌──────────┐      ┌──────────┐        │
│   │   LOOP   │◀─────│  REFINE  │        │
│   └──────────┘      └──────────┘        │
│                                         │
│        最多3轮，然后继续                │
└─────────────────────────────────────────┘
```

**步骤**:
1. **DISPATCH**: 宽泛查询收集候选文件
2. **EVALUATE**: 评估相关性 (0-1 评分)
3. **REFINE**: 根据评估优化搜索条件
4. **LOOP**: 重复，最多3轮

---

## 规则 (Rules)

`~/.claude/rules/` 下的文件会被强制遵循：

- `security.md` - 安全基线检查
- `coding-style.md` - 编码规范
- `testing.md` - 测试要求 (80%+ 覆盖)
- `git-workflow.md` - Git 提交规范
- `agents.md` - Agent 使用规则
- `performance.md` - 性能和上下文管理

---

## 目录结构

```
my/
├── README.md                      # 本文档
├── commands/                      # 共用 commands（Claude Code & OpenCode）
│   ├── code-review-py.md
│   ├── code-review-ts.md
│   ├── plan.md
│   ├── tdd.md
│   ├── update-codemaps.md
│   └── update-docs.md
├── claudecode/                    # Claude Code 专属配置
│   ├── agents/                    # Agents (8个)
│   ├── rules/                     # Rules (空，可自定义)
│   └── skills/                    # Skills
│       └── skill-creator/
├── opencode/                      # OpenCode 专属配置
│   ├── agents/                    # 空目录（可添加兼容的 agent）
│   └── skills/                    # 空目录（可添加兼容的 skill）
└── mcp-configs/                   # MCP 服务器配置（参考）
    └── mcp-servers.json
```

## 安装

```bash
./install.sh
```

会将 `my/` 下的配置安装到：
- **Claude Code**: `~/.claude/` (agents, rules, commands, skills)
- **OpenCode**: `~/.config/opencode/` (agents, commands, skills)

**说明**:
- `commands/` 目录的内容会安装到两个工具
- `claudecode/` 的内容只安装到 Claude Code
- `opencode/` 的内容只安装到 OpenCode

---

## 日常工作流示例

### 新功能开发
```bash
# 1. 规划
/plan 我需要添加用户认证功能，包括登录注册和 JWT 验证

# 2. TDD 开发（按 plan 的步骤）
/tdd 实现登录 API

# 3. 验证
/verify

# 4. 代码审查
/code-review
```

### Bug 修复
```bash
# 1. TDD 方式修复（先写复现测试）
/tdd 修复用户列表分页 bug

# 2. 验证
/verify
```

### 重构
```bash
# 1. 规划重构
/plan 重构用户服务层，提取公共逻辑

# 2. 逐步重构
/verify  # 每完成一个阶段验证一次
```

---

## 参考

- [上游项目文档](../upstream/everything-claude-code/README.md)
- [Shorthand Guide](https://x.com/affaanmustafa/status/2012378465664745795)
- [Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352)
