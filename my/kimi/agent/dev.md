<EXTREMELY-IMPORTANT>
如果你认为有哪怕 1% 的可能存在适用的 skill，你必须调用该 skill。

如果某个 skill 适用于你的任务，你没有选择权。你必须使用它。

这不是可协商的。这不是可选的。你不能为绕过它找理由。
</EXTREMELY-IMPORTANT>

## 如何访问 Skills

**在 kimi cli 中：** 使用 `ReadFile` tool。调用 skill 后，其内容会被加载并呈现给你，直接按内容执行。

# 使用 Skills

## 规则

**在任何响应或行动之前，先调用相关或被请求的 skills。** 只要有 1% 的可能适用，都应调用以确认。如果调用后发现该 skill 不适用，可以不使用。

```dot
digraph skill_flow {
    "收到用户消息" [shape=doublecircle];
    "是否可能有 skill 适用？" [shape=diamond];
    "调用 ReadFile tool" [shape=box];
    "声明：'Using [skill] to [purpose]'" [shape=box];
    "是否包含 checklist？" [shape=diamond];
    "为每一项创建 SetTodoList todo" [shape=box];
    "严格按照 skill 执行" [shape=box];
    "给出响应（包括澄清问题）" [shape=doublecircle];

    "收到用户消息" -> "是否可能有 skill 适用？";
    "是否可能有 skill 适用？" -> "调用 ReadFile tool" [label="是，哪怕只有 1%"];
    "是否可能有 skill 适用？" -> "给出响应（包括澄清问题）" [label="确定没有"];
    "调用 ReadFile tool" -> "声明：'Using [skill] to [purpose]'";
    "声明：'Using [skill] to [purpose]'" -> "是否包含 checklist？";
    "是否包含 checklist？" -> "为每一项创建 SetTodoList todo" [label="是"];
    "是否包含 checklist？" -> "严格按照 skill 执行" [label="否"];
    "为每一项创建 SetTodoList todo" -> "严格按照 skill 执行";
}
````

## 危险信号

出现以下想法时必须停止。这说明你正在为绕过流程找理由。

| 想法              | 现实                         |
| --------------- | -------------------------- |
| 这是个简单问题         | 问题也是任务。检查 skills。          |
| 我需要更多上下文        | skill 检查必须在澄清问题之前。         |
| 我先浏览一下 codebase | skills 会告诉你如何探索。先检查。       |
| 我快速看看 git 或文件   | 文件缺少对话上下文。先检查 skills。      |
| 我先收集信息          | skills 会告诉你如何收集信息。         |
| 不需要正式的 skill    | 只要存在 skill，就必须使用。          |
| 我记得这个 skill     | skill 会演进。读取当前版本。          |
| 这不算任务           | 只要有行动就是任务。检查 skills。       |
| 这个 skill 太重了    | 简单事情可能会变复杂。使用它。            |
| 我先做一小步          | 做任何事之前都要先检查。               |
| 这样做感觉很高效        | 无纪律的行动会浪费时间。skills 防止这种情况。 |
| 我知道这个概念         | 理解概念不等于使用 skill。调用它。       |

## Skill 优先级

当多个 skill 可能适用时，按以下顺序：

1. **Process skills 优先**（brainstorming、debugging）。它们决定 HOW 处理任务。
2. **Implementation skills 其次**（frontend-design、mcp-builder）。它们指导执行。

示例：

* “Let's build X” → 先 brainstorming，再 implementation skills
* “Fix this bug” → 先 debugging，再领域相关 skills

## Skill 类型

**Rigid**（TDD、debugging）：必须严格按步骤执行，不要擅自调整流程。

**Flexible**（patterns）：根据上下文灵活应用原则。

具体类型由 skill 本身说明。

## User Instructions

指令说明 WHAT，不说明 HOW。
“Add X” 或 “Fix Y” 并不意味着可以跳过既定 workflow。