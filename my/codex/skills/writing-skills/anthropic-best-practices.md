# 技能编写最佳实践

> 学习如何编写有效的技能，让 Claude 能够成功发现和使用。

好的技能简洁、结构良好，并经过真实使用测试。本指南提供实用的编写决策，帮助你编写 Claude 能够有效发现和使用的技能。

关于技能如何工作的概念背景，请参阅 [Skills 概述](/en/docs/agents-and-tools/agent-skills/overview)。

## 核心原则

### 简洁是关键

[上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows) 是公共资源。你的技能与 Claude 需要知道的所有其他内容共享上下文窗口，包括：

* 系统提示词
* 对话历史
* 其他技能的元数据
* 你的实际请求

并不是技能中的每个 token 都有即时成本。启动时，只预加载所有技能的元数据（名称和描述）。Claude 只在技能变得相关时才读取 SKILL.md，并仅在需要时读取额外文件。然而，在 SKILL.md 中保持简洁仍然很重要：一旦 Claude 加载了它，每个 token 都会与对话历史和其他上下文竞争。

**默认假设**：Claude 已经很聪明了

只添加 Claude 没有的上下文。挑战每一条信息：

* "Claude 真的需要这个解释吗？"
* "我可以假设 Claude 知道这一点吗？"
* "这段文字值得它的 token 成本吗？"

**好示例：简洁**（大约 50 个 token）：

```markdown
## 提取 PDF 文本

使用 pdfplumber 提取文本：

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**坏示例：太冗长**（大约 150 个 token）：

```markdown
## 提取 PDF 文本

PDF（Portable Document Format）文件是一种包含文本、图像和其他内容的常见文件格式。要从 PDF 提取文本，你需要使用一个库。有许多可用于 PDF 处理的库，但我们推荐 pdfplumber，因为它易于使用且能处理大多数情况。首先，你需要使用 pip 安装它。然后你可以使用下面的代码...
```

简洁版本假设 Claude 知道 PDF 是什么以及库如何工作。

### 设置适当的自由度

将特异性级别与任务的脆弱性和可变性相匹配。

**高自由度**（基于文本的指令）：

用于：

* 多种方法都有效
* 决策取决于上下文
* 启发式指导方法

示例：

```markdown
## 代码审查流程

1. 分析代码结构和组织
2. 检查潜在的 bug 或边缘情况
3. 建议改进可读性和可维护性
4. 验证对项目规范的遵循
```

**中等自由度**（带参数的伪代码或脚本）：

用于：

* 存在首选模式
* 一些变化是可接受的
* 配置影响行为

示例：

```markdown
## 生成报告

使用此模板并根据需要自定义：

```python
def generate_report(data, format="markdown", include_charts=True):
    # 处理数据
    # 以指定格式生成输出
    # 可选地包含可视化
```
```

**低自由度**（特定脚本，很少或没有参数）：

用于：

* 操作脆弱且容易出错
* 一致性至关重要
* 必须遵循特定序列

示例：

```markdown
## 数据库迁移

完全运行此脚本：

```bash
python scripts/migrate.py --verify --backup
```

