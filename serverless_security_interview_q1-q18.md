# AWS Serverless Security Interview (Interactive Set Export)

This file contains the serverless-focused (primarily Lambda/API Gateway/S3/SQS/EventBridge/Step Functions) multiple-choice interview questions that were asked in-chat (Q1–Q18), along with the correct answers and concise explanations.

---

## Q1: Lambda Permissions (Least Privilege)
**Question:** You have a Lambda function triggered by SQS, which writes to DynamoDB and logs to CloudWatch. Which approach is most secure?

- A) Use one shared “admin” IAM role for all Lambdas to simplify operations
- B) Give the Lambda execution role `dynamodb:*` on `*` and `sqs:*` on `*` to avoid permission issues
- C) Create a dedicated execution role for this Lambda with only required actions on the specific queue/table, and restrict invoke/source where possible
- D) Put permissions on the developer’s IAM user and rely on environment variables inside Lambda

**Correct answer:** C

**Why:** Dedicated per-function roles and scoped permissions reduce blast radius and enforce least privilege.

---

## Q2: Resource Policy vs IAM Role (S3 → Lambda Invoke)
**Question:** S3 triggers a Lambda. You want only that bucket to invoke the function. Best control?

- A) Add permissions to the Lambda execution role to allow `lambda:InvokeFunction`
- B) Add a Lambda resource-based policy allowing invoke only from the S3 bucket ARN (and optionally SourceAccount)
- C) Put the Lambda in a private subnet (VPC) so S3 can’t invoke it from the internet
- D) Enable CloudTrail; that will prevent unauthorized invocation

**Correct answer:** B

**Why:** Invocation is controlled by Lambda resource-based permissions (`AddPermission`) with `SourceArn`/`SourceAccount` constraints.

---

## Q3: API Gateway Authorization (Service-to-Service)
**Question:** Strongest AWS-native auth option for internal service-to-service calls?

- A) No auth + rely on obscurity of the URL
- B) API Key only
- C) IAM authorization using SigV4 (least-privilege IAM principals), optionally combined with resource policy
- D) Store a shared secret in Lambda env vars and compare to a header

**Correct answer:** C

**Why:** SigV4 + least privilege provides strong AWS-native authZ/authN; resource policies add further guardrails.

---

## Q4: Secrets in Serverless (Lambda)
**Question:** Best practice for third-party API token used by Lambda?

- A) Hardcode in code package
- B) Store in env var in plaintext
- C) Store in Secrets Manager (or SSM SecureString) with KMS, restrict IAM, fetch at runtime (cache)
- D) Put it in CloudWatch Logs once during deployment

**Correct answer:** C

**Why:** Dedicated secret stores + KMS + least privilege + rotation support.

---

## Q5: Lambda + VPC Security (Prevent Internet Egress)
**Question:** Lambda in VPC needs RDS, but must not reach public internet; still needs AWS services.

- A) Add NAT Gateway so it can reach everything
- B) Private subnets without NAT + VPC endpoints for required services
- C) Public subnets with public IPs disabled
- D) Security Groups only can block DNS-based internet

**Correct answer:** B

**Why:** No NAT removes default internet egress; VPC endpoints keep AWS service access private.

---

## Q6: Serverless Logging & Forensics
**Question:** Best combination for incident response visibility?

- A) Only CloudWatch Logs
- B) CloudTrail (mgmt + data events where relevant) + CloudWatch Logs + X-Ray + correlation IDs
- C) Only VPC Flow Logs
- D) Disable logs to reduce exposure

**Correct answer:** B

**Why:** CloudTrail provides identity/audit; logs provide app context; X-Ray traces downstream calls.

---

## Q7: SQS-triggered Lambda Poison Pill / Retry Abuse
**Question:** Best mitigation?

- A) Increase Lambda timeout
- B) Configure DLQ/redrive + max receive count + idempotency + validation
- C) Disable retries entirely
- D) Use a different region

**Correct answer:** B

**Why:** DLQ + max receives stops infinite retry loops; idempotency prevents duplicate side effects.

---

## Q8: S3 Public Access + Data Exposure
**Question:** Best control set?

- A) Make bucket public but obfuscate keys
- B) Enable Block Public Access + enforce TLS + scope access via IAM + bucket policy
- C) Rely on private-by-default with no policies
- D) Put bucket name in Secrets Manager

**Correct answer:** B

**Why:** BPA prevents accidental public exposure; policy guardrails enforce transport and least privilege.

---

