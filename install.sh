#!/bin/bash
set -e

# 将 my/ 目录下的配置安装到 Claude Code、OpenCode、Codex 和 Kimi
# Claude Code: 覆盖 ~/.claude/{agents,rules,skills}
# OpenCode:    覆盖 ~/.config/opencode/{agents,commands,skills}
# Codex:       覆盖 ~/.codex/{skills,rules}
# Kimi:        覆盖 ~/.config/agents/skills/ 或 ~/.kimi/skills/

CLAUDE_DIR="$HOME/.claude"
OPENCODE_DIR="$HOME/.config/opencode"
CODEX_DIR="$HOME/.codex"

# Kimi 支持多个可能的 skills 目录，按优先级选择
if [ -d "$HOME/.config/agents/skills" ]; then
  KIMI_SKILLS_DIR="$HOME/.config/agents/skills"
elif [ -d "$HOME/.agents/skills" ]; then
  KIMI_SKILLS_DIR="$HOME/.agents/skills"
elif [ -d "$HOME/.kimi/skills" ]; then
  KIMI_SKILLS_DIR="$HOME/.kimi/skills"
else
  # 默认使用推荐的目录
  KIMI_SKILLS_DIR="$HOME/.config/agents/skills"
fi

# 确保目录存在
mkdir -p "$CLAUDE_DIR"/{agents,rules,commands,skills,scripts/hooks,scripts/lib}
mkdir -p "$OPENCODE_DIR"/{agents,commands,skills}
mkdir -p "$CODEX_DIR"/{skills,rules}
mkdir -p "$KIMI_SKILLS_DIR"

echo "=== 安装配置文件 ==="
echo ""

# === Claude Code 安装 ===
echo ">>> 安装 Claude Code 专属配置"

