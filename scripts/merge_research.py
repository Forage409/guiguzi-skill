#!/usr/bin/env python3
"""
鬼谷子.skill 调研数据合并脚本
将6个维度的调研数据合并为结构化的方法论素材库。

用法:
    python3 merge_research.py <research目录> [输出文件]

示例:
    python3 merge_research.py examples/short-video-mastery/research/
    python3 merge_research.py examples/short-video-mastery/research/ merged.md
"""

import sys
import re
from pathlib import Path
from datetime import datetime


DIMENSION_FILES = [
    ("01-classics.md", "经典著作与权威来源", "📚"),
    ("02-cases.md", "实战案例与复盘", "🎯"),
    ("03-community.md", "社区共识与争议", "💬"),
    ("04-tools.md", "工具链与技术栈", "🔧"),
    ("05-monetization.md", "变现路径与收入数据", "💰"),
    ("06-learning-path.md", "学习路径与资源", "🗺️"),
]


def extract_sources(text: str) -> list[str]:
    urls = re.findall(r'https?://[^\s)\]]+', text)
    return list(set(urls))


def extract_key_insights(text: str) -> list[str]:
    insights = []
    for line in text.split('\n'):
        if re.match(r'^[-*]\s+\*\*', line):
            insights.append(line.strip())
        elif re.match(r'^>\s+', line) and len(line) > 10:
            insights.append(line.strip())
    return insights


def count_evidence_markers(text: str) -> int:
    return len(re.findall(
        r'来源|证据|根据|数据|报告|调研|研究表明|统计|source|evidence|一手|原始',
        text, re.IGNORECASE
    ))


def merge_research(research_dir: Path, output_path: Path | None = None) -> str:
    parts = []
    total_sources = 0
    total_insights = 0
    all_urls = []
    missing = []

    parts.append(f"# 调研数据合并报告")
    parts.append(f"\n> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    parts.append(f"> 数据目录: `{research_dir}`\n")

    for filename, label, emoji in DIMENSION_FILES:
        filepath = research_dir / filename
        if not filepath.exists():
            missing.append(label)
            continue

        text = filepath.read_text(encoding='utf-8')
        sources = extract_sources(text)
        insights = extract_key_insights(text)
        evidence = count_evidence_markers(text)

        total_sources += len(sources)
        total_insights += len(insights)
        all_urls.extend(sources)

        parts.append(f"---\n\n## {emoji} {label}\n")
        parts.append(f"**信源数**: {len(sources)} | **关键洞察**: {len(insights)} | **证据标注**: {evidence}\n")

        if insights:
            parts.append("### 关键洞察\n")
            for insight in insights[:15]:
                parts.append(insight)
            parts.append("")

        if sources:
            parts.append("### 信源列表\n")
            for url in sources[:20]:
                parts.append(f"- {url}")
            parts.append("")

    parts.append("---\n\n## 📊 合并统计\n")
    parts.append(f"- **总信源数**: {total_sources}")
    parts.append(f"- **总关键洞察**: {total_insights}")
    parts.append(f"- **去重URL数**: {len(set(all_urls))}")
    if missing:
        parts.append(f"- **缺失维度**: {', '.join(missing)}")
    parts.append(f"- **数据完整度**: {(6 - len(missing))}/6 维度")

    density = "充足" if total_sources >= 10 else "适中" if total_sources >= 5 else "稀少" if total_sources >= 2 else "极度匮乏"
    parts.append(f"- **信息密度评级**: {density}")

    if total_sources < 5:
        parts.append("\n> ⚠️ 信源数量不足，生成的方法论置信度较低，建议补充调研数据。")

    result = '\n'.join(parts) + '\n'

    if output_path:
        output_path.write_text(result, encoding='utf-8')
        print(f"✅ 合并报告已写入: {output_path}")
    else:
        default_output = research_dir / "merged-report.md"
        default_output.write_text(result, encoding='utf-8')
        print(f"✅ 合并报告已写入: {default_output}")

    print(f"   信源: {total_sources} | 洞察: {total_insights} | 密度: {density}")
    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python3 merge_research.py <research目录> [输出文件]")
        sys.exit(1)

    research_dir = Path(sys.argv[1])
    if not research_dir.is_dir():
        print(f"❌ 目录不存在: {research_dir}")
        sys.exit(1)

    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    merge_research(research_dir, output_path)


if __name__ == '__main__':
    main()
