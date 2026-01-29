# 目录结构重构执行步骤

## 第一步：创建新目录结构

```bash
# 创建 Claude Code 专属目录
mkdir -p my/claudecode/{agents,rules,skills}

# 创建 OpenCode 专属目录
mkdir -p my/opencode/{agents,skills}

# 确保 commands 目录存在（应该已存在）
mkdir -p my/commands
```

## 第二步：迁移配置文件

### 迁移 agents 到 Claude Code
```bash
mv my/agents/*.md my/claudecode/agents/
```

### 迁移 skills 到 Claude Code
```bash
mv my/skills/* my/claudecode/skills/
```

### 迁移 rules 到 Claude Code（虽为空）
```bash
mv my/rules/* my/claudecode/rules/ 2>/dev/null || true
```

## 第三步：删除旧目录

```bash
# 删除已迁移的空目录
rmdir my/agents my/skills my/rules
```

## 第四步：替换 install.sh

```bash
# 备份旧脚本
mv install.sh install.sh.old

# 使用新脚本
mv install.sh.new install.sh
chmod +x install.sh
```

## 第五步：测试安装

```bash
# 执行安装
./install.sh

# 验证安装结果
ls -la ~/.claude/agents/
ls -la ~/.claude/commands/
ls -la ~/.config/opencode/commands/
```

## 可选步骤：更新 README.md

更新 `my/README.md` 反映新的目录结构。

## 如果需要将某个 agent 移到 OpenCode

示例：将 `planner.md` 复制到 OpenCode
```bash
cp my/claudecode/agents/planner.md my/opencode/agents/
```

然后重新运行 `./install.sh`
