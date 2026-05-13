# /litigation-legal:claim-chart

Build an element-by-element claim chart mapping patent claims, contract clauses, or legal elements to evidence or prior art.

## Instructions

1. Identify the claim type:
   - **Patent**: map each claim element to accused product / prior art
   - **Contract**: map each obligation to evidence of performance or breach
   - **Regulatory**: map each regulatory requirement to evidence of compliance or violation
2. Break the claim into discrete elements.
3. For each element, identify and cite:
   - Evidence supporting infringement / breach / violation
   - Evidence supporting non-infringement / performance / compliance
   - Evidentiary gaps requiring further discovery or expert analysis
4. Assign a strength rating per element: Strong / Moderate / Weak / Unknown.

If the claim text and/or evidence are not provided, ask for them before proceeding.

## Output Format

```
CLAIM CHART: [Claim / Clause Reference]
Type: [Patent / Contract / Regulatory]
Claimant position: [Infringement / Breach / Violation]

ELEMENT-BY-ELEMENT ANALYSIS

Element 1: [Quoted element text]
  Claim construction: [Brief construction if contested]
  Supporting evidence: [Cite documents, testimony, product specs]
  Counter-evidence: [Cite opposing evidence]
  Gap: [What is missing?]
  Strength: [Strong / Moderate / Weak / Unknown]

Element 2: [...]
[Repeat for each element]

OVERALL ASSESSMENT
Elements met: [X / Y]
Weakest element: [Element #]
Discovery priorities: [Numbered list]
```

> **Attorney review required.** Claim charts are attorney-work product. Treat as privileged and confidential.
