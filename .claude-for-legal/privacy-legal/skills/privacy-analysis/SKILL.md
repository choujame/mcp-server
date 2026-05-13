---
name: privacy-analysis
description: Activate when asked to assess privacy risks, conduct a privacy impact assessment (PIA/DPIA), or review a product, feature, or process for data protection compliance.
---

# Privacy Analysis Skill

Conduct structured privacy analysis for products, features, processes, and agreements under GDPR, CCPA/CPRA, and equivalent frameworks.

## Analysis Framework

### 1. Data Mapping
Identify and document:
- **Categories of personal data** collected/processed
- **Data subjects** affected (employees, consumers, children, special categories)
- **Processing purposes** and legal basis for each (GDPR Article 6/9)
- **Data flows**: collection → storage → use → sharing → deletion
- **Third parties / processors** who receive data
- **Cross-border transfers** and applicable transfer mechanisms (SCCs, adequacy, BCRs)

### 2. Legal Basis Assessment (GDPR / Equivalent)
For each processing activity:
- Consent: freely given, specific, informed, unambiguous? Withdrawable?
- Legitimate interests: documented LIA? Can data subject object?
- Contract performance: necessary for contract?
- Legal obligation: which specific law?

### 3. Risk Identification
Evaluate risks to data subjects:
| Risk | Likelihood | Severity | Mitigation |
|------|-----------|----------|-----------|
| Unauthorised access | | | |
| Unintended secondary use | | | |
| Re-identification | | | |
| Cross-border transfer without safeguards | | | |
| Retention beyond purpose | | | |

### 4. DPIA Trigger Check (GDPR Art. 35)
Flag if any of the following apply (DPIA required):
- Systematic profiling
- Large-scale processing of special category data
- Systematic monitoring of publicly accessible areas
- Novel technology
- Automated decision-making with legal/significant effects
- Children's data at scale

### 5. Required Notices & Rights Mechanisms
Verify:
- Privacy notice covers all processing purposes
- Data subject rights procedures in place (access, erasure, portability, objection)
- Breach notification procedure (72-hour GDPR requirement; 30/45-day CCPA)
- DPA/DPO appointment where required

## Output Format

```
PRIVACY ANALYSIS
Subject: [Product / Feature / Process]
Frameworks: [GDPR, CCPA/CPRA, etc.]
Date: [Assessment date]

DATA MAP SUMMARY
[Categories of data, subjects, purposes, legal basis]

RISK SUMMARY: [High / Medium / Low overall]
[Table of identified risks]

DPIA REQUIRED: [Yes / No / Borderline — confirm with DPO]

COMPLIANCE GAPS
[Numbered list with regulatory reference and remediation]

RECOMMENDATIONS
[Prioritised action items]
```

## Guardrails

- All outputs are drafts for DPO / attorney review.
- Novel processing activities should be reviewed by specialist privacy counsel.
- Do not conclude that processing is lawful — conclude only that it "appears to meet" specified requirements.
- Flag explicitly where local derogations or member-state implementations may differ from GDPR baseline.
