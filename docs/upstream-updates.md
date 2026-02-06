# 上游仓库更新记录

最后更新：2026-02-06

---

## 同步状态

| 仓库 | 当前版本 | 同步状态 |
|------|----------|----------|
| everything-claude-code | v1.3.0-7-gc0fdd89 | ✅ 已同步 |
| anthropics-skills | a5bcdd7 | ✅ 已同步 |
| openai-skills | 2f7901e | ✅ 已同步 |
| superpowers | v4.2.0 | ✅ 已同步 |
| obsidian-skills | 34c2cda | ✅ 已同步 (无更新) |
| ai-research-skills | v1.0.0-48-g8bcf5ba | ✅ 已同步 |
| agent-browser | - | ⚠️ 网络问题，待重试 |

---

## 更新历史

| 日期 | 仓库 | 更新内容 | 推荐 | 说明 |
|------|------|----------|------|------|
| 2026-02-06 | everything-claude-code | v1.3.0 大版本更新，9 个新 commits | ⭐⭐⭐⭐⭐ | 新增交互式安装向导、多 Agent 编排、PM2 集群、中文文档、规则重构 |
| 2026-02-06 | anthropics-skills | 2 个新 commits | ⭐⭐⭐ | docx/xlsx/pdf/pptx skills 增强，移除遗留依赖 |
| 2026-02-06 | openai-skills | 14 个新 commits | ⭐⭐⭐⭐ | 新增安全最佳实践、威胁建模、所有权地图、实验性 wrapped skill |
| 2026-02-06 | superpowers | v4.2.0，16 个新 commits | ⭐⭐⭐⭐⭐ | Windows 修复、Codex 原生技能发现、worktree 要求、安装简化 |
| 2026-02-06 | ai-research-skills | v1.1.1，12 个新 commits | ⭐⭐⭐⭐ | llama.cpp 层级量化实验 demo、Windows 安装修复、OIDC 发布 |
| 2026-02-06 | obsidian-skills | 无更新 | - | 保持同步 |

---

## 详情

### everything-claude-code (2026-02-06)

**Tag:** v1.3.0

**核心更新：**

| 类型 | 内容 | 推荐 |
|------|------|------|
| **交互式安装** | `configure-ecc` skill | ⭐⭐⭐⭐⭐ |
| **多 Agent 编排** | `multi-*` 系列命令 (plan/execute/workflow/frontend/backend) | ⭐⭐⭐⭐⭐ |
| **PM2 集群** | `pm2.md` 命令 | ⭐⭐⭐⭐ |
| **会话管理** | `sessions.md` 命令 | ⭐⭐⭐⭐ |
| **规则重构** | `rules/` 分为 common/python/golang/typescript | ⭐⭐⭐⭐ |
| **中文文档** | 全文档中文翻译 | ⭐⭐⭐ |

**新增 Commands：**

| Command | 说明 | 适用场景 |
|---------|------|----------|
| `multi-plan` | 多模型协作规划，调用 Codex/Gemini 分析和规划 | 复杂项目规划 |
| `multi-execute` | 多模型协作执行 | 大规模功能开发 |
| `multi-workflow` | 完整多模型工作流 | 端到端开发 |
| `multi-frontend` | 前端专用多模型工作流 | 前端项目 |
| `multi-backend` | 后端专用多模型工作流 | 后端项目 |
| `pm2` | PM2 进程管理集群 | 生产部署 |
| `sessions` | 会话历史管理 | 会话回溯 |

**新增 Skills：**

| Skill | 说明 |
|-------|------|
| `configure-ecc` | 交互式安装向导，引导选择性安装 skills/rules |

**Rules 重构：**

```
rules/
├── common/          # 通用规则 (agents.md, coding-style.md, git-workflow.md, hooks.md, patterns.md, performance.md, security.md, testing.md)
├── python/          # Python 专用规则
├── golang/          # Go 专用规则
└── typescript/      # TypeScript 专用规则
```

**文档更新：**
- 全中文文档翻译
- 增强 CONTRIBUTING.md 模板
- 新增 GitHub Sponsors 支持

---

### anthropics-skills (2026-02-06)

**更新内容：**

| Commit | 说明 |
|--------|------|
| `#331` | 移除遗留 html2pptx.tgz 依赖 |
| `#330` | 更新 docx, xlsx, pdf, pptx skills |

**改进 Skills：**

| Skill | 改进点 |
|-------|--------|
| `docx` | 文档处理增强 |
| `xlsx` | 表格处理增强 |
| `pdf` | PDF 处理增强 |
| `pptx` | 演示文稿处理增强 |

