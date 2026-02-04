# 上游仓库更新记录

最后更新：2026-02-03

---

## 🎯 当前工作计划（2026-02-03 ~ 2026-03-03）

**专注于 upstream/everything-claude-code 仓库的深入研究与改造**

| 阶段 | 目标 | 状态 |
|------|------|------|
| 第一阶段 | 全面梳理 everything-claude-code 的所有 agents/commands/skills/rules/contexts | 🔄 进行中 |
| 第二阶段 | 识别有价值的组件，复制到 my/ 进行中文本地化改造 | ⏳ 待开始 |
| 第三阶段 | 同步更新 CLAUDE.md 和 README.md 中的可用组件列表 | ⏳ 待开始 |
| 第四阶段 | 评估改进空间，考虑向 affaan-m/everything-claude-code 贡献 | ⏳ 待开始 |

---

## 更新历史

| 日期 | 仓库 | 更新内容 | 推荐 | 说明 |
|------|------|----------|------|------|
| 2026-02-02 | everything-claude-code | 新增 5 个 Python/Django skills | ⭐⭐⭐⭐⭐ | Python/Django 全栈支持，涵盖编码规范、测试、安全、架构模式 |
| 2026-02-02 | openai-skills | 新增 12 个 curated skills | ⭐⭐⭐⭐ | Notion、Figma、Playwright、Sentry 等工具集成 |
| 2026-02-02 | ai-research-skills | npm 包 v1.1.0，新增 OpenCode 支持 | ⭐⭐⭐⭐ | AI/ML 研究知识库，20 个主题章节，新增社区链接 |
| 2026-02-02 | superpowers | 工作树要求、主分支警告机制 | ⭐⭐⭐⭐ | 新增 git worktree 使用要求、main branch red flag 警告 |
| 2026-01-30 | everything-claude-code | 新增 6 个 Java Spring Boot skills | ⭐⭐⭐⭐⭐ | 适合 Java/Spring Boot 后端开发，涵盖编码规范、架构模式、安全、TDD、JPA 验证等完整开发生态 |
| 2026-01-30 | superpowers | 新增上游跟踪 | ⭐⭐⭐⭐⭐ | 完整的软件开发工作流系统，包含 TDD、调试、协作、并行开发等 13 个 skills |

## 详情

### superpowers (2026-01-30)

**仓库地址:** https://github.com/obra/superpowers

**简介:** 完整的软件开发工作流系统，为 AI 编码代理提供可组合的 "superpowers"（技能集合）

**可用 Skills:**

| Skill | 说明 |
|-------|------|
| `brainstorming` | 交互式设计细化，通过提问将粗略想法转化为清晰规格 |
| `writing-plans` | 将工作分解为小任务（2-5 分钟），包含具体文件路径和验证步骤 |
| `executing-plans` | 批量执行计划，带人工检查点 |
| `subagent-driven-development` | 子代理驱动开发，两阶段审查（规格合规性 + 代码质量） |
| `test-driven-development` | 强制 RED-GREEN-REFACTOR 循环，先写测试 |
| `systematic-debugging` | 4 阶段根因分析过程 |
| `verification-before-completion` | 确保问题真正修复 |
| `dispatching-parallel-agents` | 并发子代理工作流 |
| `requesting-code-review` | 代码审查前检查清单 |
| `receiving-code-review` | 响应反馈的规范流程 |
| `using-git-worktrees` | 并行开发分支管理 |
| `finishing-a-development-branch` | 合并/PR 决策工作流 |
| `writing-skills` | 创建新 skills 的最佳实践 |
| `using-superpowers` | skills 系统介绍 |

**核心理念:** TDD 优先、系统化而非临时性、复杂度降低、证据优于声明

**支持平台:** Claude Code (通过插件市场)、Codex、OpenCode

### everything-claude-code (2026-01-30)

**新增 Skills:**

1. **springboot-patterns** - Spring Boot 架构模式
   - REST API 设计、分层服务、数据访问
   - 缓存、异步处理、日志记录
   - 适用：Java Spring Boot 后端开发

2. **springboot-security** - Spring Boot 安全最佳实践
   - 认证/授权、输入验证、CSRF
   - 密钥管理、安全头、速率限制
   - 依赖安全检查

