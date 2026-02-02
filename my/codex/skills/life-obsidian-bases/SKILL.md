---
name: life-obsidian-bases
description: 创建和编辑 Obsidian Bases (.base 文件)，包含 views、filters、formulas 和 summaries。当处理 .base 文件、创建类似数据库的笔记视图，或用户提到 Obsidian 中的 Bases、table views、card views、filters 或 formulas 时使用。
---

# Obsidian Bases Skill

此 skill 使 agents 能够创建和编辑有效的 Obsidian Bases（`.base` 文件），包括 views、filters、formulas 和所有相关配置。

## 概述

Obsidian Bases 是基于 YAML 的文件，用于在 Obsidian vault 中定义笔记的动态视图。Base 文件可以包含多个 views、全局 filters、formulas、property 配置和自定义 summaries。

## 文件格式

Base 文件使用 `.base` 扩展名，包含有效的 YAML。它们也可以嵌入 Markdown 代码块中。

## 完整 Schema

```yaml
# 全局 filters 应用于 base 中的所有 views
filters:
  # 可以是单个 filter 字符串
  # 或带有 and/or/not 的递归 filter 对象
  and: []
  or: []
  not: []

# 定义可在所有 views 中使用的 formula properties
formulas:
  formula_name: 'expression'

# 配置 properties 的显示名称和设置
properties:
  property_name:
    displayName: "Display Name"
  formula.formula_name:
    displayName: "Formula Display Name"
  file.ext:
    displayName: "Extension"

# 定义自定义 summary formulas
summaries:
  custom_summary_name: 'values.mean().round(3)'

# 定义一个或多个 views
views:
  - type: table | cards | list | map
    name: "View Name"
    limit: 10                    # 可选: 限制结果数量
    groupBy:                     # 可选: 分组结果
      property: property_name
      direction: ASC | DESC
    filters:                     # View 特定的 filters
      and: []
    order:                       # 按顺序显示的 properties
      - file.name
      - property_name
      - formula.formula_name
    summaries:                   # 将 properties 映射到 summary formulas
      property_name: Average
```

## Filter 语法

Filters 用于缩小结果范围。它们可以全局应用或按 view 应用。

### Filter 结构

```yaml
# 单个 filter
filters: 'status == "done"'

# AND - 所有条件必须为真
filters:
  and:
    - 'status == "done"'
    - 'priority > 3'

# OR - 任一条件可为真
filters:
  or:
    - 'file.hasTag("book")'
    - 'file.hasTag("article")'

# NOT - 排除匹配项
filters:
  not:
    - 'file.hasTag("archived")'

# 嵌套 filters
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
    - not:
        - file.hasTag("book")
        - file.inFolder("Required Reading")
```

### Filter 运算符

| 运算符 | 描述 |
|----------|-------------|
| `==` | 等于 |
| `!=` | 不等于 |
| `>` | 大于 |
| `<` | 小于 |
| `>=` | 大于或等于 |
| `<=` | 小于或等于 |
| `&&` | 逻辑与 |
| `\|\|` | 逻辑或 |
| <code>!</code> | 逻辑非 |

## Properties

### 三种 Property 类型

1. **Note properties** - 来自 frontmatter: `note.author` 或仅 `author`
2. **File properties** - 文件元数据: `file.name`, `file.mtime` 等
3. **Formula properties** - 计算值: `formula.my_formula`

### File Properties 参考

| Property | 类型 | 描述 |
|----------|------|-------------|
| `file.name` | String | 文件名 |
| `file.basename` | String | 不带扩展名的文件名 |
| `file.path` | String | 文件的完整路径 |
| `file.folder` | String | 父文件夹路径 |
| `file.ext` | String | 文件扩展名 |
| `file.size` | Number | 文件大小（字节） |
| `file.ctime` | Date | 创建时间 |
| `file.mtime` | Date | 修改时间 |
| `file.tags` | List | 文件中的所有 tags |
| `file.links` | List | 文件中的内部 links |
| `file.backlinks` | List | 链接到此文件的文件 |
| `file.embeds` | List | 笔记中的 embeds |
| `file.properties` | Object | 所有 frontmatter properties |

### `this` 关键字

- 在主内容区域：指 base 文件本身
- 嵌入时：指嵌入的文件
- 在侧边栏：指主内容中的活动文件

## Formula 语法

Formulas 从 properties 计算值。在 `formulas` 部分定义。

```yaml
formulas:
  # 简单算术
  total: "price * quantity"

  # 条件逻辑
  status_icon: 'if(done, "✅", "⏳")'

  # 字符串格式化
  formatted_price: 'if(price, price.toFixed(2) + " dollars")'

  # 日期格式化
  created: 'file.ctime.format("YYYY-MM-DD")'

  # 计算自创建以来的天数（对 Duration 使用 .days）
  days_old: '(now() - file.ctime).days'

  # 计算距截止日期的天数
  days_until_due: 'if(due_date, (date(due_date) - today()).days, "")'
```

