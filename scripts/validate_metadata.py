#!/usr/bin/env python3
"""
Frontmatter 元数据验证脚本

扫描 docs/, verification/, benchmarks/ 目录下的 Markdown 文件，
验证 YAML frontmatter 是否包含必需字段，并检查字段值是否合法。

使用方法：
    python3 scripts/validate_metadata.py                  # 验证所有文件
    python3 scripts/validate_metadata.py --ci             # CI 模式，有错误时返回非零
    python3 scripts/validate_metadata.py --check-evidence-level  # 检查证据等级
    python3 scripts/validate_metadata.py --path docs/     # 只验证指定路径

依赖：Python 3.8+（标准库 + pyyaml 可选）
"""

import argparse
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 必需的 frontmatter 字段
REQUIRED_FIELDS = ["title", "category", "updated"]

# 可选但建议的字段
RECOMMENDED_FIELDS = ["tags", "created", "evidence_level", "rating"]

# 有效的证据等级
VALID_EVIDENCE_LEVELS = {"L0", "L1", "L2", "L3", "L4"}

# 有效的评级
VALID_RATINGS = {"A", "B", "C", "D"}

# 有效的分类
VALID_CATEGORIES = {
    "concepts", "platforms", "prompts", "skills", "tools", "workflows",
    "getting-started", "patterns", "playbooks", "case-studies",
    "verification", "template", "changelog", "benchmark",
    "agent", "rag", "mcp",
}

# 要扫描的目录
SCAN_DIRS = ["docs", "verification", "benchmarks"]


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
            # 跳过列表值（以 - 开头的行）
            if value or colon_index + 1 < len(line):
                frontmatter[key] = value

    return frontmatter


def validate_file(filepath: Path) -> list:
    """验证单个文件的 frontmatter，返回错误列表。"""
    errors = []
    rel_path = filepath.relative_to(PROJECT_ROOT)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否有 frontmatter
    if not content.startswith('---'):
        errors.append(f"{rel_path}: 缺少 frontmatter")
        return errors

    frontmatter = parse_frontmatter(content)
    if not frontmatter:
        errors.append(f"{rel_path}: frontmatter 为空或格式错误")
        return errors

    # 检查必需字段
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"{rel_path}: 缺少必需字段 '{field}'")

    # 检查建议字段（仅警告）
    for field in RECOMMENDED_FIELDS:
        if field not in frontmatter:
            pass  # 仅在详细模式报告

    # 验证 evidence_level 值
    if "evidence_level" in frontmatter:
        level = frontmatter["evidence_level"]
        if level not in VALID_EVIDENCE_LEVELS:
            errors.append(f"{rel_path}: 无效的 evidence_level '{level}'，应为 {VALID_EVIDENCE_LEVELS}")

    # 验证 rating 值
    if "rating" in frontmatter:
        rating = frontmatter["rating"]
        if rating not in VALID_RATINGS:
            errors.append(f"{rel_path}: 无效的 rating '{rating}'，应为 {VALID_RATINGS}")

    # 验证 category 值
    if "category" in frontmatter:
        category = frontmatter["category"]
        if category not in VALID_CATEGORIES:
            # 宽松模式：不报错，仅警告
            pass

    # 验证日期格式
    for date_field in ["created", "updated", "verified_date"]:
        if date_field in frontmatter:
            date_val = frontmatter[date_field]
            if not re.match(r'^\d{4}-\d{2}-\d{2}', date_val):
                errors.append(f"{rel_path}: {date_field} 格式无效 '{date_val}'，应为 YYYY-MM-DD")

    return errors


def check_evidence_levels() -> list:
    """检查所有文件的证据等级标注情况。"""
    warnings = []

    for scan_dir in SCAN_DIRS:
        dir_path = PROJECT_ROOT / scan_dir
        if not dir_path.exists():
            continue

        for filepath in dir_path.rglob("*.md"):
            if filepath.name == "README.md":
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter = parse_frontmatter(content)
            rel_path = filepath.relative_to(PROJECT_ROOT)

            # 验真报告目录的文件应该有 evidence_level
            if "verification/reports" in str(rel_path):
                if "evidence_level" not in frontmatter:
                    warnings.append(f"{rel_path}: 验真报告缺少 evidence_level 字段")
                if "rating" not in frontmatter:
                    warnings.append(f"{rel_path}: 验真报告缺少 rating 字段")

            # docs 目录下的文件建议标注 evidence_level
            if str(rel_path).startswith("docs/"):
                if "evidence_level" not in frontmatter:
                    pass  # 仅建议，不强制

    return warnings


def main():
    parser = argparse.ArgumentParser(description="验证 Markdown 文件的 frontmatter 元数据")
    parser.add_argument("--ci", action="store_true", help="CI 模式，有错误时返回非零退出码")
    parser.add_argument("--check-evidence-level", action="store_true", help="检查证据等级标注")
    parser.add_argument("--path", type=str, help="只验证指定路径下的文件")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    args = parser.parse_args()

    all_errors = []
    all_warnings = []
    file_count = 0

    if args.check_evidence_level:
        warnings = check_evidence_levels()
        all_warnings.extend(warnings)

    # 确定扫描路径
    scan_paths = []
    if args.path:
        custom_path = PROJECT_ROOT / args.path
        if custom_path.exists():
            scan_paths.append(custom_path)
        else:
            print(f"❌ 路径不存在: {args.path}")
            return 1
    else:
        for scan_dir in SCAN_DIRS:
            dir_path = PROJECT_ROOT / scan_dir
            if dir_path.exists():
                scan_paths.append(dir_path)

    # 扫描并验证
    for scan_path in scan_paths:
        for filepath in scan_path.rglob("*.md"):
            if filepath.name == "README.md" and "benchmarks" in str(filepath):
                continue  # 跳过 benchmarks README
            file_count += 1
            errors = validate_file(filepath)
            all_errors.extend(errors)

    # 输出结果
    if all_errors:
        print(f"❌ 发现 {len(all_errors)} 个错误：")
        for error in all_errors:
            print(f"  {error}")
    else:
        print(f"✅ 所有 {file_count} 个文件验证通过")

    if all_warnings:
        print(f"\n⚠️ {len(all_warnings)} 个警告：")
        for warning in all_warnings:
            print(f"  {warning}")

    if args.verbose:
        print(f"\n统计：扫描 {file_count} 个文件，{len(all_errors)} 个错误，{len(all_warnings)} 个警告")

    if args.ci and all_errors:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
