Threat Model Report
Overview
This threat model evaluates the security posture of an AWS-based application architecture involving
Kubernetes (Tectonic), Apache Airflow, Spark, S3 buckets, and managed databases. It uses the STRIDE
methodology to identify potential threats and propose mitigations.
--------------------------------------------------------------------------------
STRIDE Analysis
1. Entry Points & Interfaces
#### API Gateway (Public Subnet)
- **Threats**:
- Spoofing (impersonation of users)
- Information Disclosure (data leakage)
- Denial of Service (API abuse)
- **Mitigations**:
- Enforce OAuth2, mTLS, or IAM-based auth
- Enable rate limiting, WAF, IP whitelisting
- API Gateway logging for audits
#### Airflow UI ELB
- **Threats**:
- Spoofing or Elevation of Privilege (EoP)
- Tampering with DAGs or workflows
- **Mitigations**:
- Use SSO + RBAC
- Enforce TLS, enable audit logging
#### SSM Bastion Access
- **Threats**:
- Spoofing (compromised credentials)
- Lateral movement (EoP)
- **Mitigations**:
- Use MFA and session timeout policies
- Monitor sessions with SSM Session Manager & CloudTrail
--------------------------------------------------------------------------------
2. Data Storage & Transmission
#### Databases (Customer DB, Airflow DB, PostgreSQL)
- **Threats**:
- Information Disclosure (data exfiltration)
- Tampering (unauthorized modification)
- **Mitigations**:
- Use encryption at rest (RDS, KMS)
- Apply IAM auth and subnet restrictions
- Secure backups with encryption
#### S3 Buckets (RAW, DATASETS, REPORTS, DACS)
- **Threats**:
- Information Disclosure (public access or IAM misconfig)
- **Mitigations**:
- Block public access and configure fine-grained policies
- Enable SSE (SSE-S3 or SSE-KMS)
- Enable object lock, access logging
--------------------------------------------------------------------------------
3. Kubernetes Cluster (Tectonic Workers)
- **Threats**:
- Tampering (malicious containers)
- EoP (privileged pods)
- **Mitigations**:
- Enforce PodSecurityPolicies or OPA/Gatekeeper
- Limit pod IAM roles and enable egress controls
- Use image signing and scanning (cosign, Trivy)
--------------------------------------------------------------------------------
4. Spark Cluster
- **Threats**:
- DoS (uncontrolled job submission)
- Information Disclosure (sensitive log data)
- **Mitigations**:
- Resource limits and job throttling
- Enable encrypted logging to CloudWatch with restricted access
--------------------------------------------------------------------------------
5. Observability (Datadog, CloudWatch, Sentry)
- **Threats**:
- Information Disclosure (secrets or PII in logs)
- **Mitigations**:
- Sanitize logs, redact secrets
- Secure API ingestion tokens
- Enable anomaly detection and alerting
--------------------------------------------------------------------------------
6. VPC Peering
- **Threats**:
- Lateral movement across environments
- **Mitigations**:
- Apply strict route table and security group filters
- Use separate IAM boundaries
- Monitor with GuardDuty and VPC flow logs
--------------------------------------------------------------------------------
Additional Mitigation Recommendations
| Risk Category | Mitigation |
|----------------------------|-------------------------------------------------------------------|
| IAM Misconfigurations | Least privilege, role assumptions, service control policies |
| Secrets Management | Use Secrets Manager or Vault, avoid secrets in code |
| CI/CD Security | Scan for secrets, enforce image signing and validation |
| Monitoring and Auditing | Use GuardDuty, Config, CloudTrail, and centralized log ingestion |
| Compliance and Governance | Enable AWS Audit Manager and map to control frameworks |
--------------------------------------------------------------------------------
Periodic Activities
- Conduct Red Team assessments, particularly on Bastion and Kubernetes components
- Perform threat simulations (e.g., Chaos Engineering, AWS FIS)
- Validate IAM and resource policies using AWS Access Analyzer
- Rotate TLS certificates and validate expiry monitoring
--------------------------------------------------------------------------------
Conclusion
This architecture is well-structured but must continuously evolve to respond to changing threats. The
recommendations provided above focus on reinforcing access control, data protection, secure configurations,
and proactive monitoring to ensure a robust cloud security posture.
--------------------------------------------------------------------------------
*Prepared by: Security Analysis Team*
*Date: 2025-05-14*