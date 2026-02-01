# Skill 命名规范

最后更新：2026-02-02

## 前缀分类体系

| 前缀 | 类别 | 说明 | 示例 |
|------|------|------|------|
| `dev-` | **开发** | 编码、代码审查、调试、架构设计 | `dev-plan`, `dev-review-py`, `dev-tdd` |
| `life-` | **生活** | 笔记整理、日常安排、健康、财务 | `life-notes`, `life-daily`, `life-budget` |
| `work-` | **工作** | 项目管理、会议、文档、任务跟踪 | `work-meeting`, `work-project`, `work-docs` |
| `tool-` | **工具** | 系统工具、环境配置、MCP 服务器 | `tool-mcp-builder`, `tool-sshfs-mount` |
| `learn-` | **学习** | 研究笔记、学习笔记、知识整理 | `learn-research`, `learn-paper`, `learn-summary` |

## 命名格式

```
<category>-<name>
```

### 示例对比

| 场景 | 旧命名 | 新命名 |
|------|--------|--------|
| 开发项目规划 | `plan` | `dev-plan` |
| 生活笔记整理 | `notes` | `life-notes` |
| 工作会议记录 | `meeting` | `work-meeting` |
| 系统工具配置 | `sshfs-mount` | `tool-sshfs-mount` |
| 研究论文笔记 | `research-notes` | `learn-paper` |

## 现有 Skills 映射

### 需要重命名的 Skills

| 当前名称 | 新名称 | 说明 |
|----------|--------|------|
| `plan` | `dev-plan` | 开发项目规划 |
| `tdd` | `dev-tdd` | 测试驱动开发 |
| `code-review-py` | `dev-review-py` | Python 代码审查 |
| `code-review-ts` | `dev-review-ts` | TypeScript 代码审查 |
| `python-async-modernizer` | `dev-async-modernize` | Python 异步代码现代化 |
| `macos-hidpi` | `tool-macos-hidpi` | macOS 显示器配置工具 |
| `mcp-builder` | `tool-mcp-builder` | MCP 服务器构建工具 |
| `sshfs-mount` | `tool-sshfs-mount` | SSH 远程目录挂载工具 |
| `skill-creator` | `tool-skill-creator` | Skill 创建工具 |
| `update-codemaps` | `dev-update-codemaps` | 代码地图更新 |
| `update-docs` | `dev-update-docs` | 开发文档更新 |

### 无需重命名的 Skills

| 名称 | 说明 |
|------|------|
| `rehabilitating-legacy-tests` | 已明确是开发相关，可改为 `dev-rehab-legacy-tests` |
| `test-driven-development` | 已明确是开发相关，可改为 `dev-tdd` |

## 新 Skills 命名指南

### 开发类 (dev-)

| 名称 | 说明 |
|------|------|
| `dev-plan` | 项目开发规划 |
| `dev-tdd` | 测试驱动开发 |
| `dev-review-*` | 代码审查（py/ts/js/java 等） |
| `debug-*` | 调试技巧 |
| `refactor-*` | 代码重构 |

### 生活类 (life-)

| 名称 | 说明 |
|------|------|
| `life-notes` | 笔记整理 |
| `life-daily` | 日常安排 |
| `life-health` | 健康管理 |
| `life-budget` | 财务预算 |
| `life-reading` | 阅读清单 |

### 工作类 (work-)

| 名称 | 说明 |
|------|------|
| `work-meeting` | 会议记录 |
| `work-project` | 项目管理 |
| `work-docs` | 工作文档 |
| `work-task` | 任务跟踪 |

### 工具类 (tool-)

| 名称 | 说明 |
|------|------|
| `tool-mcp-*` | MCP 相关工具 |
| `tool-sshfs-*` | SSHFS 相关工具 |
| `tool-*-*` | 各类系统工具 |

### 学习类 (learn-)

| 名称 | 说明 |
|------|------|
| `learn-paper` | 论文笔记 |
| `learn-research` | 研究笔记 |
| `learn-summary` | 知识总结 |
| `learn-course` | 课程笔记 |

## 迁移步骤

1. **创建新目录**：按照新命名创建目录
2. **复制内容**：将旧 SKILL.md 内容复制到新目录
3. **更新引用**：更新 agents/commands 中的引用
4. **删除旧目录**：确认无引用后删除

```bash
# 示例：重命名 skill
mv my/claudecode/skills/plan my/claudecode/skills/dev-plan
```
