# AWS Lambda Security - Cloud Security Architect Interview Questions

**Comprehensive guide covering 10 advanced Lambda security topics for cloud security architect interviews. Your score: 7/10 (70%)**

---

## Your Performance Summary

| Question | Topic | Your Answer | Correct | Result |
|----------|-------|-------------|---------|--------|
| 1 | Execution Role vs Resource Policy | C | B | ❌ |
| 2 | Secrets Management | B | C | ❌ |
| 3 | VPC Integration Security | C | C | ✅ |
| 4 | Function URL Security | C | B | ❌ |
| 5 | Lambda Layer Security | B | B | ✅ |
| 6 | Dead Letter Queue Security | B | B | ✅ |
| 7 | Concurrency & Throttling | B | B | ✅ |
| 8 | Code Signing | B | B | ✅ |
| 9 | Resource-Based Policy | B | B | ✅ |
| 10 | Runtime Security | B | B | ✅ |

---

## Table of Contents

1. [Lambda Permission Model](#1-lambda-permission-model)
2. [Secrets Management Best Practices](#2-secrets-management)
3. [VPC Security](#3-vpc-security)
4. [Function URL Limitations](#4-function-url-security)
5. [Layer Security](#5-layer-security)
6. [DLQ Security for PII](#6-dlq-security)
7. [Concurrency Protection](#7-concurrency-protection)
8. [Code Signing](#8-code-signing)
9. [Resource-Based Policies](#9-resource-based-policies)
10. [Runtime Management](#10-runtime-management)

---

## 1. Lambda Permission Model

### Question
Which permissions go where: DynamoDB read, S3 write, API Gateway invoke, EventBridge invoke?

**Answer: B** - DynamoDB + S3 in execution role, API Gateway + EventBridge in resource-based policy

### Key Concept
```
Execution Role (What Lambda CAN DO):
├── Lambda → DynamoDB (read)
├── Lambda → S3 (write)
├── Lambda → CloudWatch Logs
└── Lambda → KMS (decrypt secrets)

Resource-Based Policy (WHO CAN INVOKE Lambda):
├── API Gateway → Lambda
├── EventBridge → Lambda
├── S3 Events → Lambda
└── SNS → Lambda
```

### Configuration Examples

**Execution Role:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {"Effect": "Allow", "Action": ["dynamodb:GetItem"], "Resource": "arn:aws:dynamodb:*:*:table/MyTable"},
    {"Effect": "Allow", "Action": ["s3:PutObject"], "Resource": "arn:aws:s3:::my-bucket/*"},
    {"Effect": "Allow", "Action": ["logs:CreateLogStream", "logs:PutLogEvents"], "Resource": "*"}
  ]
}
```

**Resource-Based Policy:**
```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "apigateway.amazonaws.com"},
      "Action": "lambda:InvokeFunction",
      "Condition": {"ArnLike": {"AWS:SourceArn": "arn:aws:execute-api:*:*:api-id/*"}}
    },
    {
      "Effect": "Allow",
      "Principal": {"Service": "events.amazonaws.com"},
      "Action": "lambda:InvokeFunction",
      "Condition": {"ArnLike": {"AWS:SourceArn": "arn:aws:events:*:*:rule/rule-name"}}
    }
  ]
}
```

---

## 2. Secrets Management

### Question
Most secure approach for database credentials in production?

**Answer: C** - Secrets Manager with automatic rotation + runtime retrieval

### Why Secrets Manager is Best

```
Environment Variables ❌
├── Visible in Lambda console
├── Exposed in IaC templates
├── Manual rotation required
└── No audit trail

Secrets Manager ✅
├── Not stored in Lambda config
├── Retrieved at runtime
├── Automatic rotation (30 days)
├── Version management
├── CloudTrail audit trail
└── Fine-grained access control
```

### Configuration

```json
{
  "SecretId": "prod/database/credentials",
  "RotationEnabled": true,
  "RotationRules": {"AutomaticallyAfterDays": 30},
  "KmsKeyId": "arn:aws:kms:*:*:key/customer-managed-key"
}
```

**Lambda Execution Role:**
```json
{
  "Statement": [{
    "Effect": "Allow",
    "Action": ["secretsmanager:GetSecretValue"],
    "Resource": "arn:aws:secretsmanager:*:*:secret:prod/database/credentials-*"
  }]
}
```

---

## 3. VPC Security

### Question
Lambda needs RDS access (private), AWS service access (DynamoDB/S3), but NO internet access?

**Answer: C** - Private subnet + VPC endpoints (no NAT Gateway)

### Architecture

```
✅ Secure Configuration:
├── Lambda in private subnet
├── RDS in private subnet (private access)
├── VPC Gateway Endpoints: S3, DynamoDB (FREE)
├── VPC Interface Endpoints: Secrets Manager, CloudWatch (paid)
└── NO NAT Gateway = NO internet access

Security Benefits:
├── Zero internet exposure
├── All traffic on AWS network
├── Lower latency (no NAT hop)
├── Lower cost (gateway endpoints free)
└── Compliance-ready (PCI-DSS, HIPAA)
```

### Security Group Rules

```json
{
  "LambdaSG": {
    "Egress": [
      {"Protocol": "tcp", "Port": 5432, "Destination": "sg-rds"},
      {"Protocol": "tcp", "Port": 443, "Destination": "sg-vpc-endpoints"}
    ]
  },
  "RDSSG": {
    "Ingress": [
      {"Protocol": "tcp", "Port": 5432, "Source": "sg-lambda"}
    ]
  }
}
```

---

## 4. Function URL Security

### Question
What security features are available with Lambda Function URLs?

**Answer: B** - IAM auth OR public, CORS support, NO custom authorizers, NO throttling, NO WAF

### Key Limitations

```
Function URL Features:
✅ IAM authentication (SigV4)
✅ Public access (no auth)
✅ CORS configuration
✅ HTTPS only

Missing Features:
❌ Custom authorizers
❌ Request throttling
❌ WAF integration
❌ API keys
❌ Usage plans
❌ Request validation
❌ Response caching
❌ Multiple stages

Use Cases:
✅ Simple internal APIs
✅ IAM-authenticated endpoints
✅ Rapid prototyping
❌ Public production APIs (use API Gateway instead)
```

---

## 5. Layer Security

### Question
Security risks with Lambda Layers sharing libraries across 50+ functions?

**Answer: B** - Malicious code risk, use version ARNs, verify checksums, restrict permissions

### Mitigation Strategies

```
1. Version Pinning:
   ✅ Use: arn:aws:lambda:*:*:layer:name:5
   ❌ Avoid: arn:aws:lambda:*:*:layer:name (uses latest)

2. Checksum Verification:
   ├── Document SHA256 for each version
   ├── Verify before deployment
   └── Alert on unexpected changes

3. Access Control:
   ├── Restrict to specific accounts
   ├── Use aws:PrincipalOrgID for org access
   └── Never make public (*)

4. Content Scanning:
   ├── Vulnerability scanning (Snyk, Inspector)
   ├── Secret detection (git-secrets)
   ├── License compliance
   └── Dependency auditing

5. IAM Restrictions:
   ├── Only CI/CD can publish layers
   ├── Require MFA for permission changes
   └── Deny layer deletion
```

---

## 6. DLQ Security

### Question
Security controls for Lambda DLQ containing PII?

**Answer: B** - KMS encryption, restrictive policies, <14 day retention, no console access, CloudWatch alarms

### Best Practices

```
Encryption:
├── KMS customer-managed key
├── Deny console decrypt
└── Condition: kms:ViaService = sqs.amazonaws.com

Access Control:
├── Only automated processor can read
├── Deny console access (aws:via = console.amazonaws.com)
└── Least privilege IAM roles

Data Management:
├── Retention: 7 days (not default 14)
├── Automated PII redaction before logging
├── No PII in alerts
└── Secure deletion after processing

Monitoring:
├── CloudWatch alarms on queue depth
├── CloudTrail for all API calls
└── Alert on unauthorized access attempts
```

**SQS Policy Example:**
```json
{
  "Statement": [
    {
      "Sid": "DenyConsoleAccess",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "sqs:ReceiveMessage",
      "Condition": {"StringEquals": {"aws:via": "console.amazonaws.com"}}
    }
  ]
}
```

---

## 7. Concurrency Protection

### Question
How to prevent Lambda DDoS (exhaust concurrency, cost overrun, block legitimate requests)?

**Answer: B** - Reserved concurrency (cap executions), provisioned concurrency (critical functions), account limits

### Configuration

```
Reserved Concurrency:
├── Caps maximum concurrent executions
├── Example: 100 (prevents >100 concurrent)
├── Excess requests return 429 (throttled)
└── Cost protection: Max 100 executions at a time

Provisioned Concurrency:
├── Pre-warmed execution environments
├── Zero cold start
├── Auto-scaling (5 → 50)
└── Performance guarantee during attack

Account-Level Limits:
├── Default: 1,000 per region
├── Allocate to critical functions
└── Leave buffer for emergencies
```

**Cost Protection:**
```
Attack: 10,000 req/s for 1 hour

Without Reserved Concurrency:
├── Cost: ~$900 (36M executions)

With Reserved Concurrency (100):
├── Cost: ~$9 (360K executions)
├── 9,900 req/s throttled (no charge)
└── 99% cost savings
```

---

## 8. Code Signing

### Question
How to ensure only approved Lambda code deploys to production?

**Answer: B** - Code Signing with Signing Profile + verification policy (enforce mode)

### Process

```
1. CI/CD signs deployment package
   ├── AWS Signer service
   ├── SHA-384 + ECDSA signature
   └── Cryptographically verifies authenticity

2. Lambda verifies signature at deployment
   ├── Check signature valid
   ├── Verify signer in allowed list
   ├── Check not expired/revoked
   └── Reject if invalid

3. Enforcement:
   ├── "Enforce" mode: Deployment FAILS if unsigned
   ├── "Warn" mode: Deployment succeeds with warning
   └── Always use "Enforce" in production
```

**Code Signing Configuration:**
```json
{
  "CodeSigningConfig": {
    "AllowedPublishers": {
      "SigningProfileVersionArns": ["arn:aws:signer:*:*:/signing-profiles/prod-signer/v1"]
    },
    "CodeSigningPolicies": {
      "UntrustedArtifactOnDeployment": "Enforce"
    }
  }
}
```

---

## 9. Resource-Based Policies

### Question
How to restrict Lambda invocation to ONLY specific API Gateway + EventBridge rule?

**Answer: B** - Resource-based policy with SourceArn conditions + deny console access

### Complete Policy

```json
{
  "Statement": [
    {
      "Sid": "AllowSpecificAPIGateway",
      "Effect": "Allow",
      "Principal": {"Service": "apigateway.amazonaws.com"},
      "Action": "lambda:InvokeFunction",
      "Condition": {
        "ArnLike": {"AWS:SourceArn": "arn:aws:execute-api:*:*:api-abc/*/POST/payment"}
      }
    },
    {
      "Sid": "AllowSpecificEventBridgeRule",
      "Effect": "Allow",
      "Principal": {"Service": "events.amazonaws.com"},
      "Action": "lambda:InvokeFunction",
      "Condition": {
        "ArnLike": {"AWS:SourceArn": "arn:aws:events:*:*:rule/payment-events"}
      }
    },
    {
      "Sid": "DenyConsoleInvoke",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "lambda:InvokeFunction",
      "Condition": {"StringEquals": {"aws:via": "console.amazonaws.com"}}
    },
    {
      "Sid": "DenyNonServiceInvocations",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "lambda:InvokeFunction",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalServiceName": ["apigateway.amazonaws.com", "events.amazonaws.com"]
        }
      }
    }
  ]
}
```

### What This Blocks

```
✅ Allowed:
├── Specific API Gateway (api-abc)
├── Specific EventBridge rule (payment-events)
└── Automated invocations only

❌ Blocked:
├── Console test invocations
├── Manual CLI/SDK invocations
├── Different API Gateways
├── Cross-account invocations
├── Other AWS services (S3, SNS, etc.)
└── IAM users/roles
```

---

## 10. Runtime Management

### Question
Security risk with deprecated Lambda runtimes (Python 3.8, Node.js 14) across 200+ functions?

**Answer: B** - No security patches = vulnerabilities remain unpatched. Need: inventory, alerts, phased migration, runtime policy

### Risk & Mitigation

```
Deprecated Runtime Risks:
├── ❌ No security patches from AWS
├── ❌ Known CVEs remain unpatched
├── ❌ Compliance violations (PCI-DSS fails)
├── ❌ Data breach potential
└── ❌ Regulatory fines

Example CVEs:
├── Python 3.8: CVE-2023-40217 (TLS MitM)
├── Node.js 14: CVE-2023-30581 (command injection)
└── Java 11: CVE-2023-21930 (sandbox bypass)

Mitigation Strategy:
1. Automated Runtime Inventory
   ├── Daily scan across all regions
   ├── Track runtime status (active/deprecated/blocked)
   └── Store in DynamoDB

2. Deprecation Monitoring
   ├── Subscribe to AWS announcements
   ├── EventBridge rules for alerts
   └── Dashboard with compliance metrics

3. Phased Migration Plan
   ├── Phase 1: Critical functions (payment, auth)
   ├── Phase 2: High-volume functions
   ├── Phase 3: Remaining functions
   └── Target: <90 days to migrate

4. Runtime Version Policy
   ├── Approved runtimes only
   ├── CI/CD blocks deprecated runtimes
   ├── Exception process (documented)
   └── Quarterly policy reviews
```

**Runtime Policy Example:**
```json
{
  "ApprovedRuntimes": {
    "Python": ["python3.11", "python3.12"],
    "Node.js": ["nodejs18.x", "nodejs20.x"],
    "Java": ["java17", "java21"]
  },
  "DeprecatedRuntimes": {
    "Python": ["python3.8", "python3.9"],
    "Node.js": ["nodejs14.x", "nodejs16.x"]
  },
  "MigrationDeadline": "90 days from deprecation notice"
}
```

---

## Summary: Lambda Security Best Practices

### Critical Security Controls

```
1. Permission Model:
   ✅ Execution role: What Lambda can do
   ✅ Resource policy: Who can invoke Lambda
   ✅ Use least privilege for both

2. Secrets Management:
   ✅ Use Secrets Manager (not environment variables)
   ✅ Enable automatic rotation
   ✅ Retrieve at runtime, never log

3. Network Security:
   ✅ VPC private subnets for database access
   ✅ VPC endpoints for AWS services (no NAT)
   ✅ Security groups: specific port/SG rules only

4. Code Integrity:
   ✅ Code signing (enforce mode)
   ✅ Layer version pinning
   ✅ Checksum verification

5. Access Control:
   ✅ Resource-based policies with SourceArn
   ✅ Deny console invocations
   ✅ Explicit deny statements

6. Resource Protection:
   ✅ Reserved concurrency (cost cap)
   ✅ Provisioned concurrency (critical functions)
   ✅ CloudWatch alarms on throttles

7. Data Protection:
   ✅ DLQ with KMS encryption
   ✅ Short retention periods
   ✅ Automated PII redaction

8. Compliance:
   ✅ Runtime version policy
   ✅ Proactive migration planning
   ✅ Continuous vulnerability management
```

### Interview Talking Points

**For cloud security architect roles, emphasize:**

1. **Defense in Depth** - Multiple layers of security (IAM, encryption, network isolation)
2. **Least Privilege** - Granular permissions at every level
3. **Automation** - Automated security scanning, patching, compliance
4. **Monitoring** - CloudWatch, CloudTrail, EventBridge for detection
5. **Incident Response** - DLQ processing, automated remediation
6. **Cost Security** - Concurrency limits prevent bill shock from attacks
7. **Compliance** - PCI-DSS, HIPAA, SOC 2, GDPR considerations
8. **Supply Chain Security** - Layer management, code signing
9. **Data Classification** - Different controls for PII vs non-sensitive data
10. **Continuous Improvement** - Regular audits, policy updates, runtime management

---

## Key Differences: Lambda Security Controls

| Control | Purpose | Impact | Cost |
|---------|---------|--------|------|
| Execution Role | Lambda access to AWS services | Function capabilities | Free |
| Resource Policy | Control who invokes Lambda | Invocation authorization | Free |
| Code Signing | Verify code authenticity | Deployment restrictions | $0.50/signing job |
| Reserved Concurrency | Cap concurrent executions | DDoS mitigation + cost control | Free (compute costs same) |
| Provisioned Concurrency | Pre-warm environments | Performance + availability | ~$52/month per 20 instances |
| Secrets Manager | Secure credential storage | Automatic rotation + audit | $0.40/secret/month |
| VPC Endpoints | Private AWS service access | Network isolation | Gateway: Free, Interface: $0.01/hr/AZ |
| KMS CMK | Customer-controlled encryption | Full key management | $1/key/month |

---

## Areas for Improvement

Based on your performance (7/10), review these topics:

1. **Secrets Manager vs Environment Variables** (Question 2)
   - Focus: Why Secrets Manager is mandatory for production
   - Key: Automatic rotation, audit trail, not visible in console

2. **Function URL Limitations** (Question 4)
   - Focus: What Function URLs DON'T have (custom authorizers, throttling, WAF)
   - Key: Use API Gateway for production public APIs

3. **Permission Model** (Question 1)
   - Focus: Execution role vs resource-based policy distinction
   - Key: Direction of access determines which policy type

---

**Total Questions: 10**
**Your Score: 70%**
**Focus Areas: Secrets management, Function URL capabilities, permission model clarity**

You demonstrated strong understanding of VPC security, layer management, DLQ controls, concurrency, code signing, resource policies, and runtime management. Great work!

---

*Generated: November 30, 2024*
*Interview Preparation Guide for AWS Lambda Security Architecture*
