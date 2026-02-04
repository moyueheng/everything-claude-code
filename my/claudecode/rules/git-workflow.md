# Git 工作流

## Commit Message 格式

```
<type>: <description>

<optional body>
```

Types: feat, fix, refactor, docs, test, chore, perf, ci

Note: Attribution 已通过 ~/.claude/settings.json 全局禁用。

## Pull Request 工作流

创建 PR 时：
1. 分析完整 commit 历史 (不仅仅是最新 commit)
2. 使用 `git diff [base-branch]...HEAD` 查看所有变更
3. 起草全面的 PR 摘要
4. 包含测试计划和 TODOs
5. 如果是新分支，使用 `-u` flag push

## 功能实现工作流

1. **先规划**
   - 使用 **dev-planner** Agent 创建实施计划
   - 识别依赖和风险
   - 分阶段进行

2. **TDD 方法**
   - 使用 **dev-tdd-guide-ts** 或 **dev-tdd-guide-py** Agent
   - 先写测试 (RED)
   - 实现以通过测试 (GREEN)
   - 重构 (IMPROVE)
   - 验证 80%+ 覆盖率

3. **代码审查**
   - 编写代码后立即使用 **dev-code-reviewer-ts** 或 **dev-code-reviewer-py** Agent
   - 处理 CRITICAL 和 HIGH 级别问题
   - 尽可能修复 MEDIUM 级别问题

4. **Commit & Push**
   - 详细的 commit message
   - 遵循 conventional commits 格式
