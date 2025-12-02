# AWS Cross-Region Security - Security Architect Interview Questions

**Comprehensive collection of AWS cross-region security interview questions covering S3, GuardDuty, CloudTrail, KMS, VPC, Session Manager, Backup, Route 53, ACM, and Secrets Manager for security architect roles.**

---

## Table of Contents

1. [S3 Cross-Region Replication with KMS Encryption](#s3-cross-region-replication-with-kms-encryption)
2. [GuardDuty Cross-Region Findings Aggregation](#guardduty-cross-region-findings-aggregation)
3. [CloudTrail Cross-Region Logging](#cloudtrail-cross-region-logging)
4. [KMS Multi-Region Keys](#kms-multi-region-keys)
5. [VPC Peering Cross-Region Security](#vpc-peering-cross-region-security)
6. [AWS Systems Manager Session Manager Cross-Region](#aws-systems-manager-session-manager-cross-region)
7. [AWS Backup Cross-Region](#aws-backup-cross-region)
8. [Route 53 Cross-Region Failover](#route-53-cross-region-failover)
9. [AWS Certificate Manager Cross-Region](#aws-certificate-manager-cross-region)
10. [AWS Secrets Manager Cross-Region Replication](#aws-secrets-manager-cross-region-replication)

---

# S3 Cross-Region Replication with KMS Encryption

## Question 1: Encrypted S3 Replication

**Scenario:**
You need to replicate S3 bucket from us-east-1 to eu-west-1 for disaster recovery. Source bucket uses SSE-KMS with customer-managed key. Compliance requires: "Encrypted data must remain encrypted during replication, destination region must use its own KMS key."

**Question:** What's the correct architecture?

**Options:**
- A) Replicate with SSE-S3, simpler than KMS
- B) S3 replication with SSE-KMS, use same KMS key in both regions
- C) S3 replication with SSE-KMS, create separate CMK in destination region, grant source bucket role permission to use destination key
- D) Cannot replicate encrypted S3 objects across regions

**Answer:** C

---

## Explanation: Cross-Region KMS Encrypted Replication

### Architecture Diagram:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Source Region (us-east-1)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────┐         ┌─────────────────────────┐     │
│  │ KMS CMK (Source)     │         │ S3 Bucket (Source)      │     │
│  │ alias/source-key     │◄────────│ encrypted-data-bucket   │     │
│  │                      │ Decrypt │ SSE-KMS encrypted       │     │
│  │ Key ID: key-src-123  │         │                         │     │
│  └──────────────────────┘         └───────────┬─────────────┘     │
│            ▲                                   │                   │
│            │ Grant permission                  │                   │
│            │ (kms:Decrypt)                     │                   │
│  ┌─────────┴──────────────────────────────────▼─────────────────┐ │
│  │ IAM Role: S3ReplicationRole                                   │ │
│  │ arn:aws:iam::123456789012:role/S3ReplicationRole             │ │
│  │                                                               │ │
│  │ Permissions:                                                  │ │
│  │ ✅ kms:Decrypt (source key) - Decrypt objects                │ │
│  │ ✅ kms:Encrypt (destination key) - Encrypt replicas          │ │
│  │ ✅ s3:GetObject* (source bucket) - Read objects              │ │
│  │ ✅ s3:ReplicateObject (destination) - Write replicas         │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Replication (TLS encrypted)
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   Destination Region (eu-west-1)                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────┐         ┌─────────────────────────┐     │
│  │ KMS CMK (Dest)       │────────►│ S3 Bucket (Destination) │     │
│  │ alias/dest-key       │ Encrypt │ encrypted-replica-bucket│     │
│  │                      │         │ SSE-KMS encrypted       │     │
│  │ Key ID: key-dst-456  │         │ (different key)         │     │
│  └──────────────────────┘         └─────────────────────────┘     │
│            ▲                                                        │
│            │ Grant permission (kms:Encrypt)                         │
│            │ to Replication Role                                   │
└─────────────────────────────────────────────────────────────────────┘
```

### Implementation:

```python
import boto3
import json

kms_src = boto3.client('kms', region_name='us-east-1')
kms_dst = boto3.client('kms', region_name='eu-west-1')
s3 = boto3.client('s3')
iam = boto3.client('iam')

# 1. Create KMS keys in both regions
src_key = kms_src.create_key(Description='Source bucket key')
dst_key = kms_dst.create_key(Description='Destination bucket key')

src_key_arn = src_key['KeyMetadata']['Arn']
dst_key_arn = dst_key['KeyMetadata']['Arn']

# 2. Create IAM role for replication
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "s3.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}

role = iam.create_role(
    RoleName='S3CrossRegionReplicationRole',
    AssumeRolePolicyDocument=json.dumps(trust_policy)
)

replication_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:GetReplicationConfiguration", "s3:ListBucket"],
            "Resource": "arn:aws:s3:::source-encrypted-bucket"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObjectVersionForReplication",
                "s3:GetObjectVersionAcl",
                "s3:GetObjectVersionTagging"
            ],
            "Resource": "arn:aws:s3:::source-encrypted-bucket/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ReplicateObject",
                "s3:ReplicateDelete",
                "s3:ReplicateTags"
            ],
            "Resource": "arn:aws:s3:::destination-encrypted-bucket/*"
        },
        {
            "Effect": "Allow",
            "Action": ["kms:Decrypt"],
            "Resource": src_key_arn
        },
        {
            "Effect": "Allow",
            "Action": ["kms:Encrypt"],
            "Resource": dst_key_arn
        }
    ]
}

iam.put_role_policy(
    RoleName='S3CrossRegionReplicationRole',
    PolicyName='ReplicationPolicy',
    PolicyDocument=json.dumps(replication_policy)
)

# 3. Enable versioning
s3.put_bucket_versioning(
    Bucket='source-encrypted-bucket',
    VersioningConfiguration={'Status': 'Enabled'}
)

s3.put_bucket_versioning(
    Bucket='destination-encrypted-bucket',
    VersioningConfiguration={'Status': 'Enabled'}
)

# 4. Configure replication
s3.put_bucket_replication(
    Bucket='source-encrypted-bucket',
    ReplicationConfiguration={
        'Role': role['Role']['Arn'],
        'Rules': [{
            'Status': 'Enabled',
            'Priority': 1,
            'Filter': {},
            'Destination': {
                'Bucket': 'arn:aws:s3:::destination-encrypted-bucket',
                'EncryptionConfiguration': {
                    'ReplicaKmsKeyID': dst_key_arn
                }
            },
            'SourceSelectionCriteria': {
                'SseKmsEncryptedObjects': {'Status': 'Enabled'}
            }
        }]
    }
)

print("✅ Cross-region encrypted replication configured")
```

### Key Points:

- **Separate KMS keys per region** for regional isolation
- **Replication role** needs decrypt permission on source key, encrypt on destination key
- **TLS encrypted** in transit
- **Each region independently encrypted** with its own key

---

# GuardDuty Cross-Region Findings Aggregation

## Question 2: Centralized Threat Detection

**Scenario:**
Your organization has resources in 10 AWS regions. Security team needs centralized threat detection visibility.

**Question:** How do you aggregate GuardDuty findings from all regions?

**Options:**
- A) GuardDuty automatically aggregates across regions
- B) Manually enable GuardDuty in each region, use Security Hub cross-region aggregation
- C) EventBridge cross-region rules to central region
- D) GuardDuty is region-specific, cannot aggregate

**Answer:** B

---

## Explanation: Security Hub for Cross-Region Aggregation

### Architecture:

```
┌────────────────────────────────────────────────────────────────────┐
│                    Multiple AWS Regions                            │
│                                                                    │
│  us-east-1        eu-west-1        ap-south-1                     │
│  GuardDuty  →     GuardDuty  →     GuardDuty  →                  │
│     │                │                │                            │
│     └────────────────┼────────────────┘                            │
│                      │ Findings (ASFF)                             │
│                      ▼                                             │
│               Security Hub                                         │
│               (Finding Aggregator)                                 │
│                                                                    │
│  ✅ All regions → Central region (us-east-1)                      │
│  ✅ Single dashboard                                              │
│  ✅ Cross-account + Cross-region                                  │
└────────────────────────────────────────────────────────────────────┘
```

### Implementation:

```python
import boto3

regions = ['us-east-1', 'eu-west-1', 'ap-south-1', 'us-west-2']

# Enable GuardDuty in all regions
for region in regions:
    guardduty = boto3.client('guardduty', region_name=region)
    detector = guardduty.create_detector(Enable=True)
    print(f"✅ GuardDuty enabled in {region}")

# Enable Security Hub in all regions
for region in regions:
    securityhub = boto3.client('securityhub', region_name=region)
    securityhub.enable_security_hub()
    
    # Enable GuardDuty integration
    securityhub.enable_import_findings_for_product(
        ProductArn=f'arn:aws:securityhub:{region}::product/aws/guardduty'
    )
    print(f"✅ Security Hub enabled in {region}")

# Configure finding aggregation in central region
securityhub_central = boto3.client('securityhub', region_name='us-east-1')
aggregator = securityhub_central.create_finding_aggregator(
    RegionLinkingMode='ALL_REGIONS'
)

print(f"✅ Cross-region aggregation configured")
print(f"   All findings aggregated to us-east-1")
```

---

# CloudTrail Cross-Region Logging

## Question 3: Immutable Audit Trail

**Scenario:**
Compliance requires: "All API calls across all regions must be logged to a single, immutable audit trail with integrity validation."

**Question:** What's the best CloudTrail configuration?

**Options:**
- A) Enable CloudTrail in each region separately
- B) Organization trail with multi-region enabled + S3 Object Lock (compliance mode) + log file validation
- C) CloudWatch Logs only
- D) CloudTrail only captures us-east-1 events

**Answer:** B

---

## Explanation: Organization Trail with Object Lock

### Architecture:

```
All Regions → CloudTrail (Multi-Region) → S3 Bucket (Object Lock)
├── us-east-1 API calls
├── eu-west-1 API calls
├── ap-south-1 API calls
└── All other regions

S3 Bucket Configuration:
├── Object Lock (COMPLIANCE mode)
├── 7-year retention
├── SSE-KMS encryption
├── Log file validation
└── Even root cannot delete
```

### Implementation:

```python
import boto3
import json

cloudtrail = boto3.client('cloudtrail')
s3 = boto3.client('s3')
kms = boto3.client('kms')

# 1. Create KMS key
key = kms.create_key(Description='CloudTrail encryption key')
kms_key_arn = key['KeyMetadata']['Arn']

# 2. Create S3 bucket with Object Lock
bucket_name = 'cloudtrail-org-logs-immutable'
s3.create_bucket(
    Bucket=bucket_name,
    ObjectLockEnabledForBucket=True
)

# 3. Configure Object Lock (COMPLIANCE mode)
s3.put_object_lock_configuration(
    Bucket=bucket_name,
    ObjectLockConfiguration={
        'ObjectLockEnabled': 'Enabled',
        'Rule': {
            'DefaultRetention': {
                'Mode': 'COMPLIANCE',
                'Days': 2555  # 7 years
            }
        }
    }
)

# 4. Create organization trail
cloudtrail.create_trail(
    Name='organization-trail-all-regions',
    S3BucketName=bucket_name,
    IncludeGlobalServiceEvents=True,
    IsMultiRegionTrail=True,
    EnableLogFileValidation=True,
    KmsKeyId=kms_key_arn,
    IsOrganizationTrail=True
)

cloudtrail.start_logging(Name='organization-trail-all-regions')

print("✅ Immutable organization trail configured")
print("   ✅ Multi-region: All regions")
print("   ✅ Object Lock: 7 years (cannot be deleted)")
print("   ✅ Log validation: Enabled")
```

---

# KMS Multi-Region Keys

## Question 4: Cross-Region Encryption

**Scenario:**
You encrypt data in us-east-1 with KMS. Application needs to decrypt same data in eu-west-1 for disaster recovery without re-encrypting.

**Question:** What KMS feature solves this?

**Options:**
- A) Copy KMS key to another region
- B) KMS multi-region keys - same key ID, different key material per region
- C) Use same KMS key ARN in both regions
- D) Re-encrypt data in destination region

**Answer:** B (but with correction: SAME key material, not different)

---

## Explanation: KMS Multi-Region Keys

### Correct Answer Detail:

**KMS multi-region keys have SAME cryptographic key material across regions, but different key IDs.**

### Architecture:

```
Primary Key (us-east-1):
├── Key ID: mrk-abc123
├── Key Material: [SHARED]
└── Can create replicas

Replica Key (eu-west-1):
├── Key ID: mrk-def456
├── Key Material: [SHARED] ← SAME as primary
└── Can decrypt primary's ciphertext

Key Feature:
✅ Same cryptographic material
✅ Different key IDs per region
✅ Decrypt in any region without re-encryption
```

### Implementation:

```python
import boto3

kms_primary = boto3.client('kms', region_name='us-east-1')
kms_replica = boto3.client('kms', region_name='eu-west-1')

# Create multi-region primary key
primary_key = kms_primary.create_key(
    Description='Multi-region key',
    MultiRegion=True  # This makes it a multi-region key
)

primary_key_id = primary_key['KeyMetadata']['KeyId']

# Replicate to eu-west-1
replica = kms_primary.replicate_key(
    KeyId=primary_key_id,
    ReplicaRegion='eu-west-1'
)

replica_key_id = replica['ReplicaKeyMetadata']['KeyId']

# Encrypt in us-east-1
plaintext = b"Sensitive data"
ciphertext = kms_primary.encrypt(
    KeyId=primary_key_id,
    Plaintext=plaintext
)['CiphertextBlob']

# Decrypt in eu-west-1 (NO RE-ENCRYPTION!)
decrypted = kms_replica.decrypt(CiphertextBlob=ciphertext)['Plaintext']

assert decrypted == plaintext
print("✅ Cross-region decryption without re-encryption!")
```

---

# VPC Peering Cross-Region Security

## Question 5: Private Cross-Region Connectivity

**Scenario:**
You need to connect VPC in us-east-1 with VPC in eu-west-1 privately. Security requirements: "No internet exposure, encrypted in transit, least privilege security groups."

**Question:** What's the secure architecture?

**Options:**
- A) VPN connection over internet
- B) Cross-region VPC peering + reference security groups across regions
- C) Public internet with TLS
- D) Direct Connect across regions

**Answer:** B (with caveat: cannot reference SG IDs across regions, must use CIDR blocks)

---

## Explanation: Cross-Region VPC Peering

### Architecture:

```
us-east-1 VPC (10.0.0.0/16)
├── Security Group: Allow 192.168.0.0/16 (eu-west-1 CIDR)
└── Route: 192.168.0.0/16 → pcx-12345

         │ VPC Peering (pcx-12345)
         │ ✅ AWS private network
         │ ✅ Encrypted in transit
         ▼

eu-west-1 VPC (192.168.0.0/16)
├── Security Group: Allow 10.0.0.0/16 (us-east-1 CIDR)
└── Route: 10.0.0.0/16 → pcx-12345

Important: Cannot reference SG IDs across regions
```

### Implementation:

```python
import boto3

ec2_us = boto3.client('ec2', region_name='us-east-1')
ec2_eu = boto3.client('ec2', region_name='eu-west-1')

# Create peering connection
peering = ec2_us.create_vpc_peering_connection(
    PeerVpcId='vpc-eu-67890',
    VpcId='vpc-us-12345',
    PeerRegion='eu-west-1'
)

peering_id = peering['VpcPeeringConnection']['VpcPeeringConnectionId']

# Accept in eu-west-1
ec2_eu.accept_vpc_peering_connection(VpcPeeringConnectionId=peering_id)

# Update route tables (both sides)
ec2_us.create_route(
    RouteTableId='rtb-us-123',
    DestinationCidrBlock='192.168.0.0/16',
    VpcPeeringConnectionId=peering_id
)

ec2_eu.create_route(
    RouteTableId='rtb-eu-456',
    DestinationCidrBlock='10.0.0.0/16',
    VpcPeeringConnectionId=peering_id
)

# Update security groups (use CIDR, not SG IDs)
ec2_us.authorize_security_group_ingress(
    GroupId='sg-us-123',
    IpPermissions=[{
        'IpProtocol': 'tcp',
        'FromPort': 443,
        'ToPort': 443,
        'IpRanges': [{'CidrIp': '192.168.0.0/16'}]  # CIDR, not SG ID
    }]
)

print("✅ Cross-region VPC peering configured")
print("   ⚠️  Using CIDR blocks (cannot reference SG IDs across regions)")
```

---

# AWS Systems Manager Session Manager Cross-Region

## Question 6: Keyless SSH Alternative

**Scenario:**
You manage EC2 instances across 5 regions. Security requirement: "No SSH keys, no bastion hosts, all session logs must be centralized, encrypted connections."

**Question:** Best solution?

**Options:**
- A) SSH with keys from bastion host
- B) Systems Manager Session Manager with CloudWatch Logs + S3 logging in central region
- C) RDP for Windows instances
- D) AWS Cloud9 for terminal access

**Answer:** B

---

## Explanation: Session Manager Centralized Logging

### Architecture:

```
All Regions → Session Manager → Central Logging
├── us-east-1 sessions
├── eu-west-1 sessions
├── ap-south-1 sessions
└── All encrypted with KMS

Central Region (us-east-1):
├── CloudWatch Logs (90 days)
├── S3 Bucket (long-term, encrypted)
└── EventBridge (alerts)

Benefits:
✅ No SSH keys
✅ No bastion hosts
✅ IAM-based access
✅ Complete audit trail
```

### Implementation:

```python
import boto3
import json

regions = ['us-east-1', 'eu-west-1', 'ap-south-1']

# Create central logging bucket
s3 = boto3.client('s3')
s3.create_bucket(Bucket='ssm-session-logs-central')

# Create CloudWatch log group
logs = boto3.client('logs')
logs.create_log_group(logGroupName='/aws/ssm/session-logs')

# Configure Session Manager in each region
for region in regions:
    ssm = boto3.client('ssm', region_name=region)
    
    ssm.create_document(
        Content=json.dumps({
            "schemaVersion": "1.0",
            "sessionType": "Standard_Stream",
            "inputs": {
                "s3BucketName": "ssm-session-logs-central",
                "cloudWatchLogGroupName": "/aws/ssm/session-logs",
                "cloudWatchEncryptionEnabled": True,
                "kmsKeyId": "alias/ssm-encryption"
            }
        }),
        Name='SSM-SessionManagerRunShell',
        DocumentType='Session'
    )
    
    print(f"✅ Session Manager configured in {region}")

print("✅ Centralized session logging enabled")
```

---

# AWS Backup Cross-Region

## Question 7: Ransomware Protection

**Scenario:**
Ransomware protection requirement: "All EBS snapshots and RDS backups must be copied to a separate region, immutable for 30 days minimum, cannot be deleted by any user including root."

**Question:** Best architecture?

**Options:**
- A) Manual snapshot copies to another region
- B) AWS Backup with cross-region copy + vault lock (compliance mode)
- C) Lambda function to copy snapshots
- D) EBS snapshot lifecycle policy only

**Answer:** B

---

## Explanation: AWS Backup with Vault Lock

### Architecture:

```
Primary Region (us-east-1):
├── Production Resources
├── AWS Backup Plan
└── Daily backups

         │ Cross-region copy
         ▼

Secondary Region (eu-west-1):
├── Backup Vault (LOCKED)
├── Vault Lock: COMPLIANCE mode
├── Retention: 30 days minimum
└── CANNOT be deleted (even by root)

Ransomware Attack:
├── ❌ Primary backups deleted
├── ✅ Secondary backups protected (locked)
└── ✅ Restore from secondary region
```

### Implementation:

```python
import boto3

backup_primary = boto3.client('backup', region_name='us-east-1')
backup_secondary = boto3.client('backup', region_name='eu-west-1')

# Create secondary vault with lock
backup_secondary.create_backup_vault(
    BackupVaultName='vault-secondary-immutable'
)

# Apply vault lock (COMPLIANCE mode)
backup_secondary.put_backup_vault_lock_configuration(
    BackupVaultName='vault-secondary-immutable',
    MinRetentionDays=30,  # Immutable for 30 days
    MaxRetentionDays=365
)

# Create backup plan with cross-region copy
plan = backup_primary.create_backup_plan(
    BackupPlan={
        'BackupPlanName': 'ransomware-protection',
        'Rules': [{
            'RuleName': 'daily-cross-region',
            'TargetBackupVaultName': 'vault-primary',
            'ScheduleExpression': 'cron(0 2 * * ? *)',
            'CopyActions': [{
                'DestinationBackupVaultArn': 'arn:aws:backup:eu-west-1:123456:backup-vault:vault-secondary-immutable',
                'Lifecycle': {'DeleteAfterDays': 90}
            }]
        }]
    }
)

print("✅ Ransomware-proof backup configured")
print("   ✅ Cross-region copy to eu-west-1")
print("   ✅ Vault locked (30 days minimum)")
print("   🔒 Cannot be deleted by anyone")
```

---

# Route 53 Cross-Region Failover

## Question 8: DNS-Based Disaster Recovery

**Scenario:**
Application runs in us-east-1 (primary) and eu-west-1 (DR). Need automatic DNS failover if primary region fails with health checks.

**Question:** Best Route 53 configuration?

**Options:**
- A) Simple routing
- B) Weighted routing (50/50)
- C) Failover routing with health checks on primary
- D) Geolocation routing

**Answer:** C

---

## Explanation: Failover Routing with Health Checks

### Architecture:

```
Route 53 Failover:

Normal Operation:
app.example.com → PRIMARY (us-east-1)
├── Health check: HEALTHY ✅
└── All traffic to primary

Primary Region Failure:
├── Health check: UNHEALTHY ❌
├── Automatic failover (~90 seconds)
└── All traffic to SECONDARY (eu-west-1)

Recovery:
├── Primary healthy again
└── Automatic failback to primary
```

### Implementation:

```python
import boto3

route53 = boto3.client('route53')

# Create health checks
primary_hc = route53.create_health_check(
    HealthCheckConfig={
        'Type': 'HTTPS',
        'ResourcePath': '/health',
        'FullyQualifiedDomainName': 'alb-us-east-1.elb.amazonaws.com',
        'Port': 443,
        'RequestInterval': 30,
        'FailureThreshold': 3
    }
)

# Create failover records
route53.change_resource_record_sets(
    HostedZoneId='Z1234567890ABC',
    ChangeBatch={
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': 'app.example.com',
                    'Type': 'A',
                    'SetIdentifier': 'primary-us-east-1',
                    'Failover': 'PRIMARY',
                    'AliasTarget': {
                        'HostedZoneId': 'Z35SXDOTRQ7X7K',
                        'DNSName': 'alb-us-east-1.elb.amazonaws.com',
                        'EvaluateTargetHealth': True
                    },
                    'HealthCheckId': primary_hc['HealthCheck']['Id'],
                    'TTL': 60
                }
            },
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': 'app.example.com',
                    'Type': 'A',
                    'SetIdentifier': 'secondary-eu-west-1',
                    'Failover': 'SECONDARY',
                    'AliasTarget': {
                        'HostedZoneId': 'Z32O12XQLNTSW2',
                        'DNSName': 'alb-eu-west-1.elb.amazonaws.com',
                        'EvaluateTargetHealth': True
                    },
                    'TTL': 60
                }
            }
        ]
    }
)