## Functions 参考

### 全局 Functions

| Function | 签名 | 描述 |
|----------|-----------|-------------|
| `date()` | `date(string): date` | 将字符串解析为日期。格式: `YYYY-MM-DD HH:mm:ss` |
| `duration()` | `duration(string): duration` | 解析 duration 字符串 |
| `now()` | `now(): date` | 当前日期和时间 |
| `today()` | `today(): date` | 当前日期（时间 = 00:00:00） |
| `if()` | `if(condition, trueResult, falseResult?)` | 条件判断 |
| `min()` | `min(n1, n2, ...): number` | 最小数字 |
| `max()` | `max(n1, n2, ...): number` | 最大数字 |
| `number()` | `number(any): number` | 转换为数字 |
| `link()` | `link(path, display?): Link` | 创建 link |
| `list()` | `list(element): List` | 如果还不是则包装为 list |
| `file()` | `file(path): file` | 获取 file 对象 |
| `image()` | `image(path): image` | 创建用于渲染的 image |
| `icon()` | `icon(name): icon` | 按名称的 Lucide icon |
| `html()` | `html(string): html` | 渲染为 HTML |
| `escapeHTML()` | `escapeHTML(string): string` | 转义 HTML 字符 |

### Any 类型 Functions

| Function | 签名 | 描述 |
|----------|-----------|-------------|
| `isTruthy()` | `any.isTruthy(): boolean` | 强制转换为 boolean |
| `isType()` | `any.isType(type): boolean` | 检查类型 |
| `toString()` | `any.toString(): string` | 转换为 string |

### Date Functions & Fields

**Fields:** `date.year`, `date.month`, `date.day`, `date.hour`, `date.minute`, `date.second`, `date.millisecond`

| Function | 签名 | 描述 |
|----------|-----------|-------------|
| `date()` | `date.date(): date` | 移除时间部分 |
| `format()` | `date.format(string): string` | 使用 Moment.js 模式格式化 |
| `time()` | `date.time(): string` | 获取时间字符串 |
| `relative()` | `date.relative(): string` | 人类可读的相对时间 |
| `isEmpty()` | `date.isEmpty(): boolean` | 对日期始终为 false |

### Duration 类型

当两个日期相减时，结果是 **Duration** 类型（不是数字）。Duration 有自己的属性和方法。

**Duration Fields:**
| Field | 类型 | 描述 |
|-------|------|-------------|
| `duration.days` | Number | duration 中的总天数 |
| `duration.hours` | Number | duration 中的总小时数 |
| `duration.minutes` | Number | duration 中的总分钟数 |
| `duration.seconds` | Number | duration 中的总秒数 |
| `duration.milliseconds` | Number | duration 中的总毫秒数 |

**重要:** Duration 不直接支持 `.round()`、`.floor()`、`.ceil()`。你必须先访问数字字段（如 `.days`），然后应用 number functions。

```yaml
# 正确: 计算日期之间的天数
"(date(due_date) - today()).days"                    # 返回天数
"(now() - file.ctime).days"                          # 自创建以来的天数

# 正确: 如有需要，四舍五入数字结果
"(date(due_date) - today()).days.round(0)"           # 四舍五入后的天数
"(now() - file.ctime).hours.round(0)"                # 四舍五入后的小时数

# 错误 - 会导致错误:
# "((date(due) - today()) / 86400000).round(0)"      # Duration 不支持除法然后四舍五入
```

### 日期运算

```yaml
# Duration 单位: y/year/years, M/month/months, d/day/days,
#                 w/week/weeks, h/hour/hours, m/minute/minutes, s/second/seconds

# 添加/减去 durations
"date + \"1M\""           # 加 1 个月
"date - \"2h\""           # 减 2 小时
"now() + \"1 day\""       # 明天
"today() + \"7d\""        # 一周后

# 日期相减返回 Duration 类型
"now() - file.ctime"                    # 返回 Duration
"(now() - file.ctime).days"             # 获取天数作为数字
"(now() - file.ctime).hours"            # 获取小时数作为数字

# 复杂的 duration 运算
"now() + (duration('1d') * 2)"
```

### String Functions

**Field:** `string.length`

