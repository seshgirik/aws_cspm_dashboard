package com.security.demo.controller;

import com.security.demo.entity.User;
import com.security.demo.repository.UserRepository;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.*;

/**
 * OWASP Top 10 Web Application Security Demonstrations
 * This controller demonstrates both vulnerable and secure implementations
 */
@RestController
@RequestMapping("/api/owasp/web")
@RequiredArgsConstructor
@Slf4j
public class OwaspWebController {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    /**
     * OWASP #1: Broken Access Control - Demonstration
     */
    @GetMapping("/access-control/vulnerable/{userId}")
    public ResponseEntity<Map<String, Object>> vulnerableAccessControl(@PathVariable Long userId) {
        // VULNERABLE: No access control check - any authenticated user can access any user's data
        Optional<User> user = userRepository.findById(userId);
        if (user.isPresent()) {
            Map<String, Object> response = new HashMap<>();
            response.put("vulnerability", "A01:2021 – Broken Access Control");
            response.put("issue", "No check if current user owns this resource");
            response.put("userId", userId);
            response.put("username", user.get().getUsername());
            response.put("email", user.get().getEmail());
            return ResponseEntity.ok(response);
        }
        return ResponseEntity.notFound().build();
    }

    @GetMapping("/access-control/secure/{userId}")
    @PreAuthorize("hasRole('ADMIN') or #userId.toString() == authentication.principal.id.toString()")
    public ResponseEntity<Map<String, Object>> secureAccessControl(
            @PathVariable Long userId,
            @AuthenticationPrincipal UserDetails userDetails
    ) {
        // SECURE: Checks if user is admin or owns the resource
        Optional<User> user = userRepository.findById(userId);
        Optional<User> currentUser = userRepository.findByUsername(userDetails.getUsername());
        
        if (user.isPresent() && currentUser.isPresent()) {
            // Verify ownership or admin role
            if (!currentUser.get().getId().equals(userId) && 
                !userDetails.getAuthorities().stream()
                    .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"))) {
                return ResponseEntity.status(403).body(Map.of(
                    "error", "Access Denied",
                    "message", "You don't have permission to access this resource"
                ));
            }
            
            Map<String, Object> response = new HashMap<>();
            response.put("protection", "A01:2021 – Broken Access Control - PROTECTED");
            response.put("userId", userId);
            response.put("username", user.get().getUsername());
            response.put("email", user.get().getEmail());
            response.put("message", "Access granted with proper authorization check");
            return ResponseEntity.ok(response);
        }
        return ResponseEntity.notFound().build();
    }

    /**
     * OWASP #2: Cryptographic Failures - Demonstration
     */
    @GetMapping("/crypto/weak-password")
    public ResponseEntity<Map<String, Object>> demonstrateCryptoFailure() {
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "A02:2021 – Cryptographic Failures");
        
        // Demonstrate weak vs strong password storage
        String plainPassword = "myPassword123";
        
        Map<String, String> vulnerable = new HashMap<>();
        vulnerable.put("method", "Plain Text (NEVER USE)");
        vulnerable.put("stored", plainPassword);
        vulnerable.put("risk", "Critical - Password visible to anyone with database access");
        
        Map<String, String> weakHash = new HashMap<>();
        weakHash.put("method", "MD5 Hash (Deprecated)");
        weakHash.put("stored", "MD5 hashes are easily cracked");
        weakHash.put("risk", "High - Rainbow tables can crack MD5");
        
        Map<String, String> secure = new HashMap<>();
        secure.put("method", "BCrypt (Current Implementation)");
        secure.put("stored", passwordEncoder.encode(plainPassword).substring(0, 30) + "...");
        secure.put("strength", "12 rounds");
        secure.put("benefit", "Slow hashing prevents brute force attacks");
        
        response.put("plainPassword", plainPassword);
        response.put("vulnerable", vulnerable);
        response.put("weakHash", weakHash);
        response.put("secure", secure);
        response.put("recommendation", "Always use BCrypt, Argon2, or PBKDF2 for password hashing");
        