print("✅ Failover routing configured")
print("   Detection time: ~90 seconds")
print("   Total failover: ~150 seconds")
```

---

# AWS Certificate Manager Cross-Region

## Question 9: TLS Certificate Management

**Scenario:**
You need TLS certificates for CloudFront distribution (global) and ALBs in us-east-1 and eu-west-1.

**Question:** Where must ACM certificates be created?

**Options:**
- A) All in us-east-1
- B) CloudFront certificate in us-east-1, ALB certificates in their respective regions
- C) Any region, certificates work globally
- D) Must use third-party certificates for CloudFront

**Answer:** B

---

## Explanation: ACM Regional Requirements

### Key Rules:

```
CloudFront:
├── Certificate MUST be in us-east-1
├── Works globally at all edge locations
└── Cannot use certificates from other regions

ALB/NLB:
├── Certificate MUST be in same region as load balancer
├── us-east-1 ALB → us-east-1 certificate
├── eu-west-1 ALB → eu-west-1 certificate
└── Cannot share certificates across regions
```

### Implementation:

```python
import boto3

acm_us = boto3.client('acm', region_name='us-east-1')
acm_eu = boto3.client('acm', region_name='eu-west-1')

# Certificate for CloudFront (MUST be us-east-1)
cloudfront_cert = acm_us.request_certificate(
    DomainName='example.com',
    SubjectAlternativeNames=['*.example.com'],
    ValidationMethod='DNS'
)
print(f"✅ CloudFront cert (us-east-1): {cloudfront_cert['CertificateArn']}")

