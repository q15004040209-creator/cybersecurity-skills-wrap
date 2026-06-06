"""
parser.py — YAML frontmatter parser for agentskills.io SKILL.md files
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def parse_skill_md(file_path: str | Path) -> Dict[str, Any]:
    """
    Parse a SKILL.md file following the agentskills.io standard.

    Each file has:
     1. YAML frontmatter block (--- ... ---)
      2. Markdown body with sections like ## When to Use, ## Workflow, ## Verification

    Args:
        file_path: Path to the SKILL.md file.

    Returns:
        Dict with frontmatter fields + parsed body sections.
    """
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")

    # Split YAML frontmatter from Markdown body
    frontmatter_raw = ""
    body = content

    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        frontmatter_raw = fm_match.group(1)
        body = content[fm_match.end():]

    # Parse YAML frontmatter
    frontmatter: Dict[str, Any] = {}
    if frontmatter_raw:
        try:
            frontmatter = yaml.safe_load(frontmatter_raw) or {}
        except yaml.YAMLError:
            pass

    # Normalize frontmatter fields
    skill: Dict[str, Any] = {
        "name": frontmatter.get("name", path.stem),
        "description": frontmatter.get("description", ""),
        "domain": frontmatter.get("domain", ""),
        "subdomain": frontmatter.get("subdomain", ""),
        "tags": frontmatter.get("tags", []),
        "mitre_attack": frontmatter.get("mitre_attack", []),
        "atlas_techniques": frontmatter.get("atlas_techniques", []),
        "d3fend_techniques": frontmatter.get("d3fend_techniques", []),
        "nist_ai_rmf": frontmatter.get("nist_ai_rmf", []),
        "nist_csf": frontmatter.get("nist_csf", []),
        "version": frontmatter.get("version", "1.0"),
        "author": frontmatter.get("author", ""),
        "license": frontmatter.get("license", "Apache-2.0"),
        "file_path": str(path),
        "dir_name": path.parent.name,
    }

    # Parse Markdown body sections
    sections = _parse_body_sections(body)
    skill["sections"] = sections

    # When to Use
    when_to_use = sections.get("when to use", "")
    skill["when_to_use"] = when_to_use

    # Prerequisites
    prerequisites = sections.get("prerequisites", "")
    skill["prerequisites"] = prerequisites

    # Workflow
    workflow = sections.get("workflow", "")
    skill["workflow"] = workflow

    # Verification
    verification = sections.get("verification", "")
    skill["verification"] = verification

    return skill


def _parse_body_sections(body: str) -> Dict[str, str]:
    """
    Parse named sections from the Markdown body.

    Sections are marked by ## Headers (case-insensitive).
    """
    sections: Dict[str, str] = {}
    lines = body.split("\n")
    current_section = None
    current_lines: List[str] = []

    for line in lines:
        m = re.match(r"^##\s+(.+)$", line, re.IGNORECASE)
        if m:
            if current_section is not None:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = m.group(1).strip().lower()
            current_lines = []
        else:
            if current_section is not None:
                current_lines.append(line)

    if current_section is not None:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


def skill_to_dict(skill: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a skill dict to a flat serializable dict.
    Useful for JSON export.
    """
    return {
        "name": skill.get("name"),
        "description": skill.get("description"),
        "domain": skill.get("domain"),
        "subdomain": skill.get("subdomain"),
        "tags": skill.get("tags", []),
        "mitre_attack": skill.get("mitre_attack", []),
        "atlas_techniques": skill.get("atlas_techniques", []),
        "d3fend_techniques": skill.get("d3fend_techniques", []),
        "nist_ai_rmf": skill.get("nist_ai_rmf", []),
        "nist_csf": skill.get("nist_csf", []),
        "version": skill.get("version"),
        "author": skill.get("author"),
        "license": skill.get("license"),
    }