不要修改命令或添加额外的标志。
```

**类比**：将 Claude 想象成探索路径的机器人：

* **两边悬崖的窄桥**：只有一条安全的前进道路。提供特定的护栏和精确指令（低自由度）。示例：必须按精确顺序运行的数据库迁移。
* **没有危险的开放田野**：许多路径通向成功。给出一般方向，相信 Claude 能找到最佳路线（高自由度）。示例：代码审查，其中上下文决定最佳方法。

### 用你计划使用的所有模型测试

技能作为模型的补充，因此效果取决于底层模型。用你计划使用的所有模型测试你的技能。

**按模型考虑的测试**：

* **Claude Haiku**（快速、经济）：技能是否提供足够的指导？
* **Claude Sonnet**（平衡）：技能是否清晰高效？
* **Claude Opus**（强大的推理）：技能是否避免过度解释？

对 Opus 完美的可能对 Haiku 需要更多细节。如果你计划在多个模型中使用技能，目标是适用于所有模型的指令。

## 技能结构

<Note>
  **YAML Frontmatter**：SKILL.md frontmatter 支持两个字段：

  * `name` - 技能的人类可读名称（最多 64 个字符）
  * `description` - 技能做什么以及何时使用的一行描述（最多 1024 个字符）

  有关完整的技能结构详细信息，请参阅 [Skills 概述](/en/docs/agents-and-tools/agent-skills/overview#skill-structure)。
</Note>

### 命名约定

使用一致的命名模式使技能更容易引用和讨论。我们推荐使用 **动名词形式**（动词 + -ing）作为技能名称，因为这清楚地描述了技能提供的活动或能力。

**好的命名示例（动名词形式）**：

* "Processing PDFs"
* "Analyzing spreadsheets"
* "Managing databases"
* "Testing code"
* "Writing documentation"

**可接受的替代方案**：

* 名词短语："PDF Processing"、"Spreadsheet Analysis"
* 面向行动："Process PDFs"、"Analyze Spreadsheets"

**避免**：

* 模糊名称："Helper"、"Utils"、"Tools"
* 过于通用："Documents"、"Data"、"Files"
* 技能集合中不一致的模式

一致的命名使以下工作更容易：

* 在文档和对话中引用技能
* 一目了然地理解技能做什么
* 组织和搜索多个技能
* 维护专业、有凝聚力的技能库

### 编写有效的描述

`description` 字段实现技能发现，应包括技能做什么以及何时使用它。

<Warning>
  **始终用第三人称编写**。描述被注入系统提示词，不一致的观点可能导致发现问题。

  * **好**："Processes Excel files and generates reports"
  * **避免**："I can help you process Excel files"
  * **避免**："You can use this to process Excel files"
</Warning>

**具体并包含关键词**。包括技能做什么以及何时使用它的具体触发器/上下文。

每个技能只有一个描述字段。描述对技能选择至关重要：Claude 用它从潜在的 100+ 可用技能中选择正确的技能。你的描述必须提供足够的细节让 Claude 知道何时选择此技能，而 SKILL.md 的其余部分提供实现细节。

有效示例：

**PDF 处理技能：**

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Excel 分析技能：**

```yaml
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

**Git 提交助手技能：**

```yaml
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

避免像这样的模糊描述：

```yaml
description: Helps with documents
```

```yaml
description: Processes data
```

```yaml
description: Does stuff with files
```

### 渐进式披露模式

SKILL.md 作为概述，根据需要指向 Claude 的详细材料，就像入职指南中的目录。有关渐进式披露如何工作的解释，请参阅概述中的 [How Skills work](/en/docs/agents-and-tools/agent-skills/overview#how-skills-work)。

**实用指导：**

* 保持 SKILL.md 主体在 500 行以内以获得最佳性能
* 接近此限制时将内容拆分为单独的文件
* 使用以下模式有效组织指令、代码和资源

#### 视觉概览：从简单到复杂

基本技能从只包含元数据和指令的 SKILL.md 文件开始：

当技能增长时，你可以捆绑 Claude 仅在需要时加载的额外内容：

完整的技能目录结构可能如下所示：

```
pdf/
├── SKILL.md              # 主要指令（触发时加载）
├── FORMS.md              # 表单填写指南（按需加载）
├── reference.md          # API 参考（按需加载）
├── examples.md           # 使用示例（按需加载）
└── scripts/
    ├── analyze_form.py   # 实用脚本（执行，非加载）
    ├── fill_form.py      # 表单填写脚本
    └── validate.py       # 验证脚本
```

#### 模式 1：带参考的高级指南

```markdown
---
name: PDF Processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## 快速开始

使用 pdfplumber 提取文本：
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## 高级功能

**表单填写**：请参阅 [FORMS.md](FORMS.md) 获取完整指南
**API 参考**：请参阅 [REFERENCE.md](REFERENCE.md) 获取所有方法
**示例**：请参阅 [EXAMPLES.md](EXAMPLES.md) 获取常见模式
```

Claude 仅在需要时加载 FORMS.md、REFERENCE.md 或 EXAMPLES.md。

#### 模式 2：按领域组织

对于具有多个领域的技能，按领域组织内容以避免加载不相关的上下文。当用户询问销售指标时，Claude 只需要读取与销售相关的模式，而不是财务或营销数据。这保持 token 使用率低且上下文集中。

```
bigquery-skill/
├── SKILL.md (概述和导航)
└── reference/
    ├── finance.md (收入、账单指标)
    ├── sales.md (机会、管道)
    ├── product.md (API 使用、功能)
    └── marketing.md (活动、归因)
```

```markdown
# BigQuery Data Analysis

## 可用数据集

