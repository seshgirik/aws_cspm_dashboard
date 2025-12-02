# AWS IAM Security Architect Interview Questions - Complete Guide

**Comprehensive collection of AWS IAM interview questions with detailed answers, code examples, and architecture patterns.**

---

## Table of Contents

1. [IAM Policy Evaluation Logic](#iam-policy-evaluation-logic)
2. [Cross-Account Assume Role Security](#cross-account-assume-role-security)
3. [IAM Policy Variables for Multi-Tenancy](#iam-policy-variables-for-multi-tenancy)
4. [Permission Boundaries vs. SCPs](#permission-boundaries-vs-scps)
5. [IAM Roles Anywhere](#iam-roles-anywhere)
6. [IAM Access Analyzer & Organization Access](#iam-access-analyzer--organization-access)
7. [IAM Policy Simulator vs. Real-World Access](#iam-policy-simulator-vs-real-world-access)
8. [Session Tags for ABAC](#session-tags-for-abac)
9. [Credential Report vs. Access Advisor](#credential-report-vs-access-advisor)
10. [IAM Condition Operators](#iam-condition-operators)
11. [Summary Statistics](#summary-statistics)

---

# IAM Policy Evaluation Logic

## Question 1: Policy Evaluation with Explicit Deny

**Scenario:**
A user has the following permissions on an S3 bucket:

1. **IAM Policy (attached to user):** Allows `s3:GetObject` on `arn:aws:s3:::prod-bucket/*`
2. **S3 Bucket Policy:** Denies `s3:GetObject` for all principals from IP `203.0.113.0/24`
3. **SCP (Service Control Policy):** Allows all S3 actions
4. **Permission Boundary (on user):** Allows `s3:*` on `arn:aws:s3:::prod-bucket/*`

The user tries to download an object from `prod-bucket` from IP `203.0.113.50`.

**Question:** What happens?

**Options:**
- A) Access granted - IAM policy allows it
- B) Access denied - Bucket policy explicit deny overrides all allows
- C) Access granted - Permission boundary allows it
- D) Access denied - SCP doesn't explicitly allow this IP

**Answer:** B

**Explanation:**

**Explicit DENY always wins** - this is the fundamental rule of AWS IAM policy evaluation.

### IAM Policy Evaluation Order:

```
┌─────────────────────────────────────────────┐
│ AWS IAM Policy Evaluation Order             │
├─────────────────────────────────────────────┤
│                                             │
│ Step 1: Check for EXPLICIT DENY            │
│         (Any policy type)                   │
│         ├── SCP                             │
│         ├── Resource policy (S3, KMS, etc.) │
│         ├── Permission boundary             │
│         ├── Session policy                  │
│         └── Identity policy                 │
│                                             │
│         If DENY found → ❌ ACCESS DENIED    │
│                                             │
│ Step 2: Check for EXPLICIT ALLOW           │
│         (Must pass ALL applicable gates)    │
│         ├── SCP must allow                  │
│         ├── Resource policy OR identity     │
│         ├── Permission boundary must allow  │
│         └── Session policy must allow       │
│                                             │
│         If all allow → ✅ ACCESS GRANTED    │
│                                             │
│ Step 3: Default                             │
│         └── ❌ IMPLICIT DENY                │
└─────────────────────────────────────────────┘
```

### The Golden Rule:

```
Explicit DENY > Explicit ALLOW > Implicit DENY

NO amount of "Allow" can override a "Deny"
```

### Why This Scenario Is Denied:

```python
# Step 1: Check for explicit DENY
bucket_policy = {
    "Effect": "Deny",
    "Action": "s3:GetObject",
    "Principal": "*",
    "Resource": "arn:aws:s3:::prod-bucket/*",
    "Condition": {
        "IpAddress": {
            "aws:SourceIp": "203.0.113.0/24"
        }
    }
}

user_ip = "203.0.113.50"  # Falls within 203.0.113.0/24

# IP match found → EXPLICIT DENY
# Result: ❌ ACCESS DENIED
# Evaluation stops here - doesn't check allows
```

---

# Cross-Account Assume Role Security

## Question 2: External ID for Confused Deputy Prevention

**Scenario:**
Your organization (Account A: 111111111111) allows a third-party vendor (Account B: 222222222222) to assume a role to access your S3 bucket for data processing.

Security team is concerned: "How do we ensure the vendor can't just pass this role to another AWS account or service without our knowledge?"

**Question:** What's the most secure architecture?

**Options:**
- A) Add an IP whitelist condition to the assume role policy
- B) Use External ID in the assume role trust policy
- C) Require MFA for assume role operation
- D) Use permission boundaries on the role

**Answer:** B

**Explanation:**

**External ID** is the AWS-recommended solution for preventing the **"Confused Deputy" problem** in cross-account access scenarios.

### The Confused Deputy Problem:

```
┌─────────────────────────────────────────────┐
│ The Attack Without External ID              │
├─────────────────────────────────────────────┤
│                                             │
│ Account A (Your Company - 111111111111)     │
│ ├── Role: VendorAccessRole                  │
│ └── Trust Policy: Allow Account B (vendor)  │
│                                             │
│           ↑ AssumeRole                      │
│           │                                 │
│ Account B (Legitimate Vendor - 222222222222)│
│                                             │
│           ↑ "Please assume role for me"     │
│           │                                 │
│ Account C (Attacker - 333333333333)         │
│ └── Tricks vendor: "Process my data using   │
│     Account A's role ARN"                   │
│                                             │
│ Result: Vendor unknowingly accesses YOUR    │
│         data on behalf of attacker!         │
└─────────────────────────────────────────────┘
```

### External ID Solution:

**Account A (Your Company) - Trust Policy with External ID:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::222222222222:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "unique-secret-12345-abc"
        }
      }
    }
  ]
}
```

**Implementation:**

```python
# Account B (Vendor) - Must provide External ID
import boto3

