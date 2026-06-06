#!/usr/bin/env python3
"""
demo.py — Quick demo of the cybersecurity-skills-wrap library

Run with:
    python -m cybersecurity_skills_wrap.demo
    # or
    from cybersecurity_skills_wrap import SkillLibrary
    library = SkillLibrary()
    ...
"""

import sys
from pathlib import Path

# Add parent to path so we can import when running standalone
sys.path.insert(0, str(Path(__file__).parent.parent))


def print_skill(skill: dict, max_desc: int = 80):
    """Pretty-print a skill dict."""
    name = skill.get("name", "unknown")
    desc = skill.get("description", "")
    if len(desc) > max_desc:
        desc = desc[:max_desc] + "..."
    domain = skill.get("domain", "")
    tags = skill.get("tags", [])
    mitre = skill.get("mitre_attack", [])
    nist_csf = skill.get("nist_csf", [])
    atlas = skill.get("atlas_techniques", [])
    d3fend = skill.get("d3fend_techniques", [])
    nist_ai = skill.get("nist_ai_rmf", [])

    print(f"\n  📌 {name}")
    print(f"     Domain: {domain}")
    print(f"     Description: {desc}")
    if tags:
        print(f"     Tags: {', '.join(tags[:8])}")
    if mitre:
        print(f"     ATT&CK: {', '.join(mitre[:5])}")
    if nist_csf:
        print(f"     NIST CSF: {', '.join(nist_csf[:5])}")
    if atlas:
        print(f"     ATLAS: {', '.join(atlas[:3])}")
    if d3fend:
        print(f"     D3FEND: {', '.join(d3fend[:3])}")
    if nist_ai:
        print(f"     NIST AI RMF: {', '.join(nist_ai[:3])}")


def demo_search(library):
    """Demo: keyword search."""
    print("\n" + "=" * 60)
   print("🔍 DEMO 1: Keyword Search")
    print("=" * 60)

    queries = ["memory forensics", "malware analysis", "cloud security", "threat hunting"]
    for q in queries:
        skills = library.search(q, max_results=3)
        print(f"\nQuery: '{q}' → {len(skills)} results")
        for s in skills:
            print(f"  • {s['name']}")


def demo_attack_search(library):
    """Demo: ATT&CK technique search."""
    print("\n" + "=" * 60)
    print("🎯 DEMO 2: MITRE ATT&CK Technique Search")
    print("=" * 60)

    attack_ids = ["T1071", "T1055", "T1003", "T1566"]
    for aid in attack_ids:
        skills = library.get_skills_by_attack_id(aid)
        print(f"\nATT&CK {aid}: {len(skills)} skills")
        for s in skills[:3]:
            print(f"  → {s['name']}")


def demo_framework_search(library):
    """Demo: framework-specific queries."""
    print("\n" + "=" * 60)
    print("🌐 DEMO 3: Framework-Specific Queries")
    print("=" * 60)

    # NIST CSF
    categories = ["DE.CM", "PR.AT", "RS.AN"]
    for cat in categories:
        skills = library.get_skills_by_nist_csf(cat)
        print(f"\nNIST CSF {cat}: {len(skills)} skills")
        for s in skills[:3]:
            print(f"  → {s['name']}")

    # ATLAS
    atlas_ids = ["AML.T0047", "AML.T0048"]
    for aid in atlas_ids:
        skills = library.get_skills_by_atlas(aid)
        print(f"\nATLAS {aid}: {len(skills)} skills")
        for s in skills[:3]:
            print(f"  → {s['name']}")


def demo_domain_search(library):
    """Demo: domain filtering."""
    print("\n" + "=" * 60)
    print("🏷️  DEMO 4: Domain Filtering")
    print("=" * 60)

    domains = ["cloud-security", "malware-analysis", "threat-hunting"]
    for dom in domains:
        skills = library.search_by_domain(dom)
        print(f"\nDomain '{dom}': {len(skills)} skills")
        for s in skills[:3]:
            print(f"  • {s['name']}")


def demo_stats(library):
    """Demo: library statistics."""
    print("\n" + "=" * 60)
    print("📊 DEMO 5: Library Statistics")
    print("=" * 60)

    stats = library.stats()
    print(f"\n  Total skills: {stats['total_skills']}")
    print(f"  Unique ATT&CK techniques: {stats['unique_attack_ids']}")
    print(f"  Unique NIST CSF categories: {stats['unique_nist_csf_categories']}")
    print(f"  Unique ATLAS techniques: {stats['unique_atlas_techniques']}")
    print(f"  Unique D3FEND techniques: {stats['unique_d3fend_techniques']}")
    print(f"  Unique NIST AI RMF: {stats['unique_nist_ai_rmf']}")

    print("\n  Top domains:")
    sorted_domains = sorted(stats["domains"].items(), key=lambda x: x[1], reverse=True)
    for domain, count in sorted_domains[:10]:
        print(f"    {domain}: {count}")


def demo_get_skill(library):
    """Demo: get single skill."""
    print("\n" + "=" * 60)
    print("📄 DEMO 6: Single Skill Detail")
    print("=" * 60)

    skill_name = "performing-memory-forensics-with-volatility3"
    skill = library.get_skill(skill_name)
    if skill:
        print_skill(skill)
    else:
        print(f"\n  ⚠️  Skill '{skill_name}' not found in local path.")
        print("  (This is expected if skills are not checked out locally)")


def main():
    print("🛡️  Cybersecurity Skills Wrap — Library Demo")
    print("=" * 60)

    try:
        from cybersecurity_skills_wrap import SkillLibrary
    except ImportError:
        print("⚠️  Cannot import library. Install with:")
        print("    pip install -e .")
        return

    library = SkillLibrary()

    print(f"\nInitialized: {library}")
    total = len(library.all_skills())
    print(f"Loaded skills: {total}")

    if total == 0:
        print("\n⚠️  No skills loaded. Clone the upstream repo to enable full functionality:")
        print("    git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git")
        print("    # Then point SkillLibrary to the skills/ directory")
        print("\n--- Running partial demo anyway ---\n")

    demo_search(library)
    demo_attack_search(library)
    demo_framework_search(library)
    demo_domain_search(library)
    demo_stats(library)
    demo_get_skill(library)

    print("\n" + "=" * 60)
    print("✅ Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()