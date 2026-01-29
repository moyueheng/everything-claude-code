# 上游仓库更新日志

> 记录 upstream/ 目录下两个上游仓库的更新内容
> 上游仓库完全只读，仅用于跟踪和参考

---

## 2026-01-29 更新

### everything-claude-code (affaan-m/everything-claude-code)

#### 新增
- **Plugin Schema 文档** (`.claude-plugin/PLUGIN_SCHEMA_NOTES.md`)
  - 插件架构说明文档
- **skill-create-output.js 脚本** (`scripts/skill-create-output.js`)
  - 技能创建输出处理脚本，244行

#### 更新
- **README.md** - 项目文档更新
- **plugin.json** - 插件配置更新
- **多个脚本修复**
  - `scripts/hooks/check-console-log.js`
  - `scripts/lib/package-manager.js`
  - `scripts/lib/utils.js`
  - `scripts/setup-package-manager.js`

#### 值得关注
- 新增的技能创建输出处理脚本可能改进了技能开发流程
- Plugin Schema 文档有助于理解 Claude Plugin 架构

---

### anthropics-skills (anthropics/skills) - 重大架构升级

#### 🏗️ 架构升级
- **Claude Plugin 完整支持** (`.claude-plugin/`)
  - `plugin.json` - 插件主配置
  - `marketplace.json` - 市场配置
  - `PLUGIN_SCHEMA_NOTES.md` - 架构说明
- **CI/CD 工作流** (`.github/workflows/`)
  - `ci.yml` - 持续集成
  - `release.yml` / `reusable-release.yml` - 发布流程
  - `reusable-test.yml` / `reusable-validate.yml` - 测试验证
  - `maintenance.yml` - 维护任务
- **包管理器** (`.claude/package-manager.json`)

#### 🤖 新增 Agents (12个)
| Agent | 用途 |
|-------|------|
| `architect.md` | 架构设计 |
| `build-error-resolver.md` | 构建错误解决 |
| `code-reviewer.md` | 代码审查 |
| `database-reviewer.md` | 数据库审查 |
| `doc-updater.md` | 文档更新 |
| `e2e-runner.md` | E2E 测试运行 |
| `go-build-resolver.md` | Go 构建错误解决 |
| `go-reviewer.md` | Go 代码审查 |
| `planner.md` | 任务规划 |
| `refactor-cleaner.md` | 重构清理 |
| `security-reviewer.md` | 安全审查 |
| `tdd-guide.md` | TDD 指导 |

#### ⌨️ 新增 Commands (23个)
**开发工作流：**
- `plan` - 任务规划
- `orchestrate` - 编排执行
- `checkpoint` - 创建检查点
- `refactor-clean` - 重构清理

**代码质量：**
- `code-review` - 代码审查
- `test-coverage` - 测试覆盖率
- `verify` - 验证检查

**Go 语言专项：**
- `go-build` - Go 构建
- `go-review` - Go 代码审查
- `go-test` - Go 测试
- `build-fix` / `go-build` - 构建修复

**E2E 测试：**
- `e2e` - E2E 测试运行

**评估与学习：**
- `eval` - 评估执行
- `learn` - 学习模式
- `evolve` - 进化模式

**Instinct 系统：**
- `instinct-export` - 导出本能
- `instinct-import` - 导入本能
- `instinct-status` - 本能状态

**技能与文档：**
- `skill-create` - 创建技能
- `setup-pm` - 设置包管理器
- `update-codemaps` - 更新代码地图
- `update-docs` - 更新文档

#### 📚 新增 Skills (13个)
**开发模式：**
- `backend-patterns` - 后端开发模式
- `frontend-patterns` - 前端开发模式
- `coding-standards` - 编码标准

**语言专项：**
- `golang-patterns` - Go 语言模式
- `golang-testing` - Go 测试模式
- `postgres-patterns` - PostgreSQL 模式
- `clickhouse-io` - ClickHouse IO

**质量保障：**
- `security-review` - 安全审查
- `tdd-workflow` - TDD 工作流
- `verification-loop` - 验证循环
- `eval-harness` - 评估工具