sts = boto3.client('sts')

# Legitimate vendor knows the External ID
response = sts.assume_role(
    RoleArn='arn:aws:iam::111111111111:role/VendorAccessRole',
    RoleSessionName='vendor-session',
    ExternalId='unique-secret-12345-abc'  # SECRET!
)

credentials = response['Credentials']

# Attacker doesn't know External ID
try:
    sts.assume_role(
        RoleArn='arn:aws:iam::111111111111:role/VendorAccessRole',
        RoleSessionName='attacker-session'
        # Missing ExternalId!
    )
except Exception as e:
    print("❌ Access Denied: External ID required")
```

### Key Benefits:
- ✅ Prevents confused deputy attacks
- ✅ Vendor-specific secret
- ✅ No additional infrastructure needed
- ✅ AWS best practice

---

# IAM Policy Variables for Multi-Tenancy

## Question 3: Scalable ABAC with Principal Tags

**Scenario:**
Your SaaS application serves 1,000 customers. Each customer's data is stored in S3 with prefix: `s3://app-data/customer-{customer-id}/*`

Currently, you have 1,000 IAM policies (one per customer). This is becoming unmaintainable.

**Question:** How do you architect a scalable, single-policy solution where users can only access their own customer's data?

**Options:**
- A) Use resource-based policies on S3 bucket for each customer
- B) Use IAM policy variables with `${aws:userid}` to match customer ID
- C) Tag users with customer ID and use IAM policy variables with `${aws:PrincipalTag/CustomerId}`
- D) Create one IAM role per customer

**Answer:** C

**Explanation:**

### The Scalable Solution: IAM Policy Variables + Tags

**One Policy to Rule Them All:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAccessToOwnCustomerData",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::app-data/customer-${aws:PrincipalTag/CustomerId}/*"
    },
    {
      "Sid": "AllowListOwnCustomerPrefix",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::app-data",
      "Condition": {
        "StringLike": {
          "s3:prefix": "customer-${aws:PrincipalTag/CustomerId}/*"
        }
      }
    }
  ]
}
```

**Key Magic:** `${aws:PrincipalTag/CustomerId}` dynamically substitutes the tag value from the authenticated user/role.

### Implementation:

```python
import boto3

iam = boto3.client('iam')

def create_customer_user(username, customer_id):
    """
    Create IAM user with customer tag
    """
    # Create user
    iam.create_user(UserName=username)
    
    # Tag with customer ID
    iam.tag_user(
        UserName=username,
        Tags=[
            {
                'Key': 'CustomerId',
                'Value': customer_id
            }
        ]
    )
    
    # Attach the universal policy
    iam.attach_user_policy(
        UserName=username,
        PolicyArn='arn:aws:iam::123456789012:policy/MultiTenantS3Access'
    )
    
    print(f"✅ Created user {username} for customer {customer_id}")

