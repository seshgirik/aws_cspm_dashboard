# Cloud Security Architecture Summary

This document accompanies the multi-page draw.io diagram (`cloud_security_architecture.drawio`).

## Pages Overview
1. LLM Multi-Account Platform – Core topology isolating Customer, Bedrock Service, and Model Provider (Escrow) accounts with PrivateLink and strict IAM/SCP boundaries.
2. SecOps Remediation Pipeline – Bedrock Agent assisted remediation flow with knowledge base, Lambda action group, pipeline validation, and controlled SSM execution path.
3. Security Controls Overlay – Layered control families (Network, Identity & Access, Data Protection, AI Safety, Supply Chain, Observability/Response, Governance, Risk Evolution).

## XML Escaping Note
If you edit the diagram XML manually:
- Always escape raw ampersands in attribute values: use `&amp;` not `&`.
- The original parse error (`xmlParseEntityRef: no name`) was caused by unescaped `&` in labels like `IAM Boundary & SCPs`.
- Verified fix: replaced occurrences with `&amp;`.

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Diagram won't open / parse error on `xmlParseEntityRef` | Unescaped `&` | Replace with `&amp;` and re-open | 
| Appears blank | Page zoom too small or layers collapsed | Use Fit (Cmd+Shift+H) in diagrams.net |
| Missing styles | Stripped while copy/paste via chat | Upload the raw `.drawio` file directly |

## Next Improvements (Optional)
- Add threat flow annotations (MITRE ATT&CK technique references) to page 3.
- Include data classification color legend.
- Embed version + checksum metadata node.

---
Last updated: 2025-09-20
