---
name: compliance
description: Activate when asked to check, verify, or assess compliance of a document, policy, process, or product against applicable legal or regulatory requirements.
---

# Compliance Checking Skill

Help legal and compliance teams verify that documents, policies, processes, and products meet applicable legal requirements.

## Compliance Framework

### Step 1: Identify Applicable Frameworks
Based on context, identify relevant regimes:
- **Data Privacy**: GDPR, CCPA/CPRA, PIPL, PDPA, etc.
- **Financial Services**: SOX, Dodd-Frank, MiFID II, PSD2
- **Healthcare**: HIPAA, HITECH, MDR/IVDR
- **Employment**: FLSA, ADA, Title VII, local equivalents
- **Consumer Protection**: FTC Act, UDAAP, consumer credit laws
- **Industry-Specific**: FCRA, GLBA, FERPA, COPPA

### Step 2: Requirement Mapping
For each applicable framework, map:
- Specific requirements that apply
- Current document/process status: ✅ Met / ⚠️ Partial / ❌ Gap / ❓ Unclear
- Evidence or clause supporting the assessment

### Step 3: Gap Analysis
For each gap:
- Describe the gap precisely
- Reference the specific regulatory provision (article/section)
- Assess severity: Blocking / Significant / Minor
- Recommend remediation steps

### Step 4: Jurisdiction Check
- Confirm which jurisdictions apply
- Flag conflicts between jurisdictions
- Note where the most restrictive rule applies (GDPR vs. CCPA, etc.)

## Output Format

```
COMPLIANCE REVIEW
Subject: [Document / Policy / Process / Product]
Frameworks Assessed: [List]
Jurisdiction(s): [List]

OVERALL COMPLIANCE STATUS
[Compliant / Partially Compliant / Non-Compliant — pending attorney review]

REQUIREMENT MAPPING
Framework | Requirement | Status | Evidence/Notes
---------|------------|--------|---------------
[rows]

GAPS & REMEDIATION
Priority | Gap Description | Regulatory Reference | Recommended Fix
--------|----------------|---------------------|----------------
[rows]

ASSUMPTIONS
[List jurisdiction assumptions, inapplicable frameworks noted but excluded, etc.]
```

## Guardrails

- Compliance assessments are attorney-review drafts only.
- Regulatory interpretation questions (novel or contested positions) must be escalated.
- Note explicitly where the assessment is based on public regulatory guidance vs. confirmed legal advice.
- Never advise that a business is "fully compliant" — use "appears to meet requirements as assessed."
