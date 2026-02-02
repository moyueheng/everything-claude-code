---
name: code-shit-detector
description: 使用 fuck-u-code 工具检测代码屎山程度，生成质量分析报告。当用户需要：(1) 评估代码质量，(2) 检测代码中的问题（复杂度、重复度、注释率等），(3) 生成代码质量报告，(4) 识别需要重构的代码文件时使用此技能。支持 Python、JavaScript/TypeScript、Go、Java、C/C++ 等多种语言。
---

# 代码屎山检测器

## 概述

使用 `fuck-u-code` 工具对代码库进行质量分析，检测屎山代码并生成详细的检测报告。工具会从 7 个维度评估代码质量：循环复杂度、函数长度、注释率、错误处理、命名规范、代码重复度、结构分析。

## 使用方法

### 前提条件

确保已安装 `fuck-u-code` 工具：

```bash
# 使用 Go 安装
go install github.com/Done-0/fuck-u-code/cmd/fuck-u-code@latest

# 或将 Go bin 目录添加到 PATH
export PATH="$PATH:$(go env GOPATH)/bin"
```

### 基本检测

```bash
# 检测当前目录
fuck-u-code analyze

# 检测指定目录
fuck-u-code /path/to/project

# 检测 Git 仓库
fuck-u-code https://github.com/user/repo.git
```

### 常用选项

| 选项 | 简写 | 说明 |
|------|------|------|
| `--verbose` | `-v` | 显示详细报告 |
| `--top N` | `-t` | 显示最烂的前 N 个文件 |
| `--issues N` | `-i` | 每文件显示 N 个问题 |
| `--summary` | `-s` | 仅显示总结 |
| `--markdown` | `-m` | 输出 Markdown 格式 |
| `--lang` | `-l` | 报告语言 (zh-CN/en-US/ru-RU) |
| `--exclude` | `-e` | 排除指定目录或文件 |

### 推荐用法

```bash
# 生成详细的 Markdown 报告
fuck-u-code /path/to/project --markdown --top 15 --lang zh-CN > report.md

# 快速查看问题最严重的文件
fuck-u-code /path/to/project --top 10 --issues 5 --lang zh-CN

# 仅查看总结
fuck-u-code /path/to/project --summary --lang zh-CN
```

## 报告解读

### 评分等级

| 分数范围 | 等级 | 说明 |
|----------|------|------|
| 0-20 | 代码仙人 | 极其优秀的代码 |
| 20-40 | 微臭青年 | 略有异味，建议适量通风 |
| 40-60 | 屎山学徒 | 代码开始发臭，需要关注 |
| 60-80 | 屎山大帝 | 代码很烂，需要重构 |
| 80-100 | 屎山之神 | 极其糟糕的代码，必须重构 |

### 检测维度

1. **循环复杂度** - 函数逻辑复杂度，越高越难维护
2. **函数长度** - 函数行数，超过 50 行建议拆分
3. **注释覆盖率** - 代码注释比例，建议至少 10%
4. **错误处理** - 异常和错误处理完善程度
5. **命名规范** - 变量、函数命名是否符合规范
6. **代码重复度** - 重复代码比例
7. **结构分析** - 代码组织和结构合理性

## 自动化脚本

使用 `scripts/run-detector.sh` 脚本简化检测流程：

```bash
# 基本检测
./scripts/run-detector.sh /path/to/project

# 生成完整报告
./scripts/run-detector.sh /path/to/project --full

# 生成 Markdown 报告到指定文件
./scripts/run-detector.sh /path/to/project --markdown --output report.md
```

## 问题处理建议

### 高优先级
- 函数长度超过 100 行 - 必须拆分
- 循环复杂度超过 15 - 必须简化
- 完全没有注释的关键代码

### 中优先级
- 函数长度 50-100 行 - 建议拆分
- 循环复杂度 10-15 - 建议简化
- 注释率低于 5%

### 低优先级
- 命名不规范
- 轻微代码重复
- 格式问题
