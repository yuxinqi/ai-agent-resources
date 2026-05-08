#!/usr/bin/env python3
"""
Badge 生成脚本

扫描项目文件，生成各类状态 Badge（SVG 格式），
包括验真覆盖率、评级分布、文档数量等。

使用方法：
    python3 scripts/generate_badges.py                  # 生成所有 badges
    python3 scripts/generate_badges.py --output badges/  # 指定输出目录
    python3 scripts/generate_badges.py --ci              # CI 模式

依赖：Python 3.8+（标准库）
"""

import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "badges"


def generate_svg_badge(label: str, value: str, color: str) -> str:
    """生成简单的 SVG badge。"""
    # 计算 label 和 value 的宽度（粗略估算）
    label_width = len(label) * 7 + 12
    value_width = len(value) * 7 + 12
    total_width = label_width + value_width

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20">
  <defs>
    <clipPath id="round">
      <rect width="{total_width}" height="20" rx="3" fill="#fff"/>
    </clipPath>
  </defs>
  <g clip-path="url(#round)">
    <rect width="{label_width}" height="20" fill="#555"/>
    <rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>
  </g>
  <g fill="#fff" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
    <text x="{label_width // 2}" y="14" text-anchor="middle">{label}</text>
    <text x="{label_width + value_width // 2}" y="14" text-anchor="middle">{value}</text>
  </g>
</svg>'''
    return svg


def count_verification_stats() -> dict:
    """统计验真相关数据。"""
    import re

    stats = {
        "total_docs": 0,
        "verified_docs": 0,
        "evidence_levels": {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "L4": 0},
        "ratings": {"A": 0, "B": 0, "C": 0, "D": 0},
        "reports": 0,
    }

    def parse_frontmatter(content):
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

    # 扫描 docs
    docs_dir = PROJECT_ROOT / "docs"
    if docs_dir.exists():
        for filepath in docs_dir.rglob("*.md"):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            frontmatter = parse_frontmatter(content)
            stats["total_docs"] += 1

            if frontmatter.get('verification', '').lower() in ('true', 'yes'):
                stats["verified_docs"] += 1

            level = frontmatter.get('evidence_level', '')
            if level in stats["evidence_levels"]:
                stats["evidence_levels"][level] += 1

            rating = frontmatter.get('rating', '')
            if rating in stats["ratings"]:
                stats["ratings"][rating] += 1

    # 扫描验真报告
    reports_dir = PROJECT_ROOT / "verification" / "reports"
    if reports_dir.exists():
        for filepath in reports_dir.rglob("*.md"):
            stats["reports"] += 1

    return stats


def get_coverage_color(coverage: float) -> str:
    """根据覆盖率返回颜色。"""
    if coverage >= 80:
        return "#10b981"  # 绿
    elif coverage >= 60:
        return "#f59e0b"  # 黄
    elif coverage >= 40:
        return "#f97316"  # 橙
    else:
        return "#ef4444"  # 红


def main():
    parser = argparse.ArgumentParser(description="生成状态 Badges")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT), help="输出目录")
    parser.add_argument("--ci", action="store_true", help="CI 模式")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    stats = count_verification_stats()

    # 计算覆盖率
    coverage = 0
    if stats["total_docs"] > 0:
        coverage = stats["verified_docs"] / stats["total_docs"] * 100

    # 生成 badges
    badges = {
        "verification-coverage": generate_svg_badge(
            "验真覆盖率",
            f"{coverage:.0f}%",
            get_coverage_color(coverage)
        ),
        "total-docs": generate_svg_badge(
            "文档总数",
            str(stats["total_docs"]),
            "#3b82f6"
        ),
        "verified-docs": generate_svg_badge(
            "已验真",
            str(stats["verified_docs"]),
            "#10b981"
        ),
        "verification-reports": generate_svg_badge(
            "验真报告",
            str(stats["reports"]),
            "#8b5cf6"
        ),
        "evidence-L0": generate_svg_badge("L0", str(stats["evidence_levels"]["L0"]), "#10b981"),
        "evidence-L1": generate_svg_badge("L1", str(stats["evidence_levels"]["L1"]), "#3b82f6"),
        "evidence-L2": generate_svg_badge("L2", str(stats["evidence_levels"]["L2"]), "#f59e0b"),
        "evidence-L3": generate_svg_badge("L3", str(stats["evidence_levels"]["L3"]), "#f97316"),
        "evidence-L4": generate_svg_badge("L4", str(stats["evidence_levels"]["L4"]), "#ef4444"),
    }

    # 写入文件
    for name, svg in badges.items():
        filepath = output_dir / f"{name}.svg"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg)

    print(f"✅ 已生成 {len(badges)} 个 badges 到 {output_dir}/")
    print(f"   验真覆盖率: {coverage:.1f}%")
    print(f"   文档总数: {stats['total_docs']}")
    print(f"   已验真: {stats['verified_docs']}")
    print(f"   验真报告: {stats['reports']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
