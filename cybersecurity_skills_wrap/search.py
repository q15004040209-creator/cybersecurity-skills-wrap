"""
search.py — Multi-dimensional search engine for the skill library
"""

import re
from typing import List, Dict, Any


class SearchEngine:
    """
    Provides multi-dimensional search across the skill library.

    Supports:
      - Full-text search (name, description, tags)
      - ATT&CK technique ID search
      - Domain-based filtering
    """

    def __init__(self, library: "SkillLibrary"):
        self._library = library

    def search(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Full-text search across skill name, description, and tags.

        Args:
            query: Search term or phrase.
            max_results: Maximum results to return.

        Returns:
            List of skill dicts, sorted by relevance (exact match > prefix > substring).
        """
        query_lower = query.lower()
        all_skills = self._library.all_skills()

        scored: List[tuple] = []
        for skill in all_skills:
            score = 0
            name = skill.get("name", "")
            desc = skill.get("description", "")
            tags = skill.get("tags", [])
            domain = skill.get("domain", "")

            name_lower = name.lower()
            desc_lower = desc.lower() if desc else ""
            tags_str = " ".join(tags).lower() if tags else ""

            # Exact name match
            if name_lower == query_lower:
                score += 100
            # Name starts with query
            elif name_lower.startswith(query_lower):
                score += 80
            # Name contains query
            elif query_lower in name_lower:
                score += 60
            # Description exact match
            elif desc_lower == query_lower:
                score += 50
            # Description contains query
            elif query_lower in desc_lower:
                score += 40
            # Tag exact match
            elif query_lower in tags_str:
                score += 30
            # Domain match
            elif query_lower in domain.lower():
                score += 20
            # Substring in description or tags
            elif query_lower in desc_lower or query_lower in tags_str:
                score += 10

            if score > 0:
                scored.append((score, skill))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:max_results]]

    def search_by_attack(self, attack_id: str) -> List[Dict[str, Any]]:
        """
        Search skills by MITRE ATT&CK technique ID.

        Args:
            attack_id: ATT&CK ID, e.g. 'T1055' or '1055'.

        Returns:
            List of skill dicts mapped to this technique.
        """
        # Normalize: strip 'T' prefix if present
        normalized = attack_id.upper().strip()
        if normalized.startswith("T"):
            normalized = normalized[1:]

        all_skills = self._library.all_skills()
        results = []
        for skill in all_skills:
            mitre_attack = skill.get("mitre_attack", [])
            for tid in mitre_attack:
                tid_normalized = tid.upper().strip()
                if tid_normalized.startswith("T"):
                    tid_normalized = tid_normalized[1:]
                if tid_normalized == normalized or tid_normalized.endswith(normalized):
                    results.append(skill)
                    break
        return results

    def search_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """
        Search skills by security domain.

        Args:
            domain: Domain name, e.g. 'cloud-security' or 'Cloud Security'.

        Returns:
            List of skill dicts in this domain.
        """
        domain_lower = domain.lower().replace("_", "-").replace(" ", "-")
        all_skills = self._library.all_skills()
        results = []
        for skill in all_skills:
            skill_domain = skill.get("domain", "").lower().replace("_", "-").replace(" ", "-")
            if skill_domain == domain_lower or domain_lower in skill_domain:
                results.append(skill)
        return results

    def search_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Search skills by tag.

        Args:
            tag: Tag string to match.

        Returns:
            List of skill dicts with this tag.
        """
        tag_lower = tag.lower()
        all_skills = self._library.all_skills()
        return [
            s for s in all_skills
            if any(tag_lower in t.lower() for t in s.get("tags", []))
        ]