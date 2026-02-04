# Subagent 与 MCP 工具配置指南

本文档详细介绍如何在 Claude Code 中配置 Subagent 和 MCP (Model Context Protocol) 工具的访问控制。

> **官方文档参考**：
> - [Subagents 官方文档](https://code.claude.com/docs/en/sub-agents)
> - [MCP 配置官方文档](https://code.claude.com/docs/en/mcp)
> - [Settings 官方文档](https://code.claude.com/docs/en/settings)

## 目录

1. [Subagent 基本配置](#1-subagent-基本配置)
2. [MCP 工具继承机制](#2-mcp-工具继承机制)
3. [工具访问控制](#3-工具访问控制)
4. [MCP 服务器配置](#4-mcp-服务器配置)
5. [组织级 MCP 控制](#5-组织级-mcp-控制)
6. [最佳实践](#6-最佳实践)

---

## 1. Subagent 基本配置

Subagent 通过 Markdown 文件的 YAML frontmatter 定义，位于 `~/.claude/agents/` 或 `.claude/agents/` 目录。

### 基本格式

```yaml
---
name: code-reviewer
description: 代码审查专员，主动审查代码质量
tools: Read, Glob, Grep
model: sonnet
---

You are a senior code reviewer ensuring high standards of code quality and security.
```

### 配置字段说明（官方）

根据 [官方 Subagents 文档](https://code.claude.com/docs/en/sub-agents)，支持的 frontmatter 字段：

| 字段 | 必填 | 类型 | 说明 |
|------|:----:|------|------|
| `name` | 是 | string | Subagent 的唯一标识，使用小写字母和连字符 |
| `description` | 是 | string | 描述何时应该委托给此 subagent |
| `tools` | 否 | string[] | Subagent 可使用的工具（省略则继承所有工具） |
| `disallowedTools` | 否 | string[] | 禁止使用的工具，从继承或指定的列表中移除 |
| `model` | 否 | string | 模型：`sonnet` / `opus` / `haiku` / `inherit`（默认） |
| `permissionMode` | 否 | string | 权限模式：`default` / `acceptEdits` / `dontAsk` / `bypassPermissions` / `plan` |
| `skills` | 否 | string[] | 启动时注入到 subagent 上下文的 skills |
| `hooks` | 否 | object | 作用于此 subagent 的生命周期钩子 |

### 可用的内置工具

```
Read, Write, Edit, NotebookEdit, Bash, Glob, Grep, AskUserQuestion,
Task, TaskOutput, KillShell, EnterPlanMode, ExitPlanMode, TaskCreate,
TaskGet, TaskUpdate, TaskList, Skill, LSP, MCPSearch, WebFetch, WebSearch
```

---

## 2. MCP 工具继承机制

### 默认行为

根据 [官方文档](https://code.claude.com/docs/en/sub-agents)：

> **By default, subagents inherit all tools from the main conversation, including MCP tools.**

- Subagent 默认**继承**主对话的所有工具，包括 MCP 工具
- 如果不指定 `tools` 字段，subagent 可以访问所有工具
- 如果指定 `tools` 字段，subagent 只能访问列出的工具

### MCP 工具继承示例

```yaml
---
# 不指定 tools - 继承所有工具（包括所有 MCP）
name: general-helper
description: 通用助手，可以使用所有工具
model: sonnet
---
```

```yaml
---
# 指定 tools - 只能使用列出的工具
name: read-only-explorer
description: 只读探索者，不能修改文件
tools: Read, Grep, Glob
model: haiku
---
```

> **注意**：当指定 `tools` 时，只限制内置工具。MCP 工具的访问需要通过权限系统控制。

---

## 3. 工具访问控制

### 使用 tools 字段（允许列表）

```yaml
---
name: safe-researcher
description: 只读研究助手
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
---
```

### 使用 disallowedTools 字段（拒绝列表）

```yaml
---
name: code-reviewer
description: 代码审查（不能修改文件）
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit, NotebookEdit
model: opus
---
```

### 权限控制流程

```
┌─────────────────────────────────────────────────────────┐
│                    主 Claude 实例                        │
│  (所有内置工具 + 所有已启用的 MCP 工具)                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Subagent 定义       │
         │   tools /             │
         │   disallowedTools     │
         └───────────┬───────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│  指定 tools  │          │  未指定      │
│  白名单模式  │          │  全继承模式  │
└──────────────┘          └──────────────┘
```

---

## 4. MCP 服务器配置

MCP 服务器的实际配置在 `~/.claude.json` 或 `.mcp.json` 中。

### 配置位置

| 位置 | 范围 | 文件 |
|------|------|------|
| Local | 当前项目（仅你） | `~/.claude.json` |
| Project | 项目团队 | `.mcp.json` |
| User | 所有项目（仅你） | `~/.claude.json` |
| Managed | 全局组织 | `/Library/Application Support/ClaudeCode/managed-mcp.json` |

### 配置格式

根据 [MCP 官方文档](https://code.claude.com/docs/en/mcp)：

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/projects"],
      "env": {}
    },
    "memory": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "PG_CONNECTION_STRING": "postgresql://..."
      }
    }
  }
}
```

### CLI 添加 MCP 服务器

```bash
# HTTP 服务器
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Stdio 服务器
claude mcp add --transport stdio --env API_KEY=xxx api-server -- npx -y my-mcp-server

# 列出所有服务器
claude mcp list

# 删除服务器
claude mcp remove notion
```

### 环境变量扩展

支持在 `.mcp.json` 中使用环境变量：

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

---

## 5. 组织级 MCP 控制

### Managed MCP 配置

对于需要集中控制的组织，可以使用 `managed-mcp.json` 文件：

#### 位置

- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux/WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

#### 方式一：独占控制

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"]
    }
  }
}
```

用户**无法添加、修改或使用**除定义之外的其他 MCP 服务器。

#### 方式二：允许列表/拒绝列表

在 `managed-settings.json` 中使用 `allowedMcpServers` 和 `deniedMcpServers`：

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "sentry" },
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverUrl": "https://mcp.company.com/*" }
  ],
  "deniedMcpServers": [
    { "serverName": "dangerous-server" },
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

| 字段 | 说明 |
|------|------|
| `serverName` | 按服务器名称匹配 |
| `serverCommand` | 按完整命令数组匹配（stdio 服务器） |
| `serverUrl` | 按 URL 模式匹配（支持 `*` 通配符） |

---

## 6. 最佳实践

### 1. 最小权限原则

为敏感操作创建受限的 subagent：

```yaml
---
name: prod-deployer
description: 生产部署专员（危险操作，需要人工确认）
tools: Bash
model: opus
permissionMode: default
---
```

### 2. 避免 MCP 过载

根据 [官方文档](https://code.claude.com/docs/en/mcp)：

> **Critical:** Don't enable all MCPs at once. Your 200k context window can shrink to 70k with too many tools enabled.

建议：
- 配置 20-30 个 MCP 服务器
- 每个项目保持 < 10 个已启用
- 活跃工具保持在 80 个以下

```bash
# 在项目中禁用不需要的 MCP
export ENABLE_TOOL_SEARCH=auto:5  # 5% 上下文阈值时启用工具搜索
```

### 3. 使用 Hook 验证操作

通过 `PreToolUse` hooks 进行细粒度控制：

```yaml
---
name: db-reader
description: 只读数据库查询
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

验证脚本示例：

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# 阻止 SQL 写操作
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi
exit 0
```

### 4. 项目级 MCP 共享

在项目根目录创建 `.mcp.json`：

```json
{
  "mcpServers": {
    "project-docs": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./docs"]
    }
  }
}
```

### 5. 敏感数据保护

在 `.claude/settings.json` 中使用 `permissions.deny`：

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)"
    ]
  }
}
```

---

## 附录：常见问题

### Q: 如何查看当前可用的 MCP 工具？

A: 在 Claude Code 中使用 `/mcp` 命令查看 MCP 状态。

### Q: Subagent 可以使用主对话未启用的 MCP 吗？

A: 不可以。Subagent 只能访问主对话中已启用的 MCP 工具。

### Q: 如何限制 Subagent 访问特定的 MCP 工具？

A: 使用权限系统的 `allow`/`deny` 规则，或创建专门的项目配置来限制可用的 MCP 服务器。

### Q: MCP 工具太多导致上下文窗口变小怎么办？

A:
1. 使用 `ENABLE_TOOL_SEARCH=auto:5` 降低工具搜索阈值
2. 使用 `disabledMcpServers` 禁用不需要的 MCP
3. 在项目级别只配置必需的 MCP 服务器

### Q: background subagent 可以使用 MCP 工具吗？

A: 根据 [官方文档](https://code.claude.com/docs/en/sub-agents)：

> MCP tools are not available in background subagents.

---

## 参考资源

### 官方文档

| 文档 | 链接 |
|------|------|
| **Subagents** | https://code.claude.com/docs/en/sub-agents |
| **MCP 配置** | https://code.claude.com/docs/en/mcp |
| **Settings** | https://code.claude.com/docs/en/settings |
| **中文文档** | https://code.claude.com/docs/zh-CN/sub-agents |
| **中文 MCP** | https://code.claude.com/docs/zh-CN/mcp |
| **中文 Settings** | https://code.claude.com/docs/zh-CN/settings |

### 相关资源

- [MCP 协议规范](https://modelcontextprotocol.io)
- [MCP 快速入门](https://modelcontextprotocol.io/quickstart/user)
- [everything-claude-code 仓库](https://github.com/affaan-m/everything-claude-code)
