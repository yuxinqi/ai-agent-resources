#!/usr/bin/env python3
"""
INDEX.md 自动生成脚本

扫描 docs/ 目录下的所有 Markdown 文件，读取 frontmatter，
自动生成更新后的 INDEX.md。

使用方法：
    python3 scripts/generate-index.py          # 生成 INDEX.md
    python3 scripts/generate-index.py --check  # 检查 INDEX.md 是否最新（CI 用）

依赖：Python 3.6+（标准库）
"""

import os
import re
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
VERIFICATION_DIR = os.path.join(PROJECT_ROOT, "verification")
VISUALIZATION_DIR = os.path.join(PROJECT_ROOT, "visualization")
INDEX_FILE = os.path.join(PROJECT_ROOT, "INDEX.md")

# 分类映射（按展示顺序排列）
CATEGORY_MAP = {
    "concepts": ("一、核心概念 (Concepts)", "基础理论"),
    "platforms": ("二、API 平台申请与使用 (Platforms)", "平台"),
    "prompts": ("三、提示词资源 (Prompts)", "提示词"),
    "skills": ("四、Skills 资源 (Skills)", "技能"),
    "tools": ("五、工具与框架 (Tools)", "工具"),
    "workflows": ("六、流程化指南 (Workflows)", "流程"),
}

VERIFICATION_ENTRIES = [
    ("验真系统说明", "verification/README.md", "方法论", True, "A"),
    ("提示词验真模板", "verification/prompts/template.md", "模板", True, "A"),
    ("平台信息验真模板", "verification/platforms/template.md", "模板", True, "A"),
    ("Skills 验真模板", "verification/skills/template.md", "模板", True, "A"),
    ("OpenAI API 指南验真", "verification/platforms/openai-api-2026-05.md", "验真报告", True, "B"),
    ("Anthropic API 指南验真", "verification/platforms/anthropic-claude-2026-05.md", "验真报告", True, "B"),
]

VISUALIZATION_ENTRIES = [
    ("可视化总入口", "visualization/index.html", "HTML", "概念关系图谱总入口"),
]


def parse_frontmatter(content):
    """解析 Markdown 文件的 YAML frontmatter (仅分割第一个冒号，支持带 : 的值如时间戳)"""
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


def get_verification_status(frontmatter):
    """获取验真状态标记"""
    if frontmatter.get('verification', '').lower() in ('true', 'yes'):
        return "✅"
    return "⏳"


def scan_docs():
    """扫描 docs/ 目录下的所有 Markdown 文件"""
    entries = []
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in sorted(files):
            if not file.endswith('.md'):
                continue

            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, PROJECT_ROOT)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter = parse_frontmatter(content)

            # 从 frontmatter 或文档内容获取标题
            title = frontmatter.get('title', '')
            if not title:
                title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
                title = title_match.group(1) if title_match else file.replace('.md', '')

            # 获取分类
            category_dir = os.path.basename(root)
            category = frontmatter.get('category', category_dir)

            # 获取验真状态
            ver_status = get_verification_status(frontmatter)

            # 获取更新日期
            updated = frontmatter.get('updated', '-')

            entries.append({
                'title': title,
                'file': rel_path,
                'category': category,
                'verification': ver_status,
                'updated': updated,
            })

    return entries


def generate_category_table(entries, cat_key, cat_title, cat_type):
    """生成某个分类的 markdown 表格"""
    lines = []
    lines.append(f"## {cat_title}\n")
    lines.append("| 文档 | 分类 | 验真状态 | 最后更新 |")
    lines.append("|------|------|---------|---------|")

    matched = [e for e in entries if e['category'] == cat_key]
    for entry in matched:
        lines.append(
            f"| [{entry['title']}]({entry['file']}) "
            f"| {cat_type} "
            f"| {entry['verification']} "
            f"| {entry['updated']} |"
        )
    lines.append("")
    return '\n'.join(lines), len(matched)


def generate_index(entries):
    """生成 INDEX.md"""
    lines = []
    lines.append("# 📇 总索引\n")
    lines.append("> 本索引按知识领域分类，标注了每篇文档的验真状态。✅ = 已验真，⏳ = 待验真，⚠️ = 需更新。\n")
    lines.append("> 最后自动生成：{}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
    lines.append("---\n")

    # ---- 文档分类 ----
    for cat_key, (cat_title, cat_type) in CATEGORY_MAP.items():
        table_text, count = generate_category_table(entries, cat_key, cat_title, cat_type)
        lines.append(table_text)

    # ---- 验真中心 ----
    lines.append("## 七、验真中心 (Verification)\n")
    lines.append("| 文档 | 类型 | 验真状态 | 评级 |")
    lines.append("|------|------|---------|------|")
    for title, path, dtype, verified, rating in VERIFICATION_ENTRIES:
        status = "✅" if verified else "⏳"
        lines.append(f"| [{title}]({path}) | {dtype} | {status} | {rating} |")
    lines.append("")

    # ---- 可视化入口 ----
    lines.append("## 八、可视化 (Visualization)\n")
    lines.append("| 文档 | 类型 | 说明 |")
    lines.append("|------|------|------|")
    for title, path, dtype, desc in VISUALIZATION_ENTRIES:
        lines.append(f"| [{title}]({path}) | {dtype} | {desc} |")
    lines.append("")

    return '\n'.join(lines)


def check_links():
    """检查所有文档中的断裂引用（related / depends_on 指向不存在的文件）"""
    entries = scan_docs()
    has_errors = False

    for entry in entries:
        filepath = os.path.join(PROJECT_ROOT, entry['file'])
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter = parse_frontmatter(content)

        for field in ['related', 'depends_on']:
            raw = frontmatter.get(field, '')
            if not raw:
                continue
            # 处理 YAML 列表格式: "- item1\n  - item2"
            refs = re.findall(r'- (.+)', raw)
            for ref in refs:
                ref = ref.strip()
                if not ref:
                    continue
                # 解析相对路径
                ref_dir = os.path.dirname(filepath)
                ref_path = os.path.normpath(os.path.join(ref_dir, ref))
                if not os.path.exists(ref_path):
                    print(f"❌ {entry['file']}: {field} -> '{ref}' (文件不存在)")
                    has_errors = True

    if not has_errors:
        print("✅ 所有引用链接有效")
    return has_errors


def main():
    # 扫描文档
    entries = scan_docs()

    # --check-links 模式：验证链接完整性
    if "--check-links" in sys.argv:
        return 1 if check_links() else 0

    # 生成内容
    index_content = generate_index(entries)

    # --check 模式：验证 INDEX.md 是否最新
    if "--check" in sys.argv:
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                existing = f.read()
            # 忽略第一行的时间戳差异再比较
            if index_content == existing:
                print("✅ INDEX.md 是最新的")
                return 0
            else:
                print("❌ INDEX.md 已过时，请运行 python3 scripts/generate-index.py 更新")
                return 1
        else:
            print("❌ INDEX.md 不存在")
            return 1

    # 写入文件
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(index_content)

    print(f"✅ INDEX.md 已更新 ({len(entries)} 个文档)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