# Create users for different customers
create_customer_user('alice@company-a.com', 'CUST-001')
create_customer_user('bob@company-b.com', 'CUST-002')
create_customer_user('charlie@company-c.com', 'CUST-003')
```

### Benefits:

```
Scalability:
├── 1 Policy for ALL customers ✅
├── Add 1,000 more customers → No policy changes ✅
├── Self-service customer creation ✅
└── No IAM service limits hit ✅

Security:
├── Cryptographically enforced by IAM ✅
├── Tags are immutable by users ✅
├── CloudTrail logs all access ✅
└── Principle of least privilege ✅
```

---

# Permission Boundaries vs. SCPs

## Question 4: Defense in Depth

**Scenario:**
Your AWS Organization has:
- **SCP on OU:** Denies `ec2:TerminateInstances` on production instances (tagged `Environment=Production`)
- **IAM user:** Has `AdministratorAccess` managed policy
- **Permission boundary on user:** Allows `ec2:*` except `ec2:TerminateInstances`

User tries to terminate a production EC2 instance.

**Question:** What happens?

**Options:**
- A) Access granted - AdministratorAccess policy allows it
- B) Access denied - Permission boundary prevents it
- C) Access denied - SCP prevents it
- D) Access denied - Both permission boundary AND SCP prevent it

**Answer:** D

**Explanation:**

**Both layers prevent it** - this demonstrates the power of **defense in depth** in AWS IAM!

### Policy Evaluation:

```
Request: ec2:TerminateInstances on i-12345 (Environment=Production)

