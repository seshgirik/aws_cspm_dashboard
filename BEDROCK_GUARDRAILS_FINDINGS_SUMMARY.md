# AWS Bedrock Guardrails Security Findings
## Comprehensive Architecture Implementation Guide

**Created:** December 2, 2025  
**Total Findings:** 10  
**Focus:** Production-ready Bedrock Guardrails with Lambda, S3, SQS, QuickSight integration

---

## Overview

This document details 10 comprehensive security findings for AWS Bedrock Guardrails implementation, emphasizing:
- **ApplyGuardrail API** integration patterns
- **Lambda function** architecture for content validation
- **S3 audit logging** for compliance
- **SQS event processing** for async workflows
- **QuickSight dashboards** for visualization
- **CloudWatch monitoring** for continuous refinement
- **Iterative tuning** examples (healthcare topic blocking in finance chatbot)
- **PII detection** including SSN patterns

---

## Security Findings Index

### 1. ApplyGuardrail API Not Implemented (CRITICAL)
**Finding ID:** bedrock-guardrails-001  
**Architecture Gap:** Lambda -> InvokeModel (direct) without content validation

**Required Architecture:**
```
Lambda Function
  ↓
ApplyGuardrail API (INPUT validation)
  ↓
InvokeModel (if passed)
  ↓
ApplyGuardrail API (OUTPUT validation)
  ↓
S3 Audit Logging
  ↓
SQS Queue (async processing)
  ↓
QuickSight Metrics
```

**Demo Scenario:** Finance chatbot allowing healthcare queries (should be blocked)

**Key Implementation:**
- `bedrock.apply_guardrail(source='INPUT', content=user_prompt, guardrailIdentifier='finance-chatbot-guardrail')`
- Check `action='GUARDRAIL_INTERVENED'` vs `action='NONE'`
- Log interventions to S3: `s3://guardrails-audit/interventions/{date}/`

---

### 2. PII Redaction Missing - SSN Detection (CRITICAL)
**Finding ID:** bedrock-guardrails-002  
**Risk:** Social Security Numbers and sensitive data unprotected

**Demo Scenario:**
- User enters: "My SSN is 123-45-6789"
- Model processes unfiltered
- Response includes unredacted SSN
- No CloudWatch alert

**PII Types to Protect:**
- `US_SOCIAL_SECURITY_NUMBER` (SSN patterns: XXX-XX-XXXX)
- `CREDIT_DEBIT_CARD_NUMBER`
- `US_DRIVER_LICENSE`
- `EMAIL_ADDRESS`
- `PHONE_NUMBER`

**Iterative Tuning Process:**
1. Configure PII filters with ANONYMIZE action
2. Test with sample SSNs
3. Monitor CloudWatch metrics for detection rate
4. Refine regex patterns based on false positives
5. Production deployment

**S3 Audit Structure:**
```
s3://guardrails-audit/pii-detections/{yyyy}/{mm}/{dd}/
  - timestamp
  - user_id
  - pii_types_detected: ["SSN", "CREDIT_CARD"]
  - action_taken: "ANONYMIZED"
  - original_text_hash
```

**QuickSight Dashboards:**
- PII Detection Trends
- Most Common PII Types
- SSN Exposure Incidents
- Compliance Metrics (% filtered)

---

### 3. Prompt Injection Vulnerable (CRITICAL)
**Finding ID:** bedrock-guardrails-003  
**Test Results:**
- 85% jailbreak success rate (17/20 attempts)
- 92% prompt injection bypass (23/25 attempts)
- System prompts leaked in 12 cases

**LLMJacking Incident:**
- Exposed API keys found in GitHub
- $46,000 consumed in 48 hours
- No guardrails blocked unauthorized usage

---

### 4. Denied Topics - Healthcare in Finance Chatbot (HIGH)
**Finding ID:** bedrock-guardrails-004  
**Iterative Tuning Demo:**

**ITERATION 1 (Current - Bad):**
- User: "What are symptoms of high blood pressure?"
- Finance bot provides medical advice (inappropriate)

