#!/usr/bin/env python3
"""
Instinct CLI - 管理 Continuous Learning v2 的 instincts

命令：
  status   - 显示所有 instincts 及其状态
  import   - 从文件或 URL 导入 instincts
  export   - 导出 instincts 到文件
  evolve   - 将 instincts 聚类为 skills/commands/agents
"""

import argparse
import sys
import re
import urllib.request
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ─────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────

HOMUNCULUS_DIR = Path.home() / ".claude" / "homunculus"
INSTINCTS_DIR = HOMUNCULUS_DIR / "instincts"
PERSONAL_DIR = INSTINCTS_DIR / "personal"
INHERITED_DIR = INSTINCTS_DIR / "inherited"
EVOLVED_DIR = HOMUNCULUS_DIR / "evolved"
OBSERVATIONS_FILE = HOMUNCULUS_DIR / "observations.jsonl"

# 确保目录存在
for d in [
    PERSONAL_DIR,
    INHERITED_DIR,
    EVOLVED_DIR / "skills",
    EVOLVED_DIR / "commands",
    EVOLVED_DIR / "agents",
]:
    d.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────
# Instinct 解析器
# ─────────────────────────────────────────────


def parse_instinct_file(content: str) -> list[dict]:
    """解析类似 YAML 的 instinct 文件格式。"""
    instincts = []
    current = {}
    in_frontmatter = False
    content_lines = []

    for line in content.split("\n"):
        if line.strip() == "---":
            if in_frontmatter:
                # Frontmatter 结束
                in_frontmatter = False
                if current:
                    current["content"] = "\n".join(content_lines).strip()
                    instincts.append(current)
                    current = {}
                    content_lines = []
            else:
                # Frontmatter 开始
                in_frontmatter = True
                if current:
                    current["content"] = "\n".join(content_lines).strip()
                    instincts.append(current)
                current = {}
                content_lines = []
        elif in_frontmatter:
            # 解析类似 YAML 的 frontmatter
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key == "confidence":
                    current[key] = float(value)
                else:
                    current[key] = value
        else:
            content_lines.append(line)

    # 不要忘记最后一个 instinct
    if current:
        current["content"] = "\n".join(content_lines).strip()
        instincts.append(current)

    return [i for i in instincts if i.get("id")]


def load_all_instincts() -> list[dict]:
    """从 personal 和 inherited 目录加载所有 instincts。"""
    instincts = []

    for directory in [PERSONAL_DIR, INHERITED_DIR]:
        if not directory.exists():
            continue
        for file in directory.glob("*.yaml"):
            try:
                content = file.read_text()
                parsed = parse_instinct_file(content)
                for inst in parsed:
                    inst["_source_file"] = str(file)
                    inst["_source_type"] = directory.name
                instincts.extend(parsed)
            except Exception as e:
                print(f"Warning: Failed to parse {file}: {e}", file=sys.stderr)

    return instincts


# ─────────────────────────────────────────────
# Status 命令
# ─────────────────────────────────────────────


