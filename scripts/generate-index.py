#!/usr/bin/env python3
"""
INDEX.md 自动生成脚本（重构版）

扫描项目中的 Markdown 文件，读取 frontmatter，
按新的目录结构自动生成 INDEX.md。

支持目录：
- docs/getting-started, docs/concepts, docs/platforms
- docs/prompts, docs/skills, docs/tools, docs/workflows
- docs/patterns, docs/playbooks, docs/case-studies
- verification/ (reports, changelog)
- benchmarks/
- assets/, examples/

使用方法：
    python3 scripts/generate-index.py          # 生成 INDEX.md
    python3 scripts/generate-index.py --check  # 检查 INDEX.md 是否最新（CI 用）
    python3 scripts/generate-index.py --check-links  # 检查链接完整性

依赖：Python 3.8+（标准库）
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
VERIFICATION_DIR = PROJECT_ROOT / "verification"
BENCHMARKS_DIR = PROJECT_ROOT / "benchmarks"
VISUALIZATION_DIR = PROJECT_ROOT / "visualization"
INDEX_FILE = PROJECT_ROOT / "INDEX.md"

# 分类映射（按展示顺序排列）
CATEGORY_MAP = {
    "getting-started": ("一、入门指南 (Getting Started)", "入门"),
    "concepts": ("二、核心概念 (Concepts)", "概念"),
    "platforms": ("三、API 平台 (Platforms)", "平台"),
    "prompts": ("四、提示词资源 (Prompts)", "提示词"),
    "skills": ("五、Skills 资源 (Skills)", "技能"),
    "tools": ("六、工具与框架 (Tools)", "工具"),
    "workflows": ("七、流程化指南 (Workflows)", "流程"),
    "patterns": ("八、设计模式 (Patterns)", "模式"),
    "playbooks": ("九、实战手册 (Playbooks)", "实战"),
    "case-studies": ("十、案例研究 (Case Studies)", "案例"),
}

# 证据等级标记
EVIDENCE_MARKERS = {
    "L0": "🟢",
    "L1": "🔵",
    "L2": "🟡",
    "L3": "🟠",
    "L4": "🔴",
}

# 评级标记
RATING_MARKERS = {
    "A": "✅",
    "B": "🔍",
    "C": "📋",
    "D": "⏳",
}


def parse_frontmatter(content: str) -> dict:
    """解析 Markdown 文件的 YAML frontmatter。"""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).strip().split('\n'):
        colon_index = line.find(':')
        if colon_index > 0:
            key = line[:colon_index].strip()
            value = line[colon_index + 1:].strip().strip('"').strip("'")
            frontmatter[key] = value

    return frontmatter


def get_evidence_marker(frontmatter: dict) -> str:
    """获取证据等级标记。"""
    level = frontmatter.get('evidence_level', '')
    if level in EVIDENCE_MARKERS:
        return f"{EVIDENCE_MARKERS[level]} {level}"
    if frontmatter.get('verification', '').lower() in ('true', 'yes'):
        return "✅"
    return "⏳"


def get_rating_marker(frontmatter: dict) -> str:
    """获取评级标记。"""
    rating = frontmatter.get('rating', '')
    if rating in RATING_MARKERS:
        return f"{RATING_MARKERS[rating]} {rating}"
    return "-"


def scan_directory(base_dir: Path, valid_categories: list = None) -> list:
    """扫描目录下的所有 Markdown 文件。"""
    entries = []

    if not base_dir.exists():
        return entries

    for filepath in sorted(base_dir.rglob("*.md")):
        if filepath.name == "README.md" and filepath.parent != base_dir:
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter = parse_frontmatter(content)
        rel_path = filepath.relative_to(PROJECT_ROOT)

        title = frontmatter.get('title', '')
        if not title:
            title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
            title = title_match.group(1) if title_match else filepath.stem

        category_dir = filepath.parent.name
        category = frontmatter.get('category', category_dir)

        if valid_categories and category not in valid_categories:
            category = category_dir

        entries.append({
            'title': title,
            'file': str(rel_path),
            'category': category,
            'evidence': get_evidence_marker(frontmatter),
            'rating': get_rating_marker(frontmatter),
            'updated': frontmatter.get('updated', '-'),
            'frontmatter': frontmatter,
        })

    return entries


def generate_category_table(entries: list, cat_key: str, cat_title: str, cat_type: str) -> tuple:
    """生成某个分类的 markdown 表格。"""
    lines = []
    lines.append(f"## {cat_title}\n")
    lines.append("| 文档 | 分类 | 证据等级 | 评级 | 最后更新 |")
    lines.append("|------|------|---------|------|---------|")

    matched = [e for e in entries if e['category'] == cat_key]
    for entry in matched:
        lines.append(
            f"| [{entry['title']}]({entry['file']}) "
            f"| {cat_type} "
            f"| {entry['evidence']} "
            f"| {entry['rating']} "
            f"| {entry['updated']} |"
        )
    lines.append("")
    return '\n'.join(lines), len(matched)


def generate_verification_section() -> str:
    """生成验真中心部分。"""
    lines = []
    lines.append("## 十一、验真中心 (Verification)\n")

    # 验真报告
    lines.append("### 验真报告\n")
    lines.append("| 报告 | 类型 | 证据等级 | 评级 | 验真日期 |")
    lines.append("|------|------|---------|------|---------|")

    reports_dir = VERIFICATION_DIR / "reports"
    if reports_dir.exists():
        for filepath in sorted(reports_dir.rglob("*.md")):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            frontmatter = parse_frontmatter(content)
            rel_path = filepath.relative_to(PROJECT_ROOT)

            title = frontmatter.get('title', filepath.stem)
            report_type = filepath.parent.name
            evidence = get_evidence_marker(frontmatter)
            rating = get_rating_marker(frontmatter)
            verified_date = frontmatter.get('verified_date', '-')

            lines.append(
                f"| [{title}]({rel_path}) "
                f"| {report_type} "
                f"| {evidence} "
                f"| {rating} "
                f"| {verified_date} |"
            )
    lines.append("")

    # 变更日志
    lines.append("### 变更日志\n")
    changelog_dir = VERIFICATION_DIR / "changelog"
    if changelog_dir.exists():
        for filepath in sorted(changelog_dir.glob("*.md")):
            rel_path = filepath.relative_to(PROJECT_ROOT)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            frontmatter = parse_frontmatter(content)
            title = frontmatter.get('title', filepath.stem)
            lines.append(f"- [{title}]({rel_path})")
    lines.append("")

    # 验真模板
    lines.append("### 验真模板\n")
    template_entries = [
        ("提示词验真模板", "verification/prompts/template.md"),
        ("平台信息验真模板", "verification/platforms/template.md"),
        ("Skills 验真模板", "verification/skills/template.md"),
    ]
    for title, path in template_entries:
        if (PROJECT_ROOT / path).exists():
            lines.append(f"- [{title}]({path})")
    lines.append("")

    return '\n'.join(lines)


def generate_benchmarks_section() -> str:
    """生成基准测试部分。"""
    lines = []
    lines.append("## 十二、基准测试 (Benchmarks)\n")

    benchmark_entries = [
        ("提示词评估", "benchmarks/prompt-evals/README.md", "Prompt Evals"),
        ("Skills 测试", "benchmarks/skill-tests/README.md", "Skill Tests"),
        ("工作流评估", "benchmarks/workflow-evals/README.md", "Workflow Evals"),
        ("测试报告", "benchmarks/reports/README.md", "Reports"),
    ]

    lines.append("| 名称 | 说明 | 路径 |")
    lines.append("|------|------|------|")
    for title, path, desc in benchmark_entries:
        if (PROJECT_ROOT / path).exists():
            lines.append(f"| [{title}]({path}) | {desc} | {path} |")
    lines.append("")

    return '\n'.join(lines)


def generate_visualization_section() -> str:
    """生成可视化部分。"""
    lines = []
    lines.append("## 十三、可视化 (Visualization)\n")
    lines.append("| 名称 | 类型 | 说明 |")
    lines.append("|------|------|------|")

    viz_entries = [
        ("知识图谱", "visualization/index.html", "HTML", "概念关系图谱总入口"),
        ("Dashboard", "visualization/dashboard.html", "HTML", "验真状态仪表盘"),
        ("知识图谱（增强版）", "visualization/graph.html", "HTML", "增强版知识图谱"),
    ]
    for title, path, dtype, desc in viz_entries:
        if (PROJECT_ROOT / path).exists():
            lines.append(f"| [{title}]({path}) | {dtype} | {desc} |")
    lines.append("")

    return '\n'.join(lines)


def generate_assets_examples_section() -> str:
    """生成资源与示例部分。"""
    lines = []
    lines.append("## 十四、资源与示例\n")

    for dir_name, label in [("assets", "资源文件"), ("examples", "示例代码")]:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            files = list(dir_path.rglob("*"))
            md_files = [f for f in files if f.suffix == '.md' and f.name != 'README.md']
            if md_files:
                lines.append(f"### {label}\n")
                for filepath in sorted(md_files):
                    rel_path = filepath.relative_to(PROJECT_ROOT)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    frontmatter = parse_frontmatter(content)
                    title = frontmatter.get('title', filepath.stem)
                    lines.append(f"- [{title}]({rel_path})")
                lines.append("")
            else:
                lines.append(f"### {label}\n")
                lines.append(f"目录 `{dir_name}/` 存在，暂无 Markdown 文件。\n")

    return '\n'.join(lines)


def check_links() -> bool:
    """检查所有文档中的断裂引用。"""
    all_dirs = [DOCS_DIR, VERIFICATION_DIR, BENCHMARKS_DIR]
    entries = []
    for scan_dir in all_dirs:
        if scan_dir.exists():
            for filepath in scan_dir.rglob("*.md"):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                frontmatter = parse_frontmatter(content)
                entries.append({
                    'file': filepath,
                    'frontmatter': frontmatter,
                })

    has_errors = False
    for entry in entries:
        filepath = entry['file']
        frontmatter = entry['frontmatter']

        for field in ['related', 'depends_on']:
            raw = frontmatter.get(field, '')
            if not raw:
                continue
            refs = re.findall(r'- (.+)', raw)
            for ref in refs:
                ref = ref.strip()
                if not ref:
                    continue
                ref_dir = filepath.parent
                ref_path = os.path.normpath(os.path.join(ref_dir, ref))
                if not os.path.exists(ref_path):
                    rel = filepath.relative_to(PROJECT_ROOT)
                    print(f"❌ {rel}: {field} -> '{ref}' (文件不存在)")
                    has_errors = True

    if not has_errors:
        print("✅ 所有引用链接有效")
    return has_errors


def generate_index() -> str:
    """生成完整的 INDEX.md 内容。"""
    lines = []
    lines.append("# 📇 总索引\n")
    lines.append("> 本索引按知识领域分类，标注了每篇文档的证据等级和评级。")
    lines.append("> 证据等级：🟢 L0 官方验证 · 🔵 L1 实际验证 · 🟡 L2 交叉验证 · 🟠 L3 理论推导 · 🔴 L4 待验证")
    lines.append(f"> 最后自动生成：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append("---\n")

    # 扫描 docs
    all_entries = scan_directory(DOCS_DIR)

    # 文档分类
    for cat_key, (cat_title, cat_type) in CATEGORY_MAP.items():
        table_text, count = generate_category_table(all_entries, cat_key, cat_title, cat_type)
        if count > 0:
            lines.append(table_text)

    # 验真中心
    lines.append(generate_verification_section())

    # 基准测试
    lines.append(generate_benchmarks_section())

    # 可视化
    lines.append(generate_visualization_section())

    # 资源与示例
    lines.append(generate_assets_examples_section())

    return '\n'.join(lines)


def main():
    if "--check-links" in sys.argv:
        return 1 if check_links() else 0

    index_content = generate_index()

    if "--check" in sys.argv:
        if INDEX_FILE.exists():
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                existing = f.read()
            if index_content == existing:
                print("✅ INDEX.md 是最新的")
                return 0
            else:
                print("❌ INDEX.md 已过时，请运行 python3 scripts/generate-index.py 更新")
                return 1
        else:
            print("❌ INDEX.md 不存在")
            return 1

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(index_content)

    print(f"✅ INDEX.md 已更新")
    return 0


if __name__ == "__main__":
    sys.exit(main())
