---
name: case-analysis
description: Activate when asked to analyse, summarise, or assess a legal case, dispute, claim, or set of facts for litigation purposes.
---

# Case Analysis Skill

Provide structured legal case analysis for litigation matters, including fact summaries, legal issue identification, strategy assessment, and evidentiary mapping.

## Case Analysis Framework

### 1. Matter Overview
- **Parties**: Claimant(s) vs. Defendant(s) (and any third parties)
- **Jurisdiction & Court**: Applicable procedural rules
- **Stage**: Pre-litigation / Pleadings / Discovery / Trial / Appeal
- **Key dates**: Limitation periods, hearing dates, deadlines

### 2. Facts Summary
Organise facts:
- **Undisputed facts**: agreed or clearly established
- **Disputed facts**: contested and requiring proof
- **Unknown facts**: gaps requiring investigation or discovery
- **Adverse facts**: facts that hurt our client's case

### 3. Legal Issues
For each claim and defence:
- **Element**: what must be proven
- **Standard of proof**: balance of probabilities / beyond reasonable doubt / clear and convincing
- **Current strength**: Strong / Moderate / Weak / Unknown
- **Key authority**: leading case or statute

### 4. Evidence Mapping
| Element | Evidence Supporting | Evidence Against | Gap / Needed |
|---------|-------------------|-----------------|-------------|
| [Element 1] | | | |
| [Element 2] | | | |

### 5. Damages / Remedy Assessment
- **Claimed**: [amount / remedy]
- **Supportable**: [realistic range with basis]
- **Mitigation obligations**: [what client must do to mitigate]
- **Counterclaims / set-off**: [any exposure from defendant's side]

### 6. Strategic Assessment
- **Strengths**: [top 3]
- **Weaknesses**: [top 3]
- **Settlement range**: [if appropriate to assess]
- **Recommended next steps**: [discovery priorities, motions, settlement approach]

## Output Format

```
CASE ANALYSIS: [Matter Name / Reference]
Client: [Client name and position]
Jurisdiction: [Court and applicable law]
Stage: [Current procedural stage]

FACTS SUMMARY
[Undisputed | Disputed | Unknown | Adverse — bulleted under each]

LEGAL ISSUES & ELEMENT CHART
[Table: Element | Standard | Strength | Authority]

EVIDENCE MAP
[Table as above]

DAMAGES ASSESSMENT
Claimed: [X] | Supportable range: [Y–Z]

STRATEGIC ASSESSMENT
Strengths: [list]
Weaknesses: [list]
Recommended next steps: [numbered list]

PRIVILEGE NOTE
This analysis is prepared for the purpose of obtaining legal advice and is protected by attorney-client privilege / legal professional privilege.
```

## Guardrails

- All case analyses are attorney-review drafts.
- Litigation probability / win-rate assessments must not be given to clients without attorney sign-off.
- Never recommend settlement figures to clients directly — present a range for attorney consideration.
- Flag all limitation period issues prominently.
- Adverse facts must be disclosed to the responsible attorney even if not included in client-facing documents.