| Function | 签名 | 描述 |
|----------|-----------|-------------|
| `contains()` | `string.contains(value): boolean` | 检查子字符串 |
| `containsAll()` | `string.containsAll(...values): boolean` | 所有子字符串都存在 |
| `containsAny()` | `string.containsAny(...values): boolean` | 任一子字符串存在 |
| `startsWith()` | `string.startsWith(query): boolean` | 以 query 开头 |
| `endsWith()` | `string.endsWith(query): boolean` | 以 query 结尾 |
| `isEmpty()` | `string.isEmpty(): boolean` | 为空或不存在 |
| `lower()` | `string.lower(): string` | 转为小写 |
| `title()` | `string.title(): string` | 转为 Title Case |
| `trim()` | `string.trim(): string` | 移除空白字符 |
| `replace()` | `string.replace(pattern, replacement): string` | 替换模式 |
| `repeat()` | `string.repeat(count): string` | 重复字符串 |
| `reverse()` | `string.reverse(): string` | 反转字符串 |
| `slice()` | `string.slice(start, end?): string` | 子字符串 |
| `split()` | `string.split(separator, n?): list` | 分割为 list |

### Number Functions

| Function | 签名 | 描述 |
|----------|-----------|-------------|
| `abs()` | `number.abs(): number` | 绝对值 |
| `ceil()` | `number.ceil(): number` | 向上取整 |
| `floor()` | `number.floor(): number` | 向下取整 |
| `round()` | `number.round(digits?): number` | 四舍五入到指定位数 |
| `toFixed()` | `number.toFixed(precision): string` | 定点表示法 |
| `isEmpty()` | `number.isEmpty(): boolean` | 不存在 |

### List Functions

**Field:** `list.length`

| Function | 签名 | 描述 |
|----------|-----------|-------------|
| `contains()` | `list.contains(value): boolean` | 元素存在 |
| `containsAll()` | `list.containsAll(...values): boolean` | 所有元素存在 |
| `containsAny()` | `list.containsAny(...values): boolean` | 任一元素存在 |
| `filter()` | `list.filter(expression): list` | 按条件过滤（使用 `value`, `index`） |
| `map()` | `list.map(expression): list` | 转换元素（使用 `value`, `index`） |
| `reduce()` | `list.reduce(expression, initial): any` | 归约为单个值（使用 `value`, `index`, `acc`） |
| `flat()` | `list.flat(): list` | 扁平化嵌套 lists |
| `join()` | `list.join(separator): string` | 连接为 string |
| `reverse()` | `list.reverse(): list` | 反转顺序 |
| `slice()` | `list.slice(start, end?): list` | 子 list |
| `sort()` | `list.sort(): list` | 升序排序 |
| `unique()` | `list.unique(): list` | 移除重复项 |
| `isEmpty()` | `list.isEmpty(): boolean` | 无元素 |

### File Functions

| Function | 签名 | 描述 |
|----------|-----------|-------------|
| `asLink()` | `file.asLink(display?): Link` | 转换为 link |
| `hasLink()` | `file.hasLink(otherFile): boolean` | 有指向文件的 link |
| `hasTag()` | `file.hasTag(...tags): boolean` | 有任一 tags |
| `hasProperty()` | `file.hasProperty(name): boolean` | 有 property |
| `inFolder()` | `file.inFolder(folder): boolean` | 在文件夹或子文件夹中 |

### Link Functions

| Function | 签名 | 描述 |
|----------|-----------|-------------|
| `asFile()` | `link.asFile(): file` | 获取 file 对象 |
| `linksTo()` | `link.linksTo(file): boolean` | 链接到文件 |

### Object Functions

| Function | 签名 | 描述 |
|----------|-----------|-------------|
| `isEmpty()` | `object.isEmpty(): boolean` | 无 properties |
| `keys()` | `object.keys(): list` | keys 的 list |
| `values()` | `object.values(): list` | values 的 list |

### 正则表达式 Functions

| Function | 签名 | 描述 |
|----------|-----------|-------------|
| `matches()` | `regexp.matches(string): boolean` | 测试是否匹配 |

## View 类型

### Table View

```yaml
views:
  - type: table
    name: "My Table"
    order:
      - file.name
      - status
      - due_date
    summaries:
      price: Sum
      count: Average
```

### Cards View

```yaml
views:
  - type: cards
    name: "Gallery"
    order:
      - file.name
      - cover_image
      - description
```

### List View

```yaml
views:
  - type: list
    name: "Simple List"
    order:
      - file.name
      - status
```

### Map View

需要 latitude/longitude properties 和 Maps 社区插件。

```yaml
views:
  - type: map
    name: "Locations"
    # Map 特定的 lat/lng properties 设置
```

## 默认 Summary Formulas

| 名称 | 输入类型 | 描述 |
|------|------------|-------------|
| `Average` | Number | 数学平均值 |
| `Min` | Number | 最小数字 |
| `Max` | Number | 最大数字 |
| `Sum` | Number | 所有数字的总和 |
| `Range` | Number | Max - Min |
| `Median` | Number | 数学中位数 |
| `Stddev` | Number | 标准差 |
| `Earliest` | Date | 最早日期 |
| `Latest` | Date | 最新日期 |
| `Range` | Date | Latest - Earliest |
| `Checked` | Boolean | true 值的数量 |
| `Unchecked` | Boolean | false 值的数量 |
| `Empty` | Any | 空值的数量 |
| `Filled` | Any | 非空值的数量 |
| `Unique` | Any | 唯一值的数量 |

