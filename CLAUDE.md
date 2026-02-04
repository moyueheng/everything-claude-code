# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

- 重要原则： 不允许改上游仓库的任何东西， 如果修改了说明严重违反规定强行更正， 上游仓库是完全只读我们只需要跟踪就行了
- 翻译成中文的时候专有名词不需要翻译, 比如Agent, Skill, Command, Hook

## 当前工作重点（2026-02-03 ~ 2026-03-03）

**优先级：专注于上游 everything-claude-code 仓库的深入研究与改造**

未来一个月的主要工作目标是对 `upstream/everything-claude-code/` 进行系统性梳理和本地化改造：

1. **上游内容分析** - 深入研究 everything-claude-code 的所有 agents、commands、skills、rules、contexts
2. **本地化改造** - 将有价值的配置从 `upstream/` 复制到 `my/` 并进行中文改造
3. **文档更新** - 同步更新 `CLAUDE.md` 和 `README.md` 中的可用组件列表
4. **贡献上游** - 如有改进，考虑向 affaan-m/everything-claude-code 提交 PR

**工作流程**：
```bash
# 1. 更新上游
git submodule update --remote upstream/everything-claude-code

# 2. 查看新内容
cd upstream/everything-claude-code
git log HEAD@{1}..HEAD --oneline
ls -la agents/ commands/ skills/ rules/ contexts/

# 3. 复制到 my/ 改造
cp upstream/everything-claude-code/agents/some-agent.md my/claudecode/agents/some-agent.md
# 编辑改造...

# 4. 更新文档
# 编辑 CLAUDE.md 和 README.md
```

## 项目概述

