"""
frameworks.py — Framework-specific query helpers

Provides utilities to query skills by:
  - MITRE ATT&CK technique ID
  - NIST CSF 2.0 category
  - MITRE ATLAS technique ID
  - MITRE D3FEND technique ID
  - NIST AI RMF subcategory
"""

from typing import List, Dict, Any


class FrameworkMapper:
    """
    Maps skills to industry frameworks and provides framework-specific queries.
    """

    def __init__(self, library: "SkillLibrary"):
        self._library = library

    def get_skills_by_attack_id(self, attack_id: str) -> List[Dict[str, Any]]:
        """
        Get all skills mapped to a MITRE ATT&CK technique.

        Args:
            attack_id: ATT&CK technique ID, e.g. 'T1071' or '1071'.

        Returns:
            List of skill dicts.
        """
        normalized = self._normalize_attack_id(attack_id)
        all_skills = self._library.all_skills()
        results = []
        for skill in all_skills:
            for tid in skill.get("mitre_attack", []):
                if self._normalize_attack_id(tid) == normalized:
                    results.append(skill)
                    break
        return results

    def get_skills_by_nist_csf(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all skills in a NIST CSF 2.0 category.

        Args:
            category: NIST CSF category, e.g. 'DE.CM', 'PR.AT-01'.

        Returns:
            List of skill dicts.
        """
        category_upper = category.upper().strip()
        all_skills = self._library.all_skills()
        results = []
        for skill in all_skills:
            for cat in skill.get("nist_csf", []):
                if cat.upper().startswith(category_upper) or category_upper.startswith(cat.upper()):
                    results.append(skill)
                    break
        return results

    def get_skills_by_atlas(self, atlas_id: str) -> List[Dict[str, Any]]:
        """
        Get all skills mapped to a MITRE ATLAS technique.

        Args:
            atlas_id: ATLAS technique ID, e.g. 'AML.T0047'.

        Returns:
            List of skill dicts.
        """
        atlas_id_upper = atlas_id.upper().strip()
        all_skills = self._library.all_skills()
        results = []
        for skill in all_skills:
            for tid in skill.get("atlas_techniques", []):
                if tid.upper().strip() == atlas_id_upper:
                    results.append(skill)
                    break
        return results

    def get_skills_by_d3fend(self, d3fend_id: str) -> List[Dict[str, Any]]:
        """
        Get all skills mapped to a MITRE D3FEND technique.

        Args:
            d3fend_id: D3FEND technique ID, e.g. 'D3-NTA', 'D3-MA'.

        Returns:
            List of skill dicts.
        """
        d3fend_id_upper = d3fend_id.upper().strip()
        all_skills = self._library.all_skills()
        results = []
        for skill in all_skills:
            for tid in skill.get("d3fend_techniques", []):
                if tid.upper().strip() == d3fend_id_upper:
                    results.append(skill)
                    break
        return results

    def get_skills_by_nist_ai_rmf(self, rmf_id: str) -> List[Dict[str, Any]]:
        """
        Get all skills mapped to a NIST AI RMF subcategory.

        Args:
            rmf_id: NIST AI RMF subcategory, e.g. 'MEASURE-2.6'.

        Returns:
            List of skill dicts.
        """
        rmf_id_upper = rmf_id.upper().strip()
        all_skills = self._library.all_skills()
        results = []
        for skill in all_skills:
            for tid in skill.get("nist_ai_rmf", []):
                if tid.upper().strip() == rmf_id_upper:
                    results.append(skill)
                    break
        return results

    # ------------------------------------------------------------------
    # Coverage reports
    # ------------------------------------------------------------------

    def attack_coverage(self) -> Dict[str, Any]:
        """
        Return ATT&CK coverage summary.
        """
        all_skills = self._library.all_skills()
        tactic_counts: Dict[str, int] = {}
        technique_counts: Dict[str, int] = {}
        for skill in all_skills:
            for tid in skill.get("mitre_attack", []):
                technique_counts[tid] = technique_counts.get(tid, 0) + 1
                # Extract tactic from ID (e.g. TA0043 from T1071.004)
                tactic_id = self._extract_tactic_id(tid)
                if tactic_id:
                    tactic_counts[tactic_id] = tactic_counts.get(tactic_id, 0) + 1

        return {
            "unique_techniques": len(technique_counts),
            "unique_tactics": len(tactic_counts),
            "top_techniques": sorted(technique_counts.items(), key=lambda x: x[1], reverse=True)[:20],
            "tactic_counts": tactic_counts,
        }

    def nist_csf_coverage(self) -> Dict[str, Any]:
        """
        Return NIST CSF 2.0 coverage summary.
        """
        all_skills = self._library.all_skills()
        category_counts: Dict[str, int] = {}
        for skill in all_skills:
            for cat in skill.get("nist_csf", []):
                # Extract top-level category (e.g. DE.CM-01 -> DE.CM)
                top_cat = cat.split("-")[0] if "-" in cat else cat
                category_counts[top_cat] = category_counts.get(top_cat, 0) + 1

        return {
            "unique_categories": len(category_counts),
            "category_counts": category_counts,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_attack_id(tid: str) -> str:
        """Normalize an ATT&CK ID by stripping 'T' prefix."""
        normalized = tid.upper().strip()
        if normalized.startswith("T"):
            normalized = normalized[1:]
        return normalized

    @staticmethod
    def _extract_tactic_id(tid: str) -> str:
        """Extract tactic ID from technique ID (e.g. TA0043 from T1071.004)."""
        # Tactics start with TA, techniques start with T
        upper = tid.upper().strip()
        if upper.startswith("TA"):
            return upper
        if upper.startswith("T"):
            # e.g. T1071.004 -> look up TA prefix
            return ""
        return ""