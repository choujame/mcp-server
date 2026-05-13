# /commercial-legal:vendor-check

Review the vendor or supplier agreement provided, focusing on liability, IP, termination, and SLA provisions.

## Instructions

1. Read the agreement end-to-end.
2. Identify the parties, services/goods, and commercial terms.
3. Analyse and flag the following areas:

   **Liability & Indemnification**
   - Liability cap: amount, basis (fees paid, fixed, uncapped)
   - Consequential damages exclusion: present? Asymmetric?
   - Indemnification scope: IP infringement, personal injury, data breach?
   
   **IP Ownership**
   - Who owns deliverables / work product?
   - Background IP licences granted?
   - Is there a work-for-hire provision?
   
   **Termination**
   - Termination for convenience: by either party? Notice period?
   - Termination for cause: cure period? Definition of "material breach"?
   - Effect of termination: wind-down obligations, data return, transition assistance?
   
   **SLA / Service Levels**
   - Uptime commitments and measurement methodology
   - Remedies for SLA failure (credits, termination right, actual damages)
   - Exclusions from SLA (force majeure, customer-caused downtime)
   
   **Data & Security**
   - Data processing agreement / DPA in place?
   - Breach notification timeline
   - Audit rights
   - Subprocessor approval mechanism

4. Provide recommended redlines for High/Medium risk items.

If no agreement is provided, ask the user to paste the text or share the file path.

## Output

```
VENDOR AGREEMENT REVIEW: [Vendor Name]
Services: [Brief description]
Term: [Start – End]

RISK SUMMARY: [High / Medium / Low]

FINDINGS
[Categorised under: Liability | IP | Termination | SLA | Data/Security]

RECOMMENDED REDLINES
[Numbered list with current → suggested language]
```

> **Attorney review required.**
