# Claude Code 个人配置仓库

个人 Claude Code 工作流配置仓库，基于 [everything-claude-code](https://github.com/affaan-m/everything-claude-code) 改造。

---

## 📌 当前工作重点（2026-02-03 ~ 2026-03-03）

**未来一个月专注于上游 everything-claude-code 仓库的深入研究与改造**

- 系统性梳理 upstream/everything-claude-code/ 的所有配置
- 将有价值的组件复制到 my/ 进行中文本地化改造
- 同步更新文档中的可用组件列表
- 向 affaan-m/everything-claude-code 贡献改进

---

## 项目概述

这是个人 Claude Code/OpenCode 配置仓库，采用 submodule 架构管理：

- **`upstream/`** - 原项目完整内容（只读，通过 submodule 同步更新）
  - `everything-claude-code/` - affaan-m 的配置仓库（submodule）
  - `anthropics-skills/` - anthropics 官方的 skills 仓库（submodule）
  - `openai-skills/` - OpenAI 官方的 skills 仓库（submodule）
  - `ai-research-skills/` - Orchestra-Research 的 AI-research-SKILLs 仓库（submodule）
  - `obsidian-skills/` - kepano/obsidian-skills 仓库（submodule）
  - `superpowers/` - obra/superpowers 完整软件开发工作流系统（submodule）
- **`my/`** - 个人改造的配置（从 upstream 挑选并本地化）

## 目录结构

```
.
├── .plans/                     # 实施计划持久化目录
├── my/                          # 个人配置
│   ├── claudecode/              # Claude Code 专属配置
│   │   ├── agents/              # 改造后的 agents（中文/个性化）
│   │   └── skills/              # 改造后的 skills
│   ├── opencode/                # OpenCode 专属配置
│   │   ├── agents/
│   │   ├── commands/            # OpenCode commands
│   │   └── skills/
│   ├── codex/                   # Codex 专属配置
│   │   └── skills/
│   └── mcp-configs/             # MCP 服务器配置
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
├── upstream/superpowers/        # obra/superpowers 完整软件开发工作流（submodule）
│   ├── agents/
│   ├── commands/
│   ├── skills/
│   └── hooks/
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
git submodule update --remote upstream/superpowers

# 查看有什么新变化
cd upstream/everything-claude-code && git log HEAD@{1}..HEAD --oneline
cd ../anthropics-skills && git log HEAD@{1}..HEAD --oneline
cd ../openai-skills && git log HEAD@{1}..HEAD --oneline
cd ../ai-research-skills && git log HEAD@{1}..HEAD --oneline
cd ../obsidian-skills && git log HEAD@{1}..HEAD --oneline
cd ../superpowers && git log HEAD@{1}..HEAD --oneline

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

## 推荐工作流程

### 1. 规划阶段

**Claude Code**: 使用 `planner` agent
**OpenCode**: 使用 `/plan` command

**使用时机**: 新功能、复杂重构、架构变更

**流程**:
```
需求描述 → planner agent 分析 → 生成实施计划 → 用户确认 → 执行
```

### 2. 开发阶段

**Claude Code**: 使用 `tdd-guide-ts` 或 `tdd-guide-py` agent
**OpenCode**: 使用 `/tdd` command

**使用时机**: 编写新功能、修复 Bug、重构

**TDD 循环** (RED → GREEN → IMPROVE):
1. 写 User Journey
2. 生成测试用例（先写测试）
3. 运行测试（应该失败）
4. 实现代码（使测试通过）
5. 重构代码
6. 验证覆盖率 ≥ 80%

### 3. 审查阶段

**Claude Code**: 使用 `code-reviewer-ts` 或 `code-reviewer-py` agent
**OpenCode**: 使用 `/code-review-ts` 或 `/code-review-py` command

**使用时机**: 代码完成后

**并行审查**（多 agent 同时执行）:
- 代码质量和可维护性
- 安全漏洞检查
- 性能问题识别
- 一致性审查

### 4. 更新文档

**Claude Code**: 使用 `doc-updater` agent
**OpenCode**: 使用 `/update-docs` command

**使用时机**: 代码修改后同步更新相关文档

## 命名规范

| 位置 | 命名建议 | 说明 |
|------|----------|------|
| `upstream/` | 保持原名 | 不修改，仅参考 |
| `my/` | `xxx.md` 或自定义名 | 中文改造版本或原创内容 |

## 可用组件

### Agents (Claude Code)

| Agent | 描述 |
|-------|------|
| `planner` | 复杂功能和重构规划专员 |
| `architect` | 软件架构专家，系统设计和可扩展性 |
| `tdd-guide-ts` | TypeScript 测试驱动开发专家 |
| `tdd-guide-py` | Python 测试驱动开发专家 |
| `code-reviewer-ts` | TypeScript 代码审查专员 |
| `code-reviewer-py` | Python 代码审查专员 |
| `refactor-cleaner-ts` | TypeScript 死代码清理和重构 |
| `refactor-cleaner-python` | Python 死代码清理和重构 |
| `doc-updater` | 文档和代码地图专家 |

### Commands (OpenCode)

| Command | 描述 |
|---------|------|
| `/plan` | 实施规划 |
| `/tdd` | TDD 开发流程 |
| `/code-review-ts` | TypeScript 代码审查 |
| `/code-review-py` | Python 代码审查 |
| `/update-docs` | 更新文档 |
| `/update-codemaps` | 更新代码地图 |

### Skills (Claude Code)

| Skill | 描述 |
|-------|------|
| `dev-plan` | 开发项目规划 |
| `dev-tdd-ts` | TypeScript 测试驱动开发工作流 |
| `dev-tdd-py` | Python 测试驱动开发工作流 |
| `dev-review-ts` | TypeScript 代码审查 |
| `dev-review-py` | Python 代码审查 |
| `dev-async-modernize` | Python 异步代码现代化 |
| `dev-update-docs` | 开发文档更新 |
| `dev-update-codemaps` | 代码地图更新 |
| `dev-e2e` | 使用 Playwright 生成和运行端到端测试 |
| `tool-mcp-builder` | MCP 服务器构建指南 |
| `tool-macos-hidpi` | macOS HiDPI 分辨率设置 |
| `tool-sshfs-mount` | SSH 远程目录挂载 |
| `tool-skill-creator` | Skill 创建指南 |

### Skills (Codex)

| Skill | 描述 |
|-------|------|
| `dev-plan` | 开发项目规划 |
| `dev-tdd-workflow` | 通用 TDD 工作流（合并 command + skill） |
| `dev-tdd-ts` | TypeScript 测试驱动开发 |
| `dev-tdd-py` | Python 测试驱动开发 |
| `dev-rehab-legacy-tests` | 遗留测试改造 TDD 流程 |
| `life-obsidian-markdown` | Obsidian Markdown 技能 |
| `life-obsidian-bases` | Obsidian Bases 技能 |
| `life-obsidian-json-canvas` | Obsidian JSON Canvas 技能 |

## 注意事项

1. **永远不要修改 `upstream/` 目录** - 只使用 `git submodule update --remote` 更新
2. **所有个人配置放在 `my/`** - 这是唯一会被 `install.sh` 安装的目录
3. **改造前先从 upstream 复制** - 保留原文件参考，在副本上修改
4. **定期同步上游** - 获取原项目的新功能和修复
5. **实施计划统一存放在 `.plans/`** - 使用 `YYYY-MM-DD-<feature-name>.md` 命名

## 文档索引

- [配置系统对比](docs/differences.md) - OpenCode、Claude Code、Codex 配置系统对比
- [Skill 命名规范](docs/skill-naming-convention.md) - Skills 分类前缀命名规范
- [上游更新记录](docs/upstream-updates.md) - 上游仓库更新追踪

## 参考文档

- **上游项目文档**: `upstream/everything-claude-code/README.md`
- **Shorthand Guide**: [The Shorthand Guide to Everything Claude Code](https://x.com/affaanmustafa/status/2012378465664745795)
- **Longform Guide**: [The Longform Guide to Everything Claude Code](https://x.com/affaanmustafa/status/2014040193557471352)
- **本仓库详细说明**: `my/README.md`

## 许可证

MIT - Use freely, modify as needed, contribute back if you can.

---

**Star this repo if it helps. Build something great.**