**Finance**：收入、ARR、账单 → 请参阅 [reference/finance.md](reference/finance.md)
**Sales**：机会、管道、账户 → 请参阅 [reference/sales.md](reference/sales.md)
**Product**：API 使用、功能、采用 → 请参阅 [reference/product.md](reference/product.md)
**Marketing**：活动、归因、邮件 → 请参阅 [reference/marketing.md](reference/marketing.md)

## 快速搜索

使用 grep 查找特定指标：

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
```

#### 模式 3：条件详情

显示基本内容，链接到高级内容：

```markdown
# DOCX Processing

## 创建文档

使用 docx-js 创建新文档。请参阅 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

对于简单编辑，直接修改 XML。

**对于追踪更改**：请参阅 [REDLINING.md](REDLINING.md)
**对于 OOXML 详情**：请参阅 [OOXML.md](OOXML.md)
```

Claude 仅在用户需要这些功能时读取 REDLINING.md 或 OOXML.md。

### 避免深层嵌套引用

当从其他引用的文件中引用文件时，Claude 可能会部分读取文件。遇到嵌套引用时，Claude 可能会使用 `head -100` 等命令预览内容，而不是读取整个文件，导致信息不完整。

**保持引用从 SKILL.md 深度一级**。所有参考文件应直接从 SKILL.md 链接，以确保 Claude 在需要时读取完整文件。

**坏示例：太深**：

```markdown
# SKILL.md
请参阅 [advanced.md](advanced.md)...

# advanced.md
请参阅 [details.md](details.md)...

# details.md
这是实际信息...
```

**好示例：深度一级**：

```markdown
# SKILL.md

**基本用法**：[SKILL.md 中的指令]
**高级功能**：请参阅 [advanced.md](advanced.md)
**API 参考**：请参阅 [reference.md](reference.md)
**示例**：请参阅 [examples.md](examples.md)
```

### 为较长的参考文件构建带目录的结构

对于超过 100 行的参考文件，在顶部包含目录。这确保 Claude 即使在使用部分读取预览时也能看到可用信息的完整范围。

**示例**：

```markdown
# API 参考

## 目录
- 认证和设置
- 核心方法（创建、读取、更新、删除）
- 高级功能（批处理操作、webhooks）
- 错误处理模式
- 代码示例

## 认证和设置
...

## 核心方法
...
```

然后 Claude 可以根据需要读取完整文件或跳转到特定部分。

有关此基于文件的架构如何实现渐进式披露的详细信息，请参阅下面的 [Runtime environment](#runtime-environment) 部分。

## 工作流和反馈循环

### 对复杂任务使用工作流

将复杂操作分解为清晰、顺序的步骤。对于特别复杂的工作流，提供 Claude 可以复制到其响应中并在进行时勾选的清单。

**示例 1：研究综合工作流**（适用于没有代码的技能）：

```markdown
## 研究综合工作流

复制此清单并跟踪你的进度：

```
研究进度：
- [ ] 步骤 1：阅读所有源文档
- [ ] 步骤 2：识别关键主题
- [ ] 步骤 3：交叉验证声明
- [ ] 步骤 4：创建结构化摘要
- [ ] 步骤 5：验证引用
```

**步骤 1：阅读所有源文档**

审查 `sources/` 目录中的每个文档。注意主要论点和支持证据。

**步骤 2：识别关键主题**

寻找跨来源的模式。哪些主题反复出现？来源在何处同意或不同意？

**步骤 3：交叉验证声明**

对于每个主要声明，验证它是否出现在源材料中。注意哪个来源支持每个观点。

**步骤 4：创建结构化摘要**

按主题组织发现。包括：
- 主要声明
- 来自来源的支持证据
- 冲突观点（如果有）

**步骤 5：验证引用**

检查每个声明是否引用了正确的源文档。如果引用不完整，返回步骤 3。
```

此示例展示了工作流如何应用于不需要代码的分析任务。清单模式适用于任何复杂的多步骤过程。

**示例 2：PDF 表单填写工作流**（适用于带代码的技能）：

```markdown
## PDF 表单填写工作流

复制此清单并在完成项目时勾选：

```
任务进度：
- [ ] 步骤 1：分析表单（运行 analyze_form.py）
- [ ] 步骤 2：创建字段映射（编辑 fields.json）
- [ ] 步骤 3：验证映射（运行 validate_fields.py）
- [ ] 步骤 4：填写表单（运行 fill_form.py）
- [ ] 步骤 5：验证输出（运行 verify_output.py）
```

**步骤 1：分析表单**

运行：`python scripts/analyze_form.py input.pdf`

