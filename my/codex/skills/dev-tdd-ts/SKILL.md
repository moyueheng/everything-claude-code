---
name: dev-tdd-ts
description: 实现任何功能或错误修复时，在编写实现代码之前使用
metadata:
  short-description: 测试驱动开发（TDD）核心原则和流程
---

# 测试驱动开发 (TDD)

## 概述

先写测试。观察它失败。编写最小代码使其通过。

**核心原则：** 如果你没有观察到测试失败，你就不知道它是否测试了正确的东西。

**违反规则的字面就是违反规则的精神。**

## 何时使用

**始终：**
- 新功能
- 错误修复
- 重构
- 行为变更

**例外（询问你的伙伴）：**
- 一次性原型
- 生成的代码
- 配置文件

认为"这次就跳过 TDD"？停下来。那是合理化。

## 铁律

```
没有失败的测试就不要写生产代码
```

测试前写代码？删除它。重新开始。

**无例外：**
- 不要将其保留为"参考"
- 不要在写测试时"适应"它
- 不要看它
- 删除意味着删除

完全根据测试重新实现。句号。

## 红-绿-重构

```dot
digraph tdd_cycle {
    rankdir=LR;
    red [label="RED\n编写失败测试", shape=box, style=filled, fillcolor="#ffcccc"];
    verify_red [label="验证正确\n失败", shape=diamond];
    green [label="GREEN\n最小代码", shape=box, style=filled, fillcolor="#ccffcc"];
    verify_green [label="验证通过\n全部绿色", shape=diamond];
    refactor [label="REFACTOR\n清理", shape=box, style=filled, fillcolor="#ccccff"];
    next [label="下一个", shape=ellipse];

    red -> verify_red;
    verify_red -> green [label="是"];
    verify_red -> red [label="错误\n失败"];
    green -> verify_green;
    verify_green -> refactor [label="是"];
    verify_green -> green [label="否"];
    refactor -> verify_green [label="保持\n绿色"];
    verify_green -> next;
    next -> red;
}
```

### RED - 编写失败测试

编写一个最小测试展示应该发生什么。

