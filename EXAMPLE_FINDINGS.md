# Example AWS Security Findings

This document shows real examples from the generated sample data across all AWS security services.

---

## 🔴 Critical Severity Examples

### 1. Macie - Exposed PII Data
```json
{
  "Title": "S3 bucket contains unencrypted PII data",
  "Description": "Macie discovered 1,247 objects containing unencrypted personally identifiable information (PII) including credit card numbers, SSNs, and email addresses.",
  "Severity": "CRITICAL",
  "GeneratorId": "aws/macie",
  "ResourceType": "AwsS3Bucket",
  "ComplianceStatus": "NON_COMPLIANT"
}
```

### 2. IAM Access Analyzer - Public S3 Bucket
```json
{
  "Title": "S3 bucket allows public access from internet",
  "Description": "IAM Access Analyzer detected S3 bucket policy allowing anonymous public access from any AWS account or internet user.",
  "Severity": "CRITICAL",
  "GeneratorId": "aws/access-analyzer",
  "ResourceType": "AwsS3Bucket",
  "ComplianceStatus": "NON_COMPLIANT"
}
```

### 3. Route53 DNS - Malicious Domain Activity
```json
{
  "Title": "DNS queries to known malicious domains",
  "Description": "Route53 DNS logs show queries to 15 domains associated with malware C2 infrastructure from EC2 instances in production VPC.",
  "Severity": "CRITICAL",
  "GeneratorId": "aws/route53",
  "ResourceType": "AwsEc2Instance",
  "ComplianceStatus": "WARNING"
}
```

### 4. Inspector - Critical CVE Vulnerabilities
```json
{
  "Title": "EC2 instance has critical CVE vulnerabilities",
  "Description": "Inspector found 3 critical CVE vulnerabilities (CVE-2024-1234, CVE-2024-5678) on EC2 instance. Immediate patching required.",
  "Severity": "CRITICAL",
  "GeneratorId": "aws/inspector",
  "ResourceType": "AwsEc2Instance",
  "ComplianceStatus": "NON_COMPLIANT"
}
```

### 5. CloudTrail - Defense Evasion
```json
{
  "Title": "Disabled CloudTrail logging detected",
  "Description": "CloudTrail event shows StopLogging API call, attempt to disable audit logging and evade detection.",
  "Severity": "CRITICAL",
  "GeneratorId": "aws/cloudtrail",
  "ResourceType": "AwsIamUser",
  "ComplianceStatus": "NON_COMPLIANT"
}
```

---

## 🟠 High Severity Examples

### 6. WAF - SQL Injection Attacks
```json
{
  "Title": "WAF detected SQL injection attack attempts",
  "Description": "AWS WAF blocked 234 SQL injection attempts targeting application endpoint /api/users in the last hour.",
  "Severity": "HIGH",
  "GeneratorId": "aws/waf",
  "ResourceType": "AwsElbLoadBalancer",
  "ComplianceStatus": "WARNING"
}
```

### 7. VPC Flow Logs - Suspicious Traffic
```json
{
  "Title": "Unusual outbound traffic to suspicious IP address",
  "Description": "VPC Flow Logs analysis detected abnormal outbound traffic pattern to known malicious IP 203.0.113.45 from private subnet.",
  "Severity": "HIGH",
  "GeneratorId": "aws/vpc-flow-logs",
  "ResourceType": "AwsEc2Instance",
  "ComplianceStatus": "WARNING"
}
```

### 8. GuardDuty - Cryptocurrency Mining
```json
{
  "Title": "Possible cryptocurrency mining activity detected",
  "Description": "EC2 instance is querying a domain associated with cryptocurrency mining.",
  "Severity": "HIGH",
  "GeneratorId": "aws/guardduty",
  "ResourceType": "AwsEc2Instance",
  "ComplianceStatus": "WARNING"
}
```

### 9. Config - Compliance Violation
```json
{
  "Title": "Non-compliant resource detected by Config rule",
  "Description": "Security group allows inbound traffic on prohibited port 23 (Telnet), violating organization security policy.",
  "Severity": "HIGH",
  "GeneratorId": "aws/config",
  "ResourceType": "AwsEc2SecurityGroup",
  "ComplianceStatus": "NON_COMPLIANT"
}
```

### 10. Route53 - DNS Tunneling
```json
{
  "Title": "DNS tunneling activity detected",
  "Description": "Abnormal DNS query patterns suggest data exfiltration via DNS tunneling with unusually long TXT record queries.",
  "Severity": "HIGH",
  "GeneratorId": "aws/route53",
  "ResourceType": "AwsEc2Instance",
  "ComplianceStatus": "WARNING"
}
```

---

## 🟡 Medium Severity Examples

### 11. Inspector - Network Exposure
```json
{
  "Title": "Network path allows exposure to internet",
  "Description": "Inspector network reachability analysis found EC2 instance with unnecessary internet exposure through security group configuration.",
  "Severity": "MEDIUM",
  "GeneratorId": "aws/inspector",
  "ResourceType": "AwsEc2Instance",
  "ComplianceStatus": "WARNING"
}
```

