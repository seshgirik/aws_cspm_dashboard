# Scenario-Based Interview Questions for Security Architect Role

## Section 1: Application Security

### Scenario 1: Broken Authentication in a Web App
**Question:**  
You are reviewing a custom web application that uses session tokens for user authentication. During a penetration test, it was found that the tokens do not expire after logout.  
**How would you address this issue and prevent similar flaws in the future?**

**Answer:**  
- Enforce session expiration after logout using server-side invalidation.
- Use secure, random, time-bound session tokens (e.g., JWT with expiration).
- Implement controls to detect and prevent session reuse.
- Include logout endpoints in automated testing.
- Reference: OWASP Top 10 - Broken Authentication.

... (truncated for brevity) ...