"""
core.py — SkillLibrary core class
"""

import os
import re
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any

try:
    from .parser import parse_skill_md
    from .search import SearchEngine
    from .frameworks import FrameworkMapper
except ImportError:
    from parser import parse_skill_md
    from search import SearchEngine
    from frameworks import FrameworkMapper


class SkillLibrary:
    """
    Main interface for browsing and querying the 754-skill cybersecurity library.

    Example:
        library = SkillLibrary()
        skills = library.search("memory forensics")
        skill = library.get_skill("performing-memory-forensics-with-volatility3")
    """

    def __init__(self, skills_path: Optional[str] = None):
        """
        Initialize the skill library.

        Args:
            skills_path: Path to the skills root directory.
                         Defaults to the upstream repo clone.
        """
        if skills_path:
            self.skills_path = Path(skills_path)
        else:
            # Default to upstream repo location
            self.skills_path = Path(__file__).parent / "skills"

        self._cache: Dict[str, Dict[str, Any]] = {}
        self._all_skills: Optional[List[Dict[str, Any]]] = None
        self._search_engine = SearchEngine(self)
        self._framework_mapper = FrameworkMapper(self)

    # ------------------------------------------------------------------
    # Public API — loading & querying
    # ------------------------------------------------------------------

    def search(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Full-text search across all skills (name + description + tags).

        Args:
            query: Keyword or phrase to search for.
            max_results: Maximum number of results to return.

        Returns:
            List of skill dicts sorted by relevance.
        """
        return self._search_engine.search(query, max_results)

    def search_by_attack(self, attack_id: str) -> List[Dict[str, Any]]:
        """
        Search skills by MITRE ATT&CK technique ID (e.g. 'T1055', 'T1071').

        Args:
            attack_id: ATT&CK technique ID (with or without 'T' prefix).

        Returns:
            List of matching skill dicts.
        """
        return self._search_engine.search_by_attack(attack_id)

    def search_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """
        Search skills by security domain.

        Args:
            domain: Domain name (e.g. 'cloud-security', 'malware-analysis').

        Returns:
            List of matching skill dicts.
        """
        return self._search_engine.search_by_domain(domain)

    def get_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a single skill by its kebab-case name.

        Args:
            skill_name: Skill name in kebab-case (e.g. 'analyzing-network-traffic-of-malware').

        Returns:
            Skill dict or None if not found.
        """
        if skill_name in self._cache:
            return self._cache[skill_name]

        skill_path = self.skills_path / skill_name / "SKILL.md"
        if not skill_path.exists():
            # Try case-insensitive match
            for candidate in (self.skills_path).iterdir():
                if candidate.is_dir() and candidate.name.lower() == skill_name.lower():
                    skill_path = candidate / "SKILL.md"
                    break

        if not skill_path.exists():
            return None

        skill = parse_skill_md(skill_path)
        self._cache[skill_name] = skill
        return skill

    def get_skills_by_attack_id(self, attack_id: str) -> List[Dict[str, Any]]:
        """
        Get all skills mapped to a specific MITRE ATT&CK technique ID.

        Args:
            attack_id: ATT&CK technique ID (e.g. 'T1071').

        Returns:
            List of skill dicts mapped to this technique.
        """
        return self._framework_mapper.get_skills_by_attack_id(attack_id)

    def get_skills_by_nist_csf(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all skills in a specific NIST CSF 2.0 category.

        Args:
            category: NIST CSF category (e.g. 'DE.CM', 'PR.AT').

        Returns:
            List of skill dicts in this category.
        """
        return self._framework_mapper.get_skills_by_nist_csf(category)

    def get_skills_by_atlas(self, atlas_id: str) -> List[Dict[str, Any]]:
        """
        Get all skills mapped to a specific MITRE ATLAS technique ID.

        Args:
            atlas_id: ATLAS technique ID (e.g. 'AML.T0047').

        Returns:
            List of skill dicts mapped to this technique.
        """
        return self._framework_mapper.get_skills_by_atlas(atlas_id)

    def get_skills_by_d3fend(self, d3fend_id: str) -> List[Dict[str, Any]]:
        """
        Get all skills mapped to a specific MITRE D3FEND technique ID.

        Args:
            d3fend_id: D3FEND technique ID (e.g. 'D3-NTA', 'D3-MA').

        Returns:
            List of skill dicts mapped to this technique.
        """
        return self._framework_mapper.get_skills_by_d3fend(d3fend_id)

    def get_skills_by_nist_ai_rmf(self, rmf_id: str) -> List[Dict[str, Any]]:
        """
        Get all skills mapped to a specific NIST AI RMF subcategory.

        Args:
            rmf_id: NIST AI RMF subcategory (e.g. 'MEASURE-2.6').

        Returns:
            List of skill dicts mapped to this subcategory.
        """
        return self._framework_mapper.get_skills_by_nist_ai_rmf(rmf_id)

    def all_skills(self, force_reload: bool = False) -> List[Dict[str, Any]]:
        """
        Load and return all skills.

        Args:
            force_reload: If True, bypass the cache.

        Returns:
            List of all 754 skill dicts.
        """
        if self._all_skills and not force_reload:
            return self._all_skills

        skills = []
        if not self.skills_path.exists():
            return skills

        for skill_dir in self.skills_path.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                try:
                    skill = parse_skill_md(skill_md)
                    skills.append(skill)
                    self._cache[skill_dir.name] = skill
                except Exception:
                    continue

        self._all_skills = skills
        return skills

    def stats(self) -> Dict[str, Any]:
        """
        Return library statistics.

        Returns:
            Dict with counts by domain, framework coverage, etc.
        """
        all_s = self.all_skills()

        domains: Dict[str, int] = {}
        attack_ids: Dict[str, int] = {}
        nist_csf_categories: Dict[str, int] = {}
        atlas_techniques: Dict[str, int] = {}
        d3fend_techniques: Dict[str, int] = {}
        nist_ai_rmf: Dict[str, int] = {}

        for skill in all_s:
            domain = skill.get("domain", "unknown")
            domains[domain] = domains.get(domain, 0) + 1

            for tid in skill.get("mitre_attack", []):
                attack_ids[tid] = attack_ids.get(tid, 0) + 1
            for cat in skill.get("nist_csf", []):
                nist_csf_categories[cat] = nist_csf_categories.get(cat, 0) + 1
            for tid in skill.get("atlas_techniques", []):
                atlas_techniques[tid] = atlas_techniques.get(tid, 0) + 1
            for tid in skill.get("d3fend_techniques", []):
                d3fend_techniques[tid] = d3fend_techniques.get(tid, 0) + 1
            for tid in skill.get("nist_ai_rmf", []):
                nist_ai_rmf[tid] = nist_ai_rmf.get(tid, 0) + 1

        return {
            "total_skills": len(all_s),
            "domains": domains,
            "unique_attack_ids": len(attack_ids),
            "unique_nist_csf_categories": len(nist_csf_categories),
            "unique_atlas_techniques": len(atlas_techniques),
            "unique_d3fend_techniques": len(d3fend_techniques),
            "unique_nist_ai_rmf": len(nist_ai_rmf),
        }

    def __repr__(self) -> str:
        n = len(self.all_skills()) if self._all_skills else "?"
        return f"SkillLibrary(total_skills={n})"