### 12. VPC Flow Logs - Brute Force Attack
```json
{
  "Title": "High volume of rejected connection attempts",
  "Description": "VPC Flow Logs show 15,000+ rejected connection attempts to port 22 from multiple source IPs, indicating potential SSH brute force attack.",
  "Severity": "MEDIUM",
  "GeneratorId": "aws/vpc-flow-logs",
  "ResourceType": "AwsEc2Instance",
  "ComplianceStatus": "WARNING"
}
```

### 13. Config - Configuration Drift
```json
{
  "Title": "Resource configuration drift detected",
  "Description": "AWS Config detected configuration drift on 12 resources that deviate from approved baseline configuration.",
  "Severity": "MEDIUM",
  "GeneratorId": "aws/config",
  "ResourceType": "AwsS3Bucket",
  "ComplianceStatus": "NON_COMPLIANT"
}
```

---

## 🟢 Low Severity Examples

### 14. Config - Missing Tags
```json
{
  "Title": "Required tags missing on resources",
  "Description": "Config compliance check found 47 EC2 instances missing required tags (Environment, Owner, CostCenter) for governance.",
  "Severity": "LOW",
  "GeneratorId": "aws/config",
  "ResourceType": "AwsEc2Instance",
  "ComplianceStatus": "NON_COMPLIANT"
}
```

---

## 📊 Findings Distribution by Service

| Service | Findings | Categories Covered |
|---------|----------|-------------------|
| Inspector | 5 | CVEs, Runtimes, Containers, Network |
| Macie | 5 | PII, Financial, Credentials, PHI |
| Access Analyzer | 5 | Public Access, Cross-Account |
| VPC Flow Logs | 5 | Traffic Analysis, Attacks |
| WAF/Shield | 5 | Web Attacks, DDoS |
| Route53 | 5 | DNS Threats |
| Config | 5 | Compliance, Drift |
| CloudTrail Events | 5 | API Activity, IAM Changes |
| GuardDuty | 5 | Threats, Anomalies |
| S3 | 5 | Encryption, Access |
| EC2 | 5 | Security Groups, Encryption |
| IAM | 5 | Policies, MFA |
| RDS | 3 | Encryption, Access, Backups |
| Lambda | 2 | DLQ, VPC |
| KMS | 1 | Key Rotation |
| ELB | 2 | Configuration |
| CloudTrail Config | 2 | Multi-region, Validation |

**Total: 85 findings across 17 services**

---

## 🎯 Sample Analytics Queries

### Finding Types Distribution
```sql
SELECT 
    CASE 
        WHEN Types LIKE '%TTPs%' THEN 'Threat Detection'
        WHEN Types LIKE '%CVE%' THEN 'Vulnerabilities'
        WHEN Types LIKE '%PII%' THEN 'Data Exposure'
        WHEN Types LIKE '%Access Analyzer%' THEN 'Access Issues'
        ELSE 'Configuration'
    END as FindingCategory,
    COUNT(*) as Count
FROM SecurityHub.securityhubfindingsview
GROUP BY 1;
```

### Security Posture Score
```sql
WITH severity_weights AS (
    SELECT 
        CASE Severity
            WHEN 'CRITICAL' THEN 10
            WHEN 'HIGH' THEN 7
            WHEN 'MEDIUM' THEN 4
            WHEN 'LOW' THEN 1
        END as weight,
        COUNT(*) as count
    FROM SecurityHub.securityhubfindingsview
    GROUP BY Severity
)
SELECT 
    100 - (SUM(weight * count) / 10.0) as SecurityScore
FROM severity_weights;
```

---

## 💡 Use Case Scenarios

### Scenario 1: Data Breach Investigation
A security analyst notices Macie findings showing exposed PII. They can correlate with:
- CloudTrail logs (who accessed the bucket?)
- Access Analyzer (is it publicly accessible?)
- VPC Flow Logs (any suspicious data transfers?)

### Scenario 2: Compliance Audit
For PCI-DSS compliance, filter findings:
- S3 encryption violations
- RDS public accessibility
- CloudTrail logging status
- VPC Flow Logs analysis

### Scenario 3: Incident Response
GuardDuty detects crypto mining:
1. Check VPC Flow Logs for network connections
2. Review CloudTrail for API activity
3. Inspect Inspector results for vulnerabilities
4. Analyze Route53 logs for DNS queries

---

## 🔗 Integration Examples

### Send to Slack
```python
import boto3
import json

def send_critical_to_slack(finding):
    if finding['Severity']['Label'] == 'CRITICAL':
        slack_webhook = 'https://hooks.slack.com/...'
        message = {
            'text': f"🚨 CRITICAL: {finding['Title']}",
            'attachments': [{
                'color': 'danger',
                'fields': [
                    {'title': 'Resource', 'value': finding['Resources'][0]['Id']},
                    {'title': 'Region', 'value': finding['Region']}
                ]
            }]
        }
        # Send to Slack...
```

### Create Jira Ticket
```python
def create_jira_ticket(finding):
    if finding['Severity']['Label'] in ['CRITICAL', 'HIGH']:
        jira_api = 'https://company.atlassian.net/rest/api/2/issue'
        ticket = {
            'fields': {
                'project': {'key': 'SEC'},
                'summary': finding['Title'],
                'description': finding['Description'],
                'issuetype': {'name': 'Security Vulnerability'},
                'priority': {'name': 'High'}
            }
        }
        # Create Jira ticket...
```

---

Generated: November 2025  
Sample Data Version: 2.0