这是个人 Claude Code 配置仓库，基于 [everything-claude-code](https://github.com/affaan-m/everything-claude-code) 改造。

采用 submodule 架构管理：
- `upstream/` - 原项目完整内容（只读，通过 submodule 同步更新）
  - `everything-claude-code/` - affaan-m 的配置仓库（submodule）
  - `anthropics-skills/` - anthropics 官方的 skills 仓库（submodule）
  - `openai-skills/` - OpenAI 官方的 skills 仓库（submodule）
  - `superpowers/` - obra/superpowers 完整软件开发工作流系统（submodule）
  - `obsidian-skills/` - kepano/obsidian-skills 仓库（submodule）
- `my/` - 个人改造的配置（从 upstream 挑选并本地化）

## 目录结构

```
.
├── .plans/                     # 实施计划持久化目录
├── my/                          # 个人配置
│   ├── claudecode/              # Claude Code 专属配置
│   │   ├── agents/              # 改造后的 agents（中文/个性化）
│   │   ├── rules/               # 改造后的 rules（中文/个性化）
│   │   └── skills/              # 改造后的 skills
│   ├── opencode/                # OpenCode 专属配置
│   │   ├── agents/              # 改造后的 agents（从 Claude Code 转换）
│   │   ├── commands/
│   │   └── skills/
│   ├── codex/                   # Codex 专属配置
│   │   └── skills/              # 改造后的 skills
│   └── mcp-configs/             # MCP 服务器配置
│
├── upstream/everything-claude-code/  # 上游原项目（submodule）
│   ├── agents/
│   ├── rules/
│   ├── commands/
│   ├── skills/
│   ├── contexts/
│   └── ...
│
├── upstream/anthropics-skills/  # anthropics 官方 skills 仓库（submodule）
│   ├── agents/
│   └── skills/
│
├── upstream/openai-skills/      # OpenAI 官方 skills 仓库（submodule）
│   └── ...
│
├── upstream/superpowers/        # obra/superpowers 完整软件开发工作流系统（submodule）
│   ├── agents/
│   ├── commands/
│   ├── skills/
│   └── hooks/
│
├── upstream/obsidian-skills/    # kepano/obsidian-skills 仓库（submodule）
│   └── ...
│
├── install.sh                   # 安装脚本
└── MIGRATION_STEPS.md           # 迁移文档
```

## 安装配置

```bash
# 将 my/ 下的配置安装到 Claude Code 和 OpenCode
./install.sh
```

### 安装规则

安装脚本基于目录结构自动处理：

| 目录 | 目标位置 |
|------|----------|
| `my/claudecode/agents/` | Claude Code (`~/.claude/agents/`) |
| `my/claudecode/rules/` | Claude Code (`~/.claude/rules/`) |
| `my/claudecode/skills/` | Claude Code (`~/.claude/skills/`) |
| `my/opencode/agents/` | OpenCode (`~/.config/opencode/agents/`) |
| `my/opencode/commands/` | OpenCode (`~/.config/opencode/commands/`) |
| `my/opencode/skills/` | OpenCode (`~/.config/opencode/skills/`) |
| `my/codex/skills/` | Codex (`~/.codex/skills/`) |

## 日常工作流

### 从上游挑选配置

```bash
# 查看上游有哪些可用配置
ls upstream/everything-claude-code/agents/
ls upstream/everything-claude-code/skills/
ls upstream/anthropics-skills/agents/
ls upstream/anthropics-skills/skills/
ls upstream/obsidian-skills/

# 复制想用的文件到 my/ 进行改造
cp upstream/everything-claude-code/agents/planner.md my/claudecode/agents/planner.md

# 编辑改造（翻译成中文、调整内容）
vim my/claudecode/agents/planner.md

# 安装测试
./install.sh
```

### 同步上游更新

```bash
# 更新所有 submodule 到最新版本
git submodule update --remote

# 或者分别更新
git submodule update --remote upstream/everything-claude-code
git submodule update --remote upstream/anthropics-skills
git submodule update --remote upstream/openai-skills
git submodule update --remote upstream/superpowers
git submodule update --remote upstream/obsidian-skills

# 查看有什么新变化
cd upstream/everything-claude-code && git log HEAD@{1}..HEAD --oneline
cd ../anthropics-skills && git log HEAD@{1}..HEAD --oneline
cd ../openai-skills && git log HEAD@{1}..HEAD --oneline
cd ../superpowers && git log HEAD@{1}..HEAD --oneline
cd ../obsidian-skills && git log HEAD@{1}..HEAD --oneline

# 如果有新内容想改造，复制到 my/
cp upstream/everything-claude-code/agents/new-agent.md my/claudecode/agents/new-agent.md
cp upstream/anthropics-skills/skills/some-skill.md my/claudecode/skills/some-skill.md
cp upstream/openai-skills/some-skill.md my/claudecode/skills/some-skill.md
```

### 创建原创配置

直接在 `my/` 下创建新文件：

```bash
# 创建新的 agent（根据目标工具选择目录）
# Claude Code 专属:
cat > my/claudecode/agents/my-helper.md << 'EOF'
---
name: my-helper
description: 我的自定义助手
---

# My Helper

这是我自己定义的 agent...
EOF

# OpenCode command:
cat > my/opencode/commands/my-command.md << 'EOF'
description: 我的自定义命令

# My Command

这是我自己定义的 command...
EOF

./install.sh
```

## 命名规范

### 文件命名

| 位置 | 命名建议 | 说明 |
|------|----------|------|
| `upstream/` | 保持原名 | 不修改，仅参考 |
| `my/` | `xxx.md` 或自定义名 | 中文改造版本或原创内容 |

### Skill 分类前缀

所有 Skills 使用分类前缀，便于区分用途：

| 前缀 | 类别 | 示例 |
|------|------|------|
| `dev-` | 开发相关 | `dev-plan`, `dev-tdd`, `dev-review-py` |
| `life-` | 生活相关 | `life-notes`, `life-daily` |
| `work-` | 工作相关 | `work-meeting`, `work-project` |
| `tool-` | 工具相关 | `tool-mcp-builder`, `tool-sshfs-mount` |
| `learn-` | 学习相关 | `learn-paper`, `learn-research` |

详细规范见 `docs/skill-naming-convention.md`

## 注意事项

1. **永远不要修改 `upstream/` 目录** - 只使用 `git submodule update --remote` 更新
2. **所有个人配置放在 `my/`** - 这是唯一会被 `install.sh` 安装的目录
3. **改造前先从 upstream 复制** - 保留原文件参考，在副本上修改
4. **定期同步上游** - 获取原项目的新功能和修复
5. **实施计划统一存放在 `.plans/`** - 使用 `YYYY-MM-DD-<feature-name>.md` 命名

## 参考文档

- 上游项目文档：`upstream/everything-claude-code/README.md`
- 迁移方案：`MIGRATION_STEPS.md`
- 配置对比：`docs/differences.md` - OpenCode、Claude Code、Codex 配置系统对比
- Subagent MCP 配置：`docs/subagent-mcp-config.md` - Subagent 与 MCP 工具配置指南

## 可用 Agents

### Claude Code Agents (`my/claudecode/agents/`)

| 文件 | 描述 | 权限 | MCP 工具 |
|------|------|------|----------|
| `planner.md` | 复杂功能和重构规划专员 | 只读 (disallowedTools: Write/Edit) | auggie-mcp, context7 |
| `architect.md` | 软件架构专家，系统设计和可扩展性 | 只读 (disallowedTools: Write/Edit) | context7, auggie-mcp |
| `code-reviewer-py.md` | Python 代码审查专员 | 只读 (disallowedTools: Write/Edit) | context7 |
| `code-reviewer-ts.md` | TypeScript 代码审查专员 | 只读 (disallowedTools: Write/Edit) | context7 |
| `tdd-guide-py.md` | Python 测试驱动开发专家 | 完整权限 | context7 |
| `tdd-guide-ts.md` | TypeScript 测试驱动开发专家 | 完整权限 | context7 |
| `doc-updater.md` | 文档和代码地图专家 | 完整权限 | context7 |
| `refactor-cleaner-python.md` | Python 死代码清理和重构 | 完整权限 | context7 |
| `refactor-cleaner-ts.md` | TypeScript 死代码清理和重构 | 完整权限 | context7 |

**权限说明：**
- **只读 Agent**：通过 `disallowedTools: ["Write", "Edit", "NotebookEdit"]` 限制，只能提供建议，不能直接修改代码
- **完整权限 Agent**：未指定 `tools` 字段，继承所有内置工具和 MCP 工具，可以执行写入操作
- **MCP 工具访问**：所有 Agent 移除了 `tools` 限制后，都可以访问配置的 MCP 工具（context7, auggie-mcp 等）

### OpenCode Agents (`my/opencode/agents/`)

| 文件 | 描述 | 模式 |
|------|------|------|
| `planner.md` | 规划专家（只读，可访问 MCP） | subagent |
| `architect.md` | 软件架构专家（只读，可访问 MCP） | subagent |
| `code-reviewer-py.md` | Python 代码审查（只读，可访问 MCP） | subagent |
| `code-reviewer-ts.md` | TypeScript 代码审查（只读，可访问 MCP） | subagent |
| `tdd-guide-py.md` | Python TDD 测试专家（完整权限） | subagent |
| `tdd-guide-ts.md` | TypeScript TDD 测试专家（完整权限） | subagent |
| `doc-updater.md` | 文档和代码地图专家（完整权限） | subagent |
| `refactor-cleaner-python.md` | Python 重构和清理（完整权限） | subagent |
| `refactor-cleaner-ts.md` | TypeScript 重构和清理（完整权限） | subagent |

> 注意：OpenCode agents 从 Claude Code 格式转换而来，主要差异见 `docs/differences.md`

## 可用 Rules (`my/claudecode/rules/`)

| 文件 | 描述 |
|------|------|
| `coding-style.md` | 编码风格指南：不可变性、文件组织、错误处理、输入验证 |
| `git-workflow.md` | Git 工作流：Commit 格式、PR 流程、TDD 方法 |
| `testing.md` | 测试要求：80% 覆盖率、TDD 工作流、测试类型 |
| `performance.md` | 性能优化：模型选择策略、上下文窗口管理 |
| `patterns.md` | 通用设计模式：API 响应格式、Custom Hooks、Repository 模式 |
| `hooks.md` | Hooks 系统：PreToolUse、PostToolUse、Stop hooks |
| `agents.md` | Agent 编排：可用 Agents、并行任务执行、多角度分析 |
| `security.md` | 安全指南：安全检查、Secret 管理、安全响应协议 |

## 可用 Skills

### Claude Code Skills (`my/claudecode/skills/`)

| 分类 | 文件 | 描述 | 触发场景 |
|------|------|------|----------|
| **dev-** | `dev-architecture-critic/` | 全栈架构找茬与改进方向评审（偏现代 Python） | 架构评审/设计/重构 |
| **dev-** | `dev-async-modernize/` | Python 异步代码现代化 | 分析 async 代码质量问题、迁移到 TaskGroup |
| **dev-** | `dev-build-fix-py/` | Python 构建错误增量修复 | Python 构建/打包失败时逐条修复 |
| **dev-** | `dev-build-fix-ts/` | TypeScript 构建错误增量修复 | TypeScript/前端构建失败时逐条修复 |
| **dev-** | `dev-plan/` | 开发项目规划 | 新功能、复杂重构前的实施计划 |
| **dev-** | `dev-review-py/` | Python 代码审查 | 检查未提交的 Python 代码 |
| **dev-** | `dev-review-ts/` | TypeScript 代码审查 | 检查未提交的 TS/JS 代码 |
| **dev-** | `dev-tdd-ts/` | TypeScript 测试驱动开发 | TDD 工作流程 (RED-GREEN-REFACTOR) |
| **dev-** | `dev-tdd-py/` | Python 测试驱动开发 | Python TDD 工作流程 (pytest) |
| **dev-** | `dev-tdd-workflow/` | 通用 TDD 工作流（合并 command + skill） | 新功能、修复 bug、重构时强制先写测试 |
| **dev-** | `dev-update-codemaps/` | 代码地图更新 | 从代码库结构生成架构文档 |
| **dev-** | `dev-update-docs/` | 开发文档更新 | 从 package.json 和 .env.example 同步文档 |
| **tool-** | `tool-macos-hidpi/` | macOS HiDPI 分辨率设置 | 创建自定义显示器分辨率 |
| **tool-** | `tool-mcp-builder/` | MCP 服务器构建指南 | 创建 Python/TypeScript MCP 服务器 |
| **tool-** | `tool-skill-creator/` | Skill 创建指南 | 从 Git 历史提取或创建新技能 |
| **tool-** | `tool-sshfs-mount/` | SSH 远程目录挂载 | 挂载远程服务器目录到本地 |

### Codex Skills (`my/codex/skills/`)

| 分类 | 文件 | 描述 | 调用方式 |
|------|------|------|----------|
| **dev-** | `dev-architecture-critic/` | 全栈架构找茬与改进方向评审 | `$dev-architecture-critic` |
| **dev-** | `dev-plan/` | 开发项目规划 | `$dev-plan` |
| **dev-** | `dev-tdd-workflow/` | 通用 TDD 工作流（合并 command + skill） | `$dev-tdd-workflow` |
| **dev-** | `dev-tdd-ts/` | TypeScript 测试驱动开发 | `$dev-tdd-ts` |
| **dev-** | `dev-tdd-py/` | Python 测试驱动开发 | `$dev-tdd-py` |
| **dev-** | `dev-rehab-legacy-tests/` | 遗留测试改造 TDD 流程 | `$dev-rehab-legacy-tests` |
