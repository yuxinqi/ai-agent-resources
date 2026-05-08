#!/usr/bin/env python3
"""
知识图谱数据构建脚本

扫描 docs/, verification/, benchmarks/ 目录下的 Markdown 文件，
读取 frontmatter 中的 related、depends_on、follows 字段，
构建知识图谱的节点和边数据，输出为 JSON 格式。

使用方法：
    python3 scripts/build_graph.py                              # 输出到 visualization/graph-data.json
    python3 scripts/build_graph.py --output custom.json         # 输出到指定文件
    python3 scripts/build_graph.py --include-evidence           # 包含证据等级信息

依赖：Python 3.8+（标准库）
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 默认输出路径
DEFAULT_OUTPUT = PROJECT_ROOT / "visualization" / "graph-data.json"

# 扫描目录
SCAN_DIRS = ["docs", "verification", "benchmarks"]

# 分类颜色映射
CATEGORY_COLORS = {
    "concepts": "#3b82f6",
    "platforms": "#10b981",
    "prompts": "#8b5cf6",
    "skills": "#f59e0b",
    "tools": "#06b6d4",
    "workflows": "#ec4899",
    "getting-started": "#14b8a6",
    "patterns": "#f97316",
    "playbooks": "#a78bfa",
    "case-studies": "#fb923c",
    "verification": "#ef4444",
    "benchmark": "#64748b",
    "changelog": "#94a3b8",
    "template": "#475569",
}

# 边类型颜色
EDGE_COLORS = {
    "depends_on": "#3b82f6",
    "related_to": "#8b5cf6",
    "follows": "#10b981",
    "evolves_to": "#f59e0b",
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


def parse_list_field(value: str) -> list:
    """解析 YAML 列表字段（如 related: [a, b] 或 - a\n- b）。"""
    if not value:
        return []

    # 数组格式 [item1, item2]
    if value.startswith('['):
        items = re.findall(r'[^\[\],\s]+', value)
        return [item.strip() for item in items if item.strip()]

    # YAML 列表格式
    items = re.findall(r'- (.+)', value)
    return [item.strip() for item in items if item.strip()]


def resolve_reference(ref: str, source_file: Path) -> str:
    """将相对路径引用解析为项目根相对路径。"""
    if ref.startswith('/'):
        return ref.lstrip('/')

    resolved = (source_file.parent / ref).resolve()
    try:
        return str(resolved.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(resolved)


def scan_files() -> tuple:
    """扫描所有文件，构建节点和边。"""
    nodes = []
    edges = []
    node_map = {}

    for scan_dir in SCAN_DIRS:
        dir_path = PROJECT_ROOT / scan_dir
        if not dir_path.exists():
            continue

        for filepath in sorted(dir_path.rglob("*.md")):
            rel_path = str(filepath.relative_to(PROJECT_ROOT))

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter = parse_frontmatter(content)

            # 从 frontmatter 或标题获取节点名称
            title = frontmatter.get('title', '')
            if not title:
                title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
                title = title_match.group(1) if title_match else filepath.stem

            category = frontmatter.get('category', filepath.parent.name)
            evidence_level = frontmatter.get('evidence_level', '')
            rating = frontmatter.get('rating', '')

            node_id = rel_path.replace('/', '_').replace('.md', '')

            node = {
                "id": node_id,
                "name": title,
                "path": rel_path,
                "category": category,
                "color": CATEGORY_COLORS.get(category, "#64748b"),
            }

            if evidence_level:
                node["evidence_level"] = evidence_level
            if rating:
                node["rating"] = rating

            nodes.append(node)
            node_map[rel_path] = node_id

            # 解析边
            for field, edge_type in [('depends_on', 'depends_on'), ('related', 'related_to'), ('follows', 'follows')]:
                raw = frontmatter.get(field, '')
                refs = parse_list_field(raw)
                for ref in refs:
                    target_path = resolve_reference(ref, filepath)
                    edges.append({
                        "source": node_id,
                        "target_path": target_path,
                        "type": edge_type,
                        "color": EDGE_COLORS.get(edge_type, "#64748b"),
                    })

    # 解析边目标
    resolved_edges = []
    for edge in edges:
        target_id = node_map.get(edge["target_path"])
        if target_id:
            resolved_edges.append({
                "source": edge["source"],
                "target": target_id,
                "type": edge["type"],
                "color": edge["color"],
            })

    return nodes, resolved_edges


def main():
    parser = argparse.ArgumentParser(description="构建知识图谱数据")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT), help="输出文件路径")
    parser.add_argument("--include-evidence", action="store_true", help="包含证据等级信息")
    parser.add_argument("--pretty", action="store_true", help="格式化 JSON 输出")
    args = parser.parse_args()

    output_path = Path(args.output)

    nodes, edges = scan_files()

    graph_data = {
        "nodes": nodes,
        "links": edges,
        "metadata": {
            "total_nodes": len(nodes),
            "total_links": len(edges),
            "categories": list(set(n["category"] for n in nodes)),
        }
    }

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    indent = 2 if args.pretty else None
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=indent)

    print(f"✅ 知识图谱数据已生成: {output_path}")
    print(f"   节点数: {len(nodes)}")
    print(f"   边数: {len(edges)}")
    print(f"   分类数: {len(graph_data['metadata']['categories'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
