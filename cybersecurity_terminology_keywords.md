# Cybersecurity Terminology & Keywords
## Found in Repository: aws-security-sample-data

**Generated on:** December 1, 2024  
**Repository Path:** /Users/sekondav/CascadeProjects

---

## Table of Contents
1. [Security Architecture & Design](#security-architecture--design)
2. [Access Control & Identity](#access-control--identity)
3. [Network Security](#network-security)
4. [Data Protection & Encryption](#data-protection--encryption)
5. [Threat & Risk Management](#threat--risk-management)
6. [Compliance & Governance](#compliance--governance)
7. [Monitoring & Detection](#monitoring--detection)
8. [Incident Response & Recovery](#incident-response--recovery)
9. [Cloud Security Specific](#cloud-security-specific)
10. [Attack Types & Vectors](#attack-types--vectors)
11. [AWS Security Services](#aws-security-services)
12. [LLM & AI/ML Security](#llm--aiml-security)

---

## Security Architecture & Design

### Core Concepts
- **Zero-Trust** / **Zero Trust** - Security model that assumes no implicit trust
- **Defense-in-Depth** - Multi-layered security approach
- **Perimeter Security** - Traditional boundary-based security
- **Blast Radius** - Scope of potential damage from a security incident
- **Attack Surface** - Total exposure points vulnerable to attacks
- **Security Posture** - Overall security status and readiness
- **Tier** / **Multi-tier** / **Three-tier** / **N-tier** - Application architecture layers
- **Isolation** - Separation of systems and components
- **Segmentation** / **Network Segmentation** - Dividing networks into smaller segments
- **Immutable** - Unchangeable infrastructure
- **Ephemeral** - Temporary, short-lived resources
- **Stateless** - Not retaining session information

### Security Principles
- **Least Privilege** - Minimum necessary access rights
- **Security Baseline** - Minimum security requirements
- **Hardening** - Strengthening security configurations

---

## Access Control & Identity

### Authentication & Authorization
- **Multi-Factor Authentication (MFA)** - Multiple verification methods
- **Single Sign-On (SSO)** - One credential for multiple systems
- **SAML** - Security Assertion Markup Language
- **OAuth** - Open Authorization protocol
- **Identity Federation** - Linking user identities across systems

### Access Control Models
- **RBAC (Role-Based Access Control)** - Permissions based on roles
- **ABAC (Attribute-Based Access Control)** - Permissions based on attributes
- **Least Privilege** - Principle of minimal access

### Identity Management
- **Secrets Management** / **Secrets Manager** - Secure credential storage
- **Key Management** - Cryptographic key lifecycle management
- **Credential Theft** - Unauthorized credential acquisition
- **Privilege Escalation** - Gaining elevated access rights

---

## Network Security

### Network Controls
- **Firewall** - Network traffic filtering
- **WAF (Web Application Firewall)** - Application layer protection
- **Security Groups** - Virtual firewall rules
- **NACLs (Network ACLs)** - Network access control lists
- **Network Segmentation** - Dividing network into zones
- **Bastion Host** / **Jump Host** - Secure access gateway

### Network Concepts
- **VPC (Virtual Private Cloud)** - Isolated cloud network
- **Isolation** - Network separation
- **Perimeter Security** - Boundary defense

---

## Data Protection & Encryption

### Encryption Methods
- **Encryption at Rest** - Data stored securely
- **Encryption in Transit** - Data transmitted securely
- **PKI (Public Key Infrastructure)** - Certificate management framework
- **Certificate** - Digital identity verification
- **Key Management** - Cryptographic key handling

### Data Security
- **Data Loss Prevention (DLP)** - Preventing unauthorized data transfer
- **Data Exfiltration** - Unauthorized data extraction
- **Data Breach** - Unauthorized data access
- **Data Leakage** - Unintentional data exposure

---

## Threat & Risk Management

### Threat Assessment
- **Threat Model** / **Threat Modeling** - Identifying and analyzing threats
- **Threat Actor** - Entity conducting attacks
- **Attack Vector** - Path or method of attack
- **Adversary** - Hostile entity
- **Vulnerability** / **Vulnerabilities** - Security weaknesses
- **Risk Assessment** - Evaluating security risks
- **Risk Mitigation** - Reducing security risks

### Security Testing
- **Penetration Testing** / **Pen Test** / **Pentest** - Simulated attacks

---

## Compliance & Governance

### Compliance Frameworks
- **SOC2 (Service Organization Control 2)** - Trust service criteria
- **HIPAA** - Health Insurance Portability and Accountability Act
- **PCI DSS** - Payment Card Industry Data Security Standard
- **GDPR** - General Data Protection Regulation
- **NIST** - National Institute of Standards and Technology
- **ISO 27001** - Information security management standard
- **CIS Benchmark** - Security configuration guidelines
- **Security Standards** - Industry security requirements

### Governance
- **Compliance** - Adherence to regulations
- **Audit Log** / **Audit Trail** - Record of system activities

---

## Monitoring & Detection

### Detection Systems
- **SIEM (Security Information and Event Management)** - Centralized security monitoring
- **IDS (Intrusion Detection System)** - Threat detection
- **IPS (Intrusion Prevention System)** - Threat prevention

### Logging & Monitoring
- **CloudTrail** - AWS API activity logging
- **Logging** - Recording system events
- **Audit Log** - Security event records

---

## Incident Response & Recovery

### Response Activities
- **Incident Response** - Handling security incidents
- **Remediation** - Fixing security issues
- **Mitigation** - Reducing impact

---

## Cloud Security Specific

### AWS Security
- **IAM (Identity and Access Management)** - AWS access control
- **KMS (Key Management Service)** - AWS encryption key management
- **CloudTrail** - AWS activity logging
- **Lambda Security** - Serverless function security
- **VPC Security** - Virtual Private Cloud security
- **Security Groups** - AWS firewall rules
- **SCPs (Service Control Policies)** - AWS Organizations policies

### Cloud Concepts
- **Multi-Region** - Distributed across regions
- **Cross-Region** - Between different regions
- **Observability** - System visibility and monitoring

---

## Attack Types & Vectors

### Attack Methods
- **DDoS (Distributed Denial of Service)** - Overwhelming system resources
- **Denial of Service** - Making systems unavailable
- **Phishing** - Social engineering via fake communications
- **Spear Phishing** - Targeted phishing attacks
- **Social Engineering** - Manipulating people for access
- **Malware** - Malicious software
- **Ransomware** - Encryption-based extortion
- **Trojan** - Disguised malicious software
- **Virus** - Self-replicating malicious code

### Attack Tactics
- **Lateral Movement** - Moving through networks after breach
- **Privilege Escalation** - Gaining higher access levels
- **Credential Theft** - Stealing authentication credentials
- **Data Exfiltration** - Stealing data from systems

---

## AWS Security Services

### Core Services
- **AWS IAM** - Identity and Access Management
- **AWS KMS** - Key Management Service
- **AWS CloudTrail** - API activity logging
- **AWS Config** - Configuration tracking
- **AWS GuardDuty** - Threat detection
- **AWS Security Hub** - Centralized security view
- **AWS Shield** - DDoS protection
- **AWS WAF** - Web Application Firewall
- **AWS Secrets Manager** - Secret storage
- **AWS Organizations** - Multi-account management
- **AWS Lambda** - Serverless compute
- **AWS VPC** - Virtual Private Cloud
- **Amazon Bedrock** - AI/ML service security

---

## LLM & AI/ML Security

### LLM Security Posture Management (LLM SPM)
- **LLM Security Posture Management** - Comprehensive approach to securing Large Language Model infrastructure
- **AI/ML Security** - Security practices for artificial intelligence and machine learning systems
- **Model Security** - Protection of AI/ML models from attacks and misuse

### LLM-Specific Threats

#### Infrastructure Attacks
- **LLMJacking** - Hijacking cloud resources allocated for LLM inference and training
- **Cryptojacking for LLMs** - Unauthorized use of compute resources for LLM operations
- **Resource Theft** - Stealing GPU/compute credits for unauthorized LLM usage
- **Cost Exploitation** - Malicious consumption of expensive LLM API calls

#### Model Attacks
- **Model Poisoning** - Injecting malicious data into training datasets
- **Model Inversion** - Extracting training data from models
- **Model Extraction** - Stealing proprietary model architecture and weights
- **Model Evasion** - Crafting inputs to bypass model detection
- **Adversarial Attacks** - Intentionally misleading AI models with crafted inputs

#### Prompt & Input Attacks
- **Prompt Injection** - Malicious instructions embedded in prompts
- **Jailbreaking** - Bypassing safety constraints and guardrails
- **Prompt Leaking** - Exposing system prompts and instructions
- **Indirect Prompt Injection** - Injecting commands through retrieved documents
- **Context Poisoning** - Contaminating RAG context with malicious content

#### Data Security
- **Training Data Exposure** - Leaking sensitive information from training data
- **PII Leakage** - Personal Identifiable Information exposure through models
- **Memorization Attacks** - Extracting memorized training data
- **Data Poisoning** - Corrupting training datasets

### LLM Security Controls

#### Access & Authentication
- **API Key Management** - Securing LLM API credentials
- **Token Management** - Controlling LLM access tokens
- **Rate Limiting** - Preventing abuse through usage limits
- **Authentication Gates** - Controlling access to LLM endpoints

#### Monitoring & Detection
- **Prompt Monitoring** - Analyzing prompts for malicious content
- **Output Filtering** - Screening LLM responses for sensitive data
- **Usage Analytics** - Tracking LLM consumption patterns
- **Anomaly Detection** - Identifying unusual LLM usage
- **Cost Monitoring** - Tracking expensive LLM operations

#### Guardrails & Controls
- **Input Validation** - Sanitizing and validating prompts
- **Output Sanitization** - Filtering harmful or sensitive outputs
- **Content Filtering** - Blocking inappropriate content
- **Safety Layers** - Additional protection mechanisms
- **Semantic Guards** - Preventing semantic attacks

#### Infrastructure Security
- **Model Isolation** - Separating models and environments
- **Secure Model Storage** - Protecting model artifacts
- **Encrypted Inference** - Protecting data during inference
- **Secure Fine-tuning** - Protected model customization
- **Compute Isolation** - Isolating GPU/compute resources

### LLM Security Best Practices

#### Configuration Management
- **CSPM for AI/ML** - Cloud Security Posture Management for AI infrastructure
- **Model Versioning** - Tracking and securing model versions
- **Parameter Security** - Protecting model hyperparameters
- **Configuration Hardening** - Securing LLM deployment settings

#### Secrets & Credentials
- **API Key Rotation** - Regular credential updates
- **Secrets Vaulting** - Secure storage of LLM credentials
- **Credential Scanning** - Detecting exposed API keys
- **PW (Password) Protection** - Securing authentication credentials

#### Monitoring & Compliance
- **SIEM Integration** - Security monitoring for LLM operations
- **Audit Logging** - Recording LLM access and usage
- **Compliance Tracking** - Ensuring regulatory adherence
- **Usage Reporting** - Tracking LLM consumption and costs

#### Vulnerability Management
- **Model Vulnerability Scanning** - Identifying model weaknesses
- **Dependency Scanning** - Checking library vulnerabilities
- **Security Patching** - Updating vulnerable components
- **Threat Intelligence** - Staying informed on LLM threats

### LLM Attack Vectors

#### Economic Attacks
- **Cost Amplification** - Exploiting expensive operations
- **Resource Exhaustion** - Depleting compute budgets
- **Token Flooding** - Overwhelming systems with requests
- **Financial DoS** - Denial of service through cost

#### Privacy Attacks
- **Training Data Recovery** - Extracting private training data
- **Membership Inference** - Determining if data was in training set
- **Attribute Inference** - Deducing sensitive attributes
- **PII Extraction** - Recovering personal information

#### Operational Attacks
- **Service Disruption** - Making LLM services unavailable
- **Performance Degradation** - Slowing down model responses
- **Context Window Overflow** - Exceeding token limits
- **Cascading Failures** - Triggering downstream failures

### LLM Security Frameworks

#### Security Standards
- **OWASP Top 10 for LLMs** - Common LLM vulnerabilities
- **AI Security Guidelines** - Industry best practices
- **Model Cards** - Documenting model capabilities and limitations
- **AI Risk Management** - Framework for AI security risks

#### Testing & Validation
- **Red Teaming for LLMs** - Adversarial testing of models
- **Prompt Security Testing** - Validating input handling
- **Output Validation** - Testing response safety
- **Safety Benchmarking** - Measuring model safety metrics

### Cloud Provider LLM Security

#### AWS-Specific
- **Amazon Bedrock Security** - AWS managed LLM security
- **Amazon Bedrock Guardrails** - Unified safeguards framework for generative AI applications
- **Bedrock Content Filters** - Filter harmful content (hate speech, violence, sexual content, insults)
- **Bedrock Denied Topics** - Block undesirable topics based on policies
- **Bedrock Word Filters** - Block specific words or phrases
- **Bedrock PII Redaction** - Detect and redact personally identifiable information
- **Contextual Grounding Check** - Validate responses are grounded in source information
- **Prompt Attack Detection** - Detect and block prompt injection and jailbreaking attempts
- **SageMaker Security** - ML model training security
- **GuardDuty for ML** - Threat detection for ML workloads
- **AWS PrivateLink for AI** - Private connectivity for AI services

#### Multi-Cloud
- **Azure OpenAI Security** - Microsoft's LLM security
- **Google Vertex AI Security** - Google's AI platform security
- **Cross-Cloud Model Security** - Securing models across providers

---

## Additional Security Terminology

### Security Concepts
- **CIA Triad** - Confidentiality, Integrity, Availability
- **Supply Chain Security** - Third-party security risks
- **Third-Party Risk** - Vendor security concerns
- **Vendor Risk** - External service provider risks
- **Security Baseline** - Minimum security standards
- **Security Standards** - Industry best practices

---

## Summary Statistics

**Total Categories:** 12  
**Total Keywords/Terms:** 250+  
**Primary Sources:**
- Lambda Security Architect documents (highest concentration)
- Security findings JSON files
- AWS service-specific documentation
- Risk & Governance questions
- NIST/ISO compliance documents
- Threat modeling documents
- LLM & AI/ML Security research (newly added)

---

## Notes

This terminology list represents the cybersecurity vocabulary actively used within this repository's AWS security documentation, interview preparation materials, and security findings. The terms span from foundational security concepts to AWS-specific implementations and modern cloud security practices.

The repository demonstrates strong coverage of:
- Cloud security architecture
- AWS security services
- Compliance frameworks
- Threat modeling
- Identity and access management
- Serverless security (Lambda)
- Risk management
- Zero-trust principles
- **LLM & AI/ML Security (newly expanded)**

---

**Repository Focus:** AWS Cloud Security, Serverless Security, Compliance, Risk Management, LLM Security  
**Technical Depth:** Enterprise-level security architecture and implementation  
**Latest Addition:** Comprehensive LLM Security Posture Management terminology covering LLMJacking, prompt injection, model poisoning, and AI/ML security controls
