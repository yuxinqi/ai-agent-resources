#!/usr/bin/env python3
"""
链接检查脚本

扫描 Markdown 文件中的内部链接和外部链接，
检查是否存在断裂链接（404、文件不存在等）。

使用方法：
    python3 scripts/check_links.py                    # 检查内部链接
    python3 scripts/check_links.py --external         # 同时检查外部链接
    python3 scripts/check_links.py --ci               # CI 模式
    python3 scripts/check_links.py --fix              # 输出修复建议

依赖：Python 3.8+（外部链接检查需 requests）
"""

import argparse
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 扫描目录
SCAN_DIRS = ["docs", "verification", "benchmarks", "assets", "examples"]


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


def extract_links(content: str, filepath: Path) -> list:
    """从 Markdown 内容中提取所有链接。"""
    links = []

    # 匹配 Markdown 链接 [text](url)
    md_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    for match in re.finditer(md_pattern, content):
        text = match.group(1)
        url = match.group(2).strip()
        if url and not url.startswith('#'):
            links.append({"text": text, "url": url, "type": "markdown"})

    # 匹配 frontmatter 中的 related / depends_on
    frontmatter = parse_frontmatter(content)
    for field in ['related', 'depends_on']:
        raw = frontmatter.get(field, '')
        if raw:
            refs = re.findall(r'- (.+)', raw)
            for ref in refs:
                ref = ref.strip()
                if ref:
                    links.append({"text": f"frontmatter:{field}", "url": ref, "type": "frontmatter"})

    return links


def check_internal_link(url: str, filepath: Path) -> tuple:
    """检查内部链接是否存在。返回 (is_valid, resolved_path)。"""
    # 处理锚点
    anchor = ""
    if "#" in url:
        parts = url.split("#", 1)
        url = parts[0]
        anchor = parts[1]

    # 解析相对路径
    if url.startswith('/'):
        # 绝对路径（从项目根开始）
        target = PROJECT_ROOT / url.lstrip('/')
    else:
        # 相对路径
        target = (filepath.parent / url).resolve()

    # 移除锚点后的路径检查
    target_str = str(target)

    # 如果 URL 指向目录，检查是否有 index.md
    if not os.path.exists(target_str):
        # 尝试添加 .md 扩展名
        if not url.endswith('.md') and not url.endswith('.html'):
            md_target = target_str + '.md'
            if os.path.exists(md_target):
                return True, md_target

        return False, target_str

    return True, target_str


def check_external_link(url: str) -> tuple:
    """检查外部链接是否可用。返回 (is_valid, status_code)。"""
    try:
        import requests
        response = requests.head(url, timeout=10, allow_redirects=True)
        return response.status_code < 400, response.status_code
    except ImportError:
        return None, "requests 未安装"
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="检查 Markdown 文件中的断裂链接")
    parser.add_argument("--external", action="store_true", help="同时检查外部链接（需 requests）")
    parser.add_argument("--ci", action="store_true", help="CI 模式，有断裂链接时返回非零")
    parser.add_argument("--fix", action="store_true", help="输出修复建议")
    args = parser.parse_args()

    broken_links = []
    total_links = 0
    file_count = 0

    # 扫描目录
    for scan_dir in SCAN_DIRS:
        dir_path = PROJECT_ROOT / scan_dir
        if not dir_path.exists():
            continue

        for filepath in dir_path.rglob("*.md"):
            file_count += 1
            rel_path = filepath.relative_to(PROJECT_ROOT)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            links = extract_links(content, filepath)

            for link in links:
                url = link["url"]
                total_links += 1

                # 跳过纯锚点链接
                if url.startswith('#'):
                    continue

                # 跳过图片链接
                if url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                    # 检查图片文件是否存在
                    is_valid, _ = check_internal_link(url, filepath)
                    if not is_valid:
                        broken_links.append({
                            "file": str(rel_path),
                            "text": link["text"],
                            "url": url,
                            "type": "image",
                            "reason": "图片文件不存在"
                        })
                    continue

                # 内部链接
                if not url.startswith(('http://', 'https://', 'mailto:')):
                    is_valid, resolved = check_internal_link(url, filepath)
                    if not is_valid:
                        broken_links.append({
                            "file": str(rel_path),
                            "text": link["text"],
                            "url": url,
                            "type": "internal",
                            "reason": f"目标不存在: {resolved}"
                        })

                # 外部链接
                elif args.external and url.startswith(('http://', 'https://')):
                    is_valid, status = check_external_link(url)
                    if is_valid is False:
                        broken_links.append({
                            "file": str(rel_path),
                            "text": link["text"],
                            "url": url,
                            "type": "external",
                            "reason": f"HTTP {status}"
                        })

    # 输出结果
    if broken_links:
        print(f"❌ 发现 {len(broken_links)} 个断裂链接：\n")
        for bl in broken_links:
            print(f"  [{bl['type']}] {bl['file']}")
            print(f"    文本: {bl['text']}")
            print(f"    链接: {bl['url']}")
            print(f"    原因: {bl['reason']}")
            print()

        if args.fix:
            print("\n修复建议：")
            for bl in broken_links:
                if bl['type'] == 'internal':
                    print(f"  检查 {bl['file']} 中的链接 '{bl['url']}' 是否路径正确")
    else:
        print(f"✅ 所有 {total_links} 个链接检查通过（扫描 {file_count} 个文件）")

    if args.ci and broken_links:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
