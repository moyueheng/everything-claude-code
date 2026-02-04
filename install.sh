#!/bin/bash
set -e

# 将 my/ 目录下的配置安装到 Claude Code、OpenCode 和 Codex
# 将 my/ 目录下的配置安装到 Claude Code、OpenCode 和 Codex
# Claude Code: 覆盖 ~/.claude/{agents,rules,skills}
# OpenCode:    覆盖 ~/.config/opencode/{agents,commands,skills}
# Codex:       覆盖 ~/.codex/{skills,rules}

CLAUDE_DIR="$HOME/.claude"
OPENCODE_DIR="$HOME/.config/opencode"
CODEX_DIR="$HOME/.codex"

# 确保目录存在
mkdir -p "$CLAUDE_DIR"/{agents,rules,commands,skills}
mkdir -p "$OPENCODE_DIR"/{agents,commands,skills}
mkdir -p "$CODEX_DIR"/{skills,rules}

echo "=== 安装配置文件 ==="
echo ""

# === Claude Code 安装 ===
echo ">>> 安装 Claude Code 专属配置"

# 确保 hooks 目录存在
mkdir -p "$CLAUDE_DIR/hooks"

# 安装 hook 脚本（如果存在）
if [ -d "my/claudecode/hooks" ] && [ -f "my/claudecode/hooks/on-exit-plan-mode.py" ]; then
  cp my/claudecode/hooks/on-exit-plan-mode.py "$CLAUDE_DIR/hooks/"
  chmod +x "$CLAUDE_DIR/hooks/on-exit-plan-mode.py"
  echo "  ✓ hooks/on-exit-plan-mode.py"
fi

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
echo "  hooks:"
ls "$CLAUDE_DIR/hooks/" 2>/dev/null | grep -v "^\.$" | grep -v "^\.\.$" | grep "\.py$" | awk '{print "    " $NF}' || echo "    (无)"
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
echo "=== Hooks 配置 ==="
echo ""
echo "已安装的 Hooks:"
echo "  - on-exit-plan-mode.py  (ExitPlanMode → TDD 自动触发)"
echo ""
echo "注意: Hooks 需要手动配置到 ~/.claude/settings.json 中:"
echo ""
echo "  1. 复制以下配置到 settings.json 的 hooks 对象中:"
echo ""
cat my/claudecode/hooks/hooks.json | grep -v "^_comment" | grep -v "^_instructions"
echo ""
echo "  2. 或者使用 jq 合并配置:"
echo "     jq -s '.[0] * .[1]' ~/.claude/settings.json my/claudecode/hooks/hooks.json > /tmp/settings.json && mv /tmp/settings.json ~/.claude/settings.json"
echo ""
