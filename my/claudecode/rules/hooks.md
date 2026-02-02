# Hooks 系统

## Hook 类型

- **PreToolUse**: 工具执行前 (验证、参数修改)
- **PostToolUse**: 工具执行后 (自动格式化、检查)
- **Stop**: 会话结束时 (最终验证)

## 当前 Hooks (位于 ~/.claude/settings.json)

### PreToolUse
- **tmux reminder**: 提示对长时间运行的命令使用 tmux (npm, pnpm, yarn, cargo 等)
- **git push review**: Push 前打开 Zed 进行审查
- **doc blocker**: 阻止创建不必要的 .md/.txt 文件

### PostToolUse
- **PR creation**: 记录 PR URL 和 GitHub Actions 状态
- **Prettier**: 编辑后自动格式化 JS/TS 文件
- **TypeScript check**: 编辑 .ts/.tsx 文件后运行 tsc
- **console.log warning**: 警告编辑文件中的 console.log

### Stop
- **console.log audit**: 会话结束前检查所有修改文件的 console.log

## 自动接受权限

谨慎使用:
- 对可信的、定义明确的计划启用
- 对探索性工作禁用
- 永不使用 dangerously-skip-permissions flag
- 改为在 `~/.claude.json` 中配置 `allowedTools`

## TodoWrite 最佳实践

使用 TodoWrite 工具来:
- 跟踪多步骤任务的进度
- 验证对指令的理解
- 实现实时引导
- 显示细粒度的实施步骤

Todo 列表可揭示:
- 步骤顺序问题
- 遗漏项目
- 多余的不必要项目
- 错误的粒度
- 误解的需求