# 清空 Claude Code 目录
rm -rf "$CLAUDE_DIR/agents/"/* 2>/dev/null || true
rm -rf "$CLAUDE_DIR/rules/"/* 2>/dev/null || true
rm -rf "$CLAUDE_DIR/skills/"/* 2>/dev/null || true
rm -rf "$CLAUDE_DIR/commands/"/* 2>/dev/null || true

# 复制 Claude Code 专属配置
if [ -d "my/claudecode/agents" ]; then
  cp my/claudecode/agents/*.md "$CLAUDE_DIR/agents/" 2>/dev/null || true
  echo "  ✓ agents"
fi

if [ -d "my/claudecode/rules" ]; then
  cp my/claudecode/rules/*.md "$CLAUDE_DIR/rules/" 2>/dev/null || true
  echo "  ✓ rules"
fi

if [ -d "my/claudecode/skills" ]; then
  cp -r my/claudecode/skills/* "$CLAUDE_DIR/skills/" 2>/dev/null || true
  echo "  ✓ skills"
fi

# 安装 scripts (hooks 依赖)
if [ -d "my/claudecode/scripts" ]; then
  rm -rf "$CLAUDE_DIR/scripts/"/* 2>/dev/null || true
  cp -r my/claudecode/scripts/* "$CLAUDE_DIR/scripts/" 2>/dev/null || true
  echo "  ✓ scripts"
fi

# 合并 hooks.json 到 settings.json
if [ -f "my/claudecode/hooks/hooks.json" ]; then
  SETTINGS_FILE="$CLAUDE_DIR/settings.json"

  # 如果 settings.json 不存在，创建空文件
  if [ ! -f "$SETTINGS_FILE" ]; then
    echo "{}" > "$SETTINGS_FILE"
  fi

  # 使用 node 合并 JSON（保留现有的其他配置）
  node -e "
    const fs = require('fs');
    const settings = JSON.parse(fs.readFileSync('$SETTINGS_FILE', 'utf8'));
    const hooks = JSON.parse(fs.readFileSync('my/claudecode/hooks/hooks.json', 'utf8'));

    // 合并 hooks
    settings.hooks = { ...settings.hooks, ...hooks.hooks };

    // 写回
    fs.writeFileSync('$SETTINGS_FILE', JSON.stringify(settings, null, 2) + '\n');
  " 2>/dev/null && echo "  ✓ hooks" || echo "  - hooks (合并失败，请手动安装)"
fi

echo ""
echo ">>> 安装 OpenCode 专属配置"

# 清空 OpenCode 目录
rm -rf "$OPENCODE_DIR/agents/"/* 2>/dev/null || true
rm -rf "$OPENCODE_DIR/skills/"/* 2>/dev/null || true

# 复制 OpenCode 专属配置（如果目录为空则跳过）
if [ -d "my/opencode/agents" ] && [ "$(ls -A my/opencode/agents/ 2>/dev/null)" ]; then
  cp my/opencode/agents/*.md "$OPENCODE_DIR/agents/" 2>/dev/null || true
  echo "  ✓ agents"
else
  echo "  - agents (无配置)"
fi

if [ -d "my/opencode/skills" ] && [ "$(ls -A my/opencode/skills/ 2>/dev/null)" ]; then
  cp -r my/opencode/skills/* "$OPENCODE_DIR/skills/" 2>/dev/null || true
  echo "  ✓ skills"
else
  echo "  - skills (无配置)"
fi

# 复制 commands
rm -rf "$OPENCODE_DIR/commands/"/* 2>/dev/null || true
if [ -d "my/opencode/commands" ]; then
  cp my/opencode/commands/*.md "$OPENCODE_DIR/commands/" 2>/dev/null || true
  echo "  ✓ commands"
fi


echo ""
echo ">>> 安装 Codex 专属配置"

# 清空 Codex 目录
rm -rf "$CODEX_DIR/skills/"/* 2>/dev/null || true
rm -rf "$CODEX_DIR/rules/"/* 2>/dev/null || true

# 复制 Codex 专属配置（如果目录为空则跳过）
if [ -d "my/codex/skills" ] && [ "$(ls -A my/codex/skills/ 2>/dev/null)" ]; then
  cp -r my/codex/skills/* "$CODEX_DIR/skills/" 2>/dev/null || true
  echo "  ✓ skills"
else
  echo "  - skills (无配置)"
fi

if [ -d "my/codex/rules" ] && [ "$(ls -A my/codex/rules/ 2>/dev/null)" ]; then
  cp my/codex/rules/*.rules "$CODEX_DIR/rules/" 2>/dev/null || true
  echo "  ✓ rules"
else
  echo "  - rules (无配置)"
fi

# 复制 AGENTS.md（如果存在）
if [ -f "my/codex/AGENTS.md" ]; then
  cp my/codex/AGENTS.md "$CODEX_DIR/AGENTS.md" 2>/dev/null || true
  echo "  ✓ AGENTS.md"
fi

echo ""
echo ">>> 安装 Kimi 专属配置"

# 设置 Kimi agent 目录
KIMI_AGENT_DIR="$HOME/.kimi/agents"
mkdir -p "$KIMI_AGENT_DIR"

# 复制 Kimi skills（如果目录为空则跳过）
if [ -d "my/kimi/skills" ] && [ "$(ls -A my/kimi/skills/ 2>/dev/null)" ]; then
  cp -r my/kimi/skills/* "$KIMI_SKILLS_DIR/" 2>/dev/null || true
  echo "  ✓ skills -> $KIMI_SKILLS_DIR"
else
  echo "  - skills (无配置)"
fi

# 复制 Kimi agent 配置
if [ -d "my/kimi/agents" ]; then
  cp -r my/kimi/agents/* "$KIMI_AGENT_DIR/" 2>/dev/null || true
  echo "  ✓ agent config -> $KIMI_AGENT_DIR"
  echo ""
  echo "  提示: 使用以下命令启动带自动 skill 注入的 Kimi:"
  echo "    kimi --agent-file $KIMI_AGENT_DIR/dev.yaml"
  echo ""
  echo "  或设置别名:"
  echo "    alias kimi='kimi --agent-file $KIMI_AGENT_DIR/dev.yaml'"
else
  echo "  - agent config (无配置)"
fi

echo ""
echo "=== 安装完成 ==="
echo ""

echo "Claude Code (~/.claude/):"
echo "  agents:"
ls -la "$CLAUDE_DIR/agents/" 2>/dev/null | grep -E "\.md$" | awk '{print "    " $NF}' || echo "    (无)"
echo "  rules:"
ls -la "$CLAUDE_DIR/rules/" 2>/dev/null | grep -E "\.md$" | awk '{print "    " $NF}' || echo "    (无)"
echo "  commands:"
ls -la "$CLAUDE_DIR/commands/" 2>/dev/null | grep -E "\.md$" | awk '{print "    " $NF}' || echo "    (无)"
echo "  skills:"
ls "$CLAUDE_DIR/skills/" 2>/dev/null | grep -v "^\.$" | grep -v "^\.\.$" | awk '{print "    " $NF}' || echo "    (无)"
echo "  scripts/hooks:"
ls "$CLAUDE_DIR/scripts/hooks/" 2>/dev/null | grep "\.js$" | awk '{print "    " $NF}' || echo "    (无)"
echo ""

echo "OpenCode (~/.config/opencode/):"
echo "  agents:"
ls -la "$OPENCODE_DIR/agents/" 2>/dev/null | grep -E "\.md$" | awk '{print "    " $NF}' || echo "    (无)"
echo "  commands:"
ls -la "$OPENCODE_DIR/commands/" 2>/dev/null | grep -E "\.md$" | awk '{print "    " $NF}' || echo "    (无)"
echo "  skills:"
ls "$OPENCODE_DIR/skills/" 2>/dev/null | grep -v "^\.$" | grep -v "^\.\.$" | awk '{print "    " $NF}' || echo "    (无)"
echo ""

echo "Codex (~/.codex/):"
echo "  skills:"
ls "$CODEX_DIR/skills/" 2>/dev/null | grep -v "^\.$" | grep -v "^\.\.$" | awk '{print "    " $NF}' || echo "    (无)"
echo "  rules:"
ls -la "$CODEX_DIR/rules/" 2>/dev/null | grep -E "\.rules$" | awk '{print "    " $NF}' || echo "    (无)"
echo "  AGENTS.md:"
if [ -f "$CODEX_DIR/AGENTS.md" ]; then
  echo "    ✓ 已配置"
else
  echo "    (无)"
fi

echo ""
echo "Kimi ($KIMI_SKILLS_DIR):"
echo "  skills:"
ls "$KIMI_SKILLS_DIR/" 2>/dev/null | grep -v "^\.$" | grep -v "^\.\.$" | awk '{print "    " $NF}' || echo "    (无)"
echo "  agent config:"
ls "$KIMI_AGENT_DIR/" 2>/dev/null | grep -E "\.(yaml|md)$" | awk '{print "    " $NF}' || echo "    (无)"

