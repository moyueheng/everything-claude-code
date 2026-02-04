# OpenCode, Claude Code, Codex 配置对比

本文档对比三个 AI 编程工具的配置系统异同点。

## 1. Agents (代理)

### Claude Code

**特点：**
- 支持 **Subagents (子代理)** 系统
- 内置代理：Explore (只读探索)、Plan (规划)、General-purpose (通用)
- 支持自定义代理，通过 Markdown 文件定义
- 代理可以运行在前台或后台
- 支持嵌套代理调用（但子代理不能创建子代理）

**配置位置：**
- 项目级：`.claude/agents/`
- 用户级：`~/.claude/agents/`
- CLI 参数：`--agents` JSON 格式
- 插件：`agents/` 目录

**配置格式：**
```yaml
---
name: dev-code-reviewer-ts
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
permissionMode: acceptEdits
skills:
  - api-conventions
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---
系统提示词内容...
```

### OpenCode

**特点：**
- 支持 **Primary Agents (主代理)** 和 **Subagents (子代理)**
- 内置主代理：Build (默认，全工具)、Plan (受限，只读)
- 内置子代理：General (通用)、Explore (只读)
- 通过 Tab 键切换主代理
- 通过 `@mention` 调用子代理

**配置位置：**
- 全局：`~/.config/opencode/agents/`
- 项目级：`.opencode/agents/`
- JSON 配置：`opencode.json` 中的 `agent` 字段

**配置格式 (Markdown)：**
```yaml
---
description: Reviews code for quality and best practices
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false
permission:
  edit: deny
  bash:
    "*": ask
    "git diff": allow
maxSteps: 10
hidden: false
---
系统提示词内容...
```

**配置格式 (JSON)：**
```json
{
  "agent": {
    "dev-code-reviewer-ts": {
      "mode": "subagent",
      "description": "Reviews code for quality",
      "model": "anthropic/claude-sonnet-4-20250514",
      "tools": {
        "write": false,
        "edit": false
      },
      "permission": {
        "edit": "deny"
      }
    }
  }
}
```

### Codex

**特点：**
- 主要使用 **Skills (技能)** 系统，Agent 概念相对弱化
- 通过 `AGENTS.md` 文件提供项目级指令
- 支持分层指令系统（全局 + 项目 + 子目录覆盖）

**配置位置：**
- 全局：`~/.codex/AGENTS.md` 或 `~/.codex/AGENTS.override.md`
- 项目级：`.codex/AGENTS.md` 或 `AGENTS.md`
- 子目录：任意子目录中的 `AGENTS.override.md`

**配置格式：**
纯 Markdown 格式，无 YAML frontmatter：
```markdown
# 项目指令

## 代码规范
- 使用 TypeScript 严格模式
- 优先使用函数式编程

## 工作流程
1. 先运行测试
2. 然后提交代码
```

### 对比总结

| 特性 | Claude Code | OpenCode | Codex |
|------|-------------|----------|-------|
| 代理类型 | Subagents | Primary + Subagents | Skills-based |
| 配置格式 | Markdown + YAML | Markdown + YAML / JSON | Markdown |
| 内置代理 | Explore, Plan, General | Build, Plan, General, Explore | 无 |
| 代理切换 | 自动委托 / 手动调用 | Tab 键切换 / @mention | 通过 Skills |
| 权限控制 | permissionMode | permission 字段 | Rules 系统 |
| 工具限制 | tools / disallowedTools | tools 布尔值 | 通过 Rules |

---

## 2. Skills (技能)

### Claude Code

**特点：**
- Skills 已**完全取代** Commands 系统
- 支持 Agent Skills 开放标准
- 支持动态上下文注入 (`!command` 语法)
- 支持在子代理中运行 (`context: fork`)
- 支持参数传递 (`$ARGUMENTS`, `$0`, `$1` 等)