这会提取表单字段及其位置，保存到 `fields.json`。

**步骤 2：创建字段映射**

编辑 `fields.json` 为每个字段添加值。

**步骤 3：验证映射**

运行：`python scripts/validate_fields.py fields.json`

在继续之前修复任何验证错误。

**步骤 4：填写表单**

运行：`python scripts/fill_form.py input.pdf fields.json output.pdf`

**步骤 5：验证输出**

运行：`python scripts/verify_output.py output.pdf`

如果验证失败，返回步骤 2。
```

清晰的步骤防止 Claude 跳过关键验证。清单帮助 Claude 和你跟踪多步骤工作流的进度。

### 实现反馈循环

**常见模式**：运行验证器 → 修复错误 → 重复

这种模式大大提高输出质量。

**示例 1：风格指南合规**（适用于没有代码的技能）：

```markdown
## 内容审查流程

1. 按照 STYLE_GUIDE.md 中的指南起草内容
2. 对照清单审查：
   - 检查术语一致性
   - 验证示例遵循标准格式
   - 确认所有必需部分都存在
3. 如果发现问题：
   - 记录每个问题并附上具体部分参考
   - 修改内容
   - 再次审查清单
4. 仅当满足所有要求时才继续
5. 定稿并保存文档
```

这展示了使用参考文档而非脚本的验证循环模式。"验证器"是 STYLE_GUIDE.md，Claude 通过读取和比较来执行检查。

**示例 2：文档编辑流程**（适用于带代码的技能）：

```markdown
## 文档编辑流程

1. 对 `word/document.xml` 进行编辑
2. **立即验证**：`python ooxml/scripts/validate.py unpacked_dir/`
3. 如果验证失败：
   - 仔细查看错误消息
   - 修复 XML 中的问题
   - 再次运行验证
4. **仅在验证通过时才继续**
5. 重建：`python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. 测试输出文档
```

验证循环及早捕获错误。

## 内容指南

### 避免时间敏感信息

不要包含会过时的信息：

**坏示例：时间敏感**（会变错）：

```markdown
如果你在 2025 年 8 月之前做这个，使用旧 API。
2025 年 8 月之后，使用新 API。
```

**好示例**（使用 "旧模式" 部分）：

```markdown
## 当前方法

使用 v2 API 端点：`api.example.com/v2/messages`

## 旧模式

<details>
<summary>旧版 v1 API（2025-08 弃用）</summary>

v1 API 使用：`api.example.com/v1/messages`

此端点不再受支持。
</details>
```

旧模式部分提供历史上下文，而不杂乱主要内容。

### 使用一致的术语

选择一个术语并在整个技能中使用：

**好 - 一致**：

* 始终 "API endpoint"
* 始终 "field"
* 始终 "extract"

**坏 - 不一致**：

* 混合 "API endpoint"、"URL"、"API route"、"path"
* 混合 "field"、"box"、"element"、"control"
* 混合 "extract"、"pull"、"get"、"retrieve"

一致性帮助 Claude 理解和遵循指令。

## 常见模式

### 模板模式

为输出格式提供模板。将严格程度与你的需求相匹配。

**对于严格要求**（如 API 响应或数据格式）：

```markdown
## 报告结构

始终使用此确切的模板结构：

```markdown
# [分析标题]

## 执行摘要
[关键发现的一段概述]

## 关键发现
- 带有支持数据的发现 1
- 带有支持数据的发现 2
- 带有支持数据的发现 3

## 建议
1. 具体可执行的建议
2. 具体可执行的建议
```
```

**对于灵活指导**（当适应性有用时）：

```markdown
## 报告结构

这里是一个合理的默认格式，但根据分析使用你的最佳判断：

```markdown
# [分析标题]

## 执行摘要
[概述]

## 关键发现
[根据你发现的内容调整部分]

## 建议
[针对具体情境量身定制]
```

根据需要调整特定分析类型的部分。
```

### 示例模式

对于输出质量取决于看到示例的技能，提供输入/输出对，就像常规提示中一样：

```markdown
## 提交消息格式

按照这些示例生成提交消息：

**示例 1：**
输入：添加了使用 JWT 令牌的用户认证
输出：
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**示例 2：**
输入：修复了报告中日期显示不正确的 bug
输出：
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**示例 3：**
输入：更新了依赖项并重构了错误处理
输出：
```
chore: update dependencies and refactor error handling

- Upgrade lodash to 4.17.21
- Standardize error response format across endpoints
```

遵循此风格：type(scope): 简要描述，然后详细解释。
```

