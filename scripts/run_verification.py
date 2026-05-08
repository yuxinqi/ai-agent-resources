#!/usr/bin/env python3
"""
验真检查运行脚本

运行验真相关的检查任务，包括：
- 检查验真报告的完整性
- 检查文档的验真状态是否过期
- 统计验真覆盖率和评级分布

使用方法：
    python3 scripts/run_verification.py                        # 运行所有验真检查
    python3 scripts/run_verification.py --check-expiry         # 检查过期验真
    python3 scripts/run_verification.py --stats                # 输出统计数据
    python3 scripts/run_verification.py --ci                   # CI 模式

依赖：Python 3.8+（标准库）
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 验真过期天数阈值
EXPIRY_DAYS = 90

# 验真周期（天）按分类
VERIFICATION_PERIOD = {
    "platforms": 30,   # API 定价等信息变化快
    "prompts": 60,     # 提示词效果因模型版本变化
    "skills": 60,      # 技能可用性变化
    "workflows": 90,   # 工作流相对稳定
    "concepts": 180,   # 概念理论相对稳定
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


def parse_date(date_str: str) -> datetime:
    """解析日期字符串。"""
    try:
        return datetime.strptime(date_str[:10], "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def check_expiry() -> list:
    """检查已过期的验真报告。"""
    expired = []
    verification_dir = PROJECT_ROOT / "verification" / "reports"

    if not verification_dir.exists():
        return expired

    for filepath in verification_dir.rglob("*.md"):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter = parse_frontmatter(content)
        rel_path = filepath.relative_to(PROJECT_ROOT)

        # 检查 next_verification 日期
        next_ver = frontmatter.get('next_verification', '')
        if next_ver:
            next_date = parse_date(next_ver)
            if next_date and next_date < datetime.now():
                expired.append({
                    "file": str(rel_path),
                    "next_verification": next_ver,
                    "days_overdue": (datetime.now() - next_date).days,
                })

        # 检查 verified_date 是否过期
        verified_date_str = frontmatter.get('verified_date', '')
        if verified_date_str and not next_ver:
            verified_date = parse_date(verified_date_str)
            if verified_date:
                days_since = (datetime.now() - verified_date).days
                if days_since > EXPIRY_DAYS:
                    expired.append({
                        "file": str(rel_path),
                        "verified_date": verified_date_str,
                        "days_since_verification": days_since,
                    })

    return expired


def collect_stats() -> dict:
    """收集验真统计数据。"""
    stats = {
        "total_docs": 0,
        "verified_docs": 0,
        "unverified_docs": 0,
        "evidence_levels": {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "L4": 0},
        "ratings": {"A": 0, "B": 0, "C": 0, "D": 0},
        "by_category": {},
    }

    # 扫描 docs 目录
    docs_dir = PROJECT_ROOT / "docs"
    if docs_dir.exists():
        for filepath in docs_dir.rglob("*.md"):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter = parse_frontmatter(content)
            stats["total_docs"] += 1

            if frontmatter.get('verification', '').lower() in ('true', 'yes'):
                stats["verified_docs"] += 1
            else:
                stats["unverified_docs"] += 1

            level = frontmatter.get('evidence_level', '')
            if level in stats["evidence_levels"]:
                stats["evidence_levels"][level] += 1

            rating = frontmatter.get('rating', '')
            if rating in stats["ratings"]:
                stats["ratings"][rating] += 1

            category = frontmatter.get('category', filepath.parent.name)
            if category not in stats["by_category"]:
                stats["by_category"][category] = {"total": 0, "verified": 0}
            stats["by_category"][category]["total"] += 1
            if frontmatter.get('verification', '').lower() in ('true', 'yes'):
                stats["by_category"][category]["verified"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(description="运行验真检查任务")
    parser.add_argument("--check-expiry", action="store_true", help="检查过期的验真报告")
    parser.add_argument("--stats", action="store_true", help="输出验真统计数据")
    parser.add_argument("--ci", action="store_true", help="CI 模式")
    args = parser.parse_args()

    has_issues = False

    # 检查过期
    if args.check_expiry or (not args.stats):
        expired = check_expiry()
        if expired:
            print(f"⚠️ 发现 {len(expired)} 个过期验真：")
            for item in expired:
                if "next_verification" in item:
                    print(f"  {item['file']}: 已过期 {item['days_overdue']} 天（下次验真日期: {item['next_verification']}）")
                else:
                    print(f"  {item['file']}: 已 {item['days_since_verification']} 天未验真")
            has_issues = True
        else:
            print("✅ 所有验真报告在有效期内")

    # 统计数据
    if args.stats or (not args.check_expiry):
        stats = collect_stats()
        print(f"\n📊 验真统计：")
        print(f"  总文档数: {stats['total_docs']}")
        print(f"  已验真: {stats['verified_docs']}")
        print(f"  未验真: {stats['unverified_docs']}")
        if stats['total_docs'] > 0:
            coverage = stats['verified_docs'] / stats['total_docs'] * 100
            print(f"  验真覆盖率: {coverage:.1f}%")

        print(f"\n  证据等级分布：")
        for level, count in stats['evidence_levels'].items():
            print(f"    {level}: {count}")

        print(f"\n  评级分布：")
        for rating, count in stats['ratings'].items():
            print(f"    {rating}: {count}")

        print(f"\n  按分类：")
        for cat, data in stats['by_category'].items():
            print(f"    {cat}: {data['verified']}/{data['total']} 已验真")

    if args.ci and has_issues:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
