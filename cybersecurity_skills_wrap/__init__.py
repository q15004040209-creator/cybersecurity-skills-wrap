"""
cybersecurity_skills_wrap
========================
Python wrapper for Anthropic-Cybersecurity-Skills — 754 structured
cybersecurity skills for AI agents, mapped to 5 frameworks.

Supported frameworks:
  - MITRE ATT&CK v19.1
  - NIST CSF 2.0
  - MITRE ATLAS v5.4
  - MITRE D3FEND v1.3
  - NIST AI RMF 1.0
"""

from .core import SkillLibrary

__version__ = "1.0.0"
__author__ = "q15004040209-creator"
__license__ = "Apache-2.0"

__all__ = ["SkillLibrary"]