# Certificate for ALB in us-east-1
alb_us_cert = acm_us.request_certificate(
    DomainName='us.example.com',
    ValidationMethod='DNS'
)
print(f"✅ ALB us-east-1 cert: {alb_us_cert['CertificateArn']}")

# Certificate for ALB in eu-west-1
alb_eu_cert = acm_eu.request_certificate(
    DomainName='eu.example.com',
    ValidationMethod='DNS'
)
print(f"✅ ALB eu-west-1 cert: {alb_eu_cert['CertificateArn']}")

print("\n📋 Summary:")
print("   CloudFront: us-east-1 (required)")
print("   ALB us-east-1: us-east-1")
print("   ALB eu-west-1: eu-west-1 (required)")
```

---

# AWS Secrets Manager Cross-Region Replication

## Question 10: Credential Synchronization

**Scenario:**
Application uses database credentials stored in Secrets Manager. Need same credentials available in multiple regions for DR with automatic rotation.

**Question:** Best solution?

**Options:**
- A) Manually copy secrets to each region
- B) Secrets Manager replica secrets with automatic replication + rotation
- C) Parameter Store cross-region
- D) Store credentials in S3 with replication

**Answer:** B

---

## Explanation: Secrets Manager Replica Secrets

### Architecture:

```
Primary Secret (us-east-1):
├── Username: admin
├── Password: auto-rotated-xyz123
├── Rotation: Every 30 days
└── KMS encrypted

         │ Automatic replication (seconds)
         ▼

