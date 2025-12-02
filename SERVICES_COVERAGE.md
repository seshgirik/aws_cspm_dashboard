# AWS Security Services Coverage

This document outlines all AWS security services covered by the sample data generator, aligned with the comprehensive AWS security architecture.

## 📊 Coverage Summary

**Total Findings Generated:** 85+  
**Services Covered:** 17 AWS Security Services  
**Finding Categories:** 10 distinct security categories

---

## 🛡️ Security Services Matrix

| Category | Service | What It Provides | Sample Findings |
|----------|---------|------------------|-----------------|
| **Threat Detection** | GuardDuty | Threat alerts, anomalies | Malicious IPs, crypto mining, unusual API calls |
| **API Visibility** | CloudTrail | API call logs, IAM activity | Unauthorized API calls, policy changes, logging disabled |
| **Config Compliance** | AWS Config | Resource compliance, drift | Configuration drift, compliance violations, missing tags |
| **Vulnerability Scanning** | Inspector | EC2, ECR, Lambda CVEs | Critical CVE vulnerabilities, outdated runtimes |
| **Sensitive Data** | Macie | S3 PII scans | Unencrypted PII, financial data, exposed credentials |
| **Access Analysis** | IAM Access Analyzer | Public/cross-account access | Public S3 buckets, cross-account IAM roles |
| **Network Metrics** | VPC Flow Logs | Allowed/denied traffic | Suspicious outbound traffic, brute force, port scanning |
| **Edge Security** | WAF, Shield, CloudFront Logs | L7 threats, DDoS | SQL injection, XSS attacks, DDoS mitigation |
| **DNS Visibility** | Route53 DNS Logs | Malicious domain activity | DNS tunneling, DGA patterns, malicious domains |
| **Central Aggregation** | Security Hub | Unified findings | Aggregates all findings from above services |

---

## 📋 Detailed Findings by Service

### 1. GuardDuty (5 findings)
- **Purpose:** Intelligent threat detection using ML
- **Findings:**
  - EC2 instance communicating with malicious IPs
  - Unusual API call patterns (reconnaissance)
  - Cryptocurrency mining activity

### 2. CloudTrail Events (5 findings)
- **Purpose:** API activity monitoring and audit logging
- **Findings:**
  - Unauthorized API calls from unusual locations
  - IAM policy modifications by unauthorized users
  - Disabled CloudTrail logging (defense evasion)
  - Suspicious console logins without MFA
  - Root account usage violations

### 3. AWS Config (4 findings)
- **Purpose:** Resource configuration compliance tracking
- **Findings:**
  - Configuration drift from baseline
  - Non-compliant resources (prohibited ports)
  - Unauthorized resource modifications
  - Missing required tags

### 4. Inspector (4 findings)
- **Purpose:** Vulnerability scanning for workloads
- **Findings:**
  - Critical CVE vulnerabilities in EC2 instances
  - Outdated Lambda runtimes with vulnerabilities
  - ECR container images with security flaws
  - Network exposure through security groups

### 5. Macie (4 findings)
- **Purpose:** S3 sensitive data discovery
- **Findings:**
  - Unencrypted PII (SSN, credit cards, emails)
  - Sensitive financial data exposure
  - Exposed AWS credentials and API keys
  - PHI/healthcare data without HIPAA controls

### 6. IAM Access Analyzer (4 findings)
- **Purpose:** Identify public and cross-account access
- **Findings:**
  - S3 buckets with public internet access
  - IAM roles allowing external account access
  - Lambda functions with public resource policies
  - KMS keys accessible by external accounts

### 7. VPC Flow Logs (4 findings)
- **Purpose:** Network traffic analysis
- **Findings:**
  - Unusual outbound traffic to suspicious IPs
  - High volume rejected connections (brute force)
  - Data exfiltration to unexpected geolocations
  - Port scanning activity detection

### 8. WAF & Shield (4 findings)
- **Purpose:** Web application protection and DDoS mitigation
- **Findings:**
  - SQL injection attack attempts
  - Cross-site scripting (XSS) patterns
  - DDoS attacks (volumetric)
  - Rate limiting violations (credential stuffing)

### 9. Route53 DNS Logs (4 findings)
- **Purpose:** DNS query monitoring for threats
- **Findings:**
  - DNS queries to malware C2 domains
  - DNS tunneling for data exfiltration
  - Domain generation algorithm (DGA) patterns
  - Queries to newly registered domains (phishing)

### 10. S3 (4 findings)
- **Purpose:** Object storage security
- **Findings:**
  - Missing server-side encryption
  - Public access blocks not configured
  - Versioning not enabled
  - Bucket allows public READ access

### 11. EC2 (5 findings)
- **Purpose:** Compute security
- **Findings:**
  - Not managed by Systems Manager
  - Unrestricted SSH access (0.0.0.0/0)
  - Public IP addresses
  - Unencrypted EBS volumes
  - Unrestricted RDP access

