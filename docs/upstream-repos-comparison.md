# 上游仓库对比：everything-claude-code vs superpowers

> 本文档对比两个上游仓库的核心差异，便于理解各自的定位和适用场景。

## 一、基本信息

| 属性 | everything-claude-code | superpowers |
|------|----------------------|-------------|
| **作者** | Affaan Mustafa (Anthropic hackathon 获胜者) | Jesse Jesse (fsck.com) |
| **版本** | v1.2.0 | v4.2.0 |
| **定位** | 全面的配置集合 | 完整软件开发工作流系统 |
| **核心特点** | 工具库模式，灵活组合 | 强制工作流，自动触发 |

## 二、核心理念对比

### everything-claude-code
- **理念**: "给你一个丰富的工具箱，自己选择合适的工具"
- **策略**: 灵活组合、按需使用
- **触发方式**: 手动调用或根据场景主动建议

### superpowers
- **理念**: "给你一套严格的工作流，必须按流程执行"
- **策略**: 强制性最佳实践，无选择余地
- **触发方式**: 自动强制触发

### 核心差异总结
```
ECC: 用户请求 → 手动调用工具 → 灵活执行
Superpowers: 用户请求 → 自动触发工作流 → 强制执行
```

## 三、内容规模对比

| 组件 | everything-claude-code | superpowers |
|------|----------------------|-------------|
| **Agents** | 14 个 | 1 个 |
| **Skills** | 31 个 | 15 个 |
| **Commands** | 30+ 个 | 3 个 |
| **Hooks** | 20+ 个 | 1 个 |
| **Rules** | 8+ 个 | 融入 skills |

## 四、特色功能对比

### everything-claude-code 独有功能

| 功能 | 说明 | 优先级 |
|------|------|--------|
| **Continuous Learning v2** | Instinct-based 学习系统，自动提取模式 | ⭐⭐⭐ |
| **Skill Creator** | 从 Git 历史生成 skills | ⭐⭐ |
| **框架覆盖** | Django、Spring Boot、Go、React 等 | ⭐⭐ |
| **跨平台支持** | Node.js 脚本，Windows/macOS/Linux | ⭐ |
| **专业 Agents** | 规划、架构、审查、安全等 14 个 | ⭐⭐⭐ |

### superpowers 独有功能

| 功能 | 说明 | 优先级 |
|------|------|--------|
| **Systematic Debugging** | 四阶段系统化调试流程 | ⭐⭐⭐ |
| **Subagent-Driven Development** | 每任务新 subagent，两阶段审查 | ⭐⭐⭐ |
| **强制性 TDD** | "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST" | ⭐⭐⭐ |
| **Brainstorming 工作流** | 强制触发创意构思 | ⭐⭐ |
| **Git Worktrees 集成** | 自动创建隔离工作空间 | ⭐ |

## 五、工作流对比

### everything-claude-code 工作流
```
用户请求功能
    ↓
手动调用 /plan 或 planner agent
    ↓
创建实施计划
    ↓
手动选择执行方式
    ↓
使用 /tdd, /code-review 等命令
    ↓
可选：从 Git 历史生成技能
```

### superpowers 工作流
```
用户请求功能
    ↓
⚠️ 自动触发 brainstorming skill
    ↓
⚠️ 自动触发 writing-plans skill
    ↓
⚠️ 自动触发 subagent-driven-development
    ↓
⚠️ 强制使用 test-driven-development
    ↓
⚠️ 自动触发 requesting-code-review
    ↓
⚠️ 自动触发 finishing-a-development-branch
```

> ⚠️ 注意：superpowers 的工作流是**强制性和自动化**的，skills 会在特定场景自动触发。

## 六、Skills 触发方式对比

| 特性 | everything-claude-code | superpowers |
|------|----------------------|-------------|
| **触发方式** | 命令调用或 agent 使用 | 强制自动触发 |
| **强制性** | 建议，可选择性使用 | "MUST USE"，无选择余地 |
| **粒度** | 细粒度模式（框架/语言特定） | 粗粒度工作流 |
| **内容风格** | 参考文档和最佳实践 | 严格流程和检查清单 |

