# AWS Security Services - Security Architect Interview Questions

**Comprehensive collection of AWS Security Services interview questions covering GuardDuty, S3 Security, Security Hub, Inspector, WAF, and Shield for security architect roles.**

---

## Table of Contents

### Part 1: Core Security Services (Questions 1-10)
1. [GuardDuty Automated Response](#guardduty-automated-response)
2. [S3 Block Public Access](#s3-block-public-access)
3. [Security Hub Aggregation](#security-hub-aggregation)
4. [Inspector v2 Scanning](#inspector-v2-scanning)
5. [WAF vs Shield](#waf-vs-shield)
6. [S3 Encryption at Rest](#s3-encryption-at-rest)
7. [GuardDuty Threat Intelligence](#guardduty-threat-intelligence)
8. [Security Hub Automated Remediation](#security-hub-automated-remediation)
9. [WAF Rate Limiting](#waf-rate-limiting)
10. [Complete Security Stack](#complete-security-stack)

### Part 2: Advanced Deep Dive (Questions 11-20)
11. [GuardDuty EKS Protection](#guardduty-eks-protection)
12. [Macie Data Discovery](#macie-data-discovery)
13. [WAF Bot Control](#waf-bot-control)
14. [Inspector Lambda Scanning](#inspector-lambda-scanning)
15. [Security Hub Custom Standards](#security-hub-custom-standards)
16. [GuardDuty S3 Protection](#guardduty-s3-protection)
17. [Shield Advanced DRT](#shield-advanced-drt)
18. [WAF Managed Rule Groups](#waf-managed-rule-groups)
19. [Security Hub ASFF Format](#security-hub-asff-format)
20. [Multi-Account Security Architecture](#multi-account-security-architecture)

---

# PART 1: Core Security Services

# GuardDuty Automated Response

## Question 1: Threat Detection and Response

**Scenario:**
GuardDuty generates a finding: `UnauthorizedAccess:EC2/SSHBruteForce` with severity HIGH. The finding shows 547 failed SSH attempts from IP `198.51.100.50` targeting your EC2 instance in the last hour.

**Question:** What's the BEST automated response architecture?

**Options:**
- A) Manually investigate and block IP in Security Group
- B) EventBridge rule → Lambda → Block IP in NACL + isolate instance + create forensic snapshot
- C) GuardDuty automatically blocks threats - no action needed
- D) SNS notification to security team for manual review

**Answer:** B

---

## Explanation: GuardDuty is Detective, Not Preventive

### Key Concept:

```
GuardDuty = DETECTIVE service
├── Analyzes logs and traffic
├── Generates findings
└── ❌ Does NOT automatically block threats

Response = YOUR responsibility
├── Build automated workflows
├── EventBridge + Lambda
└── Integrate with security tools
```

### Complete Automated Response Architecture:

```
┌─────────────────────────────────────────────┐
│ 1. GuardDuty Finding                        │
│    Type: UnauthorizedAccess:EC2/SSHBruteForce│
│    Severity: HIGH                           │
│    Source IP: 198.51.100.50                 │
└─────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│ 2. EventBridge Rule                         │
│    Pattern match on finding type + severity │
└─────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│ 3. Lambda Function (Response Orchestrator)  │
│    ├── Extract threat details               │
│    ├── Determine response actions           │
│    └── Execute remediation                  │
└─────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│ 4. Automated Actions                        │
│    ├── Block IP in NACL (network level)     │
│    ├── Isolate instance (forensic SG)       │
│    ├── Create EBS snapshots (evidence)      │
│    ├── Notify security team (SNS)           │
│    └── Log to SIEM (integration)            │
└─────────────────────────────────────────────┘
```

### Implementation:

```python
import boto3
import json

def lambda_handler(event, context):
    """
    Automated response to GuardDuty findings
    """
    
    # Parse GuardDuty finding
    finding = event['detail']
    severity = finding['severity']
    finding_type = finding['type']
    
    # Extract threat information
    service_detail = finding['service']
    resource_detail = finding['resource']
    
    # Get malicious IP
    network_action = service_detail.get('action', {}).get('networkConnectionAction', {})
    remote_ip = network_action.get('remoteIpDetails', {}).get('ipAddressV4')
    
    # Get affected instance
    instance_details = resource_detail.get('instanceDetails', {})
    instance_id = instance_details.get('instanceId')
    
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
    print(f"🚨 GuardDuty Finding: {finding_type}")
    print(f"   Severity: {severity}")
    print(f"   Source IP: {remote_ip}")
    print(f"   Target Instance: {instance_id}")
    
    # Response based on severity
    if severity >= 7:  # HIGH or CRITICAL
        
        # Step 1: Block malicious IP at NACL level
        subnet_id = get_instance_subnet(instance_id)
        block_ip_in_nacl(subnet_id, remote_ip)
        
        # Step 2: Isolate compromised instance
        isolate_instance(instance_id)
        
        # Step 3: Create forensic snapshots
        snapshot_ids = create_forensic_snapshots(instance_id)
        
        # Step 4: Notify security team
        notify_security_team(finding, snapshot_ids)
        
        response = {
            'statusCode': 200,
            'actions_taken': {
                'ip_blocked': remote_ip,
                'instance_isolated': instance_id,
                'snapshots_created': snapshot_ids
            }
        }
    else:
        # Medium/Low severity - just alert
        notify_security_team(finding, [])
        response = {
            'statusCode': 200,
            'actions_taken': {
                'alert_sent': True
            }
        }
    
    return response


def get_instance_subnet(instance_id):
    """Get subnet ID for an instance"""
    ec2 = boto3.client('ec2')
    
    response = ec2.describe_instances(InstanceIds=[instance_id])
    subnet_id = response['Reservations'][0]['Instances'][0]['SubnetId']
    
    return subnet_id


def block_ip_in_nacl(subnet_id, malicious_ip):
    """Block IP address in Network ACL"""
    ec2 = boto3.client('ec2')
    
    # Find NACL associated with subnet
    nacls = ec2.describe_network_acls(
        Filters=[{
            'Name': 'association.subnet-id',
            'Values': [subnet_id]
        }]
    )
    
    if not nacls['NetworkAcls']:
        print(f"⚠️  No NACL found for subnet {subnet_id}")
        return
    
    nacl_id = nacls['NetworkAcls'][0]['NetworkAclId']
    
    # Add DENY rule with highest priority
    try:
        ec2.create_network_acl_entry(
            NetworkAclId=nacl_id,
            RuleNumber=1,  # Highest priority
            Protocol='-1',  # All protocols
            RuleAction='deny',
            Egress=False,  # Inbound
            CidrBlock=f'{malicious_ip}/32'
        )
        print(f"✅ Blocked {malicious_ip} in NACL {nacl_id}")
    except Exception as e:
        print(f"❌ Error blocking IP: {e}")


def isolate_instance(instance_id):
    """Isolate instance with forensic security group"""
    ec2 = boto3.client('ec2')
    
    # Get instance VPC
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]
    vpc_id = instance['VpcId']
    
    # Create forensic security group (deny all)
    try:
        forensic_sg = ec2.create_security_group(
            GroupName=f'forensic-isolation-{instance_id}',
            Description='Forensic isolation - all traffic blocked',
            VpcId=vpc_id
        )
        
        forensic_sg_id = forensic_sg['GroupId']
        
        # Remove default egress rule (deny all outbound)
        ec2.revoke_security_group_egress(
            GroupId=forensic_sg_id,
            IpPermissions=[{
                'IpProtocol': '-1',
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }]
        )
        
        # Apply forensic SG to instance
        ec2.modify_instance_attribute(
            InstanceId=instance_id,
            Groups=[forensic_sg_id]
        )
        
        print(f"✅ Instance {instance_id} isolated with SG {forensic_sg_id}")
        
    except Exception as e:
        print(f"❌ Error isolating instance: {e}")


def create_forensic_snapshots(instance_id):
    """Create EBS snapshots for forensic analysis"""
    ec2 = boto3.client('ec2')
    
    # Get all volumes attached to instance
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]
    
    block_devices = instance.get('BlockDeviceMappings', [])
    snapshot_ids = []
    
    for device in block_devices:
        volume_id = device['Ebs']['VolumeId']
        
        try:
            snapshot = ec2.create_snapshot(
                VolumeId=volume_id,
                Description=f'Forensic snapshot - GuardDuty incident {instance_id}',
                TagSpecifications=[{
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {'Key': 'Forensic', 'Value': 'true'},
                        {'Key': 'SourceInstance', 'Value': instance_id},
                        {'Key': 'Incident', 'Value': 'GuardDuty-SSHBruteForce'}
                    ]
                }]
            )
            
            snapshot_ids.append(snapshot['SnapshotId'])
            print(f"✅ Snapshot created: {snapshot['SnapshotId']}")
            
        except Exception as e:
            print(f"❌ Error creating snapshot: {e}")
    
    return snapshot_ids


def notify_security_team(finding, snapshot_ids):
    """Send notification to security team"""
    sns = boto3.client('sns')
    
    message = f"""
🚨 SECURITY ALERT - GuardDuty Finding

Finding Type: {finding['type']}
Severity: {finding['severity']}
Description: {finding['description']}

Resource:
- Instance ID: {finding['resource'].get('instanceDetails', {}).get('instanceId')}
- Region: {finding['region']}

Threat Details:
- Source IP: {finding['service'].get('action', {}).get('networkConnectionAction', {}).get('remoteIpDetails', {}).get('ipAddressV4')}
- City: {finding['service'].get('action', {}).get('networkConnectionAction', {}).get('remoteIpDetails', {}).get('city', {}).get('cityName')}
- Country: {finding['service'].get('action', {}).get('networkConnectionAction', {}).get('remoteIpDetails', {}).get('country', {}).get('countryName')}

Actions Taken:
- ✅ Malicious IP blocked at NACL level
- ✅ Instance isolated (forensic security group)
- ✅ Forensic snapshots created: {', '.join(snapshot_ids)}

Next Steps:
1. Review forensic snapshots
2. Analyze instance for indicators of compromise
3. Determine root cause
4. Terminate and replace instance if compromised

View in GuardDuty Console:
https://console.aws.amazon.com/guardduty/
"""
    
    try:
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:123456789012:security-incidents',
            Subject=f'GuardDuty Alert: {finding["type"]}',
            Message=message
        )
        print("✅ Security team notified")
    except Exception as e:
        print(f"❌ Error sending notification: {e}")
```

### EventBridge Rule Configuration:

```json
{
  "source": ["aws.guardduty"],
  "detail-type": ["GuardDuty Finding"],
  "detail": {
    "severity": [
      {"numeric": [">=", 7]}
    ],
    "type": [
      {"prefix": "UnauthorizedAccess"},
      {"prefix": "Backdoor"},
      {"prefix": "CryptoCurrency"}
    ]
  }
}
```

### CloudFormation for Complete Stack:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  GuardDutyResponseFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: GuardDutyAutomatedResponse
      Runtime: python3.11
      Handler: index.lambda_handler
      Code:
        ZipFile: |
          # Lambda code here
      Role: !GetAtt LambdaExecutionRole.Arn
      Timeout: 300
  
  GuardDutyEventRule:
    Type: AWS::Events::Rule
    Properties:
      Name: GuardDutyHighSeverityFindings
      EventPattern:
        source:
          - aws.guardduty
        detail-type:
          - GuardDuty Finding
        detail:
          severity:
            - numeric:
                - ">="
                - 7
      State: ENABLED
      Targets:
        - Arn: !GetAtt GuardDutyResponseFunction.Arn
          Id: GuardDutyResponseTarget
  
  SecurityIncidentsTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: security-incidents
      Subscription:
        - Protocol: email
          Endpoint: security-team@example.com
```

---

# S3 Block Public Access

## Question 2: Organization-Wide S3 Security

**Scenario:**
Security audit finds 3 S3 buckets with public read access. CISO mandates: "No S3 bucket should ever be public, enforce at organization level."

**Question:** What's the most comprehensive enforcement?

**Options:**
- A) Enable S3 Block Public Access at account level for all accounts
- B) Enable S3 Block Public Access at organization level + SCP to prevent disabling it
- C) Use AWS Config rule to detect public buckets
- D) Bucket policies to deny public access

**Answer:** B

---

## Explanation: Defense in Depth - Organization Level + SCP

### Multi-Layer S3 Public Access Protection:

```
Layer 1: Organization-Level Block Public Access
└── Applies to ALL accounts in organization
    └── Inherited by all accounts

Layer 2: SCP (Service Control Policy)
└── Prevents disabling Block Public Access
    └── Even administrators cannot override

Layer 3: AWS Config (Detective)
└── Monitors for any public buckets
    └── Alerts if configuration changes

Layer 4: Bucket Policies (Individual buckets)
└── Additional protection at bucket level
    └── Explicit deny for public access
```

### Complete Implementation:

```python
import boto3
import json

# Step 1: Enable Block Public Access at Organization Level
s3control = boto3.client('s3control')
orgs = boto3.client('organizations')

# Get organization ID
org = orgs.describe_organization()
org_id = org['Organization']['Id']

# Enable Block Public Access for entire organization
try:
    s3control.put_public_access_block(
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        },
        AccountId='123456789012'  # Management account
    )
    print("✅ Organization-level Block Public Access enabled")
except Exception as e:
    print(f"❌ Error: {e}")


# Step 2: Create SCP to Prevent Disabling
scp_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyDisableS3BlockPublicAccess",
            "Effect": "Deny",
            "Action": [
                "s3:PutAccountPublicAccessBlock",
                "s3:PutBucketPublicAccessBlock"
            ],
            "Resource": "*",
            "Condition": {
                "Bool": {
                    "s3:BlockPublicAcls": "false",
                    "s3:BlockPublicPolicy": "false",
                    "s3:IgnorePublicAcls": "false",
                    "s3:RestrictPublicBuckets": "false"
                }
            }
        },
        {
            "Sid": "DenyPublicBucketACLs",
            "Effect": "Deny",
            "Action": [
                "s3:PutBucketAcl",
                "s3:PutObjectAcl"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": [
                        "public-read",
                        "public-read-write",
                        "authenticated-read"
                    ]
                }
            }
        }
    ]
}

# Create and attach SCP
try:
    policy = orgs.create_policy(
        Content=json.dumps(scp_policy),
        Description='Prevent disabling S3 Block Public Access',
        Name='S3-BlockPublicAccess-Protection',
        Type='SERVICE_CONTROL_POLICY'
    )
    
    policy_id = policy['Policy']['PolicySummary']['Id']
    
    # Attach to root (applies to all accounts)
    root_id = orgs.list_roots()['Roots'][0]['Id']
    
    orgs.attach_policy(
        PolicyId=policy_id,
        TargetId=root_id
    )
    
    print(f"✅ SCP created and attached: {policy_id}")
    print("✅ Block Public Access cannot be disabled by anyone")
    
except Exception as e:
    print(f"❌ Error creating SCP: {e}")


# Step 3: AWS Config Rule for Detection
config = boto3.client('config')

try:
    config.put_config_rule(
        ConfigRule={
            'ConfigRuleName': 's3-bucket-public-read-prohibited',
            'Source': {
                'Owner': 'AWS',
                'SourceIdentifier': 'S3_BUCKET_PUBLIC_READ_PROHIBITED'
            },
            'Scope': {
                'ComplianceResourceTypes': ['AWS::S3::Bucket']
            }
        }
    )
    
    config.put_config_rule(
        ConfigRule={
            'ConfigRuleName': 's3-bucket-public-write-prohibited',
            'Source': {
                'Owner': 'AWS',
                'SourceIdentifier': 'S3_BUCKET_PUBLIC_WRITE_PROHIBITED'
            },
            'Scope': {
                'ComplianceResourceTypes': ['AWS::S3::Bucket']
            }
        }
    )
    
    config.put_config_rule(
        ConfigRule={
            'ConfigRuleName': 's3-account-level-public-access-blocks',
            'Source': {
                'Owner': 'AWS',
                'SourceIdentifier': 'S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS'
            }
        }
    )
    
    print("✅ AWS Config rules enabled for detection")
    
except Exception as e:
    print(f"❌ Error enabling Config rules: {e}")


# Step 4: Remediation for Any Public Buckets Found
def remediate_public_buckets():
    """
    Scan and remediate any public buckets
    """
    s3 = boto3.client('s3')
    
    # List all buckets
    buckets = s3.list_buckets()
    
    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        
        try:
            # Enable Block Public Access for bucket
            s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
            print(f"✅ Block Public Access enabled for bucket: {bucket_name}")
            
        except Exception as e:
            print(f"⚠️  Could not update {bucket_name}: {e}")

# Run remediation
remediate_public_buckets()

print("\n📊 Complete S3 Public Access Protection:")
print("1. ✅ Organization-level Block Public Access")
print("2. ✅ SCP prevents disabling")
print("3. ✅ AWS Config detects violations")
print("4. ✅ All buckets remediated")
```

### Why This Approach is Superior:

```
Option A (Account-level only):
├── ❌ Can be disabled by account admin
├── ❌ Not enforced across organization
└── ❌ No protection against policy changes

Option B (Organization + SCP): ✅ BEST
├── ✅ Applied to all accounts
├── ✅ Cannot be disabled (SCP enforcement)
├── ✅ Centralized management
└── ✅ Defense in depth

Option C (AWS Config only):
├── ⚠️  Detective, not preventive
├── ❌ Alerts after bucket is public
└── ❌ Doesn't block creation

Option D (Bucket policies):
├── ❌ Must configure per bucket
├── ❌ Can be overridden
└── ❌ Not scalable
```

---

# Security Hub Aggregation

## Question 3: Centralized Security Visibility

**Scenario:**
You have GuardDuty, Inspector, Macie, and AWS Config enabled across 50 accounts. Security team drowning in alerts from multiple sources.

**Question:** How does Security Hub help?

**Options:**
- A) Replaces all security services with one tool
- B) Aggregates findings from multiple services + assigns severity scores + enables cross-region aggregation
- C) Only provides compliance dashboards
- D) Automatically remediates all findings

**Answer:** B

---

## Explanation: Security Hub as Central Security Dashboard

### Security Hub Architecture:

```
┌─────────────────────────────────────────────┐
│ Multiple Security Services (Data Sources)   │
├─────────────────────────────────────────────┤
│ ├── GuardDuty (threat detection)            │
│ ├── Inspector (vulnerability scanning)      │
│ ├── Macie (data classification)             │
│ ├── IAM Access Analyzer                     │
│ ├── AWS Config (compliance)                 │
│ ├── Firewall Manager                        │
│ └── Third-party integrations                │
└─────────────────────────────────────────────┘
              ↓ (ASFF format)
┌─────────────────────────────────────────────┐
│ Security Hub (Central Aggregation)          │
├─────────────────────────────────────────────┤
│ ├── Normalize findings (ASFF)               │
│ ├── Assign severity scores (0-100)          │
│ ├── Deduplicate similar findings            │
│ ├── Aggregate across accounts/regions       │
│ └── Enable cross-account management         │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ Security Hub Dashboards                     │
├─────────────────────────────────────────────┤
│ ├── Single pane of glass                    │
│ ├── Compliance standards (CIS, PCI-DSS)     │
│ ├── Custom insights                         │
│ └── Automated remediation workflows         │
└─────────────────────────────────────────────┘
```

### Implementation:

```python
import boto3

securityhub = boto3.client('securityhub')

# Step 1: Enable Security Hub
try:
    securityhub.enable_security_hub()
    print("✅ Security Hub enabled")
except securityhub.exceptions.ResourceConflictException:
    print("ℹ️  Security Hub already enabled")

# Step 2: Enable Security Standards
standards = [
    {
        'arn': 'arn:aws:securityhub:us-east-1::standards/aws-foundational-security-best-practices/v/1.0.0',
        'name': 'AWS Foundational Security Best Practices'
    },
    {
        'arn': 'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0',
        'name': 'CIS AWS Foundations Benchmark v1.2.0'
    },
    {
        'arn': 'arn:aws:securityhub:us-east-1::standards/pci-dss/v/3.2.1',
        'name': 'PCI DSS v3.2.1'
    }
]

for standard in standards:
    try:
        securityhub.batch_enable_standards(
            StandardsSubscriptionRequests=[{
                'StandardsArn': standard['arn']
            }]
        )
        print(f"✅ Enabled: {standard['name']}")
    except Exception as e:
        print(f"⚠️  {standard['name']}: {e}")

# Step 3: Configure Finding Aggregation (Multi-Account/Multi-Region)
try:
    aggregator = securityhub.create_finding_aggregator(
        RegionLinkingMode='ALL_REGIONS',
        Regions=[]  # Empty = all regions
    )
    print(f"✅ Finding aggregator created: {aggregator['FindingAggregatorArn']}")
    print("✅ All regions will be aggregated into this region")
except securityhub.exceptions.ResourceConflictException:
    print("ℹ️  Finding aggregator already exists")

# Step 4: Create Custom Insights
insight = securityhub.create_insight(
    Name='Critical Findings Requiring Immediate Action',
    Filters={
        'SeverityLabel': [{
            'Value': 'CRITICAL',
            'Comparison': 'EQUALS'
        }],
        'WorkflowStatus': [{
            'Value': 'NEW',
            'Comparison': 'EQUALS'
        }]
    },
    GroupByAttribute='ResourceType'
)

print(f"✅ Custom insight created: {insight['InsightArn']}")

# Step 5: Get Aggregated Findings Summary
findings = securityhub.get_findings(
    Filters={
        'SeverityLabel': [{
            'Value': 'CRITICAL',
            'Comparison': 'EQUALS'
        }]
    },
    MaxResults=100
)

print(f"\n📊 Security Posture Summary:")
print(f"   Critical findings: {len(findings['Findings'])}")

# Group by service
from collections import defaultdict
by_service = defaultdict(int)

for finding in findings['Findings']:
    product_name = finding['ProductName']
    by_service[product_name] += 1

print(f"\n   Findings by service:")
for service, count in sorted(by_service.items(), key=lambda x: x[1], reverse=True):
    print(f"   - {service}: {count}")
```

### Key Features:

**1. Finding Aggregation:**
- Collects findings from 15+ AWS services
- Third-party integrations (Palo Alto, Check Point, etc.)
- Cross-account and cross-region visibility

**2. Normalized Severity Scoring:**
```python
# Different services use different severity scales
# Security Hub normalizes to 0-100

severity_mapping = {
    'INFORMATIONAL': 0,
    'LOW': 1-39,
    'MEDIUM': 40-69,
    'HIGH': 70-89,
    'CRITICAL': 90-100
}
```

**3. Compliance Standards:**
- AWS Foundational Security Best Practices
- CIS AWS Foundations Benchmark
- PCI DSS
- Custom standards (via AWS Config rules)

**4. Automated Remediation:**
```python
# Create custom action for remediation
action = securityhub.create_action_target(
    Name='RemediateNonCompliantResource',
    Description='Trigger automated remediation',
    Id='RemediateResource'
)

# EventBridge rule triggers Lambda on custom action
# Lambda performs remediation
# Updates finding status to RESOLVED
```

---

# Inspector v2 Scanning

## Question 4: Vulnerability Assessment

**Scenario:**
AWS Inspector v2 finds CVE-2024-12345 (CRITICAL severity, CVSS 9.8) in your container image. The vulnerability allows remote code execution.

**Question:** What does Inspector v2 scan?

**Options:**
- A) Only EC2 instances
- B) EC2 instances + ECR container images + Lambda functions (for OS packages and code vulnerabilities)
- C) Only network vulnerabilities
- D) IAM policies and configurations

**Answer:** B

---

## Explanation: Inspector v2 Continuous Scanning

### Inspector v2 Capabilities:

```
Inspector v2 Scans:
├── EC2 Instances
│   ├── OS packages (Amazon Linux, Ubuntu, RHEL, etc.)
│   ├── Application packages
│   └── Network reachability
│
├── ECR Container Images
│   ├── OS packages in image layers
│   ├── Application dependencies
│   └── Continuous rescan on push
│
└── Lambda Functions
    ├── OS packages in runtime
    ├── Application dependencies (layers)
    └── Code vulnerabilities (Python, Node.js, Java)

Vulnerability Sources:
├── CVE (Common Vulnerabilities and Exposures)
├── Network reachability findings
└── Code vulnerabilities (Lambda)
```

### Implementation:

```python
import boto3

inspector = boto3.client('inspector2')

# Enable Inspector v2 for all resource types
try:
    response = inspector.enable(
        accountIds=['123456789012'],
        resourceTypes=['EC2', 'ECR', 'LAMBDA']
    )
    print("✅ Inspector v2 enabled for:")
    print("   - EC2 instances")
    print("   - ECR container images")
    print("   - Lambda functions")
except Exception as e:
    print(f"❌ Error enabling Inspector: {e}")

# Get vulnerability findings
findings = inspector.list_findings(
    filterCriteria={
        'severity': [{
            'comparison': 'EQUALS',
            'value': 'CRITICAL'
        }]
    },
    maxResults=100
)

print(f"\n🔍 Critical Vulnerabilities Found: {len(findings['findings'])}")

for finding in findings['findings']:
    resource_type = finding['resourceType']
    resource_id = finding['resources'][0]['id']
    
    # Get CVE details
    if 'packageVulnerabilityDetails' in finding:
        vuln = finding['packageVulnerabilityDetails']
        cve_id = vuln['vulnerabilityId']
        package_name = vuln['vulnerablePackages'][0]['name']
        package_version = vuln['vulnerablePackages'][0]['version']
        fixed_version = vuln['vulnerablePackages'][0].get('fixedInVersion', 'N/A')
        
        # CVSS score
        cvss_score = vuln.get('cvss', [{}])[0].get('baseScore', 'N/A')
        
        print(f"\n⚠️  {cve_id}")
        print(f"   Resource: {resource_type} - {resource_id}")
        print(f"   Package: {package_name} v{package_version}")
        print(f"   Fixed in: {fixed_version}")
        print(f"   CVSS Score: {cvss_score}")

# Automated response - block vulnerable images
def block_vulnerable_images():
    """
    Prevent deployment of vulnerable container images
    """
    ecr = boto3.client('ecr')
    
    # Get vulnerable images from Inspector
    vulnerable_images = []
    
    for finding in findings['findings']:
        if finding['resourceType'] == 'AWS_ECR_CONTAINER_IMAGE':
            image_digest = finding['resources'][0]['id'].split('/')[-1]
            repo_name = finding['resources'][0]['id'].split('/')[-2]
            vulnerable_images.append((repo_name, image_digest))
    
    # Set lifecycle policy to expire vulnerable images
    for repo, digest in vulnerable_images:
        try:
            ecr.put_lifecycle_policy(
                repositoryName=repo,
                lifecyclePolicyText=json.dumps({
                    "rules": [{
                        "rulePriority": 1,
                        "description": "Remove vulnerable images",
                        "selection": {
                            "tagStatus": "any",
                            "countType": "imageCountMoreThan",
                            "countNumber": 1
                        },
                        "action": {
                            "type": "expire"
                        }
                    }]
                })
            )
            print(f"✅ Lifecycle policy set for {repo}")
        except Exception as e:
            print(f"❌ Error: {e}")

block_vulnerable_images()
```

### Continuous Scanning:

```
Inspector v2 = Always On
├── Automatically scans new resources
├── Rescans when new CVEs published
├── No manual scan initiation needed
└── Real-time findings

vs. Inspector v1 (Classic)
├── Manual scan initiation
├── Assessment runs (time-limited)
├── Requires agents
└── Deprecated
```

---

*Due to length constraints, I'll continue with the remaining questions in a structured format...*

# WAF vs Shield

## Question 5: Layer 7 vs Layer 3/4 Protection

**Answer:** B - WAF for SQL injection, Shield Standard for volumetric DDoS

### Quick Summary:
- **Shield Standard (FREE)**: Layer 3/4 DDoS protection (SYN floods, UDP reflection)
- **Shield Advanced ($3,000/month)**: Enhanced DDoS + DRT support + cost protection
- **WAF**: Layer 7 protection (SQLi, XSS, rate limiting)

---

# S3 Encryption at Rest

## Question 6: Compliance Requirements

**Answer:** B - SSE-KMS with customer-managed CMK

### Why:
- ✅ Customer-managed keys (full control)
- ✅ Automatic rotation (enable via KMS)
- ✅ CloudTrail logs all key operations
- ✅ Meets compliance requirements (HIPAA, PCI-DSS)

---

# GuardDuty Threat Intelligence

## Question 7: Multi-Source Analysis

**Answer:** B - AWS threat intel + VPC Flow Logs + DNS logs + CloudTrail events

### Data Sources:
- VPC Flow Logs (network traffic patterns)
- DNS Logs (DNS queries)
- CloudTrail Events (API calls)
- EKS Audit Logs (Kubernetes)
- S3 Data Events (object access)
- AWS + third-party threat intelligence feeds

---

# Security Hub Automated Remediation

## Question 8: Custom Actions

**Answer:** C - Custom Action → EventBridge → Lambda

### Pattern:
```
Security Hub Finding 
→ Custom Action 
→ EventBridge 
→ Lambda 
→ Remediation 
→ Update Finding Status
```

---

# WAF Rate Limiting

## Question 9: Credential Stuffing Defense

**Answer:** B - Rate-based rule: 100 requests/5min + CAPTCHA

### Why:
- Stops distributed attacks (1,000 IPs)
- Allows legitimate users (CAPTCHA challenge)
- Adaptive protection

---

# Complete Security Stack

## Question 10: Defense in Depth

**Answer:** B - Shield + WAF + GuardDuty + Inspector + Security Hub

### Each Service's Role:
- **Shield**: Layer 3/4 DDoS
- **WAF**: Layer 7 attacks
- **GuardDuty**: Threat detection
- **Inspector**: Vulnerability scanning
- **Security Hub**: Centralized visibility

---

# PART 2: Advanced Deep Dive

# GuardDuty EKS Protection

## Question 11: Kubernetes Security

**Answer:** B - Kubernetes audit logs + runtime monitoring

### Detects:
- Privileged containers
- Anonymous API access
- Suspicious kubectl commands
- Container escape attempts

---

# Macie Data Discovery

## Question 12: PII Classification

**Answer:** B - Macie = Data classification; GuardDuty = Threat detection

### Difference:
- **Macie**: Discovers and classifies sensitive data (PII/PHI)
- **GuardDuty**: Detects malicious activity and threats

---

# WAF Bot Control

## Question 13: Bot Management

**Answer:** B - AWS Bot Control + CAPTCHA

### Implementation:
```python
'AWSManagedRulesBotControlRuleSet'
├── Verified bots → Allow
├── Unverified scrapers → Challenge (CAPTCHA)
└── Malicious bots → Block
```

---

# Inspector Lambda Scanning

## Question 14: Lambda Vulnerabilities

**Answer:** B - Code + dependencies + layers

### Scans:
- Application dependencies (npm, pip, maven)
- Lambda layers
- Runtime environment
- Known CVEs

---

# Security Hub Custom Standards

## Question 15: Custom Compliance Checks

**Answer:** B - AWS Config custom rules → Security Hub (ASFF)

### Pattern:
```
AWS Config Custom Rule 
→ Compliance evaluation 
→ ASFF format 
→ Security Hub dashboard
```

---

# GuardDuty S3 Protection

## Question 16: S3 Threat Detection

**Answer:** B - S3 data events + CloudTrail management events

### Monitors:
- Object access patterns (GetObject, PutObject)
- Bucket configuration changes
- Block Public Access changes
- Anonymous access attempts

---

# Shield Advanced DRT

## Question 17: Enhanced DDoS Protection

**Answer:** B - DRT + cost protection + advanced metrics

### Benefits:
- 24/7 DDoS Response Team
- Cost protection during attacks
- Advanced real-time metrics
- Proactive engagement

---

# WAF Managed Rule Groups

## Question 18: OWASP Protection

**Answer:** B - Core Rule Set (CRS)

### Protects Against:
- SQL injection
- XSS
- LFI/RFI
- Command injection
- Path traversal

---

# Security Hub ASFF Format

## Question 19: Finding Format

**Answer:** B - AWS Security Finding Format (ASFF)

### Standardized Schema:
- Normalized across all services
- Consistent severity scoring
- Required for Security Hub ingestion

---

# Multi-Account Security Architecture

## Question 20: Centralized Management

**Answer:** B - Delegated admin account

### Pattern:
```
Management Account 
→ Designate Security Account as delegated admin 
→ Auto-enable across all org accounts 
→ Centralized visibility
```

---

# Summary & Key Takeaways

## Your Performance:
- **Total Questions:** 20
- **Correct Answers:** 18
- **Score:** 90%

### Questions Breakdown:
1. ✅ GuardDuty Automated Response
2. ✅ S3 Block Public Access + SCP
3. ✅ Security Hub Aggregation
4. ❌ Inspector v2 (missed EC2+ECR+Lambda)
5. ✅ WAF vs Shield
6. ✅ SSE-KMS Encryption
7. ✅ GuardDuty Threat Intel
8. ✅ Security Hub Remediation
9. ✅ WAF Rate Limiting
10. ✅ Complete Security Stack
11. ✅ GuardDuty EKS Protection
12. ❌ Macie vs GuardDuty (classification vs detection)
13. ✅ WAF Bot Control
14. ✅ Inspector Lambda Scanning
15. ✅ Security Hub Custom Standards
16. ✅ GuardDuty S3 Protection
17. ✅ Shield Advanced DRT
18. ✅ WAF Managed Rules
19. ✅ Security Hub ASFF
20. ✅ Multi-Account Architecture

---

## Service Comparison Matrix:

| Service | Purpose | Detection/Prevention | Scope |
|---------|---------|---------------------|-------|
| **GuardDuty** | Threat detection | Detective | VPC + DNS + CloudTrail + EKS + S3 |
| **Macie** | Data classification | Detective | S3 buckets (PII/PHI) |
| **Inspector** | Vulnerability scanning | Detective | EC2 + ECR + Lambda |
| **Security Hub** | Central dashboard | Aggregation | All security services |
| **WAF** | Application firewall | Preventive | Layer 7 (HTTP/HTTPS) |
| **Shield** | DDoS protection | Preventive | Layer 3/4 |
| **Config** | Compliance monitoring | Detective | All resources |

---

## Best Practices:

### 1. **GuardDuty**
```
✅ Enable in all accounts/regions
✅ Enable S3 Protection
✅ Enable EKS Protection
✅ Build automated response (EventBridge + Lambda)
✅ Integrate with Security Hub
```

### 2. **S3 Security**
```
✅ Organization-level Block Public Access
✅ SCP to prevent disabling
✅ SSE-KMS for sensitive data
✅ Bucket policies with explicit deny
✅ VPC endpoints for private access
```

### 3. **Security Hub**
```
✅ Enable all standards (CIS, PCI-DSS, FSBP)
✅ Configure finding aggregation
✅ Create custom insights
✅ Build remediation workflows
✅ Integrate third-party tools
```

### 4. **Inspector**
```
✅ Enable for EC2 + ECR + Lambda
✅ Continuous scanning (always on)
✅ Block vulnerable images in CI/CD
✅ Prioritize by CVSS score
✅ Automate patching
```

### 5. **WAF**
```
✅ Use Managed Rule Groups (CRS)
✅ Implement rate limiting
✅ Enable Bot Control
✅ CAPTCHA for suspicious traffic
✅ Monitor via CloudWatch
```

### 6. **Shield**
```
✅ Shield Standard (automatic, free)
✅ Shield Advanced for critical apps
✅ Associate with CloudFront + ALB + Route53
✅ Configure DRT access (Advanced only)
✅ Review cost protection reports
```

---

## Architecture Decision Tree:

```
Need threat detection?
└── GuardDuty

Need to find sensitive data?
└── Macie

Need vulnerability scanning?
└── Inspector v2

Need centralized security view?
└── Security Hub

Need to block web attacks?
└── WAF

Need DDoS protection?
├── Basic → Shield Standard (FREE)
└── Advanced → Shield Advanced ($3K/month)

Need compliance monitoring?
└── AWS Config + Security Hub

Need automated response?
└── EventBridge + Lambda
```

---

## Interview Talking Points:

**For Security Architect roles, emphasize:**

1. **Defense in Depth** - Multiple security layers working together
2. **Automated Response** - EventBridge + Lambda for threat response
3. **Centralized Visibility** - Security Hub as single pane of glass
4. **Continuous Scanning** - Inspector v2 always-on protection
5. **Multi-Account Strategy** - Delegated admin for scale
6. **Compliance** - CIS, PCI-DSS, HIPAA standards
7. **Cost Optimization** - Shield Standard is free, use Advanced selectively
8. **Integration** - Services complement each other
9. **ASFF Format** - Standardized finding format
10. **Proactive Security** - Preventive controls (WAF, Shield) + Detective controls (GuardDuty, Inspector)

---

*Generated: November 30, 2024*
*Total Questions: 20*
*Your Score: 90%*
*Focus Areas: Multi-service integration, automated response patterns*

**You're ready for advanced AWS Security Architect interviews!**
