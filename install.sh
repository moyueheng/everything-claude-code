#!/bin/bash
set -e

CLAUDE_DIR="$HOME/.claude"

# 确保目录存在
mkdir -p "$CLAUDE_DIR"/{agents,rules,commands,skills}

echo "=== 安装 my/ 下的配置到 Claude Code ==="

# 复制所有配置
cp my/agents/*.md "$CLAUDE_DIR/agents/" 2>/dev/null || true
cp my/rules/*.md "$CLAUDE_DIR/rules/" 2>/dev/null || true
cp my/commands/*.md "$CLAUDE_DIR/commands/" 2>/dev/null || true
cp -r my/skills/* "$CLAUDE_DIR/skills/" 2>/dev/null || true

echo "✓ 安装完成"
echo ""
echo "已安装的配置:"
ls -la "$CLAUDE_DIR/agents/" 2>/dev/null || echo "  (无 agents)"
ls -la "$CLAUDE_DIR/rules/" 2>/dev/null || echo "  (无 rules)"