---

### openai-skills (2026-02-06)

**更新内容：**

| Commit | 说明 | 推荐 |
|--------|------|------|
| `#108` | 移除 atlas (暂时) | - |
| `#83` | 新增安全最佳实践、所有权地图、威胁模型 skills | ⭐⭐⭐⭐⭐ |
| `#79` | 新增实验性 wrapped skill | ⭐⭐⭐ |
| `#78` | 新增 Figma MCP skill (之前已记录) | ⭐⭐⭐⭐ |
| 其他 | 部署脚本修复、skill-installer 更新 | ⭐⭐⭐ |

**新增 Curated Skills：**

| Skill | 说明 | 适用场景 |
|-------|------|----------|
| `security-best-practices` | 安全最佳实践 | 代码安全审查 |
| `ownership-map` | 所有权地图 | 架构分析 |
| `threat-model` | 威胁建模 | 安全设计 |
| `wrapped` | 实验性 wrapped skill | 包装处理 |

---

### superpowers (2026-02-06)

**Tag:** v4.2.0

**核心更新：**

| 更新 | 说明 | 推荐 |
|------|------|------|
| Windows 修复 | 完整 Windows 支持 | ⭐⭐⭐⭐ |
| Codex 原生技能发现 | 简化安装流程 | ⭐⭐⭐⭐⭐ |
| Worktree 要求 | 新增并行开发工作树要求 | ⭐⭐⭐⭐ |
| 安装简化 | 移除 bootstrap CLI、AGENTS.md gatekeeper | ⭐⭐⭐⭐ |

**重要 Commits：**

| Commit | 说明 |
|--------|------|
| `#331` | 修复 Windows hook 执行 (Claude Code 2.1.x) |
| `#382` | 新增 subagent worktree 要求 |
| `#361` | Codex bootstrap 支持 subagent 协作 |

**安全改进：**
- 主分支 red flag 警告（禁止直接在 main 开发）
- Worktree 要求确保并行开发配置正确

---

### ai-research-skills (2026-02-06)

**Tag:** v1.1.1

**核心更新：**

| 更新 | 说明 | 推荐 |
|------|------|------|
| llama.cpp demo | 新增层级量化实验 demo | ⭐⭐⭐⭐ |
| Windows 修复 | 修复安装问题 | ⭐⭐⭐ |
| OIDC 发布 | 切换到可信发布 | ⭐⭐⭐ |
| Bug 修复 | Agents 选择框显示问题 | ⭐⭐⭐ |

**新增 Demo：**

| Demo | 说明 |
|------|------|
| `llama-cpp-layer-wise-quantization` | llama.cpp 层级量化实验 |

---

### obsidian-skills (2026-02-06)

**状态:** 无更新，保持同步

---

### agent-browser (2026-02-06)

**状态:** ⚠️ 网络问题，clone 失败，待重试

---

## 推荐迁移清单

### 高优先级 (⭐⭐⭐⭐⭐)

| 项目 | 路径 | 说明 |
|------|------|------|
| 多 Agent 编排 | `commands/multi-*.md` | 大规模项目必备 |
| 交互式安装 | `skills/configure-ecc/` | 简化新用户上手 |
| PM2 集群 | `commands/pm2.md` | 生产部署 |
| 会话管理 | `commands/sessions.md` | 会话历史 |
| 规则重构 | `rules/` | 新的组织结构 |
| 安全技能 | `openai-skills` security 相关 | 安全开发 |

### 中优先级 (⭐⭐⭐⭐)

| 项目 | 路径 | 说明 |
|------|------|------|
| superpowers v4.2.0 | `upstream/superpowers/` | Codex 原生支持 |
| 文档处理增强 | `anthropics-skills/` docx/xlsx/pdf/pptx | 文档操作 |
| llama.cpp demo | `ai-research-skills/` | 量化实验 |

### 低优先级 (⭐⭐⭐)

| 项目 | 路径 | 说明 |
|------|------|------|
| 中文文档 | `everything-claude-code/docs/` | 中文用户参考 |
| GitHub Sponsors | - | 赞助支持 |

---

## 迁移建议

1. **规则重构** - 新的 common/python/golang/typescript 分类更清晰，建议迁移
2. **多 Agent 编排** - 如果需要大规模并行开发，强烈推荐
3. **superpowers v4.2.0** - 如果使用 Codex，务必升级以获得原生技能发现
4. **configure-ecc** - 可作为 install.sh 的替代方案，提供交互式选择