示例帮助 Claude 比单独描述更清楚地理解所需的风格和细节水平。

### 条件工作流模式

引导 Claude 通过决策点：

```markdown
## 文档修改工作流

1. 确定修改类型：

   **创建新内容？** → 遵循下面的 "创建工作流"
   **编辑现有内容？** → 遵循下面的 "编辑工作流"

2. 创建工作流：
   - 使用 docx-js 库
   - 从头开始构建文档
   - 导出为 .docx 格式

3. 编辑工作流：
   - 解压现有文档
   - 直接修改 XML
   - 每次更改后验证
   - 完成时重新打包
```

<Tip>
  如果工作流变得庞大或复杂，步骤很多，考虑将它们推入单独的文件，并告诉 Claude 根据手头的任务读取适当的文件。
</Tip>

## 评估和迭代

### 首先构建评估

**在编写大量文档之前创建评估。** 这确保你的技能解决实际问题，而不是记录想象的问题。

**评估驱动开发：**

1. **识别差距**：在没有技能的情况下在代表性任务上运行 Claude。记录具体失败或缺失的上下文
2. **创建评估**：构建三个测试这些差距的场景
3. **建立基线**：衡量 Claude 没有技能时的表现
4. **编写最小指令**：创建刚好足够的内容来解决差距并通过评估
5. **迭代**：执行评估，与基线比较，并完善

这种方法确保你解决实际问题，而不是可能永远不会实现的需求。

**评估结构**：

```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate PDF processing library or command-line tool",
    "Extracts text content from all pages in the document without missing any pages",
    "Saves the extracted text to a file named output.txt in a clear, readable format"
  ]
}
```

<Note>
  此示例演示了带有简单测试标准的数据驱动评估。我们目前不提供运行这些评估的内置方法。用户可以创建自己的评估系统。评估是衡量技能效果的事实来源。
</Note>

### 与 Claude 迭代开发技能

最有效的技能开发过程涉及 Claude 本身。与一个 Claude 实例（"Claude A"）合作创建一个将被其他实例（"Claude B"）使用的技能。Claude A 帮助你设计和完善指令，而 Claude B 在真实任务中测试它们。这有效是因为 Claude 模型理解如何编写有效的代理指令以及代理需要什么信息。

**创建新技能：**

1. **没有技能的情况下完成任务**：与 Claude A 使用正常提示完成问题。在你工作时，你会自然地提供上下文、解释偏好和分享程序知识。注意你反复提供的信息。

2. **识别可重用模式**：完成任务后，识别你提供的对类似未来任务有用的上下文。

   **示例**：如果你完成了 BigQuery 分析，你可能提供了表名、字段定义、过滤规则（如 "始终排除测试账户"）和常见查询模式。

3. **让 Claude A 创建技能**："创建一个技能，捕获我们刚才使用的 BigQuery 分析模式。包括表模式、命名约定和关于过滤测试账户的规则。"

   <Tip>
     Claude 模型原生理解技能格式和结构。你不需要特殊的系统提示或 "编写技能" 技能来让 Claude 帮助创建技能。只需让 Claude 创建一个技能，它就会生成具有适当 frontmatter 和主体内容的正确结构化 SKILL.md 内容。
   </Tip>

4. **审查简洁性**：检查 Claude A 是否添加了不必要的解释。问："删除关于胜率含义的解释——Claude 已经知道这一点。"

5. **改进信息架构**：让 Claude A 更有效地组织内容。例如："组织这个，使表模式在单独的参考文件中。我们稍后可能会添加更多表。"

6. **在类似任务上测试**：使用 Claude B（加载了技能的新实例）在相关用例上测试。观察 Claude B 是否找到正确的信息、正确应用规则并成功处理任务。

7. **根据观察迭代**：如果 Claude B 遇到困难或遗漏了什么，带着 specifics 返回 Claude A："当 Claude 使用此技能时，它忘记了按 Q4 日期过滤。我们应该添加关于日期过滤模式的部分吗？"

**迭代现有技能：**

改进技能时，相同的分层模式继续。你在以下之间交替：

* **与 Claude A 合作**（帮助完善技能的专家）
* **与 Claude B 测试**（使用技能执行实际工作的代理）
* **观察 Claude B 的行为** 并将见解带回 Claude A

1. **在真实工作流中使用技能**：给 Claude B（加载了技能的）实际任务，而非测试场景

