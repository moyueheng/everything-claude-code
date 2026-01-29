# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

- 重要原则： 不允许改上游仓库的任何东西， 如果修改了说明严重违反规定强行更正， 上游仓库是完全只读我们只需要跟踪就行了

## 项目概述

这是个人 Claude Code 配置仓库，基于 [everything-claude-code](https://github.com/affaan-m/everything-claude-code) 改造。

采用 subtree 架构管理：
- `upstream/` - 原项目完整内容（只读，通过 subtree 同步更新）
  - `everything-claude-code/` - affaan-m 的配置仓库
  - `anthropics-skills/` - anthropics 官方的 skills 仓库
- `my/` - 个人改造的配置（从 upstream 挑选并本地化）

## 目录结构

```
.
├── my/                          # 个人配置
│   ├── claudecode/              # Claude Code 专属配置
│   │   ├── agents/              # 改造后的 agents（中文/个性化）
│   │   ├── rules/               # 改造后的 rules
│   │   └── skills/              # 改造后的 skills
│   └── opencode/                # OpenCode 专属配置
│       ├── agents/
│       ├── commands/
│       └── skills/
│
├── upstream/everything-claude-code/  # 上游原项目（subtree 管理）
│   ├── agents/
│   ├── rules/
│   ├── commands/
│   ├── skills/
│   └── ...
│
├── upstream/anthropics-skills/  # anthropics 官方 skills 仓库（subtree 管理）
│   └── skills/
│
├── install.sh                   # 安装脚本
└── MIGRATION_TO_SUBTREE.md      # 迁移文档
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

## 日常工作流

### 从上游挑选配置

```bash
# 查看上游有哪些可用配置
ls upstream/everything-claude-code/agents/

# 复制想用的文件到 my/ 进行改造
cp upstream/everything-claude-code/agents/planner.md my/claudecode/agents/planner.md

# 编辑改造（翻译成中文、调整内容）
vim my/claudecode/agents/planner.md

# 安装测试
./install.sh
```

### 同步上游更新

```bash
# 拉取 everything-claude-code 最新内容
git subtree pull --prefix=upstream/everything-claude-code \
  https://github.com/affaan-m/everything-claude-code.git main --squash

# 拉取 anthropics-skills 最新内容
git subtree pull --prefix=upstream/anthropics-skills \
  https://github.com/anthropics/skills.git main --squash

# 查看有什么新变化
git diff HEAD~1 --name-only

# 如果有新内容想改造，复制到 my/
cp upstream/everything-claude-code/agents/new-agent.md my/claudecode/agents/new-agent.md
cp upstream/anthropics-skills/skills/some-skill.md my/claudecode/skills/some-skill.md
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

| 位置 | 命名建议 | 说明 |
|------|----------|------|
| `upstream/` | 保持原名 | 不修改，仅参考 |
| `my/` | `xxx.md` 或自定义名 | 中文改造版本或原创内容 |

## 注意事项

1. **永远不要修改 `upstream/` 目录** - 只使用 `subtree pull` 更新
2. **所有个人配置放在 `my/`** - 这是唯一会被 `install.sh` 安装的目录
3. **改造前先从 upstream 复制** - 保留原文件参考，在副本上修改
4. **定期同步上游** - 获取原项目的新功能和修复

## 参考文档

- 上游项目文档：`upstream/everything-claude-code/README.md`
- 迁移方案：`MIGRATION_TO_SUBTREE.md`