**ITERATION 2 (After Configuration):**
```
Denied Topic: "Healthcare and Medical Advice"
Definition: "Do not provide medical diagnoses, treatment 
recommendations, or health-related guidance"
```
- CloudWatch metric: `BedrockGuardrails_TopicPolicyViolation`

**ITERATION 3 (Refinement):**
- User: "Does my health insurance cover financial planning?"
- Initially BLOCKED (false positive - "health" keyword)
- **Refine:** Allow health insurance financial questions
- Re-test and adjust sensitivity

**Architecture Components:**
- Lambda ApplyGuardrail topic validation
- S3 topic violation logs
- SQS intervention events
- QuickSight topic blocking trends

**Denied Topics Configuration:**
1. Healthcare/Medical (HIGH sensitivity)
2. Legal Advice (HIGH)
3. Political Content (MEDIUM)
4. Competitor Products (LOW)

---

### 5. Contextual Grounding Disabled (HIGH)
**Finding ID:** bedrock-guardrails-005  
**Problem:** Hallucination rate 34% in RAG applications

**Incident:** Model fabricated warranty terms not in documentation

---

### 6. Word Filters Not Set (MEDIUM)
**Finding ID:** bedrock-guardrails-006  
**Gaps:** No competitor names, confidential project code names, profanity blocking

---

### 7. CloudWatch Monitoring Missing (HIGH)
**Finding ID:** bedrock-guardrails-007  
**Complete Monitoring Architecture:**

**Lambda CloudWatch Integration:**
```python
cloudwatch.put_metric_data(
    Namespace='BedrockGuardrails',
    MetricName='GuardrailIntervention',
    Value=1 if intervened else 0,
    Dimensions=[
        {'Name':'GuardrailId', 'Value':'finance-chatbot'},
        {'Name':'PolicyType', 'Value':'TopicPolicy'}
    ]
)
```

**Metrics to Track:**
- `BedrockGuardrails_TotalInvocations`
- `BedrockGuardrails_InterventionRate (%)`
- `BedrockGuardrails_PolicyTypeDistribution`
- `BedrockGuardrails_LatencyP50/P95/P99`
- `BedrockGuardrails_CostPerIntervention`
- `Custom_FalsePositiveRate`
- `Custom_TuningIterations`

**S3 Audit Trail:**
```
s3://guardrails-monitoring/interventions/{yyyy}/{mm}/{dd}/{timestamp}-{request_id}.json
```
Contains:
- user_query
- model_response
- guardrail_assessment_full
- action_taken
- timestamp

**SQS Event Stream:**
```json
{
  "event_type": "guardrail_intervention",
  "guardrail_id": "finance-chatbot",
  "policy": "healthcare_topic_blocked",
  "query_hash": "abc123",
  "timestamp": "2025-12-02T05:45:00Z"
}
```

**QuickSight Visualizations:**
1. Guardrail Intervention Rate (line chart over time)
2. Top Blocked Topics (bar chart)
3. PII Detection Heatmap (by type and hour)
4. Content Filter Triggers (pie chart by category)
5. Latency Impact Analysis (guardrail overhead)
6. Iterative Tuning Effectiveness (before/after comparisons)

**CloudWatch Alarms:**
- High intervention rate: >100 blocks/hour (potential attack)
- Zero interventions: guardrail may be disabled
- Latency spike: >500ms processing
- PII detection surge: compliance review needed

**Continuous Refinement Loop:**
1. Weekly review QuickSight metrics
2. Identify false positives in S3 logs
3. Adjust guardrail configurations
4. Deploy new version
5. Measure improvement in CloudWatch
6. Document changes in version control

---

### 8. Streaming Responses Unprotected (HIGH)
**Finding ID:** bedrock-guardrails-008  
**Issue:** `InvokeModelWithResponseStream` bypassing guardrails  
**Volume:** 15,000+ streaming invocations/day unfiltered

---

