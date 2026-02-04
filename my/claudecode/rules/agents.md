# Agent 编排

## 可用 Agents

位于 `~/.claude/agents/`:

| Agent | 用途 | 使用时机 |
|-------|---------|-------------|
| dev-planner | 实施规划 | 复杂功能、重构 |
| dev-architect | 系统设计 | 架构决策 |
| dev-tdd-guide-ts | 测试驱动开发 | 新功能、bug 修复 |
| dev-tdd-guide-py | 测试驱动开发 | 新功能、bug 修复 |
| dev-code-reviewer-ts | 代码审查 | 编写代码后 |
| dev-code-reviewer-py | 代码审查 | 编写代码后 |
| dev-refactor-cleaner-ts | 死代码清理 | 代码维护 |
| dev-refactor-cleaner-python | 死代码清理 | 代码维护 |
| dev-doc-updater | 文档 | 更新文档 |

## 立即使用 Agent

无需用户提示:
1. 复杂功能请求 - 使用 **dev-planner** Agent
2. 代码刚编写/修改 - 使用 **dev-code-reviewer-ts** 或 **dev-code-reviewer-py** Agent
3. Bug 修复或新功能 - 使用 **dev-tdd-guide-ts** 或 **dev-tdd-guide-py** Agent
4. 架构决策 - 使用 **dev-architect** Agent

## 并行任务执行

对独立操作 ALWAYS 使用并行 Task 执行:

```markdown
# GOOD: 并行执行
并行启动 3 个 Agent:
1. Agent 1: auth.ts 的安全性分析
2. Agent 2: 缓存系统的性能审查
3. Agent 3: utils.ts 的类型检查

# BAD: 不必要的顺序执行
先 Agent 1，然后 Agent 2，然后 Agent 3
```

## 多角度分析

对于复杂问题，使用分角色子 Agent:
- 事实审查者
- 高级工程师
- 安全专家
- 一致性审查者
- 冗余检查者