## 七、Agents 对比

### everything-claude-code 的 Agents
- `planner.md` - 复杂功能和重构规划
- `architect.md` - 系统架构设计
- `code-reviewer.md` - 代码质量审查
- `security-reviewer.md` - 安全漏洞分析
- `build-error-resolver.md` - 构建错误修复
- `tdd-guide.md` - TDD 流程指导
- `python-reviewer.md` - Python 专项审查
- `go-reviewer.md` - Go 专项审查
- ... (共 14 个)

### superpowers 的 Agents
- `code-reviewer.md` - 面向规划的代码审查（唯一 agent）

**差异**: ECC 提供多个专项 agents，superpowers 将所有流程融入 skills 中。

## 八、Hooks 系统对比

| 特性 | everything-claude-code | superpowers |
|------|----------------------|-------------|
| **实现方式** | Node.js 脚本 | Shell 脚本 |
| **事件类型** | PreToolUse, PostToolUse, Stop, SessionStart, SessionEnd, PreCompact | 仅 SessionStart |
| **功能** | 代码检查、格式化、会话持久化、模式提取 | 仅会话启动 |
| **复杂度** | 高（20+ hooks） | 低（1 个 hook） |

## 九、适用场景对比

### 选择 everything-claude-code 的场景

✅ 需要快速启动、灵活配置
✅ 使用多种框架和语言（TS/Python/Go）
✅ 需要自动化模式提取和持续学习
✅ 希望从 Git 历史生成团队技能
✅ 需要跨平台兼容性（Windows/macOS/Linux）
✅ 希望根据需求选择性使用工具
✅ 需要丰富的参考库和模式

### 选择 superpowers 的场景

✅ 重视严格工程纪律和流程的团队
✅ 需要强制性 TDD 实践
✅ 复杂项目需要系统化调试
✅ 希望自动化工作流减少人为错误
✅ 愿意遵循严格流程换取高质量
✅ 需要多 subagent 协作开发
✅ 重视证据导向的开发方式

## 十、集成建议

针对本项目的配置策略：

### 优先从 superpowers 整合（核心工作流）

| Skill | 说明 | 优先级 |
|-------|------|--------|
| `systematic-debugging/` | 系统化调试流程 | ⭐⭐⭐ |
| `test-driven-development/` | 严格 TDD 执行 | ⭐⭐⭐ |
| `subagent-driven-development/` | Subagent 驱动开发 | ⭐⭐⭐ |
| `writing-plans/` | 编写实施计划 | ⭐⭐ |
| `brainstorming/` | 创意构思工作流 | ⭐⭐ |

### 优先从 everything-claude-code 整合（工具库）

| 组件 | 说明 | 优先级 |
|------|------|--------|
| `continuous-learning-v2/` | Instinct-based 学习系统 | ⭐⭐⭐ |
| `agents/` (planner, architect, reviewers) | 专业 agents | ⭐⭐⭐ |
| `commands/` (skill-create, instinct-*) | 工具命令 | ⭐⭐ |
| `rules/` | 编码风格、安全、测试规则 | ⭐⭐ |
| `hooks/` | 完整 hooks 系统 | ⭐⭐ |
| `backend-patterns/`, `frontend-patterns/` | 框架特定模式 | ⭐ |

## 十一、总结

| 维度 | everything-claude-code | superpowers |
|------|----------------------|-------------|
| **形象比喻** | 瑞士军刀 | 军队操典 |
| **核心价值** | 丰富、灵活、可选 | 严格、系统、强制 |
| **最佳用途** | 快速启动，按需选择 | 质量保障，流程规范 |
| **配合建议** | 提供工具库和模式参考 | 提供核心工作流框架 |

---

## 参考链接

- everything-claude-code: `upstream/everything-claude-code/`
- superpowers: `upstream/superpowers/`
- 更新日志: `docs/upstream-updates.md`
