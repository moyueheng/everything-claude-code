# Fork 迁移到 Subtree 方案（简化版）

## 目标结构

```
your-repo/
├── .git/
├── upstream/                          # subtree 管理的上游代码（只读参考）
│   └── everything-claude-code/
│       ├── agents/
│       ├── rules/
│       ├── commands/
│       └── skills/
│
├── my/                                # 你的改造内容（从这里挑选文件安装）
│   ├── agents/
│   ├── rules/
│   ├── commands/
│   └── skills/
│
├── install.sh                         # 安装脚本
└── README.md
```

## 迁移步骤

### 步骤 1：备份并清理

```bash
# 检查状态
git status

# 保存当前修改到新分支
git checkout -b backup-before-migration
git add .
git commit -m "backup: 迁移前备份"

# 回到主分支
git checkout main
git checkout -b migrate-to-subtree

# 删除原项目文件（保留 .git 和你的 README）
rm -rf agents/ rules/ commands/ skills/ hooks/ scripts/ tests/
rm -rf contexts/ mcp-configs/ examples/ .claude-plugin/
rm -f marketplace.json CONTRIBUTING.md CLAUDE.md

# 提交清理
git add -A
git commit -m "chore: 清理原项目文件，准备迁移到 subtree"
```

### 步骤 2：添加 upstream 作为 subtree

```bash
git subtree add --prefix=upstream/everything-claude-code \
  https://github.com/affaan-m/everything-claude-code.git main --squash
```

### 步骤 3：创建你的目录

```bash
mkdir -p my/{agents,rules,commands,skills}
git add my/
git commit -m "chore: 创建个人配置目录"
```

### 步骤 4：挑选文件改造

```bash
# 从 upstream 复制你想用的文件到 my/
cp upstream/everything-claude-code/agents/planner.md my/agents/planner-zh.md
cp upstream/everything-claude-code/rules/security.md my/rules/security-zh.md

# 编辑改造（翻译成中文、调整内容）
vim my/agents/planner-zh.md
```

### 步骤 5：创建安装脚本

创建 `install.sh`：

```bash
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
```

```bash
chmod +x install.sh
git add install.sh
git commit -m "feat: 添加安装脚本"
```

### 步骤 6：合并到主分支

```bash
git checkout main
git merge migrate-to-subtree --no-ff -m "feat: 迁移到 subtree 架构"
git push origin main
```

## 日常使用

### 同步上游更新

```bash
git subtree pull --prefix=upstream/everything-claude-code \
  https://github.com/affaan-m/everything-claude-code.git main --squash

# 查看有什么新文件
git diff HEAD~1 --name-only
```

### 添加新配置

```bash
# 从 upstream 挑选新文件
cp upstream/everything-claude-code/agents/new-agent.md my/agents/new-agent-zh.md
vim my/agents/new-agent-zh.md

git add my/
git commit -m "feat: 添加 new-agent 中文版本"
```

### 安装到 Claude

```bash
./install.sh
```

## 原则

- `upstream/`：**只读**，只用 `subtree pull` 更新，从不修改
- `my/`：**你的改造区**，从 upstream 复制文件过来改造，或直接创建新文件
