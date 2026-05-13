---
name: legal-risk-assessment
description: Activate when asked to assess, evaluate, or rate the legal risk of a document, clause, transaction, or situation. Provides structured risk scoring with mitigation recommendations.
---

# Legal Risk Assessment Skill

Provide structured legal risk assessments for contracts, transactions, policies, and business decisions.

## Risk Scoring Framework

Rate each identified risk on two axes:
- **Likelihood**: Unlikely (1) / Possible (2) / Probable (3)
- **Impact**: Low (1) / Significant (2) / Severe (3)
- **Risk Score** = Likelihood × Impact (1–9)

| Score | Level | Action |
|-------|-------|--------|
| 7–9   | 🔴 Critical | Escalate; do not proceed without legal sign-off |
| 4–6   | 🟠 High | Negotiate mitigation; obtain management approval |
| 2–3   | 🟡 Medium | Document and monitor; consider standard protections |
| 1     | 🟢 Low | Note for record; no action required |

## Assessment Areas

### 1. Contractual Risk
- Liability exposure (uncapped, asymmetric, consequential damages)
- Indemnification obligations
- Warranty commitments
- Termination rights and consequences

### 2. Regulatory & Compliance Risk
- Applicable regulations (GDPR, CCPA, SOX, HIPAA, industry-specific)
- Licensing requirements
- Sanctions and export controls
- Anti-bribery / anti-corruption (FCPA, UK Bribery Act)

### 3. IP Risk
- Ownership of work product
- Licence scope and field-of-use restrictions
- Infringement exposure
- Trade secret protection

### 4. Reputational / Operational Risk
- Reputational harm from association with counterparty
- Operational dependency risk (sole-source, critical path)
- Data breach / security obligations

## Output Format

```
LEGAL RISK ASSESSMENT
Subject: [Document / Transaction / Situation]
Date: [Assessment date]
Prepared by: AI draft — attorney review required

OVERALL RISK RATING: [Critical / High / Medium / Low]

RISK REGISTER
# | Risk Description | Likelihood | Impact | Score | Level | Mitigation
--|-----------------|------------|--------|-------|-------|----------
[rows]

PRIORITY MITIGATIONS
1. [Most critical action]
2. [Second action]
...

ASSUMPTIONS & LIMITATIONS
[List jurisdiction assumptions, missing information, areas requiring specialist review]
```

## Guardrails

- Scores are indicative only — actual risk depends on facts not always visible in the document.
- All assessments are attorney-review drafts.
- Escalate novel regulatory questions to specialist counsel.
- Do not opine on litigation probability or litigation value.
