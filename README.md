#🛡️ Cybersecurity Skills Wrap

> **网络安全技能库封装** — 754 个结构化安全技能，映射 5 大行业框架，为 AI Agent 提供专家级安全分析能力

[English](#english) | [中文](#中文)

---

## English

### What is This?

`cybersecurity-skills-wrap` is a Python wrapper for the [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) project — 754 structured cybersecurity skills for AI agents, spanning 26 security domains.

Every skill maps to **5 industry frameworks** simultaneously:

| Framework | Version | Coverage |
|-----------|---------|----------|
| **MITRE ATT&CK** | v19.1 | 15 tactics · 286 techniques |
| **NIST CSF 2.0** | 2.0 | 6 functions · 22 categories |
| **MITRE ATLAS** | v5.4 | 16 tactics · 84 techniques (AI/ML threats) |
| **MITRE D3FEND** | v1.3 | 7 categories · 267 countermeasures |
| **NIST AI RMF** | 1.0 | 4 functions · 72 subcategories |

### Why?

AI agents today can write code and search the web — but they lack the **practitioner playbooks** that turn a generic LLM into a capable security analyst. This project fills that gap.

### Installation

```bash
pip install cybersecurity-skills-wrap
```

Or from source:

```bash
git clone https://github.com/q15004040209-creator/cybersecurity-skills-wrap.git
cd cybersecurity-skills-wrap
pip install -e .
```

### Quick Start

```python
from cybersecurity_skills_wrap import SkillLibrary

# Initialize the skill library
library = SkillLibrary()

# Search skills by keyword
skills = library.search("memory forensics")
print(f"Found {len(skills)} skills")
for skill in skills[:5]:
    print(f"  - {skill['name']}: {skill['description'][:60]}...")

# Search by MITRE ATT&CK technique
skills = library.search_by_attack("T1055")  # Process injection
print(f"\nSkills for T1055: {len(skills)}")

# Search by domain
cloud_skills = library.search_by_domain("cloud-security")
print(f"\nCloud security skills: {len(cloud_skills)}")

# Get full skill detail
skill = library.get_skill("performing-memory-forensics-with-volatility3")
print(f"\nSkill: {skill['name']}")
print(f"Tags: {skill['tags']}")
print(f"ATLAS: {skill['atlas_techniques']}")
print(f"D3FEND: {skill['d3fend_techniques']}")
print(f"NIST AI RMF: {skill['nist_ai_rmf']}")
print(f"NIST CSF: {skill['nist_csf']}")
```

### Framework Mapping Example

```python
from cybersecurity_skills_wrap import SkillLibrary

library = SkillLibrary()

# Get all skills mapped to a specific ATT&CK technique
skills = library.get_skills_by_attack_id("T1071")  # Application Layer Protocol
print(f"ATT&CK T1071 — Application Layer Protocol")
for skill in skills:
    print(f"  → {skill['name']}")

# Get all skills in a NIST CSF 2.0 category
skills = library.get_skills_by_nist_csf("DE.CM")  # Detect — Continuous Monitoring
print(f"\nNIST CSF DE.CM — Continuous Monitoring")
for skill in skills:
    print(f"  → {skill['name']}")

# Get ATLAS skills for AI/ML threat detection
skills = library.get_skills_by_atlas("AML.T0047")  # Model evasion
print(f"\nATLAS AML.T0047 — Model Evasion")
for skill in skills:
    print(f"  → {skill['name']}")
```

### Supported Frameworks

```
✅ MITRE ATT&CK v19.1     — 15 tactics, 286 techniques
✅ NIST CSF 2.0            — 6 functions, 22 categories
✅ MITRE ATLAS v5.4 — 16 tactics, 84 techniques (AI/ML)
✅ MITRE D3FEND v1.3       — 7 categories, 267 countermeasures
✅ NIST AI RMF 1.0         — 4 functions, 72 subcategories
```

###26 Security Domains

Cloud Security · Threat Hunting · Threat Intelligence · Web App Security · Network Security · Malware Analysis · Digital Forensics · Security Operations · IAM · SOC Operations · Container Security · OT/ICS Security · API Security · Vulnerability Management · Incident Response · Red Teaming · Penetration Testing · Endpoint Security · DevSecOps · Phishing Defense · Cryptography · Zero Trust · Mobile Security · Ransomware Defense · Compliance & Governance · Deception Technology

### License

Apache 2.0 — same as the upstream project.

---

## 中文

### 这是什么？

`cybersecurity-skills-wrap` 是 [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) 项目的 Python 封装包 — 包含 **754 个结构化网络安全技能**，覆盖 **26 个安全领域**，每个技能同时映射到 **5 大行业框架**。

###核心价值

- **一次映射，五重合规**：每个技能同时标注 ATT&CK、NIST CSF、ATLAS、D3FEND、AI RMF
- **26 个安全领域**：从云安全到 OT/ICS，从威胁狩猎到数字取证
- **AI Native**：专为 AI Agent 设计，前端matter 仅 ~30 tokens，支持快速扫描所有 754 技能
- **真实专家工作流**：不是脚本集合，而是结构化的分析师执行手册

### 安装

```bash
pip install cybersecurity-skills-wrap
```

或从源码安装：

```bash
git clone https://github.com/q15004040209-creator/cybersecurity-skills-wrap.git
cd cybersecurity-skills-wrap
pip install -e .
```

### 快速开始

```python
from cybersecurity_skills_wrap import SkillLibrary

# 初始化技能库
library = SkillLibrary()

# 按关键词搜索技能
skills = library.search("memory forensics")
print(f"找到 {len(skills)} 个相关技能")
for skill in skills[:5]:
    print(f"  - {skill['name']}: {skill['description'][:60]}...")

# 按 MITRE ATT&CK 技术ID搜索
skills = library.search_by_attack("T1055")  # 进程注入
print(f"\nT1055 相关技能: {len(skills)}")

# 按领域搜索
cloud_skills = library.search_by_domain("cloud-security")
print(f"\n云安全技能: {len(cloud_skills)}")

# 获取完整技能详情
skill = library.get_skill("performing-memory-forensics-with-volatility3")
print(f"\n技能名: {skill['name']}")
print(f"标签: {skill['tags']}")
print(f"ATLAS: {skill['atlas_techniques']}")
print(f"D3FEND: {skill['d3fend_techniques']}")
print(f"NIST AI RMF: {skill['nist_ai_rmf']}")
print(f"NIST CSF: {skill['nist_csf']}")
```

### 框架映射示例

```python
from cybersecurity_skills_wrap import SkillLibrary

library = SkillLibrary()

# 获取映射到特定 ATT&CK 技术ID的所有技能
skills = library.get_skills_by_attack_id("T1071")  # 应用层协议
print(f"ATT&CK T1071 — 应用层协议")
for skill in skills:
    print(f"  → {skill['name']}")

# 获取 NIST CSF 2.0 类别中的所有技能
skills = library.get_skills_by_nist_csf("DE.CM")  # 检测 — 持续监控
print(f"\nNIST CSF DE.CM — 持续监控")
for skill in skills:
    print(f"  → {skill['name']}")

# 获取 ATLAS AI/ML 威胁检测技能
skills = library.get_skills_by_atlas("AML.T0047")  # 模型规避
print(f"\nATLAS AML.T0047 — 模型规避")
for skill in skills:
    print(f"  → {skill['name']}")
```

### 五大框架覆盖

```
✅ MITRE ATT&CK v19.1     — 15 个战术，286 个技术
✅ NIST CSF 2.0           — 6 个功能，22 个类别
✅ MITRE ATLAS v5.4 — 16 个战术，84 个技术（AI/ML 威胁）
✅ MITRE D3FEND v1.3      — 7 个类别，267 个防御对策
✅ NIST AI RMF 1.0        — 4 个功能，72 个子类别
```

### 26 个安全领域

云安全 · 威胁狩猎 · 威胁情报 · Web 应用安全 · 网络安全 · 恶意软件分析 · 数字取证 · 安全运营 · 身份与访问管理 · SOC 运营 · 容器安全 · OT/ICS 安全 · API 安全 · 漏洞管理 · 事件响应 · 红队攻防 · 渗透测试 · 端点安全 · DevSecOps · 钓鱼防御 · 密码学 · 零信任架构 · 移动安全 · 勒索软件防御 · 合规与治理 · 欺骗技术

### 开源协议

Apache 2.0 — 与上游项目保持一致

---

## 📦 Package Structure

```
cybersecurity_skills_wrap/
├── __init__.py
├── core.py          # SkillLibrary 核心类
├── parser.py        # YAML frontmatter 解析器
├── search.py        # 多维度搜索功能
├── frameworks.py    # 框架映射查询
└── demo.py          # 演示脚本
```

##🔗 Links

- **上游项目**: [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)
- **本仓库**: [q15004040209-creator/cybersecurity-skills-wrap](https://github.com/q15004040209-creator/cybersecurity-skills-wrap)
- **agentskills.io 标准**: [https://agentskills.io](https://agentskills.io)