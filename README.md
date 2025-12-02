# AWS Security Findings Sample Data Generator

This tool generates realistic sample data for various AWS security issues detected by AWS Security Hub and other AWS security services.

## Overview

The generator creates sample findings for **85+ security issues** across all major AWS security services:

### Configuration & Compliance
- **AWS Config** (4): Configuration drift, compliance violations, unauthorized changes, missing tags
- **S3** (4): Encryption, public access, versioning, bucket policies
- **EC2** (5): Security groups, public IPs, EBS encryption, SSH/RDP access
- **IAM** (5): Root keys, MFA, password policies, excessive permissions
- **RDS** (3): Encryption, public access, backups
- **CloudTrail** (2): Multi-region trails, log validation
- **Lambda** (2): Dead-letter queues, VPC configuration
- **KMS** (1): Key rotation
- **ELB** (2): Security configurations

### Threat Detection
- **GuardDuty** (3): Malicious IPs, unusual API calls, cryptocurrency mining
- **VPC Flow Logs** (4): Suspicious traffic, brute force attacks, data exfiltration, port scanning
- **Route53 DNS Logs** (4): Malicious domains, DNS tunneling, DGA activity, newly registered domains

### Vulnerability Scanning
- **Inspector** (4): CVE vulnerabilities, outdated runtimes, container vulnerabilities, network exposure

### Sensitive Data Discovery
- **Macie** (4): PII data, financial data, exposed credentials, PHI/healthcare data

### Access Analysis
- **IAM Access Analyzer** (4): Public access, cross-account access, public Lambda policies, external KMS access

### Network Security
- **WAF & Shield** (4): SQL injection, XSS attacks, DDoS attacks, rate limiting violations

### API Activity Monitoring
- **CloudTrail Events** (5): Unauthorized API calls, IAM changes, logging disabled, suspicious logins, root account usage

## Features

- Generates findings with realistic AWS resource ARNs
- Multiple severity levels: **CRITICAL**, **HIGH**, **MEDIUM**, **LOW**
- Compliance statuses: **NON_COMPLIANT**, **WARNING**
- Organized by date for S3/Athena compatibility
- Summary reports with statistics

## Usage

### Basic Usage

```bash
python3 generate_security_findings.py
```

This will generate:
- `security_findings_all.json` - All findings in a single file
- `findings_by_date/` - Findings organized by date (YYYY/MM/DD format)
- `findings_summary.json` - Statistical summary of findings

### Customization

Edit the script to customize:
- Number of findings per service (default: 5)
- Account IDs
- Regions
- Add new security issue types

## Output Format

Findings are generated in AWS Security Hub format compatible with the CloudFormation template structure:

```json
{
  "id": "uuid",
  "detail": {
    "findings": [{
      "AwsAccountId": "123456789012",
      "CreatedAt": "2024-11-24T10:30:00.000Z",
      "UpdatedAt": "2024-11-24T12:30:00.000Z",
      "Description": "Security issue description",
      "ProductArn": "arn:aws:securityhub:...",
      "GeneratorId": "aws-foundational-security-best-practices/...",
      "Region": "us-east-1",
      "Compliance": {"status": "NON_COMPLIANT"},
      "Workflow": {"status": "NEW"},
      "Types": "Software and Configuration Checks/...",
      "Title": "Issue title",
      "Severity": {"Label": "HIGH"},
      "Resources": [{
        "Id": "arn:aws:...",
        "Type": "AwsS3Bucket"
      }]
    }]
  }
}
```

## Integration with CloudFormation Template

The generated data is compatible with the `S3AthenaWorkshopTemplate.yaml` template:

1. Deploy the CloudFormation stack
2. Upload generated findings to the S3 bucket created by the template
3. Query findings using Athena with the pre-configured views

### Upload to S3

```bash
# Upload date-organized findings
aws s3 sync findings_by_date/ s3://YOUR-BUCKET-NAME/raw/firehose/
```

### Query in Athena

```sql
SELECT * FROM SecurityHub.securityhubfindingsview
WHERE Severity = 'CRITICAL'
ORDER BY CreatedAt DESC;
```

## Sample Statistics

Typical generation produces:
- **85+ total findings** (5 per service across 17 services)
- **Severity distribution:**
  - CRITICAL: 10 findings
  - HIGH: 34 findings  
  - MEDIUM: 29 findings
  - LOW: 12 findings
- **Compliance statuses:**
  - NON_COMPLIANT: 52 findings
  - WARNING: 33 findings (threat/anomaly detections)
- Findings distributed across multiple AWS regions (us-east-1, us-west-2, eu-west-1, ap-southeast-1)
- Covers all major AWS security service categories

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## License

This tool generates sample data for testing and demonstration purposes only.
