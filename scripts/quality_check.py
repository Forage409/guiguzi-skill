#!/usr/bin/env python3
"""
鬼谷子.skill 质量检查脚本
自动检查生成的领域Skill是否通过质量标准。

用法:
    python3 quality_check.py <SKILL.md路径>
    python3 quality_check.py research/        # 检查调研数据质量

示例:
    python3 quality_check.py examples/short-video-mastery/SKILL.md
    python3 quality_check.py examples/short-video-mastery/research/
"""

import sys
import re
from pathlib import Path


def check_core_principles(content: str) -> tuple[bool, str]:
    """检查核心原理数量（3-7条）"""
    in_section = False
    count = 0
    for line in content.split('\n'):
        if re.match(r'^##\s+.*核心原理|Core Principle', line, re.IGNORECASE):
            in_section = True
            continue
        if in_section and re.match(r'^##\s+', line) and '核心原理' not in line:
            break
        if in_section and re.match(r'^###\s+', line):
            count += 1
    if count == 0:
        patterns = re.findall(r'^###\s+原理\s*\d', content, re.MULTILINE)
        count = len(patterns)
    if count == 0:
        return False, "未检测到核心原理章节"
    passed = 3 <= count <= 7
    return passed, f"{count}条核心原理 {'✅' if passed else '❌ (应为3-7条)'}"


def check_traps(content: str) -> tuple[bool, str]:
    """检查致命陷阱数量（5-10条）"""
    in_section = False
    count = 0
    for line in content.split('\n'):
        if re.match(r'^##\s+.*致命陷阱|Fatal Trap', line, re.IGNORECASE):
            in_section = True
            continue
        if in_section and re.match(r'^##\s+', line) and '陷阱' not in line:
            break
        if in_section and re.match(r'^###\s+', line):
            count += 1
    if count == 0:
        patterns = re.findall(r'^###\s+陷阱\s*\d', content, re.MULTILINE)
        count = len(patterns)
    if count == 0:
        return False, "未检测到致命陷阱章节"
    passed = 5 <= count <= 10
    return passed, f"{count}条致命陷阱 {'✅' if passed else '❌ (应为5-10条)'}"


def check_roadmap(content: str) -> tuple[bool, str]:
    """检查是否有阶段路线图"""
    stages = re.findall(r'^###\s+.*阶段\s*\d|Phase\s*\d|Stage\s*\d', content, re.MULTILINE | re.IGNORECASE)
    if not stages:
        stages = re.findall(r'存活期|成长期|变现期|规模化', content)
    count = len(stages)
    if count == 0:
        return False, "❌ 未找到阶段路线图"
    passed = count >= 3
    return passed, f"{count}个阶段 {'✅' if passed else '❌ (应≥3个阶段)'}"


def check_monetization(content: str) -> tuple[bool, str]:
    """检查变现路径"""
    has_section = bool(re.search(r'变现地图|变现路径|Monetization', content, re.IGNORECASE))
    if not has_section:
        return False, "❌ 未找到变现地图章节"
    has_income = bool(re.search(r'收入范围|收入.*\d|月入|年入|\$|¥|元/月', content))
    has_steps = bool(re.search(r'从零到|第一笔收入|启动条件', content))
    score = sum([has_income, has_steps])
    passed = score >= 1
    details = []
    if has_income:
        details.append("有收入数据")
    if has_steps:
        details.append("有起步路径")
    return passed, f"变现路径: {', '.join(details) if details else '内容不足'} {'✅' if passed else '❌'}"


def check_honest_boundary(content: str) -> tuple[bool, str]:
    """检查诚实边界"""
    boundary_match = re.search(
        r'(?:##\s+.*诚实边界|## Honest Boundar)(.*?)(?=\n##\s|\Z)',
        content, re.DOTALL | re.IGNORECASE
    )
    if not boundary_match:
        return False, "❌ 未找到诚实边界章节"
    boundary_text = boundary_match.group(1)
    items = re.findall(r'^[-*]\s+', boundary_text, re.MULTILINE)
    count = len(items)
    passed = count >= 3
    return passed, f"诚实边界: {count}条 {'✅' if passed else '❌ (应≥3条)'}"