### 12. IAM (5 findings)
- **Purpose:** Identity and access management
- **Findings:**
  - Root account access keys exist
  - Weak password policies
  - Unused credentials (90+ days)
  - Full administrative privileges
  - MFA not enabled

### 13. RDS (3 findings)
- **Purpose:** Database security
- **Findings:**
  - Database instances not encrypted
  - Public accessibility enabled
  - Automated backups disabled

### 14. Lambda (2 findings)
- **Purpose:** Serverless compute security
- **Findings:**
  - No dead-letter queue configured
  - Not running in VPC

### 15. KMS (1 finding)
- **Purpose:** Encryption key management
- **Findings:**
  - Key rotation not enabled

### 16. ELB (2 findings)
- **Purpose:** Load balancer security
- **Findings:**
  - ALB not dropping invalid headers
  - Classic LB without connection draining

### 17. CloudTrail Configuration (2 findings)
- **Purpose:** Audit trail configuration
- **Findings:**
  - Not enabled in all regions
  - Log file validation disabled

---

## 🎯 MITRE ATT&CK Coverage

The sample findings map to various MITRE ATT&CK tactics:

- **Initial Access:** Brute force, phishing, exploit public-facing apps
- **Execution:** Malware, cryptocurrency mining
- **Persistence:** Valid accounts
- **Privilege Escalation:** IAM policy manipulation
- **Defense Evasion:** Disable logging
- **Credential Access:** Credential stuffing
- **Discovery:** Network/cloud service discovery
- **Command & Control:** C2 communication, DNS tunneling, DGA
- **Exfiltration:** Data transfer to unusual locations
- **Impact:** DDoS, ransomware indicators

---

## 🔄 Data Flow Architecture

```
AWS Services → Security Services → Security Hub → S3 → Athena → QuickSight
                                                                      ↓
GuardDuty ──────────────┐                                     Dashboards
CloudTrail ─────────────┤                                     & Analytics
Config ─────────────────┤
Inspector ──────────────┤
Macie ──────────────────┤→ Security Hub → EventBridge → Firehose → S3
Access Analyzer ────────┤   (Centralized)                            ↓
VPC Flow Logs ──────────┤                                         Athena
WAF/Shield ─────────────┤                                        Queries
Route53 DNS ────────────┘
```

---

## 🚀 Use Cases

This comprehensive sample data is ideal for:

1. **Security Hub Demos:** Show unified security findings
2. **SIEM Integration Testing:** Feed into Splunk, Datadog, etc.
3. **Incident Response Training:** Realistic security scenarios
4. **Compliance Reporting:** PCI-DSS, HIPAA, SOC 2, etc.
5. **Security Analytics:** Build dashboards with QuickSight/Athena
6. **Detection Engineering:** Test SIEM rules and alerts
7. **Executive Reporting:** Security posture visibility
8. **Red Team/Blue Team:** Attack simulation data

---

## 📈 Sample Queries

### Query 1: Critical Findings by Service
```sql
SELECT 
    REGEXP_EXTRACT(GeneratorId, '([^/]+)$') as Service,
    COUNT(*) as CriticalCount
FROM SecurityHub.securityhubfindingsview
WHERE Severity = 'CRITICAL'
GROUP BY REGEXP_EXTRACT(GeneratorId, '([^/]+)$')
ORDER BY CriticalCount DESC;
```

### Query 2: Top 10 Security Issues
```sql
SELECT 
    FindingTitle,
    Severity,
    COUNT(*) as Occurrences
FROM SecurityHub.securityhubfindingsview
GROUP BY FindingTitle, Severity
ORDER BY Occurrences DESC
LIMIT 10;
```

### Query 3: Threat Detection Timeline
```sql
SELECT 
    DATE_TRUNC('day', CreatedAt) as Day,
    COUNT(*) as ThreatCount
FROM SecurityHub.securityhubfindingsview
WHERE ComplianceStatus = 'WARNING'
GROUP BY DATE_TRUNC('day', CreatedAt)
ORDER BY Day;
```

### Query 4: Non-Compliant Resources by Region
```sql
SELECT 
    Region,
    ResourceType,
    COUNT(*) as Count
FROM SecurityHub.securityhubfindingsview
WHERE ComplianceStatus = 'NON_COMPLIANT'
GROUP BY Region, ResourceType
ORDER BY Count DESC;
```

---

## 🔗 Integration Points

### Security Hub Integration
All findings follow AWS Security Hub Finding Format (ASFF), making them compatible with:
- AWS Security Hub console
- AWS EventBridge rules
- Custom SIEM integrations
- Third-party security tools

### QuickSight Dashboards
Create visualizations for:
- Compliance posture over time
- Severity distribution by service
- Top security risks
- Resource compliance by account/region
- Threat detection trends

---

Generated: November 2025  
Version: 2.0  
Findings Count: 85+