Replica Secrets:
├── eu-west-1: Same credentials (auto-synced)
└── ap-south-1: Same credentials (auto-synced)

Rotation Flow:
1. Primary secret rotated (us-east-1)
2. Lambda updates database password
3. Replicas auto-sync within seconds
4. All regions have new password
```

### Implementation:

```python
import boto3
import json

secrets_primary = boto3.client('secretsmanager', region_name='us-east-1')

# Create secret with replicas
secret = secrets_primary.create_secret(
    Name='database/production/credentials',
    SecretString=json.dumps({
        "username": "admin",
        "password": "initial-password",
        "host": "db.us-east-1.rds.amazonaws.com",
        "port": 5432
    }),
    AddReplicaRegions=[
        {'Region': 'eu-west-1'},
        {'Region': 'ap-south-1'}
    ]
)

# Enable automatic rotation
secrets_primary.rotate_secret(
    SecretId=secret['ARN'],
    RotationLambdaARN='arn:aws:lambda:us-east-1:123456:function:RotateSecret',
    RotationRules={'AutomaticallyAfterDays': 30}
)

print("✅ Secret created with replication")
print("   Primary: us-east-1")
print("   Replicas: eu-west-1, ap-south-1")
print("   Rotation: Every 30 days")
print("   ✅ Replicas auto-sync on rotation")