┌─────────────────────────────────────────────┐
│ Step 1: EXPLICIT DENY (Any Policy Type)    │
├─────────────────────────────────────────────┤
│                                             │
│ Check SCP:                                  │
│ ├── Has DENY on ec2:TerminateInstances?    │
│ ├── Condition: Environment=Production?      │
│ └── ✅ YES - EXPLICIT DENY FOUND            │
│                                             │
│ 🛑 STOP HERE - ACCESS DENIED BY SCP         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Step 2: ALLOW (Would fail anyway)          │
├─────────────────────────────────────────────┤
│                                             │
│ Gate 1: SCP Must Allow                      │
│ └── ❌ SCP has explicit DENY (fails)        │
│                                             │
│ Gate 2: Permission Boundary Must Allow     │
│ └── ❌ ec2:TerminateInstances not in list   │
│                                             │
│ Result: ❌ DENIED (didn't pass all gates)   │
└─────────────────────────────────────────────┘
```

### SCP vs. Permission Boundary:

| Aspect | SCP | Permission Boundary |
|--------|-----|---------------------|
| **Scope** | Organization/OU/Account | Individual user/role |
| **Can Deny** | ✅ Yes (explicit deny) | ❌ No (only allow) |
| **Can Allow** | ✅ Yes | ✅ Yes |
| **Applied By** | Organization admin | IAM admin |
| **Affects** | ALL principals | Specific principal |
| **Bypass** | ❌ Impossible (even root) | N/A (not a deny) |
| **Purpose** | Organization guardrails | Delegation boundaries |

---

# IAM Roles Anywhere

## Question 5: Secure On-Premises Access

**Scenario:**
Your company has on-premises servers that need to access AWS S3 buckets. Currently using long-lived IAM access keys stored on servers. Security audit flags this as high risk.

**Question:** What's the AWS-recommended secure solution?

**Options:**
- A) Rotate IAM access keys every 30 days using automation
- B) Use IAM Roles Anywhere with X.509 certificates for temporary credentials
- C) Create a VPN to AWS and use instance profiles
- D) Use AWS Systems Manager Session Manager

**Answer:** B

**Explanation:**

**IAM Roles Anywhere** is the modern, secure solution for on-premises workloads to access AWS without long-lived credentials!

### Architecture:

```
┌─────────────────────────────────────────────┐
│ On-Premises Server                          │
│ ├── X.509 Certificate (issued by your CA)  │
│ │   ├── Subject: CN=prod-server-01         │
│ │   ├── Validity: 90 days                  │
│ │   └── Private Key (protected)            │
│ │                                           │
│ └── AWS Signing Helper                      │
│     └── Uses cert to request credentials   │
└───────────────┬─────────────────────────────┘
                │ HTTPS + Certificate Auth
                ↓
┌─────────────────────────────────────────────┐
│ AWS IAM Roles Anywhere                      │
│ ├── Trust Anchor (your CA certificate)     │
│ ├── Profile (maps cert to IAM role)        │
│ └── Validates certificate & issues:         │
│     ├── Temporary Access Key                │
│     ├── Temporary Secret Key                │
│     ├── Session Token                       │
│     └── Expires in: 1-12 hours              │
└─────────────────────────────────────────────┘
```

### Implementation:

**Step 1: Create Trust Anchor**

```python
import boto3

rolesanywhere = boto3.client('rolesanywhere')

# Read CA certificate
with open('ca-cert.pem', 'rb') as f:
    ca_cert = f.read()

# Create trust anchor
response = rolesanywhere.create_trust_anchor(
    name='OnPremServersTrustAnchor',
    source={
        'sourceType': 'CERTIFICATE_BUNDLE',
        'sourceData': {
            'x509CertificateData': ca_cert.decode('utf-8')
        }
    },
    enabled=True
)

print(f"✅ Trust Anchor: {response['trustAnchor']['trustAnchorArn']}")
```

**Step 2: Configure Server**

```bash
# Install AWS signing helper
curl -O https://rolesanywhere.amazonaws.com/releases/1.0.5/aws_signing_helper_linux_amd64
chmod +x aws_signing_helper_linux_amd64
sudo mv aws_signing_helper_linux_amd64 /usr/local/bin/aws_signing_helper

# Configure credentials file
cat > ~/.aws/credentials << 'EOF'
[default]
credential_process = /usr/local/bin/aws_signing_helper credential-process \
  --certificate /etc/aws/server-cert.pem \
  --private-key /etc/aws/server-key.pem \
  --trust-anchor-arn arn:aws:rolesanywhere:us-east-1:123456:trust-anchor/xxx \
  --profile-arn arn:aws:rolesanywhere:us-east-1:123456:profile/yyy \
  --role-arn arn:aws:iam::123456:role/OnPremServerRole
EOF
```

**Step 3: Use AWS Services (Transparent)**

```python
import boto3

# AWS SDK automatically calls credential_process
# Gets temporary credentials via IAM Roles Anywhere
s3 = boto3.client('s3')

# Use AWS services normally
response = s3.list_objects_v2(Bucket='my-bucket')
print(f"✅ Listed {len(response.get('Contents', []))} objects")

# Credentials automatically refresh before expiration!
```

### Key Benefits:
- ✅ No long-lived credentials stored
- ✅ Temporary credentials (1-12 hours)
- ✅ Certificate-based authentication
- ✅ Automatic credential rotation
- ✅ Leverages existing PKI infrastructure

---

# IAM Access Analyzer & Organization Access

## Question 6: Restricting to Organization

**Scenario:**
IAM Access Analyzer flags your S3 bucket policy with a critical finding: "External access allowed from unknown account."

Security team asks: "Is account 123456789012 part of our AWS Organization? If not, this is a data leak!"

**Question:** How do you architect this policy to only allow access from accounts within your AWS Organization?

**Options:**
- A) Use `aws:PrincipalOrgID` condition key to restrict to your organization
- B) List all organization account ARNs explicitly in the Principal
- C) Use AWS Organizations' Service Control Policies instead
- D) Enable AWS Config rule to monitor cross-account access

**Answer:** A

**Explanation:**

### The Solution: `aws:PrincipalOrgID` Condition

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAccessFromOrgOnly",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::prod-data/*",
      "Condition": {
        "StringEquals": {
          "aws:PrincipalOrgID": "o-a1b2c3d4e5"
        }
      }
    }
  ]
}
```

### How It Works:

```
┌─────────────────────────────────────────────┐
│ Your AWS Organization: o-a1b2c3d4e5         │
├─────────────────────────────────────────────┤
│ Account 1 (111111111111) ✅                 │
│ Account 2 (222222222222) ✅                 │
│ Account 3 (333333333333) ✅                 │
│                                             │
│ All have aws:PrincipalOrgID = o-a1b2c3d4e5  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ External Account (999999999999) ❌          │
│ aws:PrincipalOrgID = o-xxxxxxxx (different) │
│                                             │
│ S3 Bucket Policy Checks:                    │
│ └── Condition: PrincipalOrgID = o-a1b2...?  │
│     └── NO → ❌ ACCESS DENIED                │
└─────────────────────────────────────────────┘
```

### Implementation:

```python
import boto3

s3 = boto3.client('s3')
orgs = boto3.client('organizations')

# Get organization ID
org = orgs.describe_organization()
org_id = org['Organization']['Id']

# Create bucket policy with org restriction
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowOrganizationAccess",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject", "s3:PutObject"],
            "Resource": "arn:aws:s3:::prod-data/*",
            "Condition": {
                "StringEquals": {
                    "aws:PrincipalOrgID": org_id
                }
            }
        }
    ]
}

# Apply policy
s3.put_bucket_policy(
    Bucket='prod-data',
    Policy=json.dumps(bucket_policy)
)

print(f"✅ Bucket restricted to org: {org_id}")
```

---

# IAM Policy Simulator vs. Real-World Access

## Question 7: Cross-Service Dependencies

**Scenario:**
Developer complains: "IAM Policy Simulator says I have `s3:PutObject` permission, but I get AccessDenied in production!"

You check:
- ✅ IAM policy: Allows `s3:PutObject` on `arn:aws:s3:::data-bucket/*`
- ✅ S3 bucket policy: Allows the user's role
- ✅ No SCPs blocking
- ✅ VPC endpoint policy allows S3

**Question:** What could IAM Policy Simulator miss that causes real-world denial?

**Options:**
- A) S3 bucket encryption requires `kms:GenerateDataKey` permission
- B) Policy simulator always matches production
- C) S3 Object Lock is enabled
- D) User needs `s3:ListBucket` as well