3. **java-coding-standards** - Java 编码规范
   - 命名规范、不可变性设计
   - Optional 使用、流式处理
   - 异常处理、泛型、项目布局

4. **springboot-tdd** - Spring Boot 测试驱动开发
   - JUnit 5、Mockito、MockMvc
   - Testcontainers、JaCoCo 覆盖率
   - 适用：功能开发、bug 修复、重构

5. **jpa-patterns** - JPA/Hibernate 模式
   - 实体设计、关联关系
   - N+1 查询预防、事务管理
   - 审计、索引、分页、连接池

6. **springboot-verification** - Spring Boot 验证流程
   - 构建验证、静态分析
   - 测试覆盖率、安全扫描
   - 发布/PR 前的完整验证循环

### everything-claude-code (2026-02-02)

**新增 Python/Django 支持：**

| Skill | 说明 | 适用场景 |
|-------|------|----------|
| `python-patterns` | Python 架构模式、函数式编程、类型注解 | Python 项目架构设计 |
| `python-testing` | 测试框架 (pytest/unittest)、mock、fixture | Python 测试策略 |
| `django-patterns` | Django 模型、视图、URL、ORM 最佳实践 | Django 后端开发 |
| `django-security` | 认证、授权、CSRF、XSS、SQL 注入防护 | Django 安全加固 |
| `django-tdd` | Django 测试驱动开发、工厂模式、集成测试 | Django TDD 流程 |
| `django-verification` | 代码审查、安全检查、发布前验证 | Django 项目验证 |

**新增 Agent：**

| Agent | 说明 |
|-------|------|
| `python-reviewer` | Python 代码审查专员，检查代码质量、安全性、可维护性 |

**新增 Command：**

| Command | 说明 |
|---------|------|
| `python-review` | Python 代码审查命令，触发 python-reviewer agent |

---

### openai-skills (2026-02-02)

**新增 Curated Skills：**

| Skill | 说明 | 适用场景 |
|-------|------|----------|
| `atlas` | 项目启动模板，快速初始化 | 新项目脚手架 |
| `cloudflare-deploy` | Cloudflare Pages/Workers 部署 | 边缘部署 |
| `develop-web-game` | 游戏开发流程 | 浏览器游戏 |
| `figma-implement-design` | Figma 设计转代码 | UI 还原 |
| `jupyter-notebook` | 数据科学工作流 | 数据分析/ML |
| `linear` | Linear 项目管理集成 | 任务追踪 |
| `notion-knowledge-capture` | Notion 知识捕获 | 文档管理 |
| `notion-meeting-intelligence` | Notion 会议智能分析 | 会议记录 |
| `notion-research-documentation` | Notion 研究文档 | 研究笔记 |
| `notion-spec-to-implementation` | Notion 规格到实现 | 需求转化 |
| `openai-docs` | OpenAI 文档查询 | API 参考 |
| `playwright` | Playwright 自动化测试 | E2E 测试 |
| `sentry` | Sentry 错误监控集成 | 生产监控 |
| `transcribe` | 语音转文字 | 音频处理 |
| `vercel-deploy` | Vercel 部署 | 前端托管 |

---

### ai-research-skills (2026-02-02)

**更新内容：**
- npm 包 v1.1.0：新增 OpenCode 支持
- 新增社区链接：Slack、Twitter、LinkedIn
- 完整的 AI/ML 研究知识库，包含 20 个主题章节

**知识库涵盖主题：**
模型架构、Tokenization、微调、可解释性、数据处理、后训练、安全对齐、分布式训练、基础设施、优化、评估、推理服务、MLOps、Agents、RAG、提示工程、可观测性、多模态、新兴技术、论文写作

---

### superpowers (2026-02-02)

**更新内容：**

| Skill | 更新内容 |
|-------|----------|
| `subagent-driven-development` | 新增主分支 red flag 警告，禁止在 main 分支直接开发 |
| `executing-plans` | 新增 git worktree 使用要求，确保并行开发时工作树配置正确 |
| `using-git-worktrees` | 更新子代理调用场景说明 |

**安全改进：**
- 新增 Test 9：主分支 red flag 警告测试
- 新增工作树要求测试

---

### anthropics-skills
- 无更新

### obsidian-skills
- 无更新
