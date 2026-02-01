---
name: writing-plans
description: 在有多步骤任务的需求或规格时，在接触代码之前使用
metadata:
  short-description: 编写详细的实现规划文档
---

# 编写规划 (Writing Plans)

## 概述

编写全面的实现规划，假设工程师对我们的代码库一无所知。记录他们每个任务需要知道的一切：需要修改哪些文件、代码如何编写、需要查阅哪些测试和文档、如何测试。将完整规划分解为小粒度任务。遵循 DRY、YAGNI、TDD、频繁提交。

假设他们是熟练的开发者，但几乎不了解我们的工具集或问题域。假设他们对良好的测试设计不太熟悉。

**开始时声明：** "我将使用 writing-plans skill 来创建实现规划。"

**上下文：** 这应该在独立的工作目录中运行（由 brainstorming skill 创建）。

**保存规划到：** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 小粒度任务拆分

**每个步骤是一个动作（2-5分钟）：**
- "编写失败的测试" - 一步
- "运行测试确保它失败" - 一步
- "编写最小代码使测试通过" - 一步
- "运行测试确保通过" - 一步
- "提交" - 一步

## 规划文档头部

**每个规划必须以这个头部开始：**

```markdown
# [功能名称] 实现规划

> **给 Claude：** 必需子技能：使用 executing-plans 来逐个任务实现此规划。

**目标：** [一句话描述这个功能构建什么]

**架构：** [2-3句话描述方法]

**技术栈：** [关键技术/库]

---
```

## 任务结构

```markdown
### 任务 N: [组件名称]

**文件：**
- 创建: `exact/path/to/file.py`
- 修改: `exact/path/to/existing.py:123-145`
- 测试: `tests/exact/path/to/test.py`

**步骤 1: 编写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**步骤 2: 运行测试验证失败**

运行: `pytest tests/path/test.py::test_name -v`
预期: FAIL with "function not defined"

**步骤 3: 编写最小实现**

```python
def function(input):
    return expected
```

**步骤 4: 运行测试验证通过**

运行: `pytest tests/path/test.py::test_name -v`
预期: PASS

**步骤 5: 提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## 记住

- 总是使用精确的文件路径
- 规划中包含完整的代码（不是 "添加验证" 这种模糊描述）
- 提供精确的命令和预期输出
- 使用 @ 语法引用相关技能
- 遵循 DRY、YAGNI、TDD、频繁提交

## 执行交接

保存规划后，提供执行选择：

**"规划已完成并保存到 `docs/plans/<filename>.md`。两种执行选项：**

**1. 子代理驱动（当前会话）** - 我为每个任务分派新的子代理，任务之间进行审查，快速迭代

**2. 并行会话（独立会话）** - 在新的工作目录中打开新会话使用 executing-plans 批量执行并检查点

**选择哪种方式？"**

**如果选择子代理驱动：**
- **必需子技能：** 使用 subagent-driven-development
- 保持当前会话
- 每个任务使用新的子代理 + 代码审查

**如果选择并行会话：**
- 引导他们到工作目录中打开新会话
- **必需子技能：** 新会话使用 executing-plans