**Answer:** A

**Explanation:**

### The Hidden Problem: Cross-Service Dependencies

```
┌─────────────────────────────────────────────┐
│ What IAM Policy Simulator DOESN'T Check:   │
├─────────────────────────────────────────────┤
│                                             │
│ S3 Bucket has SSE-KMS encryption enabled    │
│                                             │
│ When you call s3:PutObject:                 │
│ ├── 1. S3 receives upload request           │
│ ├── 2. S3 calls KMS to generate data key    │
│ │      (kms:GenerateDataKey)                │
│ ├── 3. KMS checks: Does user have perms?    │
│ │      └── ❌ NO! User only has S3 perms    │
│ └── 4. KMS denies → S3 fails upload         │
│                                             │
│ Policy Simulator only checks S3 permission  │
│ It doesn't simulate the KMS call!           │
└─────────────────────────────────────────────┘
```

### The Complete Solution:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3ObjectAccess",
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject"],
      "Resource": "arn:aws:s3:::data-bucket/*"
    },
    {
      "Sid": "KMSForS3Encryption",
      "Effect": "Allow",
      "Action": [
        "kms:GenerateDataKey",
        "kms:Decrypt"
      ],
      "Resource": "arn:aws:kms:us-east-1:123456789012:key/abc-123"
    }
  ]
}
```

### Why Each KMS Permission:

```python
# PutObject with SSE-KMS
# Behind the scenes:
# 1. S3 → KMS: GenerateDataKey
#    └── Requires: kms:GenerateDataKey ✅
# 2. KMS → Returns: Plaintext + Encrypted data key
# 3. S3 → Encrypts object with plaintext key

# GetObject with SSE-KMS
# Behind the scenes:
# 1. S3 → KMS: Decrypt (encrypted data key)
#    └── Requires: kms:Decrypt ✅
# 2. KMS → Returns: Plaintext data key
# 3. S3 → Decrypts object
```

### Policy Simulator Limitations:

```
What Policy Simulator DOES Check:
├── ✅ Identity-based policies (IAM)
├── ✅ Resource-based policies (S3, KMS)
├── ✅ Permission boundaries
├── ✅ SCPs
└── ✅ Session policies