        return ResponseEntity.ok(response);
    }

    /**
     * OWASP #3: Injection - SQL Injection Protection
     */
    @GetMapping("/injection/search")
    public ResponseEntity<Map<String, Object>> searchUsers(
            @RequestParam String username,
            @RequestParam(defaultValue = "secure") String mode
    ) {
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "A03:2021 – Injection");
        
        if ("vulnerable".equals(mode)) {
            // DEMONSTRATION ONLY - Actual vulnerable code would look like:
            // "SELECT * FROM users WHERE username = '" + username + "'"
            response.put("demonstration", "SQL Injection Example");
            response.put("vulnerableQuery", "SELECT * FROM users WHERE username = '" + username + "'");
            response.put("attack", "Input: ' OR '1'='1' -- would return all users");
            response.put("risk", "Attacker can read, modify, or delete entire database");
            response.put("note", "This is demonstration only - we use JPA which prevents SQL injection");
        } else {
            // SECURE: Using JPA/Hibernate with parameterized queries
            Optional<User> user = userRepository.findByUsername(username);
            response.put("protection", "SQL Injection - PROTECTED");
            response.put("method", "JPA/Hibernate Parameterized Query");
            response.put("query", "Prepared statement: SELECT * FROM users WHERE username = ?");
            response.put("found", user.isPresent());
            if (user.isPresent()) {
                response.put("username", user.get().getUsername());
            }
            response.put("benefit", "Parameters are escaped automatically, preventing injection");
        }
        
        return ResponseEntity.ok(response);
    }

    /**
     * OWASP #4: Insecure Design - Demonstration
     */
    @PostMapping("/design/password-reset")
    public ResponseEntity<Map<String, Object>> passwordResetDemo(
            @RequestParam String email,
            @RequestParam(defaultValue = "secure") String mode
    ) {
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "A04:2021 – Insecure Design");
        
        Optional<User> user = userRepository.findByEmail(email);
        
        if ("vulnerable".equals(mode)) {
            // VULNERABLE: Reveals if user exists
            if (user.isEmpty()) {
                response.put("status", "error");
                response.put("message", "Email not found in system");
                response.put("issue", "Information disclosure - attacker can enumerate users");
            } else {
                response.put("status", "success");
                response.put("message", "Reset link sent to " + email);
                response.put("issue", "Confirms user exists");
            }
        } else {
            // SECURE: Generic message regardless of whether user exists
            response.put("status", "success");
            response.put("message", "If this email exists in our system, you will receive a password reset link");
            response.put("protection", "Prevents user enumeration");
            response.put("benefit", "Attacker cannot determine valid email addresses");
            
            if (user.isPresent()) {
                response.put("note", "User exists - reset email would be sent (demo mode)");
            } else {
                response.put("note", "User doesn't exist - but same message shown");
            }
        }
        
        return ResponseEntity.ok(response);
    }

    /**
     * OWASP #5: Security Misconfiguration - Demonstration
     */
    @GetMapping("/misconfiguration/info")
    public ResponseEntity<Map<String, Object>> securityConfiguration(
            HttpServletRequest request
    ) {
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "A05:2021 – Security Misconfiguration");
        
        Map<String, Object> vulnerable = new HashMap<>();
        vulnerable.put("exposedHeaders", List.of("Server: Apache Tomcat/10.x", "X-Powered-By: Spring"));
        vulnerable.put("issue", "Exposes technology stack to attackers");
        vulnerable.put("stackTraces", "Detailed error messages with stack traces in production");
        vulnerable.put("defaultCredentials", "admin/admin or test/test still active");
        
        Map<String, Object> secure = new HashMap<>();
        secure.put("securityHeaders", Map.of(
            "Content-Security-Policy", request.getHeader("Content-Security-Policy") != null ? "Enabled" : "Missing",
            "X-Frame-Options", request.getHeader("X-Frame-Options") != null ? "Enabled" : "Missing",
            "X-Content-Type-Options", "nosniff",
            "Strict-Transport-Security", "max-age=31536000"
        ));
        secure.put("errorHandling", "Generic error messages only");
        secure.put("serverHeader", "Removed or generic");
        secure.put("defaultCredentials", "Changed or disabled");
        
        response.put("vulnerable", vulnerable);
        response.put("secure", secure);
        response.put("currentHeaders", Map.of(
            "CSP", request.getHeader("Content-Security-Policy"),
            "X-Frame-Options", request.getHeader("X-Frame-Options")
        ));
        
        return ResponseEntity.ok(response);
    }

    /**
     * OWASP #7: Identification and Authentication Failures
     */
    @PostMapping("/auth/weak-password-check")
    public ResponseEntity<Map<String, Object>> checkPasswordStrength(@RequestBody Map<String, String> request) {
        String password = request.get("password");
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "A07:2021 – Identification and Authentication Failures");
        
        List<String> weaknesses = new ArrayList<>();
        int score = 0;
        
        if (password == null || password.length() < 8) {
            weaknesses.add("Password too short (minimum 8 characters)");
        } else {
            score += 25;
        }
        
        if (!password.matches(".*[A-Z].*")) {
            weaknesses.add("Missing uppercase letter");
        } else {
            score += 25;
        }
        
        if (!password.matches(".*[a-z].*")) {
            weaknesses.add("Missing lowercase letter");
        } else {
            score += 25;
        }
        
        if (!password.matches(".*[0-9].*")) {
            weaknesses.add("Missing number");
        } else {
            score += 15;
        }
        
        if (!password.matches(".*[!@#$%^&*()_+\\-=\\[\\]{};':\"\\\\|,.<>/?].*")) {
            weaknesses.add("Missing special character");
        } else {
            score += 10;
        }
        
        // Check common passwords
        List<String> commonPasswords = List.of("password", "123456", "qwerty", "admin", "letmein");
        if (commonPasswords.stream().anyMatch(cp -> password.toLowerCase().contains(cp))) {
            weaknesses.add("Contains common password pattern");
            score = Math.max(0, score - 50);
        }
        
        String strength;
        if (score < 40) {
            strength = "Weak";
        } else if (score < 70) {
            strength = "Moderate";
        } else {
            strength = "Strong";
        }
        
        response.put("password", password);
        response.put("strength", strength);
        response.put("score", score);
        response.put("weaknesses", weaknesses);
        response.put("recommendation", "Use at least 12 characters with uppercase, lowercase, numbers, and symbols");
        
        Map<String, Object> protection = new HashMap<>();
        protection.put("minLength", 6);
        protection.put("complexity", "Enforced in RegisterRequest DTO");
        protection.put("commonPasswordCheck", "Should be implemented");
        protection.put("rateLimiting", "Prevents brute force attacks");
        protection.put("mfa", "Recommended for sensitive operations");
        
        response.put("currentProtection", protection);
        
        return ResponseEntity.ok(response);
    }

    /**
     * OWASP #9: Security Logging and Monitoring Failures
     */
    @GetMapping("/logging/demo")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Map<String, Object>> demonstrateLogging(
            @AuthenticationPrincipal UserDetails userDetails
    ) {
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "A09:2021 – Security Logging and Monitoring Failures");
        
        // Log this security-relevant event
        log.info("Security audit: User '{}' accessed logging demonstration", userDetails.getUsername());
        log.info("IP Address: Could be logged from HttpServletRequest");
        log.info("Timestamp: {}", new Date());
        
        Map<String, Object> vulnerable = new HashMap<>();
        vulnerable.put("issues", List.of(
            "No logging of authentication failures",
            "No logging of authorization failures",
            "No logging of sensitive data access",
            "No log retention policy",
            "Logs stored without encryption"
        ));
        
        Map<String, Object> secure = new HashMap<>();
        secure.put("whatToLog", List.of(
            "All authentication attempts (success and failure)",
            "All authorization failures",
            "Input validation failures",
            "Access to sensitive data",
            "Configuration changes",
            "Administrative actions"
        ));
        secure.put("logFormat", "Structured logging (JSON) for easy parsing");
        secure.put("retention", "90 days minimum for security logs");
        secure.put("monitoring", "Real-time alerts for suspicious patterns");
        secure.put("encryption", "Logs encrypted at rest and in transit");
        
        response.put("vulnerable", vulnerable);
        response.put("secure", secure);
        response.put("currentImplementation", Map.of(
            "framework", "SLF4J + Logback",
            "level", "DEBUG (should be INFO in production)",
            "output", "Console (should be file/centralized logging system)"
        ));
        response.put("note", "This access has been logged for demonstration");
        
        return ResponseEntity.ok(response);
    }

    /**
     * OWASP #10: Server-Side Request Forgery (SSRF)
     */
    @GetMapping("/ssrf/fetch-url")
    public ResponseEntity<Map<String, Object>> ssrfDemo(
            @RequestParam String url,
            @RequestParam(defaultValue = "secure") String mode
    ) {
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "A10:2021 – Server-Side Request Forgery (SSRF)");
        
        if ("vulnerable".equals(mode)) {
            // VULNERABLE: No URL validation
            response.put("demonstration", "SSRF Vulnerability");
            response.put("providedUrl", url);
            response.put("issue", "Server would fetch: " + url);
            response.put("attacks", List.of(
                "http://localhost:8080/actuator - Access internal endpoints",
                "http://169.254.169.254/latest/meta-data/ - AWS metadata",
                "file:///etc/passwd - Local file access",
                "http://internal-admin:8080 - Internal network scan"
            ));
            response.put("risk", "Attacker can access internal resources and services");
        } else {
            // SECURE: URL whitelist validation
            List<String> allowedDomains = List.of("api.example.com", "data.company.com");
            boolean isAllowed = false;
            
            try {
                java.net.URL parsedUrl = new java.net.URL(url);
                String host = parsedUrl.getHost();
                
                // Check if host is in whitelist
                isAllowed = allowedDomains.stream().anyMatch(domain -> host.equals(domain));
                
                // Additional checks
                boolean isPrivate = host.equals("localhost") || 
                                  host.equals("127.0.0.1") ||
                                  host.startsWith("192.168.") ||
                                  host.startsWith("10.") ||
                                  host.equals("169.254.169.254");
                
                if (isPrivate) {
                    response.put("status", "blocked");
                    response.put("reason", "Private/Internal IP address");
                } else if (!isAllowed) {
                    response.put("status", "blocked");
                    response.put("reason", "Domain not in whitelist");
                } else {
                    response.put("status", "allowed");
                    response.put("message", "URL would be fetched (demo mode)");
                }
                
                response.put("protection", "SSRF - PROTECTED");
                response.put("providedUrl", url);
                response.put("allowedDomains", allowedDomains);
                response.put("validation", Map.of(
                    "schemeCheck", "Only HTTP/HTTPS allowed",
                    "domainWhitelist", "Strict whitelist enforced",
                    "privateIPBlock", "Blocks localhost, RFC1918, cloud metadata",
                    "redirectsDisabled", "Should disable HTTP redirects"
                ));
                
            } catch (Exception e) {
                response.put("status", "error");
                response.put("message", "Invalid URL format");
            }
        }
        
        return ResponseEntity.ok(response);
    }

    /**
     * Get all OWASP Web Top 10 demonstrations
     */
    @GetMapping("/demonstrations")
    public ResponseEntity<Map<String, Object>> getAllDemonstrations() {
        Map<String, Object> response = new HashMap<>();
        response.put("title", "OWASP Top 10 Web Application Security Risks (2021)");
        
        List<Map<String, String>> demonstrations = new ArrayList<>();
        
        demonstrations.add(Map.of(
            "id", "A01",
            "name", "Broken Access Control",
            "endpoint", "/api/owasp/web/access-control/vulnerable/{userId}",
            "secureEndpoint", "/api/owasp/web/access-control/secure/{userId}"
        ));
        
        demonstrations.add(Map.of(
            "id", "A02",
            "name", "Cryptographic Failures",
            "endpoint", "/api/owasp/web/crypto/weak-password"
        ));
        
        demonstrations.add(Map.of(
            "id", "A03",
            "name", "Injection",
            "endpoint", "/api/owasp/web/injection/search?username=admin&mode=secure"
        ));
        
        demonstrations.add(Map.of(
            "id", "A04",
            "name", "Insecure Design",
            "endpoint", "/api/owasp/web/design/password-reset?email=test@example.com&mode=secure"
        ));
        
        demonstrations.add(Map.of(
            "id", "A05",
            "name", "Security Misconfiguration",
            "endpoint", "/api/owasp/web/misconfiguration/info"
        ));
        
        demonstrations.add(Map.of(
            "id", "A07",
            "name", "Identification and Authentication Failures",
            "endpoint", "/api/owasp/web/auth/weak-password-check"
        ));
        
        demonstrations.add(Map.of(
            "id", "A09",
            "name", "Security Logging and Monitoring Failures",
            "endpoint", "/api/owasp/web/logging/demo"
        ));
        
        demonstrations.add(Map.of(
            "id", "A10",
            "name", "Server-Side Request Forgery (SSRF)",
            "endpoint", "/api/owasp/web/ssrf/fetch-url?url=http://example.com&mode=secure"
        ));
        
        response.put("demonstrations", demonstrations);
        response.put("note", "All endpoints demonstrate both vulnerable and secure implementations");
        
        return ResponseEntity.ok(response);
    }
}
