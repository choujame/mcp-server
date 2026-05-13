---
name: nda-triage
description: Activate when asked to review, triage, or compare an NDA (non-disclosure agreement), confidentiality agreement, or CDA. Provides rapid structured triage highlighting key deviations from standard form.
---

# NDA Triage Skill

Rapidly triage NDAs for in-house counsel or external lawyers. Focus on deviations from market-standard positions — don't re-explain boilerplate.

## Triage Checklist

### Threshold Questions
1. **One-way or mutual?** Note which party discloses.
2. **Scope of Confidential Information** — Is it defined by: written designation only? Oral disclosures included? Overly broad (e.g., "all information shared")?
3. **Permitted Purposes** — Is the permitted use clearly limited to a specific transaction or evaluation?

### Key Terms to Extract
| Term | Standard Position | This NDA |
|------|------------------|----------|
| Term | 2–3 years | ? |
| Survival of obligations | 3–5 years post-disclosure | ? |
| Return/destroy obligation | Yes | ? |
| Residuals clause | Absent (or limited to unaided memory) | ? |
| Injunctive relief acknowledged | Yes | ? |
| Governing law | Neutral/recipient-friendly | ? |

### Red Flags
- **Residuals clause** — allows use of "residual knowledge" retained in employees' unaided memory; effectively guts the NDA for know-how.
- **Overly broad definition** — captures publicly available information or information already known to recipient.
- **No survival period** — obligations end when term ends, not when disclosure ends.
- **Unilateral injunctive relief** — only one party can seek it.
- **Broad assignment** — NDA binds successors without restricting the disclosing party from assigning obligations to a competitor.
- **Missing exclusions** — standard carve-outs (public domain, independent development, court order) should always be present.

## Output Format

```
NDA TRIAGE
Type: [One-way / Mutual]
Disclosing Party: [Name]
Receiving Party: [Name]
Term: [Duration] | Survival: [Duration]
Governing Law: [Jurisdiction]

TRAFFIC LIGHT SUMMARY
🔴 High concern: [list]
🟡 Moderate concern: [list]
🟢 Acceptable: [list]

DEVIATION TABLE
[Table showing standard vs this NDA for each key term]

RECOMMENDED ACTIONS
[Numbered list of specific changes to negotiate]
```

## Guardrails

- This is a triage, not a comprehensive review. Flag if a fuller review is warranted.
- All outputs are drafts for attorney review.
- Explicitly note governing law and flag if it is unusual for the client's home jurisdiction.