def cmd_status(args):
    """显示所有 instincts 的状态。"""
    instincts = load_all_instincts()

    if not instincts:
        print("No instincts found.")
        print(f"\nInstinct directories:")
        print(f"  Personal:  {PERSONAL_DIR}")
        print(f"  Inherited: {INHERITED_DIR}")
        return

    # 按领域分组
    by_domain = defaultdict(list)
    for inst in instincts:
        domain = inst.get("domain", "general")
        by_domain[domain].append(inst)

    # 打印标题
    print(f"\n{'=' * 60}")
    print(f"  INSTINCT STATUS - {len(instincts)} total")
    print(f"{'=' * 60}\n")

    # 按来源汇总
    personal = [i for i in instincts if i.get("_source_type") == "personal"]
    inherited = [i for i in instincts if i.get("_source_type") == "inherited"]
    print(f"  Personal:  {len(personal)}")
    print(f"  Inherited: {len(inherited)}")
    print()

    # 按领域打印
    for domain in sorted(by_domain.keys()):
        domain_instincts = by_domain[domain]
        print(f"## {domain.upper()} ({len(domain_instincts)})")
        print()

        for inst in sorted(domain_instincts, key=lambda x: -x.get("confidence", 0.5)):
            conf = inst.get("confidence", 0.5)
            conf_bar = "█" * int(conf * 10) + "░" * (10 - int(conf * 10))
            trigger = inst.get("trigger", "unknown trigger")
            source = inst.get("source", "unknown")

            print(f"  {conf_bar} {int(conf * 100):3d}%  {inst.get('id', 'unnamed')}")
            print(f"            trigger: {trigger}")

            # 从内容中提取 action
            content = inst.get("content", "")
            action_match = re.search(
                r"## Action\s*\n\s*(.+?)(?:\n\n|\n##|$)", content, re.DOTALL
            )
            if action_match:
                action = action_match.group(1).strip().split("\n")[0]
                print(
                    f"            action: {action[:60]}{'...' if len(action) > 60 else ''}"
                )

            print()

    # 观察统计
    if OBSERVATIONS_FILE.exists():
        obs_count = sum(1 for _ in open(OBSERVATIONS_FILE))
        print(f"─────────────────────────────────────────────────────────")
        print(f"  Observations: {obs_count} events logged")
        print(f"  File: {OBSERVATIONS_FILE}")

    print(f"\n{'=' * 60}\n")


# ─────────────────────────────────────────────
# Import 命令
# ─────────────────────────────────────────────


def cmd_import(args):
    """从文件或 URL 导入 instincts。"""
    source = args.source

    # 获取内容
    if source.startswith("http://") or source.startswith("https://"):
        print(f"Fetching from URL: {source}")
        try:
            with urllib.request.urlopen(source) as response:
                content = response.read().decode("utf-8")
        except Exception as e:
            print(f"Error fetching URL: {e}", file=sys.stderr)
            return 1
    else:
        path = Path(source).expanduser()
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            return 1
        content = path.read_text()

    # 解析 instincts
    new_instincts = parse_instinct_file(content)
    if not new_instincts:
        print("No valid instincts found in source.")
        return 1

    print(f"\nFound {len(new_instincts)} instincts to import.\n")

    # 加载现有的
    existing = load_all_instincts()
    existing_ids = {i.get("id") for i in existing}

    # 分类
    to_add = []
    duplicates = []
    to_update = []

    for inst in new_instincts:
        inst_id = inst.get("id")
        if inst_id in existing_ids:
            # 检查是否需要更新
            existing_inst = next((e for e in existing if e.get("id") == inst_id), None)
            if existing_inst:
                if inst.get("confidence", 0) > existing_inst.get("confidence", 0):
                    to_update.append(inst)
                else:
                    duplicates.append(inst)
        else:
            to_add.append(inst)

    # 按最小置信度过滤
    min_conf = args.min_confidence or 0.0
    to_add = [i for i in to_add if i.get("confidence", 0.5) >= min_conf]
    to_update = [i for i in to_update if i.get("confidence", 0.5) >= min_conf]

    # 显示汇总
    if to_add:
        print(f"NEW ({len(to_add)}):")
        for inst in to_add:
            print(
                f"  + {inst.get('id')} (confidence: {inst.get('confidence', 0.5):.2f})"
            )

    if to_update:
        print(f"\nUPDATE ({len(to_update)}):")
        for inst in to_update:
            print(
                f"  ~ {inst.get('id')} (confidence: {inst.get('confidence', 0.5):.2f})"
            )

    if duplicates:
        print(
            f"\nSKIP ({len(duplicates)} - already exists with equal/higher confidence):"
        )
        for inst in duplicates[:5]:
            print(f"  - {inst.get('id')}")
        if len(duplicates) > 5:
            print(f"  ... and {len(duplicates) - 5} more")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return 0

    if not to_add and not to_update:
        print("\nNothing to import.")
        return 0

    # 确认
    if not args.force:
        response = input(f"\nImport {len(to_add)} new, update {len(to_update)}? [y/N] ")
        if response.lower() != "y":
            print("Cancelled.")
            return 0

    # 写入 inherited 目录
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    source_name = Path(source).stem if not source.startswith("http") else "web-import"
    output_file = INHERITED_DIR / f"{source_name}-{timestamp}.yaml"

    all_to_write = to_add + to_update
    output_content = (
        f"# Imported from {source}\n# Date: {datetime.now().isoformat()}\n\n"
    )

    for inst in all_to_write:
        output_content += "---\n"
        output_content += f"id: {inst.get('id')}\n"
        output_content += f'trigger: "{inst.get("trigger", "unknown")}"\n'
        output_content += f"confidence: {inst.get('confidence', 0.5)}\n"
        output_content += f"domain: {inst.get('domain', 'general')}\n"
        output_content += f"source: inherited\n"
        output_content += f'imported_from: "{source}"\n'
        if inst.get("source_repo"):
            output_content += f"source_repo: {inst.get('source_repo')}\n"
        output_content += "---\n\n"
        output_content += inst.get("content", "") + "\n\n"

    output_file.write_text(output_content)

    print(f"\n Import complete!")
    print(f"   Added: {len(to_add)}")
    print(f"   Updated: {len(to_update)}")
    print(f"   Saved to: {output_file}")

    return 0