2. **观察 Claude B 的行为**：注意它在何处挣扎、成功或做出意外选择

   **示例观察**："当我让 Claude B 提供区域销售报告时，它编写了查询但忘记过滤测试账户，即使技能提到了这条规则。"

3. **返回 Claude A 寻求改进**：分享当前的 SKILL.md 并描述你观察到的内容。问："我注意到 Claude B 在我要求区域报告时忘记过滤测试账户。技能提到了过滤，但也许它不够突出？"

4. **审查 Claude A 的建议**：Claude A 可能建议重新组织以使规则更突出，使用更强的语言如 "MUST filter" 而非 "always filter"，或重构工作流部分。

5. **应用和测试更改**：用 Claude A 的改进更新技能，然后在类似请求上再次与 Claude B 测试

6. **根据使用情况重复**：随着你遇到新场景，继续这个观察-完善-测试循环。每次迭代都基于真实代理行为而非假设来改进技能。

**收集团队反馈：**

1. 与队友分享技能并观察他们的使用
2. 问：技能是否按预期激活？指令是否清晰？缺少什么？
3. 合并反馈以解决你自己使用模式中的盲点

**为什么这种方法有效**：Claude A 理解代理需求，你提供领域专业知识，Claude B 通过真实使用揭示差距，迭代完善基于观察到的行为而非假设来改进技能。

### 观察 Claude 如何导航技能

迭代技能时，注意 Claude 在实践中实际如何使用它们。注意：

* **意外的探索路径**：Claude 是否以你未预料的顺序读取文件？这可能表明你的结构不如你想象的直观
* **遗漏的连接**：Claude 是否未能遵循对重要文件的引用？你的链接可能需要更明确或突出
* **过度依赖某些部分**：如果 Claude 反复读取同一文件，考虑该内容是否应放在主 SKILL.md 中
* **被忽略的内容**：如果 Claude 从未访问捆绑的文件，它可能是不必要的或在主指令中信号不良

基于这些观察而非假设进行迭代。技能的 'name' 和 'description' 特别关键。Claude 在决定是否响应当前任务触发技能时使用这些。确保它们清楚地描述技能做什么以及何时应该使用。

## 反模式避免

### 避免 Windows 风格路径

始终在文件路径中使用正斜杠，即使在 Windows 上：

* ✓ **好**：`scripts/helper.py`、`reference/guide.md`
* ✗ **避免**：`scripts\helper.py`、`reference\guide.md`

Unix 风格路径在所有平台上都有效，而 Windows 风格路径在 Unix 系统上会导致错误。

### 避免提供太多选项

除非必要，不要呈现多种方法：

```markdown
**坏示例：太多选择**（令人困惑）：
"你可以使用 pypdf，或 pdfplumber，或 PyMuPDF，或 pdf2image，或..."

**好示例：提供默认值**（带有逃生舱）：
"使用 pdfplumber 进行文本提取：
```python
import pdfplumber
```

对于需要 OCR 的扫描 PDF，改用 pdf2image 和 pytesseract。"
```

## 高级：带可执行代码的技能

