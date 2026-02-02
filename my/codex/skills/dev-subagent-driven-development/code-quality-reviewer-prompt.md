# 代码质量审查者 Prompt 模板

分派代码质量审查者子代理时使用此模板。

**目的：** 验证实现构建良好（干净、测试良好、可维护）

**仅在规范合规性审查通过后分派。**

```
Task tool (superpowers:code-reviewer):
  使用位于 requesting-code-review/code-reviewer.md 的模板

  WHAT_WAS_IMPLEMENTED: [来自实现者的报告]
  PLAN_OR_REQUIREMENTS: 来自 [plan-file] 的任务 N
  BASE_SHA: [任务前的提交]
  HEAD_SHA: [当前提交]
  DESCRIPTION: [任务摘要]
```

**代码审查者返回：** 优点、问题（严重/重要/轻微）、评估