**学习与优化：**
- `continuous-learning` - 持续学习
- `continuous-learning-v2` - 持续学习 v2（增强版）
- `iterative-retrieval` - 迭代检索
- `strategic-compact` - 战略压缩

**项目管理：**
- `project-guidelines-example` - 项目规范示例

#### 📋 新增 Rules (8个)
- `agents.md` - Agent 使用规范
- `coding-style.md` - 编码风格
- `git-workflow.md` - Git 工作流
- `hooks.md` - Hooks 规范
- `patterns.md` - 设计模式
- `performance.md` - 性能规范
- `security.md` - 安全规范
- `testing.md` - 测试规范

#### 🌐 完整的中文文档
- `docs/zh-TW/` - 繁体中文完整翻译
  - 所有 agents、commands、rules、skills 的中文版本
  - `README.zh-CN.md` - 简体中文 README

#### 🪝 Hooks 系统
- `session-start` - 会话开始钩子
- `session-end` - 会话结束钩子
- `pre-compact` - 压缩前钩子
- `evaluate-session` - 会话评估
- `check-console-log` - 检查 console.log
- `suggest-compact` - 建议压缩

#### 🧪 测试与工具
- 完整的测试套件 (`tests/`)
- CI 验证脚本 (`scripts/ci/`)
- 工具脚本 (`scripts/lib/`)

#### 🗑️ 移除的内容
以下技能已被移除：
- `algorithmic-art` - 算法艺术
- `brand-guidelines` - 品牌指南
- `canvas-design` - Canvas 设计（含大量字体文件）
- `doc-coauthoring` - 文档协作
- `docx` - Word 文档处理
- `frontend-design` - 前端设计
- `internal-comms` - 内部通讯
- `mcp-builder` - MCP 构建器
- `pdf` - PDF 处理
- `pptx` - PPT 处理
- `skill-creator` - 技能创建器
- `slack-gif-creator` - Slack GIF 创建器
- `theme-factory` - 主题工厂
- `web-artifacts-builder` - Web 工件构建器
- `webapp-testing` - Web 应用测试
- `xlsx` - Excel 处理

#### ⚠️ 重大变更
- **架构重构**：从单一技能集合转变为完整的 Claude Plugin 生态系统
- **技能精简**：移除了 15+ 个具体工具类技能，聚焦于开发工作流和质量保障
- **新增繁体中文支持**：完整的中文文档体系

#### 🔥 最值得关注的更新

1. **continuous-learning-v2** - 增强版持续学习
   - 包含 observer agent、instinct CLI、evolve 命令
   - 支持本能导出/导入

2. **security-review** - 安全审查技能
   - 包含云基础设施安全审查
   - 专门的安全审查 agent

3. **golang-patterns + golang-testing** - Go 开发完整方案
   - Go 代码模式
   - Go 测试最佳实践
   - 专门的 Go 相关 agents 和 commands

4. **完整的繁体中文文档** - `docs/zh-TW/`
   - 所有核心文档都有中文版本
   - 方便中文用户理解和使用

5. **CI/CD 工作流** - 企业级质量保障
   - 自动化测试
   - 自动发布流程
   - 代码验证

---

## 更新建议

### 推荐复制到 my/ 进行本地化的内容：

**高优先级：**
1. `agents/planner.md` - 任务规划器
2. `agents/code-reviewer.md` - 代码审查员
3. `skills/continuous-learning-v2/` - 持续学习 v2
4. `skills/security-review/` - 安全审查
5. `rules/coding-style.md` - 编码风格规范

**中优先级：**
1. `commands/plan.md` - 规划命令
2. `commands/code-review.md` - 代码审查命令
3. `skills/tdd-workflow/` - TDD 工作流
4. `skills/verification-loop/` - 验证循环

**参考学习：**
1. `docs/zh-TW/` 下的中文翻译
2. `.github/workflows/` 的 CI 配置
3. `hooks/` 的钩子系统实现

---

*最后更新：2026-01-29*