def check_evidence(content: str) -> tuple[bool, str]:
    """检查是否有证据/来源标注"""
    evidence_markers = len(re.findall(
        r'来源|证据|根据|数据|报告|调研|研究表明|统计|source|evidence',
        content, re.IGNORECASE
    ))
    passed = evidence_markers >= 5
    return passed, f"证据标注: {evidence_markers}处 {'✅' if passed else '❌ (应≥5处)'}"


def check_anti_bs(content: str) -> tuple[bool, str]:
    """检查是否避免了废话"""
    bs_patterns = [
        r'要用心', r'因人而异', r'要看情况', r'要坚持不懈',
        r'要有耐心', r'要深入理解', r'取决于很多因素',
    ]
    bs_count = 0
    found = []
    for pattern in bs_patterns:
        matches = re.findall(pattern, content)
        if matches:
            bs_count += len(matches)
            found.append(pattern.replace(r'', ''))
    passed = bs_count <= 2
    if found:
        return passed, f"发现{bs_count}处废话模式 {'⚠️ 建议修改' if not passed else '✅ 可接受'}: {', '.join(found[:3])}"
    return True, "无废话模式 ✅"


def check_research_dir(research_path: Path) -> None:
    """检查调研目录的数据质量"""
    print(f"\n调研数据质量检查: {research_path}")
    print("=" * 50)

    expected_files = [
        ("01-classics.md", "经典著作"),
        ("02-cases.md", "实战案例"),
        ("03-community.md", "社区共识"),
        ("04-tools.md", "工具链"),
        ("05-monetization.md", "变现路径"),
        ("06-learning-path.md", "学习路径"),
    ]

    total_sources = 0
    primary_count = 0
    missing = []

    for filename, label in expected_files:
        filepath = research_path / filename
        if not filepath.exists():
            print(f"  {label:<8} ❌ 文件缺失: {filename}")
            missing.append(label)
            continue

        text = filepath.read_text(encoding='utf-8')
        lines = len(text.split('\n'))
        urls = len(re.findall(r'https?://', text))
        primary = len(re.findall(r'一手|原始|本人|亲述|primary|firsthand', text, re.IGNORECASE))
        secondary = len(re.findall(r'二手|转述|secondary', text, re.IGNORECASE))

        total_sources += urls
        primary_count += primary

        status = "✅" if lines > 20 and urls >= 2 else "⚠️"
        print(f"  {label:<8} {status} {lines}行 | {urls}个链接 | 一手{primary} 二手{secondary}")

    print("-" * 50)
    print(f"  总信源: {total_sources} {'✅' if total_sources >= 10 else '❌ (应≥10)'}")
    print(f"  缺失维度: {len(missing)} {'✅' if len(missing) == 0 else '⚠️ ' + ', '.join(missing)}")


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 quality_check.py <SKILL.md路径>")
        print("  python3 quality_check.py <research/目录>")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_dir():
        check_research_dir(target)
        sys.exit(0)

    if not target.exists():
        print(f"❌ 文件不存在: {target}")
        sys.exit(1)

    content = target.read_text(encoding='utf-8')

    checks = [
        ("核心原理", check_core_principles),
        ("致命陷阱", check_traps),
        ("阶段路线图", check_roadmap),
        ("变现路径", check_monetization),
        ("诚实边界", check_honest_boundary),
        ("证据标注", check_evidence),
        ("废话检测", check_anti_bs),
    ]

    print(f"质量检查: {target.name}")
    print("=" * 50)

    passed_count = 0
    total = len(checks)

    for name, check_fn in checks:
        passed, detail = check_fn(content)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name:<10} {status}  {detail}")
        if passed:
            passed_count += 1

    print("=" * 50)
    print(f"结果: {passed_count}/{total} 通过")

    if passed_count == total:
        print("🎉 全部通过，可以交付")
    elif passed_count >= total - 1:
        print("⚠️ 基本通过，建议修复不通过项")
    else:
        print("❌ 多项不通过，建议回到Phase 2迭代")

    sys.exit(0 if passed_count == total else 1)


if __name__ == '__main__':
    main()