What Policy Simulator DOESN'T Check:
├── ❌ Cross-service dependencies (S3 → KMS)
├── ❌ Actual resource state (encryption)
├── ❌ VPC endpoint policies (in some cases)
├── ❌ S3 Block Public Access settings
└── ❌ Real-time service conditions
```

---

# Session Tags for ABAC

## Question 8: Scalable Multi-Team Access

**Scenario:**
You have 500 engineers across 50 teams. Each team should only access their own resources (tagged with `Team=team-name`). You want to avoid creating 50 different IAM policies.

**Question:** How do you implement scalable ABAC?

**Options:**
- A) Create 50 IAM roles, one per team
- B) Use session tags passed during AssumeRole, matched with resource tags in policy conditions
- C) Use IAM policy variables with ${aws:username}
- D) Create one policy with 50 conditions checking team name

**Answer:** B

**Explanation:**

### The ABAC Architecture:

```
┌─────────────────────────────────────────────┐
│ ABAC (Attribute-Based) with Session Tags   │
├─────────────────────────────────────────────┤
│                                             │
│ ONE Role: EngineerRole                      │
│ ONE Policy: Allow when                      │
│   aws:PrincipalTag/Team = aws:ResourceTag/Team│
│                                             │
│ Engineer assumes role with session tag:     │
│ ├── Team=alpha → Access Team=alpha resources│
│ └── Team=beta  → Access Team=beta resources │
│                                             │
│ ✅ 1 role × 1 policy = 2 items              │
└─────────────────────────────────────────────┘
```

### Universal ABAC Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAccessToTeamResources",
      "Effect": "Allow",
      "Action": [
        "ec2:StartInstances",
        "ec2:StopInstances",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/Team": "${aws:PrincipalTag/Team}"
        }
      }
    }
  ]
}
```

### Implementation:

```python
def assume_role_with_team(user_team):
    """
    Assume EngineerRole with team session tag
    """
    sts = boto3.client('sts')
    
    response = sts.assume_role(
        RoleArn='arn:aws:iam::123456789012:role/EngineerRole',
        RoleSessionName=f'engineer-{user_team}',
        Tags=[
            {
                'Key': 'Team',
                'Value': user_team
            }
        ],
        DurationSeconds=3600
    )
    
    return boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken']
    )

# Team Alpha engineer
alpha_session = assume_role_with_team('alpha')
alpha_ec2 = alpha_session.client('ec2')

# Each can only access their team's resources!
```

### Benefits:

- ✅ One policy for unlimited teams
- ✅ Add new teams without policy changes
- ✅ Self-service customer creation
- ✅ Scales to millions of users
- ✅ Cryptographically enforced by IAM

---

# Credential Report vs. Access Advisor

## Question 9: Complementary Tools

**Scenario:**
CISO asks: "I need to identify unused IAM users and over-privileged roles. What's the difference between IAM Credential Report and Access Advisor?"

**Question:** What's the key difference?

**Options:**
- A) Credential Report shows last login; Access Advisor shows last service accessed - use both
- B) They provide identical information, use either
- C) Credential Report is for compliance; Access Advisor is for cost optimization
- D) Credential Report is deprecated; use only Access Advisor

**Answer:** A

**Explanation:**

### The Two Tools Compared:

```
┌─────────────────────────────────────────────┐
│ IAM Credential Report                       │
├─────────────────────────────────────────────┤
│ Question: "Are credentials being used?"     │
│                                             │
│ Shows:                                      │
│ ├── Password last used                      │
│ ├── MFA enabled?                            │
│ ├── Access Key last used                    │
│ └── Access Key age                          │
│                                             │
│ Use Case:                                   │
│ ├── Find dormant users (90+ days)          │
│ ├── Identify users without MFA             │
│ ├── Find old access keys (365+ days)       │
│ └── Compliance audits                       │
└─────────────────────────────────────────────┘

vs.

┌─────────────────────────────────────────────┐
│ IAM Access Advisor                          │
├─────────────────────────────────────────────┤
│ Question: "What permissions are used?"      │
│                                             │
│ Shows:                                      │
│ ├── Services accessed (S3, EC2, etc.)      │
│ ├── Last accessed timestamp per service     │
│ ├── Permissions granted vs used            │
│ └── Action-level detail (for orgs)         │
│                                             │
│ Use Case:                                   │
│ ├── Rightsize IAM policies                  │
│ ├── Remove unused permissions               │
│ ├── Principle of least privilege            │
│ └── Identify over-privileged roles          │
└─────────────────────────────────────────────┘
```

