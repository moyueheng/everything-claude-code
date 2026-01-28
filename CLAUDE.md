# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Claude Code 插件仓库，包含经过实战验证的配置集合，包括 agents、skills、hooks、commands 和 rules。

## 关键命令

### 测试
```bash
# 运行所有测试
node tests/run-all.js

# 运行单个测试文件
node tests/lib/utils.test.js
node tests/lib/package-manager.test.js
node tests/hooks/hooks.test.js
```

### 包管理器设置
```bash
# 检测当前包管理器
node scripts/setup-package-manager.js --detect

# 设置全局包管理器
node scripts/setup-package-manager.js --global pnpm

# 设置项目包管理器
node scripts/setup-package-manager.js --project bun
```

## 安装

### 方式一：作为插件安装（推荐）

```bash
# 添加市场
/plugin marketplace add affaan-m/everything-claude-code

# 安装插件
/plugin install everything-claude-code@everything-claude-code
```

### 方式二：通过 cp 手动安装

如需完全控制安装内容，可手动复制组件：

```bash
# 克隆仓库
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code

# 复制 agents
cp agents/*.md ~/.claude/agents/

# 复制 rules（注意：plugin 不支持自动安装 rules，必须手动安装）
cp rules/*.md ~/.claude/rules/

# 复制 commands
cp commands/*.md ~/.claude/commands/

# 复制 skills（递归复制）
cp -r skills/* ~/.claude/skills/

# 项目级 rules（仅当前项目）
mkdir -p .claude/rules
cp rules/*.md .claude/rules/
```

**补充配置：**

- **Hooks**: 将 `hooks/hooks.json` 的内容合并到 `~/.claude/settings.json`
- **MCP**: 将 `mcp-configs/mcp-servers.json` 中需要的服务复制到 `~/.claude.json`，并替换 API key 占位符

## 架构概述

### 目录结构

```
everything-claude-code/
|-- .claude-plugin/          # 插件清单文件
|   |-- plugin.json          # 插件元数据和组件路径
|   |-- marketplace.json     # 市场目录配置
|
|-- agents/                  # 专业化子代理
|-- skills/                  # 工作流定义和领域知识
|-- commands/                # 斜杠命令
|-- rules/                   # 始终遵循的指南
|-- hooks/                   # 基于触发器的自动化
|
|-- scripts/                 # 跨平台 Node.js 脚本
|   |-- lib/                 # 共享工具库
|   |   |-- utils.js         # 跨平台文件/路径/系统工具
|   |   |-- package-manager.js # 包管理器检测和选择
|   |-- hooks/               # Hook 实现
|   |   |-- session-start.js   # 会话开始时加载上下文
|   |   |-- session-end.js     # 会话结束时保存状态
|   |   |-- pre-compact.js     # 压缩前保存状态
|   |   |-- suggest-compact.js # 建议压缩时机
|   |   |-- evaluate-session.js # 从会话中提取模式
|   |-- setup-package-manager.js
|
|-- tests/                   # 测试套件
|-- contexts/                # 动态系统提示注入上下文
|-- mcp-configs/             # MCP 服务器配置
```

### 核心组件

1. **Agents（代理）**：处理特定委托任务的子代理，如 planner、architect、code-reviewer 等
2. **Skills（技能）**：工作流定义，由命令或代理调用
3. **Commands（命令）**：快速执行的斜杠命令
4. **Rules（规则）**：始终遵循的指南
5. **Hooks（钩子）**：基于工具事件的自动化触发器

### Hooks 系统

Hooks 定义在 `hooks/hooks.json` 中，支持以下触发点：
- `PreToolUse`：工具使用前（如阻止非 tmux 中运行的 dev server）
- `PostToolUse`：工具使用后（如检查 console.log）
- `PreCompact`：上下文压缩前
- `SessionStart`：新会话开始时
- `SessionEnd`：会话结束时

### 跨平台支持

所有 hooks 和脚本均使用 Node.js 重写，支持 Windows、macOS 和 Linux。

包管理器检测优先级：
1. 环境变量 `CLAUDE_PACKAGE_MANAGER`
2. 项目配置 `.claude/package-manager.json`
3. `package.json` 的 `packageManager` 字段
4. Lock 文件检测
5. 全局配置 `~/.claude/package-manager.json`
6. 回退到第一个可用的包管理器

### 工具库（scripts/lib/utils.js）

提供跨平台的工具函数：
- 目录管理：`getHomeDir()`, `getClaudeDir()`, `getSessionsDir()`, `getLearnedSkillsDir()`
- 文件操作：`findFiles()`, `readFile()`, `writeFile()`, `replaceInFile()`
- Git 操作：`isGitRepo()`, `getGitModifiedFiles()`
- 系统命令：`commandExists()`, `runCommand()`

## 开发注意事项

1. 修改 hooks 或脚本时，确保跨平台兼容性
2. 所有脚本必须使用 Node.js shebang：`#!/usr/bin/env node`
3. 使用 `scripts/lib/utils.js` 中的工具函数而非直接调用系统命令
4. 测试新功能时使用 `node tests/run-all.js` 运行完整测试套件
5. Hooks 通过 stderr 输出到 Claude Code（使用 `log()` 函数）
6. 通过 stdout 返回数据给 Claude（使用 `output()` 函数）

## 长形式指南相关

该项目实现了长形式指南中描述的高级模式：
- **Token 优化**：模型选择、后台进程
- **内存持久化**：会话生命周期 hooks
- **持续学习**：从会话中自动提取模式
- **验证循环**：检查点评估
- **并行化**：Git worktrees 支持
