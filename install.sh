#!/bin/bash
set -e

CLAUDE_DIR="$HOME/.claude"
OPENCODE_DIR="$HOME/.config/opencode"

# 确保目录存在
mkdir -p "$CLAUDE_DIR"/{agents,rules,commands,skills}
mkdir -p "$OPENCODE_DIR"/{agents,commands,skills}

echo "=== 安装 my/ 下的配置 ==="

# 清空并重新复制所有配置到 Claude Code（目录级别覆盖）
rm -rf "$CLAUDE_DIR/agents/"/* 2>/dev/null || true
rm -rf "$CLAUDE_DIR/rules/"/* 2>/dev/null || true
rm -rf "$CLAUDE_DIR/commands/"/* 2>/dev/null || true
rm -rf "$CLAUDE_DIR/skills/"/* 2>/dev/null || true

cp my/agents/*.md "$CLAUDE_DIR/agents/" 2>/dev/null || true
cp my/rules/*.md "$CLAUDE_DIR/rules/" 2>/dev/null || true
cp my/commands/*.md "$CLAUDE_DIR/commands/" 2>/dev/null || true
cp -r my/skills/* "$CLAUDE_DIR/skills/" 2>/dev/null || true

# 清空并重新复制所有配置到 OpenCode（目录级别覆盖）
rm -rf "$OPENCODE_DIR/agents/"/* 2>/dev/null || true
rm -rf "$OPENCODE_DIR/commands/"/* 2>/dev/null || true
rm -rf "$OPENCODE_DIR/skills/"/* 2>/dev/null || true

cp my/agents/*.md "$OPENCODE_DIR/agents/" 2>/dev/null || true
cp my/commands/*.md "$OPENCODE_DIR/commands/" 2>/dev/null || true
cp -r my/skills/* "$OPENCODE_DIR/skills/" 2>/dev/null || true

echo "✓ 安装完成"
echo ""
echo "已安装到 Claude Code (~/.claude/):"
ls -la "$CLAUDE_DIR/agents/" 2>/dev/null || echo "  (无 agents)"
ls -la "$CLAUDE_DIR/rules/" 2>/dev/null || echo "  (无 rules)"
ls -la "$CLAUDE_DIR/commands/" 2>/dev/null || echo "  (无 commands)"
ls -la "$CLAUDE_DIR/skills/" 2>/dev/null || echo "  (无 skills)"
echo ""
echo "已安装到 OpenCode (~/.config/opencode/):"
ls -la "$OPENCODE_DIR/agents/" 2>/dev/null || echo "  (无 agents)"
ls -la "$OPENCODE_DIR/commands/" 2>/dev/null || echo "  (无 commands)"
ls -la "$OPENCODE_DIR/skills/" 2>/dev/null || echo "  (无 skills)"
