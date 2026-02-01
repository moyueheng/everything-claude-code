# 上游仓库更新记录

最后更新：2026-01-30

| 日期 | 仓库 | 更新内容 | 推荐 | 说明 |
|------|------|----------|------|------|
| 2026-01-30 | superpowers | 新增上游跟踪 | ⭐⭐⭐⭐⭐ | 完整的软件开发工作流系统，包含 TDD、调试、协作、并行开发等 13 个 skills |
| 2026-01-30 | everything-claude-code | 新增 6 个 Java Spring Boot skills | ⭐⭐⭐⭐⭐ | 适合 Java/Spring Boot 后端开发，涵盖编码规范、架构模式、安全、TDD、JPA 验证等完整开发生态 |

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

### anthropics-skills
- 无更新

### openai-skills
- 无更新
