---
name: dev-update-codemaps
description: 分析代码库结构并更新架构文档
---

# 更新代码地图

分析代码库结构并更新架构文档。

## 前置步骤：项目类型检测

首先通过 Glob 工具扫描项目根目录，确定项目类型：

| 检测条件 | 项目类型 | 分析工具 |
|---------|---------|---------|
| `pyproject.toml`, `setup.py`, `requirements.txt` 存在 | Python | `ast` 模块、`uv run` 执行分析脚本 |
| `package.json`, `tsconfig.json` 存在 | TypeScript/Node.js | `madge`、TypeScript Compiler API |
| `go.mod` 存在 | Go | `go list`、`go mod graph` |
| `Cargo.toml` 存在 | Rust | `cargo tree` |
| `pom.xml`, `build.gradle` 存在 | Java | 自定义分析或工具 |
| 以上都不存在 | 通用 | 目录结构遍历、文件树分析 |

## 分析流程

### 1. 代码结构扫描

根据项目类型选择分析方法：

**Python 项目：**
```bash
# 使用 Python ast 模块分析导入和依赖
uv run python -c "
import ast
import sys
from pathlib import Path

def analyze_imports(file_path):
    tree = ast.parse(Path(file_path).read_text())
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.append([alias.name for alias in node.names])
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    return imports
"
```

**TypeScript/Node.js 项目：**
```bash
# 使用 madge 分析依赖关系
npx madge --image deps.svg --extensions ts,tsx,js,jsx src/
```

**通用方法（任何语言）：**
- 使用 `tree` 或 `find` 命令获取目录结构
- 通过 Glob 模式匹配识别模块边界
- 分析文件命名约定推断模块组织

### 2. 生成代码地图

创建 `codemaps/` 目录，生成以下文件（根据项目实际情况选择）：

| 文件 | 内容 | 适用项目 |
|------|------|---------|
| `architecture.md` | 整体架构、层划分、入口点 | 所有 |
| `backend.md` | 后端结构、API 路由、服务层 | 后端项目 |
| `frontend.md` | 前端结构、组件树、状态管理 | 前端项目 |
| `data.md` | 数据模型、Schema、数据库关系 | 有数据层的项目 |
| `dependencies.md` | 模块依赖关系图（简化版） | 所有 |

代码地图格式示例：
```markdown
# 项目架构

生成时间: {{timestamp}}

## 目录结构
```
src/
├── core/           # 核心业务逻辑
├── api/            # API 接口层
└── utils/          # 工具函数
```

## 模块依赖
- api → core
- core → utils
```

### 3. 差异对比

1. 读取上一版本的代码地图（如果存在）
2. 计算差异百分比（基于行数、结构变化等）
3. 如果变化 > 30%，使用 AskUserQuestion 请求用户批准后再更新

### 4. 更新和报告

1. 为每个代码地图添加新鲜度时间戳
2. 将差异报告保存到 `.reports/codemap-diff.txt`
3. 输出更新摘要

## 分析原则

- **关注高层结构** — 模块、包、层之间的组织关系
- **忽略实现细节** — 函数内部逻辑、具体算法
- **保持精简** — 代码地图应该易于阅读，而非完整的代码文档
- **自动适配** — 根据项目特征选择最合适的分析方法

## 示例输出

```
✓ 检测到 Python 项目
✓ 扫描了 47 个源文件
✓ 生成 4 个代码地图文件
✓ 与上一版本差异: 15%
📁 codemaps/architecture.md
📁 codemaps/backend.md
📁 codemaps/data.md
📄 .reports/codemap-diff.txt
```
