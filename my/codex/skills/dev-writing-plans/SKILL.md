---
name: dev-writing-plans
description: 当拥有多步骤任务的规格或需求时使用，在接触代码之前制定实施计划
---

# 编写实施计划

## 概述

编写全面的实施计划，假设工程师对我们的代码库一无所知且品味存疑。记录他们需要知道的一切：每个任务需要修改哪些文件、代码、测试、可能需要查看的文档、如何测试。将整个计划分解为小块任务。DRY、YAGNI、TDD、频繁提交。

假设他们是熟练的开发者，但几乎不了解我们的工具集或问题域。假设他们不太擅长测试设计。

**开始时宣布：**"我正在使用 writing-plans skill 来创建实施计划。"

**上下文：** 这应该在由 brainstorming skill 创建的独立 worktree 中运行。

**保存计划到：** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 小块任务粒度

**每个步骤是一个动作（2-5 分钟）：**
- "编写失败的测试" - 一步
- "运行测试确保它失败" - 一步
- "编写最小实现使测试通过" - 一步
- "运行测试确保它们通过" - 一步
- "提交" - 一步

## 计划文档头部

**每个计划必须以这个头部开始：**

```markdown
# [功能名称] 实施计划

> **给 Claude：** 必需子技能：使用 superpowers:executing-plans 来逐个任务实施此计划。

**目标：** [一句话描述要构建什么]

**架构：** [2-3 句话描述方法]

**技术栈：** [关键技术/库]

---
```

## 任务结构

```markdown
### 任务 N：[组件名称]

**文件：**
- 创建：`exact/path/to/file.py`
- 修改：`exact/path/to/existing.py:123-145`
- 测试：`tests/exact/path/to/test.py`

**步骤 1：编写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**步骤 2：运行测试验证它失败**

运行：`pytest tests/path/test.py::test_name -v`
预期：FAIL with "function not defined"

**步骤 3：编写最小实现**

```python
def function(input):
    return expected
```

**步骤 4：运行测试验证它通过**

运行：`pytest tests/path/test.py::test_name -v`
预期：PASS

**步骤 5：提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## 记住

- 始终使用精确的文件路径
- 计划中包含完整代码（不是"添加验证"）
- 精确命令和预期输出
- 使用 @ 语法引用相关技能
- DRY、YAGNI、TDD、频繁提交

## 执行交接

保存计划后，提供执行选择：

**"计划已完成并保存到 `docs/plans/<filename>.md`。两种执行选项：**

**1. 子代理驱动（本会话）** - 我为每个任务分派新的子代理，任务之间进行审核，快速迭代

**2. 并行会话（独立）** - 在新会话中打开 executing-plans，批量执行带检查点

**选择哪种方式？"**

**如果选择子代理驱动：**
- **必需子技能：** 使用 superpowers:subagent-driven-development
- 保持在本会话
- 每个任务使用新的子代理 + 代码审核

**如果选择并行会话：**
- 指导他们在 worktree 中打开新会话
- **必需子技能：** 新会话使用 superpowers:executing-plans