## Q9: KMS & Serverless Encryption Pitfall
**Question:** Lambda writes to DynamoDB encrypted with CMK; prod fails with KMS `AccessDeniedException`. Most likely cause?

- A) DynamoDB can’t use CMKs with Lambda
- B) Missing IAM KMS permissions and/or KMS key policy doesn’t allow role/service usage
- C) CloudWatch Logs misconfigured
- D) Lambda timeout too low

**Correct answer:** B

**Why:** KMS requires both IAM allow and key policy allow; prod role/key policy mismatches are common.

---

## Q10: Serverless Supply Chain Risk
**Question:** Best prevention strategy for malicious dependency versions?

- A) Fetch latest packages at runtime
- B) Pin versions + controlled CI builds + scanning + artifact integrity/provenance
- C) Increase Lambda memory
- D) Hide the repo

**Correct answer:** B

**Why:** Reproducible builds + pinned deps + scanning reduce supply-chain exposure.

---

## Q11: Multi-Tenant Serverless Authorization
**Question:** Prevent cross-tenant data leakage when using `tenantId` from JWT to query data.

- A) Trust tenantId in request body if it usually matches
- B) Derive tenantId only from validated identity context; never from user input; check before data access
- C) Increase Lambda memory
- D) Use a single DynamoDB table without indexes

**Correct answer:** B

**Why:** Prevents IDOR/broken auth by making tenancy decisions server-side.

---

## Q12: Concurrency as a Security/Cost Control
**Question:** Best control set for spikes causing cost and downstream overload?

- A) Reserved concurrency + API Gateway throttling + backpressure (e.g., SQS buffering)
- B) Increase Lambda timeout
- C) Disable logs
- D) Bigger ZIP

**Correct answer:** A

**Why:** Caps scaling, controls rate at the edge, and buffers spikes.

---

## Q13: EventBridge Security (Event Injection)
**Question:** Prevent unauthorized principals from publishing events that trigger workflows.

- A) Allow anyone to PutEvents; validate only in Lambda
- B) Event bus resource policy restricting PutEvents + tight event patterns
- C) Put EventBridge in a VPC
- D) Increase Lambda timeout

**Correct answer:** B

**Why:** Platform-level authorization on the event bus prevents injection.

---

## Q14: SSRF / Egress Abuse from Lambda
**Question:** Lambda fetches user-provided URLs. Best approach?

- A) Allow all outbound; SSRF not relevant
- B) Validate/allowlist, block metadata/internal ranges, restrict egress (no NAT, endpoints/proxy)
- C) Base64-encode the URL
- D) Increase memory

**Correct answer:** B

**Why:** SSRF is common; combine strict input validation with egress controls.

---

## Q15: API Gateway + WAF
**Question:** Best production hardening for public serverless API?

- A) Put Lambda in VPC
- B) Attach AWS WAF with managed rules + rate limits + logging
- C) Use API key (blocks SQLi)
- D) Disable CORS

**Correct answer:** B

**Why:** WAF mitigates common web attacks and abusive traffic; complements auth.

---

## Q16: Over-Permissive Lambda Invocation
**Question:** Lambda resource policy has `"Principal": "*"` allowing `lambda:InvokeFunction`. Best assessment?

- A) Safe due to execution role
- B) High risk unless tightly constrained by SourceArn/SourceAccount conditions
- C) Not a problem if logs enabled
- D) Only affects internal AWS services

**Correct answer:** B

**Why:** Resource policy controls invocation; broad principals can enable unauthorized execution and cost/abuse.

---

## Q17: S3 Write-Then-Read Data Leak
**Question:** Lambda writes `uploads/{userId}/file.json`. Users sometimes access others’ files. Best fix?

- A) Hash userId in key
- B) Use pre-signed URLs + bucket/IAM conditions limiting prefixes per principal; avoid broad raw S3 access
- C) Make bucket private and assume fixed
- D) Log all GETs

**Correct answer:** B

**Why:** Authorization must be enforced; obfuscation and logging don’t prevent access.

---

## Q18: Step Functions Security (Workflow / “Agentic” Risk)
**Question:** Developer wants `AdministratorAccess` on Step Functions execution role.

- A) Accept it
- B) Least privilege: scope role to required actions/resources; separate roles per task where possible; restrict input/output; enable logging
- C) Put Step Functions in a VPC
- D) Disable CloudTrail

**Correct answer:** B

**Why:** Over-broad workflow roles create large blast radius; least privilege + data scoping reduces risk.
