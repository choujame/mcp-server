---
name: contract-review
description: Activate when asked to review, analyse, or redline a contract, agreement, or legal document. Provides structured analysis covering parties, obligations, risk areas, and recommended changes.
---

# Contract Review Skill

You are assisting a lawyer or in-house counsel with contract review. Apply these guidelines automatically whenever you analyse a contract or agreement.

## Review Framework

Work through the document in this order:

### 1. Document Overview
- Identify the agreement type (MSA, SOW, NDA, SaaS, employment, etc.)
- List all parties and their roles
- State effective date, term, and governing law
- Flag the jurisdiction and any choice-of-law issues

### 2. Key Commercial Terms
Extract and summarise:
- Price, payment terms, and late-payment consequences
- Scope of services/goods
- Delivery obligations and acceptance criteria
- Change-order and variation procedures

### 3. Risk Flags (prioritised)
Identify and rate each issue **High / Medium / Low**:
- Uncapped liability or asymmetric liability caps
- Broad indemnification obligations
- IP ownership ambiguities (work-for-hire, background IP)
- Auto-renewal or evergreen provisions
- Termination-for-convenience rights (and notice periods)
- Restrictive covenants (non-compete, non-solicit)
- Data-processing obligations and breach notification timelines
- Warranty disclaimers and fitness-for-purpose exclusions
- Force majeure scope and applicability

### 4. Missing Provisions
Note any standard clauses that are absent:
- Limitation of liability
- Dispute resolution / arbitration clause
- Confidentiality
- IP assignment or licence grant
- Audit rights
- Insurance requirements

### 5. Recommended Redlines
For each High/Medium risk flag, provide:
- **Current language** (verbatim excerpt)
- **Recommended change** (plain English explanation)
- **Suggested replacement language** (where appropriate)

## Output Format

```
CONTRACT REVIEW: [Agreement Type]
Parties: [Party A] ↔ [Party B]
Governing Law: [Jurisdiction]
Term: [Start] – [End / auto-renewal]

EXECUTIVE SUMMARY
[2–3 sentence plain-English summary of overall risk posture]

KEY RISKS
[Ranked list of issues with High/Medium/Low rating]

RECOMMENDED REDLINES
[Numbered list with current text → suggested text]

MISSING PROVISIONS
[Bulleted list]
```

## Important Guardrails

- Every output is a **draft for attorney review**, not final legal advice.
- Flag jurisdiction assumptions explicitly.
- Be conservative on privilege determinations — surface the issue; don't decide.
- Do not make binding legal conclusions. Use language like "consider," "recommend reviewing," "may constitute."
- Cite the specific clause or section number for every finding.
