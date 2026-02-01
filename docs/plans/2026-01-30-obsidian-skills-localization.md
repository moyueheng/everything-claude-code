# Obsidian Skills 本地化 实现规划

> **给 Claude：** 必需子技能：使用 executing-plans 来逐个任务实现此规划。

**目标：** 将 `upstream/obsidian-skills` 中的所有 Skill 复制到 `my/claudecode/skills/` 与 `my/codex/skills/`，并将内容翻译为中文（保留专有名词与技术名词），形成可安装的本地化版本。

**架构：** 以“上游只读、my 可改造”为原则，逐个 Skill 目录复制到 `my` 对应位置后再本地化 `SKILL.md` 及相关说明文件。翻译时保持原有结构与代码示例，确保 Codex/Claude Code 可以直接安装与使用。

**技术栈：** shell 文件操作、Markdown 文档编辑、`install.sh` 安装脚本

---

### 任务 1: 盘点上游 Obsidian Skills

**文件：**
- 读取: `upstream/obsidian-skills/skills/*/SKILL.md`
- 记录清单: `docs/plans/2026-01-30-obsidian-skills-localization.md`

**步骤 1: 列出上游 Skill 目录**

运行: `ls upstream/obsidian-skills/skills`
预期: 列出所有技能目录名称

**步骤 2: 确认每个 Skill 的文件结构**

运行: `find upstream/obsidian-skills/skills -maxdepth 2 -type f`
预期: 列出每个 Skill 目录中的文件

**步骤 3: 记录清单**

在本规划中记录每个 Skill 名称及包含的文件（例如 `SKILL.md`、`references/` 等）

---

### 任务 2: 复制到 `my/claudecode/skills/` 并中文化

**文件：**
- 创建: `my/claudecode/skills/<skill-name>/...`
- 修改: `my/claudecode/skills/<skill-name>/SKILL.md`

**步骤 1: 复制目录**

运行: `cp -R upstream/obsidian-skills/skills/<skill-name> my/claudecode/skills/<skill-name>`
预期: 对应目录完整复制

**步骤 2: 中文化 `SKILL.md`**

- 保留 YAML 头部字段名与结构
- 翻译标题、说明文字、步骤描述
- 保留专有名词（例如 Obsidian、JSON Canvas）与代码块

**步骤 3: 若存在 references/assets/scripts**

- 翻译说明性 Markdown
- 保持代码与配置文件原样

---

### 任务 3: 复制到 `my/codex/skills/` 并中文化

**文件：**
- 创建: `my/codex/skills/<skill-name>/...`
- 修改: `my/codex/skills/<skill-name>/SKILL.md`

**步骤 1: 复制目录**

运行: `cp -R upstream/obsidian-skills/skills/<skill-name> my/codex/skills/<skill-name>`
预期: 对应目录完整复制

**步骤 2: 中文化 `SKILL.md`**

- 保持与 Claude Code 版本一致的翻译风格
- 保持结构、代码块与示例

---

### 任务 4: 安装验证

**文件：**
- 修改: `install.sh`（如需要）

**步骤 1: 运行安装脚本**

运行: `./install.sh`
预期: Codex 与 Claude Code 的 skills 目录包含新加入的 Obsidian skills

**步骤 2: 验证安装输出**

确认输出中包含 `obsidian-skills` 对应的 skill 目录

---

### 任务 5: 提交变更

**步骤 1: 查看变更**

运行: `git status -sb`
预期: `my/claudecode/skills/<skill-name>` 与 `my/codex/skills/<skill-name>` 新增

**步骤 2: 提交**

运行:
```bash
git add my/claudecode/skills my/codex/skills
git commit -m "feat: add obsidian skills (zh)"
```

---

## 上游清单（待补充）

- obsidian-markdown
- obsidian-bases
- json-canvas