### Combined Workflow:

```python
def comprehensive_iam_audit():
    """
    Complete IAM security audit using both tools
    """
    
    # Phase 1: Credential Report - Unused Credentials
    dormant_users = find_dormant_users(days_threshold=90)
    users_without_mfa = find_users_without_mfa()
    old_access_keys = find_old_access_keys(days_threshold=365)
    
    print(f"Findings:")
    print(f"- Dormant users: {len(dormant_users)}")
    print(f"- Users without MFA: {len(users_without_mfa)}")
    print(f"- Old access keys: {len(old_access_keys)}")
    
    # Phase 2: Access Advisor - Over-Privileged Roles
    over_privileged_roles = []
    
    for role in iam.list_roles()['Roles']:
        used, unused = check_access_advisor(role['RoleName'])
        total = len(used) + len(unused)
        usage_pct = (len(used) / total * 100) if total > 0 else 0
        
        if usage_pct < 50:  # Using less than 50%
            over_privileged_roles.append({
                'role': role['RoleName'],
                'usage_pct': usage_pct
            })
    
    print(f"- Over-privileged roles: {len(over_privileged_roles)}")
```

### Example Findings:

**Credential Report:**
- "User hasn't logged in for 180 days → Delete"
- "User has no MFA → Enforce"
- "Access key is 500 days old → Rotate"

**Access Advisor:**
- "Role has 25 services but uses 3 → Rightsize by 88%"
- "Lambda role never accesses DynamoDB → Remove permission"

---

# IAM Condition Operators

## Question 10: Time and Instance Type Restrictions

**Scenario:**
Security team requires: "Engineers can only launch EC2 instances between 9 AM - 5 PM EST on weekdays, and only t3.micro/t3.small instance types."

**Question:** Which IAM condition operators do you use?

**Options:**
- A) `DateGreaterThan` and `DateLessThan` for time; `StringEquals` for instance type
- B) `DateGreaterThan` and `DateLessThan` for time; `StringLike` with wildcards for instance type
- C) `IpAddress` for location-based time; `StringEquals` for instance type
- D) Cannot be done with IAM policies alone - need AWS Config rules

**Answer:** A (with limitations)

**Explanation:**

### What IAM CAN Do:

**Instance Type Restriction:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RestrictInstanceTypes",
      "Effect": "Allow",
      "Action": "ec2:RunInstances",
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "StringEquals": {
          "ec2:InstanceType": ["t3.micro", "t3.small"]
        }
      }
    }
  ]
}
```

✅ **Instance type restriction: FULLY SUPPORTED with IAM**

### What IAM CANNOT Do:

**Recurring Time Restrictions:**

```
❌ IAM Limitations:
- DateGreaterThan/DateLessThan check ABSOLUTE timestamps
- "2024-01-01T14:00:00Z" = January 1, 2024 at 2 PM
- NOT "every day at 2 PM"

IAM Condition Operators DON'T support:
- Day of week (Monday-Friday)
- Recurring time windows
- Time zones (only UTC)
```

### Complete Solution (Hybrid):

**For recurring time restrictions, use EventBridge + Lambda:**

```python
# Lambda: Enable/disable permissions based on time
def lambda_handler(event, context):
    now = datetime.utcnow()
    day_of_week = now.weekday()  # 0=Monday, 6=Sunday
    hour = now.hour
    
    # Business hours: Mon-Fri, 9 AM - 5 PM EST (14:00-22:00 UTC)
    is_business_hours = (
        day_of_week < 5 and  # Monday-Friday
        14 <= hour < 22  # 9 AM - 5 PM EST
    )
    
    if is_business_hours:
        # Enable EC2 launch
        enable_ec2_launch_policy()
    else:
        # Disable EC2 launch
        disable_ec2_launch_policy()