# ─────────────────────────────────────────────
# Export 命令
# ─────────────────────────────────────────────


def cmd_export(args):
    """导出 instincts 到文件。"""
    instincts = load_all_instincts()

    if not instincts:
        print("No instincts to export.")
        return 1

    # 按领域过滤
    if args.domain:
        instincts = [i for i in instincts if i.get("domain") == args.domain]

    # 按最小置信度过滤
    if args.min_confidence:
        instincts = [
            i for i in instincts if i.get("confidence", 0.5) >= args.min_confidence
        ]

    if not instincts:
        print("No instincts match the criteria.")
        return 1

    # 生成输出
    output = f"# Instincts export\n# Date: {datetime.now().isoformat()}\n# Total: {len(instincts)}\n\n"

    for inst in instincts:
        output += "---\n"
        for key in ["id", "trigger", "confidence", "domain", "source", "source_repo"]:
            if inst.get(key):
                value = inst[key]
                if key == "trigger":
                    output += f'{key}: "{value}"\n'
                else:
                    output += f"{key}: {value}\n"
        output += "---\n\n"
        output += inst.get("content", "") + "\n\n"

    # 写入文件或 stdout
    if args.output:
        Path(args.output).write_text(output)
        print(f"Exported {len(instincts)} instincts to {args.output}")
    else:
        print(output)

    return 0


# ─────────────────────────────────────────────
# Evolve 命令
# ─────────────────────────────────────────────