**配置位置：**
- 项目级：`.claude/skills/<name>/SKILL.md`
- 用户级：`~/.claude/skills/<name>/SKILL.md`
- 插件：`<plugin>/skills/<name>/SKILL.md`
- 兼容：`.claude/commands/` (旧格式)

**配置格式：**
```yaml
---
name: explain-code
description: Explains code with visual diagrams
argument-hint: "[filename]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
model: sonnet
context: fork
agent: Explore
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---

When explaining code, always include:
1. **Start with an analogy**
2. **Draw a diagram**
```

**调用方式：**
- 自动调用：Claude 根据 description 自动选择
- 手动调用：`/skill-name` 或 `/explain-code`
- 子代理中预加载：`skills: [explain-code]`

### OpenCode

**特点：**
- 通过 `skill` 工具动态加载
- 支持 Claude Code 兼容路径
- 渐进式披露：只加载名称和描述，调用时才加载完整内容

**配置位置：**
- 项目级：`.opencode/skills/<name>/SKILL.md`
- 全局：`~/.config/opencode/skills/<name>/SKILL.md`
- Claude 兼容：`.claude/skills/<name>/SKILL.md` 和 `~/.claude/skills/<name>/SKILL.md`

**配置格式：**
```yaml
---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
---

## What I do
- Draft release notes from merged PRs
- Propose a version bump
```

**调用方式：**
- 工具调用：`skill({ name: "git-release" })`
- 权限控制：通过 `permission.skill` 配置

### Codex