## 完整示例

### 任务追踪 Base

```yaml
filters:
  and:
    - file.hasTag("task")
    - 'file.ext == "md"'

formulas:
  days_until_due: 'if(due, (date(due) - today()).days, "")'
  is_overdue: 'if(due, date(due) < today() && status != "done", false)'
  priority_label: 'if(priority == 1, "🔴 High", if(priority == 2, "🟡 Medium", "🟢 Low"))'

properties:
  status:
    displayName: Status
  formula.days_until_due:
    displayName: "Days Until Due"
  formula.priority_label:
    displayName: Priority

views:
  - type: table
    name: "Active Tasks"
    filters:
      and:
        - 'status != "done"'
    order:
      - file.name
      - status
      - formula.priority_label
      - due
      - formula.days_until_due
    groupBy:
      property: status
      direction: ASC
    summaries:
      formula.days_until_due: Average

  - type: table
    name: "Completed"
    filters:
      and:
        - 'status == "done"'
    order:
      - file.name
      - completed_date
```

### 阅读列表 Base

```yaml
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")

formulas:
  reading_time: 'if(pages, (pages * 2).toString() + " min", "")'
  status_icon: 'if(status == "reading", "📖", if(status == "done", "✅", "📚"))'
  year_read: 'if(finished_date, date(finished_date).year, "")'

properties:
  author:
    displayName: Author
  formula.status_icon:
    displayName: ""
  formula.reading_time:
    displayName: "Est. Time"

views:
  - type: cards
    name: "Library"
    order:
      - cover
      - file.name
      - author
      - formula.status_icon
    filters:
      not:
        - 'status == "dropped"'

  - type: table
    name: "Reading List"
    filters:
      and:
        - 'status == "to-read"'
    order:
      - file.name
      - author
      - pages
      - formula.reading_time
```

### 项目笔记 Base

```yaml
filters:
  and:
    - file.inFolder("Projects")
    - 'file.ext == "md"'

formulas:
  last_updated: 'file.mtime.relative()'
  link_count: 'file.links.length'

summaries:
  avgLinks: 'values.filter(value.isType("number")).mean().round(1)'

properties:
  formula.last_updated:
    displayName: "Updated"
  formula.link_count:
    displayName: "Links"

views:
  - type: table
    name: "All Projects"
    order:
      - file.name
      - status
      - formula.last_updated
      - formula.link_count
    summaries:
      formula.link_count: avgLinks
    groupBy:
      property: status
      direction: ASC

  - type: list
    name: "Quick List"
    order:
      - file.name
      - status
```

### 每日笔记索引

```yaml
filters:
  and:
    - file.inFolder("Daily Notes")
    - '/^\d{4}-\d{2}-\d{2}$/.matches(file.basename)'

formulas:
  word_estimate: '(file.size / 5).round(0)'
  day_of_week: 'date(file.basename).format("dddd")'

properties:
  formula.day_of_week:
    displayName: "Day"
  formula.word_estimate:
    displayName: "~Words"

views:
  - type: table
    name: "Recent Notes"
    limit: 30
    order:
      - file.name
      - formula.day_of_week
      - formula.word_estimate
      - file.mtime
```

## 嵌入 Bases

嵌入 Markdown 文件：

```markdown
![[MyBase.base]]

<!-- 特定 view -->
![[MyBase.base#View Name]]
```

## YAML 引号规则

- 对包含双引号的 formulas 使用单引号: `'if(done, "Yes", "No")'`
- 对简单字符串使用双引号: `"My View Name"`
- 在复杂表达式中正确转义嵌套引号

## 常见模式

### 按 Tag 过滤
```yaml
filters:
  and:
    - file.hasTag("project")
```

### 按文件夹过滤
```yaml
filters:
  and:
    - file.inFolder("Notes")
```

### 按日期范围过滤
```yaml
filters:
  and:
    - 'file.mtime > now() - "7d"'
```

### 按 Property 值过滤
```yaml
filters:
  and:
    - 'status == "active"'
    - 'priority >= 3'
```

### 组合多个条件
```yaml
filters:
  or:
    - and:
        - file.hasTag("important")
        - 'status != "done"'
    - and:
        - 'priority == 1'
        - 'due != ""'
```

## 参考

- [Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Functions](https://help.obsidian.md/bases/functions)
- [Views](https://help.obsidian.md/bases/views)
- [Formulas](https://help.obsidian.md/formulas)