### 9. Multiple Models Inconsistent (CRITICAL)
**Finding ID:** bedrock-guardrails-009  
**Inventory:**
- 5 Claude models (2 with guardrails)
- 3 Titan models (0 with guardrails)
- 2 Llama models (0 with guardrails)
- 3 Cohere models (1 with guardrails)

**Solution:** Organization-wide baseline with SCPs

---

### 10. Cost Monitoring Missing - LLMJacking Risk (CRITICAL)
**Finding ID:** bedrock-guardrails-010  
**Historical Incident:** $46K consumption in 48 hours from compromised API keys

**Protection Required:**
- AWS Budgets alerts (daily/weekly)
- CloudWatch anomaly detection
- Rate limiting per API key
- Secret scanning in repos
- API key rotation (30 days)
- Emergency circuit breakers

---

## Implementation Checklist

### Phase 1: Core Guardrails (Week 1)
- [ ] Create guardrail configurations for each use case
- [ ] Integrate ApplyGuardrail API in Lambda functions
- [ ] Configure content filters (hate speech, violence, sexual content, insults)
- [ ] Set up PII redaction (SSN, credit cards, emails, phone numbers)
- [ ] Test with sample harmful content and PII

### Phase 2: S3 & SQS Infrastructure (Week 2)
- [ ] Create S3 buckets for audit logs
- [ ] Set up SQS queues for intervention events
- [ ] Deploy Lambda consumers for event processing
- [ ] Implement log aggregation and archival

### Phase 3: Monitoring (Week 3)
- [ ] Configure CloudWatch custom metrics
- [ ] Set up alarms for critical thresholds
- [ ] Create SNS topics for alerting
- [ ] Enable CloudTrail logging for audit

### Phase 4: Visualization (Week 4)
- [ ] Set up Athena for S3 log queries
- [ ] Create QuickSight dashboards
- [ ] Configure scheduled reports
- [ ] Train team on dashboard usage

### Phase 5: Iterative Tuning (Ongoing)
- [ ] Week 1: Deploy healthcare topic blocking for finance chatbot
- [ ] Week 2: Collect metrics and identify false positives
- [ ] Week 3: Refine topic definitions based on data
- [ ] Week 4: Add additional denied topics (legal, political)
- [ ] Weekly: Review QuickSight metrics
- [ ] Monthly: Comprehensive policy review

---

## Cost Optimization

**Guardrails Pricing:**
- Charged per content unit processed
- Input text units
- Output text units
- Number of evaluations

**Optimization Strategies:**
1. Cache common validations
2. Optimize filter configurations
3. Use appropriate filter strengths
4. Implement client-side pre-filtering where safe

---

## Compliance Mapping

| Finding | OWASP LLM | GDPR | HIPAA | PCI-DSS | SOC 2 |
|---------|-----------|------|-------|---------|-------|
| ApplyGuardrail API | LLM02 | - | - | - | - |
| PII Redaction | LLM06 | Art 32 | 164.312 | 3.4 | - |
| Prompt Injection | LLM01 | - | - | - | - |
| Denied Topics | - | - | - | - | - |
| CloudWatch Monitoring | - | - | - | - | CC7.2 |
| Cost Monitoring | - | - | - | - | - |

---

## Next Steps

1. **Review Findings:** Security team assessment
2. **Prioritize Implementation:** CRITICAL findings first
3. **Allocate Resources:** Lambda development, SQS/S3 setup, QuickSight config
4. **Pilot Testing:** Start with finance chatbot healthcare blocking demo
5. **Production Rollout:** Phase-based deployment
6. **Continuous Monitoring:** Weekly QuickSight reviews
7. **Documentation:** Maintain guardrail policy documentation

---

## References

- [AWS Bedrock Guardrails Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [ApplyGuardrail API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ApplyGuardrail.html)
- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Iterative Tuning Best Practices](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-best-practices.html)

---

**Status:** Ready for implementation  
**Contact:** Security Architecture Team  
**Last Updated:** December 2, 2025