<好>
```typescript
test('重试失败操作 3 次', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
清晰的名称，测试真实行为，一件事
</好>

<坏>
```typescript
test('重试有效', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
模糊的名称，测试 mock 而非代码
</坏>

**要求：**
- 一个行为
- 清晰的名称
- 真实代码（除非不可避免，否则不要用 mock）

### 验证 RED - 观察失败

**强制性。绝不跳过。**

```bash
npm test path/to/test.test.ts
```

确认：
- 测试失败（不是错误）
- 失败消息是预期的
- 因功能缺失而失败（不是拼写错误）

**测试通过了？** 你在测试现有行为。修复测试。

**测试出错？** 修复错误，重新运行直到正确失败。

### GREEN - 最小代码

编写最简单的代码通过测试。

<好>
```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```
刚好通过
</好>

<坏>
```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> {
  // YAGNI
}
```
过度工程
</坏>

不要添加功能、重构其他代码或超出测试范围的"改进"。

### 验证 GREEN - 观察通过

**强制性。**

```bash
npm test path/to/test.test.ts
```

确认：
- 测试通过
- 其他测试仍然通过
- 输出干净（无错误、警告）

**测试失败？** 修复代码，不是测试。

**其他测试失败？** 立即修复。

### REFACTOR - 清理

仅在通过之后：
- 移除重复
- 改进名称
- 提取辅助函数

保持测试绿色。不要添加行为。

### 重复

下一个功能的下一个失败测试。

## 好的测试

| 质量 | 好 | 坏 |
|------|-----|-----|
| **最小** | 一件事。名称中有"and"？拆分它。 | `test('验证邮箱和域名和空格')` |
| **清晰** | 名称描述行为 | `test('test1')` |
| **展示意图** | 演示期望的 API | 模糊代码应该做什么 |

## 为什么顺序很重要

**"我稍后会写测试来验证它有效"**

之后编写的测试立即通过。立即通过证明不了什么：
- 可能测试错误的东西
- 可能测试实现而非行为
- 可能遗漏你忘记的边缘情况
- 你从未看到它捕获 bug

测试优先迫使你看到测试失败，证明它确实测试了某些东西。

**"我已经手动测试了所有边缘情况"**

手动测试是临时的。你认为你测试了一切但：
- 没有测试记录
- 代码更改时无法重新运行
- 压力下容易忘记情况
- "我试的时候有效" ≠ 全面

自动化测试是系统的。它们每次都以相同方式运行。

**"删除 X 小时的工作是浪费"**

沉没成本谬误。时间已经过去了。你现在的选择：
- 删除并用 TDD 重写（X 更多小时，高信心）
- 保留并稍后添加测试（30 分钟，低信心，可能有 bug）

"浪费"是保留你无法信任的代码。没有真实测试的可工作代码是技术债务。

**"TDD 是教条的，务实意味着适应"**

TDD 就是务实的：
- 在提交前发现 bug（比之后调试更快）
- 防止回归（测试立即捕获破坏）
- 记录行为（测试展示如何使用代码）
- 启用重构（自由更改，测试捕获破坏）

"务实"的捷径 = 生产环境调试 = 更慢。

**"测试后达到相同目标 - 这是精神而非仪式"**

不。测试后回答"这是做什么？"测试优先回答"这应该做什么？"

测试后受你的实现偏见。你测试你构建的，而非必需的。你验证记住的边缘情况，而非发现的。

测试优先在实现前强制发现边缘情况。测试后验证你是否记住了一切（你没有）。

30 分钟的测试后 ≠ TDD。你得到覆盖率，失去测试有效的证明。

## 常见合理化借口

| 借口 | 现实 |
|------|------|
| "太简单无法测试" | 简单代码会坏。测试需要 30 秒。 |
| "我稍后会测试" | 立即通过的测试证明不了什么。 |
| "测试后达到相同目标" | 测试后 = "这是做什么？" 测试优先 = "这应该做什么？" |
| "已经手动测试过了" | 临时 ≠ 系统。无记录，无法重新运行。 |
| "删除 X 小时是浪费" | 沉没成本谬误。保留未验证代码是技术债务。 |
| "保留作为参考，先写测试" | 你会适应它。那就是测试后。删除意味着删除。 |
| "需要先探索" | 可以。扔掉探索，用 TDD 开始。 |
| "测试难 = 设计不清晰" | 听测试的。难测试 = 难使用。 |
| "TDD 会拖慢我" | TDD 比调试快。务实 = 测试优先。 |
| "手动测试更快" | 手动不能证明边缘情况。每次更改你都会重新测试。 |
| "现有代码没有测试" | 你在改进它。为现有代码添加测试。 |

## 红旗 - 停止并重新开始

- 测试前写代码
- 实现后写测试
- 测试立即通过
- 无法解释为什么测试失败
- "稍后"添加测试
- 合理化"就这一次"
- "我已经手动测试过了"
- "测试后达到相同目的"
- "这是关于精神而非仪式"
- "保留作为参考"或"适应现有代码"
- "已经花了 X 小时，删除是浪费"
- "TDD 是教条的，我是务实的"
- "这不同，因为..."

**所有这些都意味着：删除代码。用 TDD 重新开始。**

## 示例：错误修复

**错误：** 接受空邮箱

**RED**
```typescript
test('拒绝空邮箱', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('需要邮箱');
});
```

**验证 RED**
```bash
$ npm test
FAIL: expected '需要邮箱', got undefined
```

**GREEN**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: '需要邮箱' };
  }
  // ...
}
```

**验证 GREEN**
```bash
$ npm test
PASS
```

**REFACTOR**
如果需要，提取验证用于多个字段。

## 验证清单

标记工作完成之前：

- [ ] 每个新函数/方法都有测试
- [ ] 在实现之前观察每个测试失败
- [ ] 每个测试因预期原因失败（功能缺失，不是拼写错误）
- [ ] 为通过每个测试编写了最小代码
- [ ] 所有测试通过
- [ ] 输出干净（无错误、警告）
- [ ] 测试使用真实代码（仅当不可避免时使用 mock）
- [ ] 覆盖边缘情况和错误

无法勾选所有框？你跳过了 TDD。重新开始。

## 卡住时

| 问题 | 解决方案 |
|------|----------|
| 不知道如何测试 | 编写期望的 API。先写断言。问你的伙伴。 |
| 测试太复杂 | 设计太复杂。简化接口。 |
| 必须 mock 一切 | 代码太耦合。使用依赖注入。 |
| 测试设置庞大 | 提取辅助函数。仍然复杂？简化设计。 |

## 调试集成

发现 bug？编写重现它的失败测试。遵循 TDD 循环。测试证明修复并防止回归。

永远不要没有测试就修复 bug。

## 测试反模式

添加 mock 或测试工具时，阅读 testing-anti-patterns.md 以避免常见陷阱：
- 测试 mock 行为而非真实行为
- 向生产类添加仅测试方法
- 不理解依赖就 mock

## 最终规则

```
生产代码 → 测试存在且先失败
否则 → 不是 TDD
```

没有你的伙伴的许可，无例外。