# Application code (any region)
secrets_local = boto3.client('secretsmanager', region_name='eu-west-1')
creds = secrets_local.get_secret_value(SecretId='database/production/credentials')
print(f"✅ Read from eu-west-1 replica: {creds['SecretString']}")
```

---

# Summary & Key Takeaways

## Your Performance:
- **Total Questions:** 10
- **Correct Answers:** 6
- **Score:** 60%

### Questions Breakdown:
1. ✅ S3 Cross-Region Replication (KMS)
2. ❌ GuardDuty Aggregation (need Security Hub)
3. ✅ CloudTrail Organization Trail
4. ❌ KMS Multi-Region (same material, not different)
5. ❌ VPC Peering (CIDR blocks, not SG IDs)
6. ✅ Session Manager
7. ✅ AWS Backup Vault Lock
8. ✅ Route 53 Failover
9. ❌ ACM Regional Requirements
10. ✅ Secrets Manager Replication

---

## Cross-Region Security Patterns

### 1. Data Replication:
```
S3: Cross-region replication with separate KMS keys
RDS: Read replicas with encrypted snapshots
DynamoDB: Global tables with encryption
```

### 2. Key Management:
```
Standard Keys: Regional (separate per region)
Multi-Region Keys: Same material, different IDs
Use Case: Decrypt in any region without re-encryption
```

### 3. Monitoring & Logging:
```
GuardDuty: Regional (aggregate via Security Hub)
CloudTrail: Multi-region trail (single configuration)
Security Hub: Finding aggregator (central dashboard)
```

### 4. Network Connectivity:
```
VPC Peering: Private, encrypted, CIDR-based rules
Transit Gateway: Hub-and-spoke, multi-region peering
PrivateLink: Service endpoints (regional)
```

### 5. Disaster Recovery:
```
Route 53: Failover routing with health checks
AWS Backup: Cross-region with vault lock
Secrets Manager: Replica secrets (auto-sync)
```

---

## Best Practices

### Security:
- ✅ Use separate KMS keys per region
- ✅ Enable encryption in transit (TLS)
- ✅ Enable encryption at rest (KMS)
- ✅ Use Object Lock for immutability
- ✅ Enable audit logging (CloudTrail)
- ✅ Centralize monitoring (Security Hub)

### High Availability:
- ✅ Multi-region architecture
- ✅ Automated failover (Route 53)
- ✅ Cross-region backups
- ✅ Replica resources in DR region
- ✅ Test failover regularly

### Compliance:
- ✅ Data residency (regional keys/storage)
- ✅ Immutable logs (Object Lock)
- ✅ Audit trail (CloudTrail + validation)
- ✅ Encryption everywhere
- ✅ Access control (IAM + SCPs)

---

## Regional Limitations to Remember

```
Service              | Limitation
---------------------|----------------------------
KMS                  | Keys are regional (except multi-region keys)
ACM                  | CloudFront certs must be in us-east-1
Security Groups      | Cannot reference IDs across regions
GuardDuty            | Regional service (aggregate via Security Hub)
VPC Peering          | No transitive peering
Secrets Manager      | Replicas are read-only
Route 53             | Global service (but health checks are regional)
S3                   | Bucket names globally unique
```

---

## Disaster Recovery Timing

```
Service                 | Failover Time
------------------------|------------------
Route 53 Failover       | ~150 seconds
RDS Cross-Region Replica| Seconds to minutes (depends on replication lag)
S3 Replication          | Typically < 15 minutes
Secrets Manager Replica | Seconds
AWS Backup Restore      | Minutes to hours (depends on data size)
VPC Peering             | Instant (once configured)
```

---

## Cost Considerations

```
Cross-Region Data Transfer:
├── $0.02 per GB (out to another region)
├── Free within same region
└── Plan for data transfer costs

Services:
├── GuardDuty: Per 1M events
├── Security Hub: Per finding
├── Secrets Manager: $0.40/secret/month + replicas
├── AWS Backup: Storage + restore
├── CloudTrail: Free (first trail), data events cost
└── KMS: $1/key/month + API calls
```

---

## Interview Talking Points

**For Security Architect roles, emphasize:**

1. **Defense in Depth** - Multiple security layers across regions
2. **Regional Isolation** - Separate keys, separate encryption
3. **Immutability** - Object Lock, Vault Lock for compliance
4. **Centralized Monitoring** - Security Hub aggregation
5. **Disaster Recovery** - Multi-region architecture
6. **Compliance** - Data residency, encryption, audit logs
7. **Automation** - Automatic failover, replication, rotation
8. **Cost Optimization** - Data transfer, replica costs
9. **Zero Trust** - IAM-based access, no SSH keys
10. **Incident Response** - Session Manager, automated remediation

---

*Generated: November 30, 2024*
*Total Questions: 10*
*Your Score: 60%*
*Focus Areas: Regional limitations, service-specific requirements, cross-region patterns*

**You're building strong cross-region security knowledge!**
