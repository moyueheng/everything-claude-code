# Claude Code 个人配置仓库

个人 Claude Code 工作流配置仓库，基于 [everything-claude-code](https://github.com/affaan-m/everything-claude-code) 改造。

---

## 项目概述

这是个人 Claude Code/OpenCode 配置仓库，采用 submodule 架构管理：

- **`upstream/`** - 原项目完整内容（只读，通过 submodule 同步更新）
  - `everything-claude-code/` - affaan-m 的配置仓库（submodule）
  - `anthropics-skills/` - anthropics 官方的 skills 仓库（submodule）
  - `openai-skills/` - OpenAI 官方的 skills 仓库（submodule）
  - `ai-research-skills/` - Orchestra-Research 的 AI-research-SKILLs 仓库（submodule）
  - `obsidian-skills/` - kepano/obsidian-skills 仓库（submodule）
- **`my/`** - 个人改造的配置（从 upstream 挑选并本地化）

## 目录结构

```
.
├── my/                          # 个人配置
│   ├── commands/                # 共用 commands（安装到 Claude Code 和 OpenCode）
│   ├── claudecode/              # Claude Code 专属配置
│   │   ├── agents/              # 改造后的 agents（中文/个性化）
│   │   ├── rules/               # 改造后的 rules
│   │   └── skills/              # 改造后的 skills
│   └── opencode/                # OpenCode 专属配置
│       ├── agents/
│       └── skills/
│
├── upstream/everything-claude-code/  # 上游原项目（submodule）
│   ├── agents/
│   ├── rules/
│   ├── commands/
│   ├── skills/
│   └── ...
│
├── upstream/anthropics-skills/  # anthropics 官方 skills 仓库（submodule）
│   └── skills/
│
├── upstream/openai-skills/      # OpenAI 官方 skills 仓库（submodule）
│   └── ...
│
├── upstream/ai-research-skills/ # Orchestra-Research AI-research-SKILLs（submodule）
│   └── ...
│
├── upstream/obsidian-skills/    # kepano/obsidian-skills（submodule）
│   └── ...
│
├── install.sh                   # 安装脚本
└── README.md                    # 本文档
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
| `my/commands/` | Claude Code (`~/.claude/commands/`) + OpenCode (`~/.config/opencode/commands/`) |
| `my/claudecode/agents/` | Claude Code (`~/.claude/agents/`) |
| `my/claudecode/rules/` | Claude Code (`~/.claude/rules/`) |
| `my/claudecode/skills/` | Claude Code (`~/.claude/skills/`) |
| `my/opencode/agents/` | OpenCode (`~/.config/opencode/agents/`) |
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
# 更新所有 submodule 到最新版本
git submodule update --remote

# 或者分别更新
git submodule update --remote upstream/everything-claude-code
git submodule update --remote upstream/anthropics-skills
git submodule update --remote upstream/openai-skills
git submodule update --remote upstream/ai-research-skills
git submodule update --remote upstream/obsidian-skills

# 查看有什么新变化
cd upstream/everything-claude-code && git log HEAD@{1}..HEAD --oneline
cd ../anthropics-skills && git log HEAD@{1}..HEAD --oneline
cd ../openai-skills && git log HEAD@{1}..HEAD --oneline
cd ../ai-research-skills && git log HEAD@{1}..HEAD --oneline
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

# 共用 command:
cat > my/commands/my-command.md << 'EOF'
description: 我的自定义命令

# My Command

这是我自己定义的 command...
EOF

./install.sh
```

## 推荐工作流程

### 1. 规划阶段 - `/plan`

**使用时机**: 新功能、复杂重构、架构变更

**流程**:
```
需求描述 → planner agent 分析 → 生成实施计划 → 用户确认 → 执行
```

### 2. 开发阶段 - `/tdd`

**使用时机**: 编写新功能、修复 Bug、重构

**TDD 循环** (RED → GREEN → IMPROVE):
1. 写 User Journey
2. 生成测试用例（先写测试）
3. 运行测试（应该失败）
4. 实现代码（使测试通过）
5. 重构代码
6. 验证覆盖率 ≥ 80%

### 3. 审查阶段 - `/code-review`

**使用时机**: 代码完成后

**并行审查**（多 agent 同时执行）:
- 代码质量和可维护性
- 安全漏洞检查
- 性能问题识别
- 一致性审查

### 4. 更新文档 - `/update-docs`

**使用时机**: 代码修改后同步更新相关文档

## 命名规范

| 位置 | 命名建议 | 说明 |
|------|----------|------|
| `upstream/` | 保持原名 | 不修改，仅参考 |
| `my/` | `xxx.md` 或自定义名 | 中文改造版本或原创内容 |

## 可用组件

### Agents (Claude Code)

- `planner` - 功能实施规划
- `architect` - 系统设计决策
- `tdd-guide` - 测试驱动开发
- `code-reviewer-ts` - TypeScript 代码审查
- `code-reviewer-py` - Python 代码审查
- `refactor-cleaner-ts` - TypeScript 死代码清理
- `refactor-cleaner-python` - Python 死代码清理
- `doc-updater` - 文档更新

### Commands (共用)

- `/plan` - 实施规划
- `/tdd` - TDD 开发流程
- `/code-review-ts` - TypeScript 代码审查
- `/code-review-py` - Python 代码审查
- `/update-docs` - 更新文档
- `/update-codemaps` - 更新代码地图

### Skills (Claude Code)

- `skill-creator` - 从 Git 历史提取技能
- `python-async-modernizer` - Python 异步代码分析和现代化（检测阻塞调用、迁移到 TaskGroup）

## 注意事项

1. **永远不要修改 `upstream/` 目录** - 只使用 `git submodule update --remote` 更新
2. **所有个人配置放在 `my/`** - 这是唯一会被 `install.sh` 安装的目录
3. **改造前先从 upstream 复制** - 保留原文件参考，在副本上修改
4. **定期同步上游** - 获取原项目的新功能和修复

## 参考文档

- **上游项目文档**: `upstream/everything-claude-code/README.md`
- **Shorthand Guide**: [The Shorthand Guide to Everything Claude Code](https://x.com/affaanmustafa/status/2012378465664745795)
- **Longform Guide**: [The Longform Guide to Everything Claude Code](https://x.com/affaanmustafa/status/2014040193557471352)
- **本仓库详细说明**: `my/README.md`

## 许可证

MIT - Use freely, modify as needed, contribute back if you can.

---

**Star this repo if it helps. Build something great.**
