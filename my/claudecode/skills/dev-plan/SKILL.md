---
name: dev-plan
description: 重述需求、评估风险、创建分步实施计划并持久化到 .plans。WAIT for user CONFIRM before touching any code.
---

# 开发规划 Skill

此 Skill 在编写任何代码之前创建可执行、可审查、可追踪的实施计划，并将计划持久化到 `.plans/`。

## 产出与约束

**产出：**
- 计划文件：`.plans/YYYY-MM-DD-<feature-name>.md`
- 回复中给出：需求重述、关键风险、执行选项与确认请求

**约束：**
- 未获得明确确认，不得编写任何代码
- 计划必须包含精确路径、命令、预期结果与测试策略

## 何时激活

在以下情况使用此 Skill：
- 开始新功能开发
- 进行重大架构变更
- 处理复杂重构
- 多个文件/组件会受到影响
- 需求不清晰或模棱两可

## Agent 协作协议（必须执行）

- `dev-planner` Agent：**必须调用**，生成计划初稿与任务拆分
- `dev-architect` Agent：当涉及架构决策/跨模块/性能/可靠性/安全时 **必须调用**，合并建议到计划
- `dev-tdd-guide-ts` / `dev-tdd-guide-py` Agent：依据技术栈 **必须调用其一**，补齐测试策略与用例覆盖
- `dev-code-reviewer-ts` / `dev-code-reviewer-py` Agent：计划执行后用于审查（在交接中明确）
- `dev-doc-updater` Agent：若计划涉及文档/目录结构变更则调用


## 工作流程（严格顺序）

1. **需求重述**：用清晰术语复述要构建的内容与成功标准
2. **澄清问题**：积极和用户澄清在计划过程中遇到的问题
3. **现状梳理**：识别受影响模块/依赖，必要时使用 auggie-mcp 检索
4. **架构与风险**：记录方案、权衡、依赖与潜在阻塞点
5. **任务拆分**：按 2-5 分钟的可执行步骤拆分
6. **测试策略**：补齐单元/集成/E2E 覆盖与命令
7. **复杂度评估**：High/Medium/Low + 关键不确定点
8. **计划持久化**：写入 `.plans/` 文件（见下文模板）
9. **输出交接**：给出执行选项并等待确认

## 积极提问原则

**规划过程中必须主动使用 `AskUserQuestion`：**
- 需求不清晰时 → 询问具体细节
- 有多种实现方案时 → 让用户选择
- 技术选型不确定时 → 确认用户偏好
- 优先级不明确时 → 询问 must-have 与 nice-to-have
- 边界条件模糊时 → 确认行为

**提问示例：**
- "数据持久化方案？(Redis / PostgreSQL / SQLite)"
- "是否需要支持批量操作？"
- "错误处理策略：静默失败 / 记录日志 / 抛出异常？"
- "实时性要求：WebSocket / Server-Sent Events / 轮询？"

## 计划文档规范

### 文件位置（必须）

- 保存到：`.plans/YYYY-MM-DD-<feature-name>.md`
- 若 `.plans/` 不存在，先创建目录
- `<feature-name>` 使用 kebab-case 且仅包含 ASCII

### Plan Header（必须包含）

```markdown
# [功能名称] 实施计划

> **For Claude:** REQUIRED SUB-SKILL: 使用 dev-tdd-workflow 按任务实施此计划。

**Goal:** [一句话描述要构建什么]

**Architecture:** [2-3 句话描述实现方法与关键权衡]

**Tech Stack:** [关键技术/库]

**Dependencies:** [外部服务/模块/数据]

**Risks:** [High/Medium/Low + 简述]

**Complexity:** [High/Medium/Low]

---
```

### 计划主体必须包含

- 需求重述
- 成功标准（可勾选）
- 任务清单（Task 1..N）
- 依赖关系
- 风险与缓解
- 测试策略（单元/集成/E2E + 命令）
- 预估复杂度与不确定点

### 任务结构

**每个任务一个动作（2-5 分钟）：**
- "编写失败的测试" - 一个步骤
- "运行测试确保它失败" - 一个步骤
- "编写最小实现让测试通过" - 一个步骤
- "运行测试确保通过" - 一个步骤
- "提交" - 一个步骤

### 任务详细格式

```markdown
### Task N: [组件名称]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: 编写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: 运行测试验证失败**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: 编写最小实现**

```python
def function(input):
    return expected
```

**Step 4: 运行测试验证通过**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: 提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```

## 重要说明

**关键**：在用户明确用 "yes" 或 "proceed" 或类似的肯定回答确认计划之前，**不会**编写任何代码。

如需修改，请回复：
- "modify: [你的修改内容]"
- "different approach: [替代方案]"
- "skip phase 2 and do phase 3 first"

## 与其他 Skills 配合

规划完成后：
- 使用 `dev-tdd-workflow` 进行测试驱动开发（统一 TDD 流程）
- 遇到构建错误时修复
- 完成后使用 `dev-review-ts` 或 `dev-review-py` Skill 审查代码

## Related Agents

- `dev-planner` Agent：输出可执行实施计划（必用）
- `dev-architect` Agent：架构审查与权衡
- `dev-tdd-guide-ts` / `dev-tdd-guide-py` Agent：测试策略与用例覆盖
- `dev-code-reviewer-ts` / `dev-code-reviewer-py` Agent：实现后代码审查

## 计划保存位置

计划保存到: `.plans/YYYY-MM-DD-<feature-name>.md`

## 记住原则

- 始终使用精确文件路径
- 计划中包含完整代码（不是"添加验证"这种模糊描述）
- 包含精确命令和预期输出
- 使用 @ 语法引用相关 skills
- DRY, YAGNI, TDD, 频繁提交
