# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

- 重要原则： 不允许改上游仓库的任何东西， 如果修改了说明严重违反规定强行更正， 上游仓库是完全只读我们只需要跟踪就行了

## 项目概述

这是个人 Claude Code 配置仓库，基于 [everything-claude-code](https://github.com/affaan-m/everything-claude-code) 改造。

采用 submodule 架构管理：
- `upstream/` - 原项目完整内容（只读，通过 submodule 同步更新）
  - `everything-claude-code/` - affaan-m 的配置仓库（submodule）
  - `anthropics-skills/` - anthropics 官方的 skills 仓库（submodule）
  - `openai-skills/` - OpenAI 官方的 skills 仓库（submodule）
- `my/` - 个人改造的配置（从 upstream 挑选并本地化）

## 目录结构

```
.
├── my/                          # 个人配置
│   ├── claudecode/              # Claude Code 专属配置
│   │   ├── agents/              # 改造后的 agents（中文/个性化）
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

# 查看有什么新变化
cd upstream/everything-claude-code && git log HEAD@{1}..HEAD --oneline
cd ../anthropics-skills && git log HEAD@{1}..HEAD --oneline
cd ../openai-skills && git log HEAD@{1}..HEAD --oneline

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

## 参考文档

- 上游项目文档：`upstream/everything-claude-code/README.md`
- 迁移方案：`MIGRATION_STEPS.md`
- 配置对比：`docs/differences.md` - OpenCode、Claude Code、Codex 配置系统对比

## 可用 Agents

### Claude Code Agents (`my/claudecode/agents/`)

| 文件 | 描述 | 工具 |
|------|------|------|
| `architect.md` | 软件架构专家，系统设计和可扩展性 | Read, Grep, Glob |
| `code-reviewer-py.md` | Python 代码审查专员 | Read, Grep, Glob, Bash |
| `code-reviewer-ts.md` | TypeScript 代码审查专员 | Read, Grep, Glob, Bash |
| `doc-updater.md` | 文档和代码地图专家 | Read, Write, Edit, Bash, Grep, Glob |
| `planner.md` | 复杂功能和重构规划专员 | Read, Grep, Glob |
| `refactor-cleaner-python.md` | Python 死代码清理和重构 | Read, Write, Edit, Bash, Grep, Glob |
| `refactor-cleaner-ts.md` | TypeScript 死代码清理和重构 | Read, Write, Edit, Bash, Grep, Glob |
| `tdd-guide-ts.md` | TypeScript 测试驱动开发专家 | Read, Write, Edit, Bash, Grep |
| `tdd-guide-py.md` | Python 测试驱动开发专家 | Read, Write, Edit, Bash, Grep |

### OpenCode Agents (`my/opencode/agents/`)

| 文件 | 描述 | 模式 |
|------|------|------|
| `architect.md` | 软件架构专家（只读） | subagent |
| `code-reviewer-py.md` | Python 代码审查 | subagent |
| `code-reviewer-ts.md` | TypeScript 代码审查 | subagent |
| `doc-updater.md` | 文档和代码地图专家 | subagent |
| `planner.md` | 规划专家（只读） | subagent |
| `refactor-cleaner-python.md` | Python 重构和清理 | subagent |
| `refactor-cleaner-ts.md` | TypeScript 重构和清理 | subagent |
| `tdd-guide-ts.md` | TypeScript TDD 测试专家 | subagent |
| `tdd-guide-py.md` | Python TDD 测试专家 | subagent |

> 注意：OpenCode agents 从 Claude Code 格式转换而来，主要差异见 `docs/differences.md`

## 可用 Skills

### Claude Code Skills (`my/claudecode/skills/`)

| 分类 | 文件 | 描述 | 触发场景 |
|------|------|------|----------|
| **dev-** | `dev-async-modernize/` | Python 异步代码现代化 | 分析 async 代码质量问题、迁移到 TaskGroup |
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
| **dev-** | `dev-tdd-ts/` | TypeScript 测试驱动开发 | `$dev-tdd-ts` |
| **dev-** | `dev-tdd-py/` | Python 测试驱动开发 | `$dev-tdd-py` |
| **dev-** | `dev-rehab-legacy-tests/` | 遗留测试改造 TDD 流程 | `$dev-rehab-legacy-tests` |