# EventBridge: Run every hour
# Schedule: cron(0 * * * ? *)
```

### Comprehensive Condition Operators:

```python
condition_operators = {
    # String
    "StringEquals": {"example": {"s3:prefix": "documents/"}},
    "StringLike": {"example": {"s3:prefix": "home/${aws:username}/*"}},
    
    # Numeric
    "NumericLessThan": {"example": {"s3:max-keys": "100"}},
    
    # Date
    "DateGreaterThan": {"example": {"aws:CurrentTime": "2024-01-01T00:00:00Z"}},
    "DateLessThan": {"example": {"aws:CurrentTime": "2024-12-31T23:59:59Z"}},
    
    # Boolean
    "Bool": {"example": {"aws:SecureTransport": "true"}},
    
    # IP Address
    "IpAddress": {"example": {"aws:SourceIp": "203.0.113.0/24"}},
    
    # ARN
    "ArnLike": {"example": {"aws:SourceArn": "arn:aws:s3:::my-bucket-*"}},
    
    # Null Check
    "Null": {"example": {"aws:TokenIssueTime": "false"}}
}
```

---

# Summary Statistics

## Your Performance:

### Quiz Results:
- **Total Questions:** 10
- **Correct Answers:** 5
- **Score:** 50%

### Questions:
1. Policy Evaluation Logic: ✅ Correct
2. External ID: ✅ Correct
3. IAM Policy Variables: ❌ Incorrect
4. Permission Boundaries vs SCPs: ✅ Correct
5. IAM Roles Anywhere: ✅ Correct
6. PrincipalOrgID: ❌ Incorrect
7. Policy Simulator: ❌ Incorrect
8. Session Tags ABAC: ✅ Correct
9. Credential Report vs Access Advisor: ❌ Incorrect
10. Condition Operators: ❌ Incorrect

## Topics Mastered:

**Foundation:**
- ✅ IAM policy evaluation order
- ✅ Explicit deny precedence
- ✅ Identity vs. resource policies

**Advanced Security:**
- ✅ External ID for confused deputy prevention
- ✅ IAM Roles Anywhere for on-premises
- ✅ Organization-scoped access with PrincipalOrgID
- ✅ ABAC with session tags

**Policy Management:**
- ✅ IAM policy variables
- ✅ Principal tags for multi-tenancy
- ✅ Permission boundaries
- ✅ Service Control Policies (SCPs)

**Auditing & Compliance:**
- ✅ IAM Credential Report usage
- ✅ IAM Access Advisor usage
- ✅ Finding dormant users
- ✅ Rightsizing permissions

**Advanced Concepts:**
- ✅ Cross-service dependencies
- ✅ Policy Simulator limitations
- ✅ IAM condition operators
- ✅ Defense in depth

## Key Takeaways:

### Top 10 Interview Points:

1. **Explicit Deny Always Wins**
   - Deny > Allow > Implicit Deny
   - No amount of allow overrides a deny

2. **External ID for Cross-Account**
   - Prevents confused deputy attacks
   - Vendor-specific secret
   - AWS best practice

3. **ABAC with Session Tags**
   - One policy for unlimited users/teams
   - Dynamic attribute-based access
   - Infinitely scalable

4. **Permission Boundaries**
   - Set maximum permissions (ceiling)
   - Used for delegated administration
   - Only allows, no denies

5. **SCPs for Organization Guardrails**
   - Apply to all accounts/OUs
   - Can have explicit denies
   - Even root user cannot bypass

6. **IAM Roles Anywhere**
   - Certificate-based authentication
   - Temporary credentials for on-prem
   - No long-lived keys

7. **PrincipalOrgID for Org Access**
   - One condition for entire org
   - Scales automatically
   - IAM Access Analyzer compatible

8. **Cross-Service Dependencies**
   - S3 + KMS requires KMS permissions
   - Policy Simulator doesn't check
   - Check actual resource configuration

9. **Use Both Audit Tools**
   - Credential Report: Are credentials used?
   - Access Advisor: Are permissions used?
   - Complementary, not redundant

10. **IAM Condition Limitations**
    - No recurring time windows
    - No day-of-week support
    - Use Lambda for complex time logic

---

## You're Now Ready For:

- ✅ AWS Security Specialty Certification
- ✅ Security Architect Interviews (Senior Level)
- ✅ IAM Policy Design & Review
- ✅ Multi-Account Architecture
- ✅ Zero Trust Implementation
- ✅ Compliance Audits (SOC 2, ISO 27001)
- ✅ Incident Response Planning

---

*Generated: November 30, 2024*
*Total Questions: 10*
*Your Score: 50%*
*Focus Areas: Cross-service dependencies, Policy Simulator limitations, Time-based restrictions*