def cmd_evolve(args):
    """分析 instincts 并建议演化到 skills/commands/agents。"""
    instincts = load_all_instincts()

    if len(instincts) < 3:
        print("Need at least 3 instincts to analyze patterns.")
        print(f"Currently have: {len(instincts)}")
        return 1

    print(f"\n{'=' * 60}")
    print(f"  EVOLVE ANALYSIS - {len(instincts)} instincts")
    print(f"{'=' * 60}\n")

    # 按领域分组
    by_domain = defaultdict(list)
    for inst in instincts:
        domain = inst.get("domain", "general")
        by_domain[domain].append(inst)

    # 按领域的高置信度 instincts（skill 候选）
    high_conf = [i for i in instincts if i.get("confidence", 0) >= 0.8]
    print(f"High confidence instincts (>=80%): {len(high_conf)}")

    # 找到聚类（具有相似 triggers 的 instincts）
    trigger_clusters = defaultdict(list)
    for inst in instincts:
        trigger = inst.get("trigger", "")
        # 标准化 trigger
        trigger_key = trigger.lower()
        for keyword in [
            "when",
            "creating",
            "writing",
            "adding",
            "implementing",
            "testing",
        ]:
            trigger_key = trigger_key.replace(keyword, "").strip()
        trigger_clusters[trigger_key].append(inst)

    # 找到有 3+ instincts 的聚类（好的 skill 候选）
    skill_candidates = []
    for trigger, cluster in trigger_clusters.items():
        if len(cluster) >= 2:
            avg_conf = sum(i.get("confidence", 0.5) for i in cluster) / len(cluster)
            skill_candidates.append(
                {
                    "trigger": trigger,
                    "instincts": cluster,
                    "avg_confidence": avg_conf,
                    "domains": list(set(i.get("domain", "general") for i in cluster)),
                }
            )

    # 按聚类大小和置信度排序
    skill_candidates.sort(key=lambda x: (-len(x["instincts"]), -x["avg_confidence"]))

    print(f"\nPotential skill clusters found: {len(skill_candidates)}")

    if skill_candidates:
        print(f"\n## SKILL CANDIDATES\n")
        for i, cand in enumerate(skill_candidates[:5], 1):
            print(f'{i}. Cluster: "{cand["trigger"]}"')
            print(f"   Instincts: {len(cand['instincts'])}")
            print(f"   Avg confidence: {cand['avg_confidence']:.0%}")
            print(f"   Domains: {', '.join(cand['domains'])}")
            print(f"   Instincts:")
            for inst in cand["instincts"][:3]:
                print(f"     - {inst.get('id')}")
            print()

    # Command 候选（具有高置信度的工作流 instincts）
    workflow_instincts = [
        i
        for i in instincts
        if i.get("domain") == "workflow" and i.get("confidence", 0) >= 0.7
    ]
    if workflow_instincts:
        print(f"\n## COMMAND CANDIDATES ({len(workflow_instincts)})\n")
        for inst in workflow_instincts[:5]:
            trigger = inst.get("trigger", "unknown")
            # 建议命令名称
            cmd_name = (
                trigger.replace("when ", "")
                .replace("implementing ", "")
                .replace("a ", "")
            )
            cmd_name = cmd_name.replace(" ", "-")[:20]
            print(f"  /{cmd_name}")
            print(f"    From: {inst.get('id')}")
            print(f"    Confidence: {inst.get('confidence', 0.5):.0%}")
            print()

    # Agent 候选（复杂多步模式）
    agent_candidates = [
        c
        for c in skill_candidates
        if len(c["instincts"]) >= 3 and c["avg_confidence"] >= 0.75
    ]
    if agent_candidates:
        print(f"\n## AGENT CANDIDATES ({len(agent_candidates)})\n")
        for cand in agent_candidates[:3]:
            agent_name = cand["trigger"].replace(" ", "-")[:20] + "-agent"
            print(f"  {agent_name}")
            print(f"    Covers {len(cand['instincts'])} instincts")
            print(f"    Avg confidence: {cand['avg_confidence']:.0%}")
            print()

    if args.generate:
        print("\n[Would generate evolved structures here]")
        print("  Skills would be saved to:", EVOLVED_DIR / "skills")
        print("  Commands would be saved to:", EVOLVED_DIR / "commands")
        print("  Agents would be saved to:", EVOLVED_DIR / "agents")

    print(f"\n{'=' * 60}\n")
    return 0


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Instinct CLI for Continuous Learning v2"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status
    status_parser = subparsers.add_parser("status", help="Show instinct status")

    # Import
    import_parser = subparsers.add_parser("import", help="Import instincts")
    import_parser.add_argument("source", help="File path or URL")
    import_parser.add_argument(
        "--dry-run", action="store_true", help="Preview without importing"
    )
    import_parser.add_argument("--force", action="store_true", help="Skip confirmation")
    import_parser.add_argument(
        "--min-confidence", type=float, help="Minimum confidence threshold"
    )

    # Export
    export_parser = subparsers.add_parser("export", help="Export instincts")
    export_parser.add_argument("--output", "-o", help="Output file")
    export_parser.add_argument("--domain", help="Filter by domain")
    export_parser.add_argument(
        "--min-confidence", type=float, help="Minimum confidence"
    )

    # Evolve
    evolve_parser = subparsers.add_parser("evolve", help="Analyze and evolve instincts")
    evolve_parser.add_argument(
        "--generate", action="store_true", help="Generate evolved structures"
    )

    args = parser.parse_args()

    if args.command == "status":
        return cmd_status(args)
    elif args.command == "import":
        return cmd_import(args)
    elif args.command == "export":
        return cmd_export(args)
    elif args.command == "evolve":
        return cmd_evolve(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