**特点：**
- 基于 [Agent Skills 开放标准](https://agentskills.io)
- 支持渐进式披露（只加载元数据，调用时才加载完整内容）
- 支持显式调用（`$skill-name`）和隐式调用

**配置位置：**
- 项目级：`.codex/skills/<name>/SKILL.md`
- 用户级：`~/.codex/skills/<name>/SKILL.md`
- 系统级：`/etc/codex/skills/<name>/SKILL.md`
- 上级目录：`../.codex/skills/`

**配置格式：**
```yaml
---
name: draft-commit-message
description: Draft a conventional commit message when the user asks for help
metadata:
  short-description: Draft an informative commit message
---

Draft a conventional commit message that matches the change summary.

Requirements:
- Use the Conventional Commits format
- Use the imperative mood
```

**调用方式：**
- 显式调用：`$skill-name` 或 `$draft-commit-message`
- 隐式调用：Codex 根据任务自动选择
- 通过 `$skill-installer` 安装新技能

### 对比总结

| 特性 | Claude Code | OpenCode | Codex |
|------|-------------|----------|-------|
| 标准 | Agent Skills 标准 | Agent Skills 标准 | Agent Skills 标准 |
| 调用方式 | `/skill-name` | `skill()` 工具 | `$skill-name` |
| 子代理支持 | 是 (`context: fork`) | 通过 Agents | 有限 |
| 动态注入 | `!command` 语法 | 不支持 | 不支持 |
| 参数传递 | `$ARGUMENTS`, `$0`, `$1` | 不支持 | 不支持 |
| 权限控制 | `disable-model-invocation` | `permission.skill` | `[[skills.config]]` |
| 安装机制 | 手动创建 | 手动创建 | `$skill-installer` |

---

## 3. Commands (命令)

### Claude Code

**状态：** Skills 已完全取代 Commands
- 旧 `.claude/commands/` 目录仍兼容
- 建议迁移到 `.claude/skills/`

### OpenCode

**特点：**
- 自定义斜杠命令
- 支持参数传递
- 支持 shell 输出注入
- 支持文件引用

**配置位置：**
- 全局：`~/.config/opencode/commands/`
- 项目级：`.opencode/commands/`
- JSON 配置：`opencode.json` 中的 `command` 字段

**配置格式 (Markdown)：**
```yaml
---
description: Run tests with coverage
agent: build
model: anthropic/claude-3-5-sonnet-20241022
subtask: true
---
Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

**配置格式 (JSON)：**
```json
{
  "command": {
    "test": {
      "template": "Run the full test suite...",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-3-5-sonnet-20241022",
      "subtask": true
    }
  }
}
```

**调用方式：**
- `/command-name` 例如 `/test`
- 参数传递：`/component Button` (使用 `$ARGUMENTS` 或 `$1`, `$2`)
- Shell 注入：`!command` 语法
- 文件引用：`@filename`

### Codex

**特点：**
- 内置斜杠命令（`/help`, `/compact` 等）
- 通过 Skills 实现自定义命令
- IDE 和 CLI 都支持

**内置命令：**
- `/help` - 显示帮助
- `/compact` - 压缩上下文
- `/clear` - 清除屏幕
- `/history` - 显示历史
- `/skills` - 显示可用技能

**调用方式：**
- `/command-name`
- 通过 `$skill-name` 调用技能

### 对比总结

| 特性 | Claude Code | OpenCode | Codex |
|------|-------------|----------|-------|
| 状态 | 被 Skills 取代 | 独立系统 | 内置 + Skills |
| 配置格式 | N/A (已弃用) | Markdown / JSON | 通过 Skills |
| 参数支持 | N/A | `$ARGUMENTS`, `$1`, `$2` | 通过 Skills |
| Shell 注入 | N/A | `!command` | 有限 |
| 文件引用 | N/A | `@filename` | 有限 |
| 子代理触发 | N/A | `subtask: true` | 通过 Skills |

---

## 4. Rules (规则)

### Claude Code

**特点：**
- 通过 `CLAUDE.md` 提供项目级指令
- 支持全局 `~/.claude/CLAUDE.md`
- 支持嵌套目录自动发现

**配置位置：**
- 项目级：`CLAUDE.md`
- 用户级：`~/.claude/CLAUDE.md`
- 嵌套目录：任意子目录中的 `.claude/skills/`

**配置格式：**
纯 Markdown：
```markdown
# Project Guidelines

## Code Style
- Use TypeScript with strict mode
- Prefer functional programming patterns
```

### OpenCode

**特点：**
- 通过 `AGENTS.md` 提供项目级指令
- 支持 Claude Code 兼容（`CLAUDE.md`）
- 支持外部文件引用

**配置位置：**
- 项目级：`AGENTS.md`
- 全局：`~/.config/opencode/AGENTS.md`
- Claude 兼容：`CLAUDE.md` (如果 AGENTS.md 不存在)
- 全局 Claude 兼容：`~/.claude/CLAUDE.md`

**配置格式：**
纯 Markdown：
```markdown
# SST v3 Monorepo Project

## Project Structure
- `packages/` - Contains all workspace packages
- `infra/` - Infrastructure definitions

## Code Standards
- Use TypeScript with strict mode
```

**外部文件引用：**
```json
{
  "instructions": ["CONTRIBUTING.md", "docs/guidelines.md"]
}
```

### Codex

**特点：**
- 双层规则系统：**Rules** (命令控制) + **AGENTS.md** (项目指令)
- Rules 控制沙箱外命令执行
- AGENTS.md 提供项目上下文

**Rules 配置位置：**
- `~/.codex/rules/default.rules`
- `./codex/rules/*.rules`

**Rules 配置格式：**
Starlark 语言：
```starlark
prefix_rule(
    pattern = ["gh", "pr", "view"],
    decision = "prompt",
    justification = "Viewing PRs is allowed with approval",
    match = [
        "gh pr view 7888",
        "gh pr view --repo openai/codex",
    ],
    not_match = [
        "gh pr --repo openai/codex view 7888",
    ],
)
```

**AGENTS.md 配置：**
同 OpenCode，支持分层：
1. `~/.codex/AGENTS.md` (全局)
2. `AGENTS.md` (项目根目录)
3. `AGENTS.override.md` (子目录覆盖)

### 对比总结

| 特性 | Claude Code | OpenCode | Codex |
|------|-------------|----------|-------|
| 项目指令 | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| 全局指令 | `~/.claude/CLAUDE.md` | `~/.config/opencode/AGENTS.md` | `~/.codex/AGENTS.md` |
| 分层覆盖 | 嵌套目录发现 | 单文件 | 多层 + override |
| 命令控制 | 通过 Hooks | 通过 Permissions | Rules (Starlark) |
| 外部引用 | 不支持 | `instructions` 数组 | `project_doc_fallback_filenames` |
| 文件大小限制 | 无明确限制 | 无明确限制 | `project_doc_max_bytes` (32KB 默认) |

---

## 5. Hooks (钩子)

### Claude Code

**特点：**
- 丰富的生命周期钩子系统
- 支持 PreToolUse / PostToolUse 等事件
- 支持子代理生命周期事件
- 通过命令或 JSON 配置

**支持的事件：**
- `PreToolUse` - 工具调用前
- `PostToolUse` - 工具调用后
- `PermissionRequest` - 权限请求时
- `UserPromptSubmit` - 用户提交提示时
- `Notification` - 通知时
- `Stop` - 停止时
- `SubagentStop` - 子代理停止时
- `PreCompact` - 压缩前
- `Setup` - 初始化时
- `SessionStart` / `SessionEnd` - 会话开始/结束

**配置方式 (JSON)：**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '...' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/run-linter.sh"
          }
        ]
      }
    ]
  }
}
```

**配置方式 (Agent frontmatter)：**
```yaml
---
name: db-reader
description: Execute read-only database queries
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

### OpenCode

**特点：**
- 通过 **Plugins** 系统实现钩子
- JavaScript/TypeScript 编写
- 丰富的事件类型

**配置位置：**
- 全局：`~/.config/opencode/plugins/`
- 项目级：`.opencode/plugins/`
- npm 包：`opencode.json` 中的 `plugin` 字段

**支持的事件：**
- **命令事件**：`command.executed`
- **文件事件**：`file.edited`, `file.watcher.updated`
- **安装事件**：`installation.updated`
- **LSP 事件**：`lsp.client.diagnostics`, `lsp.updated`
- **消息事件**：`message.part.removed`, `message.updated`
- **权限事件**：`permission.asked`, `permission.replied`
- **会话事件**：`session.created`, `session.compacted`, `session.error`
- **工具事件**：`tool.execute.before`, `tool.execute.after`
- **TUI 事件**：`tui.prompt.append`, `tui.command.execute`

**配置格式 (JavaScript/TypeScript)：**
```javascript
// .opencode/plugins/example.js
export const MyPlugin = async ({ project, client, $, directory, worktree }) => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool === "read" && output.args.filePath.includes(".env")) {
        throw new Error("Do not read .env files")
      }
    },
    "tool.execute.after": async (input, output) => {
      console.log(`Tool ${input.tool} executed`)
    },
    "session.idle": async ({ event }) => {
      await $`osascript -e 'display notification "Session completed!" with title "opencode"'`
    }
  }
}
```

### Codex

**特点：**
- 没有独立的 Hooks 系统
- 通过 **Rules** 控制命令执行
- 通过 **AGENTS.md** 提供上下文

### 对比总结

| 特性 | Claude Code | OpenCode | Codex |
|------|-------------|----------|-------|
| 实现方式 | JSON / YAML 配置 | JavaScript/TypeScript Plugins | Rules 系统 |
| 事件丰富度 | 高 | 很高 | 低 |
| 编程能力 | 有限（shell 命令） | 完整 JS/TS | Starlark (Rules) |
| 子代理事件 | 支持 | 通过 session 事件 | 不支持 |
| 工具拦截 | PreToolUse / PostToolUse | tool.execute.before / after | 通过 Rules |
| 自定义工具 | 不支持 | 支持 | 有限 |
| 包管理 | 无 | npm / Bun | 无 |

---

## 6. MCP (Model Context Protocol)

### Claude Code

**特点：**
- 完整的 MCP 服务器支持
- 支持 HTTP、SSE、stdio 传输
- 支持 OAuth 认证
- 支持工具搜索 (Tool Search)
- 支持资源引用 (`@server:protocol://resource`)
- 支持提示作为命令 (`/mcp__server__prompt`)

**配置方式 (CLI)：**
```bash
# HTTP 服务器
claude mcp add --transport http notion https://mcp.notion.com/mcp

# SSE 服务器（已弃用）
claude mcp add --transport sse asana https://mcp.asana.com/sse

# stdio 服务器
claude mcp add --transport stdio --env KEY=value myserver -- npx -y @package/mcp-server

# 从 JSON 添加
claude mcp add-json my-server '{"type":"http","url":"..."}'

# 从 Claude Desktop 导入
claude mcp add-from-claude-desktop
```

**配置位置：**
- 用户级：`~/.claude.json`
- 项目级：`.mcp.json`
- 托管：`/Library/Application Support/ClaudeCode/managed-mcp.json`

**配置格式 (JSON)：**
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "local-server": {
      "type": "stdio",
      "command": "/path/to/server",
      "args": ["--port", "8080"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**范围层级：**
1. Local (默认) - `~/.claude.json` 项目路径下
2. Project - `.mcp.json` 项目根目录
3. User - `~/.claude.json` 跨项目

### OpenCode

**特点：**
- 支持本地和远程 MCP 服务器
- 支持 OAuth 自动认证
- 支持工具权限控制
- 支持 glob 模式匹配

**配置位置：**
- `opencode.json` 中的 `mcp` 字段

**配置格式 (JSON)：**
```json
{
  "mcp": {
    "my-local-mcp-server": {
      "type": "local",
      "command": ["npx", "-y", "my-mcp-command"],
      "environment": {
        "MY_ENV_VAR": "my_env_var_value"
      },
      "enabled": true,
      "timeout": 5000
    },
    "my-remote-mcp": {
      "type": "remote",
      "url": "https://my-mcp-server.com",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer MY_API_KEY"
      },
      "oauth": {
        "clientId": "{env:MY_MCP_CLIENT_ID}",
        "scope": "tools:read tools:execute"
      }
    }
  }
}
```

**工具权限控制：**
```json
{
  "tools": {
    "my-mcp*": false
  },
  "agent": {
    "my-agent": {
      "tools": {
        "my-mcp*": true
      }
    }
  }
}
```

**OAuth 认证：**
```bash
opencode mcp auth my-oauth-server
opencode mcp list
opencode mcp logout my-oauth-server
```

### Codex

**特点：**
- 支持 STDIO 和 HTTP (Streamable) 服务器
- 支持 Bearer Token 和 OAuth 认证
- CLI 和 IDE 共享配置

**配置位置：**
- 全局：`~/.codex/config.toml`
- 项目级：`.codex/config.toml` (仅限可信项目)

**配置方式 (CLI)：**
```bash
# 添加 stdio 服务器
codex mcp add context7 -- npx -y @upstash/context7-mcp

# 查看所有 MCP 命令
codex mcp --help

# TUI 中查看
/mcp
```

**配置格式 (TOML)：**
```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.context7.env]
MY_ENV_VAR = "MY_ENV_VALUE"

[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
http_headers = { "X-Figma-Region" = "us-east-1" }

[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
enabled_tools = ["open", "screenshot"]
disabled_tools = ["screenshot"]
startup_timeout_sec = 20
tool_timeout_sec = 45
enabled = true
```

**OAuth 配置：**
```toml
[mcp_servers.my-oauth-server]
type = "remote"
url = "https://mcp.example.com/mcp"
oauth = { }

# 或预注册客户端
[mcp_servers.my-oauth-server.oauth]
clientId = "{env:MY_MCP_CLIENT_ID}"
clientSecret = "{env:MY_MCP_CLIENT_SECRET}"
scope = "tools:read tools:execute"
```

### 对比总结

| 特性 | Claude Code | OpenCode | Codex |
|------|-------------|----------|-------|
| 传输类型 | HTTP, SSE, stdio | local (stdio), remote (HTTP) | STDIO, Streamable HTTP |
| 配置文件 | `.claude.json`, `.mcp.json` | `opencode.json` | `config.toml` |
| 认证方式 | OAuth, Header | OAuth, Header | Bearer Token, OAuth |
| 范围层级 | Local, Project, User | 统一配置 | Global, Project |
| 工具权限 | allowlist/denylist | glob 模式 + agent 覆盖 | enabled_tools / disabled_tools |
| 环境变量 | 支持扩展 `${VAR}` | 支持 `{env:VAR}` | 支持 `{env:VAR}` |
| 工具搜索 | 支持 (自动/手动) | 不支持 | 不支持 |
| 资源引用 | `@server:protocol://` | 不支持 | 不支持 |
| 提示命令 | `/mcp__server__prompt` | 不支持 | 不支持 |
| 管理命令 | `claude mcp *` | `opencode mcp *` | `codex mcp *` |

---

## 7. 配置系统总览

### 配置文件格式对比

| 工具 | 主配置文件 | 格式 | Agents | Skills | Commands | Rules | MCP |
|------|-----------|------|--------|--------|----------|-------|-----|
| **Claude Code** | `settings.json` | JSON | ✅ | ✅ | ❌ (已弃用) | ❌ (用 Hooks) | ✅ |
| **OpenCode** | `opencode.json` | JSON | ✅ | ✅ | ✅ | ✅ (AGENTS.md) | ✅ |
| **Codex** | `config.toml` | TOML | ❌ (用 Skills) | ✅ | ❌ (用 Skills) | ✅ (Rules + AGENTS.md) | ✅ |

### 目录结构对比

**Claude Code：**
```
~/.claude/
├── agents/          # 代理定义
├── skills/          # 技能定义
├── CLAUDE.md        # 全局规则
└── settings.json    # 设置和钩子

.claude/             # 项目级
├── agents/
├── skills/
└── CLAUDE.md

.mcp.json            # MCP 配置（项目级）
```

**OpenCode：**
```
~/.config/opencode/
├── agents/          # 代理定义
├── skills/          # 技能定义
├── commands/        # 自定义命令
├── plugins/         # 插件（Hooks）
├── AGENTS.md        # 全局规则
└── opencode.json    # 主配置

.opencode/           # 项目级
├── agents/
├── skills/
├── commands/
├── plugins/
└── AGENTS.md
```

**Codex：**
```
~/.codex/
├── skills/          # 技能定义
├── rules/           # 规则文件
├── AGENTS.md        # 全局指令
└── config.toml      # 主配置

.codex/              # 项目级
├── skills/
└── AGENTS.md
```

### 关键差异总结

1. **Agents：**
   - Claude Code 和 OpenCode 都有完整的 Agent 系统
   - Codex 主要通过 Skills 实现类似功能

2. **Skills：**
   - 三者都支持 Agent Skills 开放标准
   - Claude Code 功能最丰富（动态注入、子代理运行）
   - OpenCode 和 Codex 相对简洁

3. **Commands：**
   - Claude Code 已弃用，被 Skills 取代
   - OpenCode 有独立的 Commands 系统
   - Codex 通过 Skills 实现

4. **Rules：**
   - Claude Code 使用 Hooks 进行控制
   - OpenCode 使用 Permissions 系统
   - Codex 使用 Starlark 编写的 Rules 文件

5. **Hooks：**
   - Claude Code 有内置的 Hooks 系统（JSON/YAML 配置）
   - OpenCode 通过 Plugins 实现（JavaScript/TypeScript）
   - Codex 没有独立 Hooks 系统

6. **MCP：**
   - 三者都支持 MCP 标准
   - Claude Code 功能最完整（工具搜索、资源引用、提示命令）
   - OpenCode 和 Codex 支持核心功能

7. **配置语言：**
   - Claude Code: JSON + Markdown
   - OpenCode: JSON + Markdown
   - Codex: TOML + Markdown + Starlark (Rules)