以下部分专注于包含可执行脚本的技能。如果你的技能仅使用 markdown 指令，跳到 [有效技能清单](#checklist-for-effective-skills)。

### 解决，不回避

为技能编写脚本时，处理错误条件而不是回避给 Claude。

**好示例：显式处理错误**：

```python
def process_file(path):
    """处理文件，如果不存在则创建它。"""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # 创建带有默认内容的文件而不是失败
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        # 提供替代方案而不是失败
        print(f"Cannot access {path}, using default")
        return ''
```

**坏示例：回避给 Claude**：

```python
def process_file(path):
    # 只是失败，让 Claude 想办法
    return open(path).read()
```

配置参数也应该有正当理由并记录，以避免 "巫毒常量"（Ousterhout 定律）。如果你不知道正确的值，Claude 如何确定它？

**好示例：自文档化**：

```python
# HTTP 请求通常在 30 秒内完成
# 更长的超时考虑慢连接
REQUEST_TIMEOUT = 30

# 三次重试平衡可靠性 vs 速度
# 大多数间歇性故障在第二次重试时解决
MAX_RETRIES = 3
```

**坏示例：魔法数字**：

```python
TIMEOUT = 47  # 为什么是 47？
RETRIES = 5   # 为什么是 5？
```

### 提供实用脚本

即使 Claude 可以编写脚本，预制脚本也有优势：

**实用脚本的好处**：

* 比生成的代码更可靠
* 节省 token（无需将代码包含在上下文中）
* 节省时间（无需代码生成）
* 确保跨使用的一致性

上图展示了可执行脚本如何与指令文件一起工作。指令文件（forms.md）引用脚本，Claude 可以在不将内容加载到上下文的情况下执行它。

**重要区别**：在你的指令中明确 Claude 应该：

* **执行脚本**（最常见）："运行 `analyze_form.py` 提取字段"
* **将其作为参考阅读**（用于复杂逻辑）："查看 `analyze_form.py` 了解字段提取算法"

对于大多数实用脚本，执行更受青睐，因为它更可靠和高效。有关脚本执行如何工作的详细信息，请参阅下面的 [Runtime environment](#runtime-environment) 部分。

**示例**：

```markdown
## 实用脚本

**analyze_form.py**：从 PDF 提取所有表单字段

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

输出格式：
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**：检查重叠的边界框

```bash
python scripts/validate_boxes.py fields.json
# 返回："OK" 或列出冲突
```

**fill_form.py**：将字段值应用到 PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
```

### 使用视觉分析

当输入可以渲染为图像时，让 Claude 分析它们：

```markdown
## 表单布局分析

1. 将 PDF 转换为图像：
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. 分析每个页面图像以识别表单字段
3. Claude 可以直观地看到字段位置和类型
```

<Note>
  在此示例中，你需要编写 `pdf_to_images.py` 脚本。
</Note>

Claude 的视觉能力帮助理解布局和结构。

### 创建可验证的中间输出

当 Claude 执行复杂的开放式任务时，它可能会犯错。"计划-验证-执行" 模式通过让 Claude 首先在结构化格式中创建计划，然后用脚本验证该计划再执行它来及早捕获错误。

**示例**：想象让 Claude 根据电子表格更新 PDF 中的 50 个表单字段。没有验证的话，Claude 可能引用不存在的字段，创建冲突的值，遗漏必填字段，或错误地应用更新。

**解决方案**：使用上面显示的工作流模式（PDF 表单填写），但添加一个在应用更改之前验证的中间 `changes.json` 文件。工作流变为：分析 → **创建计划文件** → **验证计划** → 执行 → 验证。

**为什么这种模式有效：**

* **及早捕获错误**：验证在应用更改之前发现问题
* **机器可验证**：脚本提供客观验证
* **可逆的计划**：Claude 可以在不接触原件的情况下迭代计划
* **清晰的调试**：错误消息指向具体问题

**何时使用**：批处理操作、破坏性更改、复杂验证规则、高风险操作。

**实现提示**：使验证脚本具有详细的特定错误消息，如 "找不到字段 'signature_date'。可用字段：customer_name、order_total、signature_date_signed" 以帮助 Claude 修复问题。

### 打包依赖

技能在具有平台特定限制的代码执行环境中运行：

* **claude.ai**：可以从 npm 和 PyPI 安装包并从 GitHub 仓库拉取
* **Anthropic API**：没有网络访问和运行时包安装

在你的 SKILL.md 中列出所需的包，并在 [code execution tool documentation](/en/docs/agents-and-tools/tool-use/code-execution-tool) 中验证它们是否可用。

### 运行时环境

技能在具有文件系统访问、bash 命令和代码执行能力的代码执行环境中运行。有关此架构的概念解释，请参阅概述中的 [The Skills architecture](/en/docs/agents-and-tools/agent-skills/overview#the-skills-architecture)。

**这如何影响你的编写：**

**Claude 如何访问技能：**

1. **元数据预加载**：启动时，所有技能的 YAML frontmatter 中的名称和描述被加载到系统提示词中
2. **按需读取文件**：Claude 使用 bash Read 工具在需要时从文件系统访问 SKILL.md 和其他文件
3. **高效执行脚本**：实用脚本可以通过 bash 执行，而无需将完整内容加载到上下文中。只有脚本的输出消耗 token
4. **大文件无上下文惩罚**：参考文件、数据或文档在实际读取之前不消耗上下文 token

* **文件路径很重要**：Claude 像文件系统一样导航你的技能目录。使用正斜杠（`reference/guide.md`），而非反斜杠
* **文件命名描述性**：使用指示内容的名称：`form_validation_rules.md`，而非 `doc2.md`
* **为发现组织**：按领域或功能构建目录结构
  * 好：`reference/finance.md`、`reference/sales.md`
  * 坏：`docs/file1.md`、`docs/file2.md`
* **捆绑综合资源**：包含完整的 API 文档、广泛的示例、大型数据集；访问之前无上下文惩罚
* **对确定性操作优先使用脚本**：编写 `validate_form.py` 而非让 Claude 生成验证代码
* **明确执行意图**：
  * "运行 `analyze_form.py` 提取字段"（执行）
  * "查看 `analyze_form.py` 了解提取算法"（作为参考阅读）
* **测试文件访问模式**：通过真实请求验证 Claude 能否导航你的目录结构

**示例：**

```
bigquery-skill/
├── SKILL.md（概述，指向参考文件）
└── reference/
    ├── finance.md（收入指标）
    ├── sales.md（管道数据）
    └── product.md（使用分析）
```

当用户询问收入时，Claude 读取 SKILL.md，看到对 `reference/finance.md` 的引用，并调用 bash 仅读取该文件。sales.md 和 product.md 文件保留在文件系统上，在需要之前消耗零上下文 token。这种基于文件的模型实现了渐进式披露。Claude 可以导航并有选择地加载每个任务所需的确切内容。

有关技术架构的完整详细信息，请参阅 Skills 概述中的 [How Skills work](/en/docs/agents-and-tools/agent-skills/overview#how-skills-work)。

### MCP 工具引用

如果你的技能使用 MCP（Model Context Protocol）工具，始终使用完全限定工具名称以避免 "tool not found" 错误。

**格式**：`ServerName:tool_name`

**示例**：

```markdown
使用 BigQuery:bigquery_schema 工具检索表模式。
使用 GitHub:create_issue 工具创建问题。
```

其中：

* `BigQuery` 和 `GitHub` 是 MCP 服务器名称
* `bigquery_schema` 和 `create_issue` 是这些服务器内的工具名称

没有服务器前缀，Claude 可能无法定位工具，尤其是当多个 MCP 服务器可用时。

### 避免假设工具已安装

不要假设包可用：

```markdown
**坏示例：假设安装**：
"使用 pdf 库处理文件。"

**好示例：明确依赖**：
"安装所需包：`pip install pypdf`

然后使用它：
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
```

## 技术说明

### YAML frontmatter 要求

SKILL.md frontmatter 仅包括 `name`（最多 64 个字符）和 `description`（最多 1024 个字符）字段。有关完整的结构详细信息，请参阅 [Skills overview](/en/docs/agents-and-tools/agent-skills/overview#skill-structure)。

### Token 预算

保持 SKILL.md 主体在 500 行以内以获得最佳性能。如果你的内容超出此范围，使用前面描述的渐进式披露模式将其拆分为单独的文件。有关架构详细信息，请参阅 [Skills overview](/en/docs/agents-and-tools/agent-skills/overview#how-skills-work) 中的 "How Skills work"。

## 有效技能清单

分享技能之前，验证：

### 核心质量

* [ ] 描述具体并包含关键词
* [ ] 描述包括技能做什么以及何时使用它
* [ ] SKILL.md 主体在 500 行以内
* [ ] 额外细节在单独文件中（如果需要）
* [ ] 无时间敏感信息（或在 "旧模式" 部分）
* [ ] 整个术语一致
* [ ] 示例具体，非抽象
* [ ] 文件引用深度一级
* [ ] 适当使用渐进式披露
* [ ] 工作流有清晰步骤

### 代码和脚本

* [ ] 脚本解决问题而非回避给 Claude
* [ ] 错误处理显式且有帮助
* [ ] 无 "巫毒常量"（所有值都有理由）
* [ ] 所需包在指令中列出并验证为可用
* [ ] 脚本有清晰文档
* [ ] 无 Windows 风格路径（所有正斜杠）
* [ ] 关键操作的验证/验证步骤
* [ ] 质量关键任务的反馈循环

### 测试

* [ ] 至少创建了三个评估
* [ ] 用 Haiku、Sonnet 和 Opus 测试
* [ ] 用真实使用场景测试
* [ ] 合并团队反馈（如适用）

## 下一步

<CardGroup cols={2}>
  <Card title="Get started with Agent Skills" icon="rocket" href="/en/docs/agents-and-tools/agent-skills/quickstart">
    Create your first Skill
  </Card>

  <Card title="Use Skills in Claude Code" icon="terminal" href="/en/docs/claude-code/skills">
    Create and manage Skills in Claude Code
  </Card>

  <Card title="Use Skills with the API" icon="code" href="/en/api/skills-guide">
    Upload and use Skills programmatically
  </Card>
</CardGroup>
