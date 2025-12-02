
## 🛡️ Threat Model for Web Application Architecture

### 🔹 Components:
- Browser (User Login)
- Web Server
- Application Server
- Backend Database
- S3 Bucket
- Web Application Firewall (WAF)
- Virtual Private Cloud (VPC)
- IAM / Cognito
- CI/CD Pipeline
- Secrets Management
- API Gateway
- Load Balancer
- Monitoring & Logging
- CDN
- Caching Layer
- Backup & Disaster Recovery

---

### ⚙️ 1. Asset and Data Flow Overview

**Data Flow:**
User (Browser) → CDN → Load Balancer → WAF → API Gateway → Web Server → App Server → Database / S3 Bucket

**Trust Boundaries:**
- Between Browser and CDN (Public Internet)
- CDN to Load Balancer (TLS termination)
- Load Balancer to WAF to API Gateway (Edge Security)
- Inside VPC: Web/App/DB/S3
- Between App Server and CI/CD, Secrets Manager, and Monitoring Services

---

## 🔍 2. STRIDE-Based Threat Identification

### 📁 A. Browser (Client Side)
| STRIDE | Threat | Mitigation |
|--------|--------|------------|
| Spoofing | Phishing | Enforce HTTPS, HSTS, CSP |
| Tampering | JS injection (XSS) | Input validation, CSP |
| Repudiation | Action denial | Session/activity logs |
| Info Disclosure | Cache leaks | Secure headers (no-store) |
| DoS | Form spam | CAPTCHA, rate limiting |
| Elevation of Privilege | Client-side bypass | Enforce server-side validation |

### 📁 B. Web Server
| STRIDE | Threat | Mitigation |
|--------|--------|------------|
| Spoofing | Forged headers | Token validation, whitelisting |
| Tampering | URL manipulation | Canonicalization, strict routing |
| Repudiation | Log deletion | Centralized immutable logs |
| Info Disclosure | Directory access | Disable directory listing |
| DoS | Request floods | Rate limiting, WAF rules |
| Elevation of Privilege | Admin panel exposure | Route access control |

### 📁 C. Application Server
| STRIDE | Threat | Mitigation |
|--------|--------|------------|
| Spoofing | API abuse | OAuth2, signed tokens |
| Tampering | Payload modification | Input validation, HMAC |
| Repudiation | Action denial | App-layer audit logs |
| Info Disclosure | Stack trace | Generic error messages |
| DoS | Infinite loops | Throttling, input checks |
| Elevation of Privilege | Insecure endpoints | RBAC, endpoint protection |

### 📁 D. Database
| STRIDE | Threat | Mitigation |
|--------|--------|------------|
| Spoofing | Fake app server | IAM-based DB auth |
| Tampering | SQL injection | Parameterized queries |
| Repudiation | No DB audit | Query logging enabled |
| Info Disclosure | Sensitive data | Encryption at rest/transit |
| DoS | Query flooding | Throttling, pool limits |
| Elevation of Privilege | Broad access | Least privilege DB roles |

### 📁 E. S3 Bucket
| STRIDE | Threat | Mitigation |
|--------|--------|------------|
| Spoofing | URL tampering | Pre-signed URLs |
| Tampering | File overwrite | Bucket versioning |
| Repudiation | No logging | Enable access logs |
| Info Disclosure | Public access | Block public access |
| DoS | Flood uploads | S3 quota, lifecycle rules |
| Elevation of Privilege | Write to protected folders | Fine-grained IAM |

### 📁 F. WAF
| STRIDE | Threat | Mitigation |
|--------|--------|------------|
| Tampering | Misconfigured rules | RBAC, rule audits |
| DoS | Rule bypass | Test with payloads regularly |
| Info Disclosure | Verbose error messages | Generic messages only |

### 📁 G. VPC
| STRIDE | Threat | Mitigation |
|--------|--------|------------|
| Spoofing | Internal IP spoofing | Security groups, NACLs |
| Tampering | Data sniffing | TLS internally |
| Info Disclosure | Open subnets | Use private subnets |
| DoS | Routing attack | Control routes, firewalling |
| Elevation of Privilege | Cross-resource misuse | VPC policies, IAM controls |

---

## 📌 Summary Table
| Component | Key Threats |
|-----------|-------------|
| Browser | XSS, phishing, session hijacking |
| Web Server | URL tampering, DoS, spoofing |
| App Server | API abuse, insecure auth flows |
| Database | SQL injection, sensitive data exposure |
| S3 Bucket | Public data leaks, overwrite |
| WAF | Rule misconfig, false negatives |
| VPC | Internal data exfiltration, IP spoofing |

---

## 🚀 Summary of Suggested Additions for Real-Time Deployment

| Missing Component         | Purpose                                |
|---------------------------|----------------------------------------|
| IAM / Cognito / Auth0     | Authentication and RBAC                |
| Monitoring & Logging      | Observability and incident response    |
| CI/CD Pipeline            | Automated secure deployments           |
| Secrets Management        | Secure configuration handling          |
| API Gateway               | Request routing, throttling, auth      |
| Load Balancer             | High availability                      |
| CDN                       | Faster content delivery                |
| Caching Layer             | Scalability and latency improvement    |
| Security Services         | Runtime and network protection         |
| Backup/DR Strategy        | Resilience and data safety             |

---

## 📊 Visual Diagram
(See attached image for full data flow and trust boundaries.)
