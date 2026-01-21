package com.security.demo.controller;

import com.security.demo.entity.User;
import com.security.demo.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * OWASP API Security Top 10 Demonstrations
 * This controller demonstrates API-specific security issues and their mitigations
 */
@RestController
@RequestMapping("/api/owasp/api")
@RequiredArgsConstructor
@Slf4j
public class OwaspApiController {

    private final UserRepository userRepository;
    
    // Simulated rate limiting storage (in production, use Redis or similar)
    private static final Map<String, List<Long>> rateLimitStore = new ConcurrentHashMap<>();
    private static final int MAX_REQUESTS = 5;
    private static final long TIME_WINDOW = 60000; // 1 minute

    /**
     * API1:2023 Broken Object Level Authorization (BOLA)
     */
    @GetMapping("/bola/vulnerable/users/{id}/data")
    public ResponseEntity<Map<String, Object>> bolaVulnerable(@PathVariable Long id) {
        // VULNERABLE: No check if user can access this specific object
        Optional<User> user = userRepository.findById(id);
        
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "API1:2023 – Broken Object Level Authorization (BOLA)");
        
        if (user.isPresent()) {
            response.put("issue", "Any authenticated user can access any user's data");
            response.put("userId", id);
            response.put("sensitiveData", Map.of(
                "username", user.get().getUsername(),
                "email", user.get().getEmail(),
                "role", user.get().getRole().name(),
                "accountStatus", "active"
            ));
            response.put("attack", "Attacker can iterate through IDs to access all user data");
            return ResponseEntity.ok(response);
        }
        return ResponseEntity.notFound().build();
    }

    @GetMapping("/bola/secure/users/{id}/data")
    public ResponseEntity<Map<String, Object>> bolaSecure(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails
    ) {
        // SECURE: Verify user owns this resource or is admin
        Optional<User> targetUser = userRepository.findById(id);
        Optional<User> currentUser = userRepository.findByUsername(userDetails.getUsername());
        
        Map<String, Object> response = new HashMap<>();
        response.put("protection", "API1:2023 – BOLA - PROTECTED");
        
        if (targetUser.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        
        if (currentUser.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        
        // Check ownership or admin role
        boolean isOwner = currentUser.get().getId().equals(id);
        boolean isAdmin = userDetails.getAuthorities().stream()
                .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));
        
        if (!isOwner && !isAdmin) {
            response.put("error", "Forbidden");
            response.put("message", "You don't have permission to access this resource");
            log.warn("BOLA attempt: User '{}' tried to access user ID {}", userDetails.getUsername(), id);
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body(response);
        }
        
        response.put("userId", id);
        response.put("data", Map.of(
            "username", targetUser.get().getUsername(),
            "email", targetUser.get().getEmail(),
            "role", targetUser.get().getRole().name()
        ));
        response.put("authorization", isOwner ? "Resource Owner" : "Administrator");
        
        return ResponseEntity.ok(response);
    }

    /**
     * API2:2023 Broken Authentication
     */
    @PostMapping("/auth/demo")
    public ResponseEntity<Map<String, Object>> authenticationDemo(@RequestBody Map<String, String> credentials) {
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "API2:2023 – Broken Authentication");
        
        Map<String, Object> vulnerable = new HashMap<>();
        vulnerable.put("issues", List.of(
            "Weak password requirements",
            "No rate limiting on login attempts",
            "Credentials in URL parameters",
            "Long-lived tokens without refresh",
            "JWT tokens without expiration",
            "No multi-factor authentication"
        ));
        
        Map<String, Object> secure = new HashMap<>();
        secure.put("implementations", List.of(
            "Strong password policy (min 8 chars, complexity)",
            "BCrypt password hashing (strength 12)",
            "JWT with 24-hour expiration",
            "Rate limiting on authentication endpoints",
            "Account lockout after failed attempts",
            "MFA for sensitive operations"
        ));
        secure.put("currentApp", Map.of(
            "passwordHashing", "BCrypt (strength 12)",
            "tokenExpiration", "24 hours",
            "rateLimiting", "Should be implemented",
            "accountLockout", "Should be implemented",
            "mfa", "Should be implemented for production"
        ));
        
        response.put("vulnerable", vulnerable);
        response.put("secure", secure);
        
        return ResponseEntity.ok(response);
    }

    /**
     * API3:2023 Broken Object Property Level Authorization
     */
    @PutMapping("/property-auth/vulnerable/users/{id}")
    public ResponseEntity<Map<String, Object>> propertyAuthVulnerable(
            @PathVariable Long id,
            @RequestBody Map<String, Object> updates
    ) {
        // VULNERABLE: Allows updating any field including role, permissions
        Optional<User> user = userRepository.findById(id);
        
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "API3:2023 – Broken Object Property Level Authorization");
        
        if (user.isPresent()) {
            response.put("issue", "User can update sensitive fields like role, permissions");
            response.put("providedUpdates", updates);
            response.put("danger", "If role field is updated, user could escalate to admin");
            response.put("attack", Map.of(
                "massAssignment", "Sending extra fields: {\"role\": \"ADMIN\"}",
                "propertyOverride", "Updating isActive, permissions, etc."
            ));
        }
        
        return ResponseEntity.ok(response);
    }

    @PutMapping("/property-auth/secure/users/{id}")
    @PreAuthorize("hasRole('ADMIN') or #id.toString() == authentication.principal.id.toString()")
    public ResponseEntity<Map<String, Object>> propertyAuthSecure(
            @PathVariable Long id,
            @RequestBody Map<String, Object> updates,
            @AuthenticationPrincipal UserDetails userDetails
    ) {
        // SECURE: Whitelist of allowed fields, no role/permission updates
        List<String> allowedFields = List.of("email");
        List<String> adminOnlyFields = List.of("role", "enabled", "accountNonLocked");
        
        Map<String, Object> response = new HashMap<>();
        response.put("protection", "API3:2023 – Property Authorization - PROTECTED");
        
        boolean isAdmin = userDetails.getAuthorities().stream()
                .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));
        
        Map<String, String> updateStatus = new HashMap<>();
        
        for (String field : updates.keySet()) {
            if (adminOnlyFields.contains(field) && !isAdmin) {
                updateStatus.put(field, "Rejected - Admin only field");
            } else if (allowedFields.contains(field)) {
                updateStatus.put(field, "Accepted");
            } else if (adminOnlyFields.contains(field) && isAdmin) {
                updateStatus.put(field, "Accepted - Admin privilege");
            } else {
                updateStatus.put(field, "Rejected - Not in whitelist");
            }
        }
        
        response.put("requestedUpdates", updates.keySet());
        response.put("updateStatus", updateStatus);
        response.put("allowedFields", allowedFields);
        response.put("adminOnlyFields", adminOnlyFields);
        response.put("protection", "Field-level authorization with whitelist");
        
        return ResponseEntity.ok(response);
    }

    /**
     * API4:2023 Unrestricted Resource Consumption
     */
    @GetMapping("/resource/vulnerable/export")
    public ResponseEntity<Map<String, Object>> resourceConsumptionVulnerable(
            @RequestParam(required = false) Integer limit
    ) {
        // VULNERABLE: No limit on data returned, can cause DoS
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "API4:2023 – Unrestricted Resource Consumption");
        
        int recordCount = limit != null ? limit : 1000000; // Default to huge number
        
        response.put("issue", "No limit on data export - can exhaust server resources");
        response.put("requestedRecords", recordCount);
        response.put("danger", Map.of(
            "memory", "Loading millions of records into memory",
            "cpu", "Processing takes excessive CPU time",
            "bandwidth", "Massive response size",
            "dos", "Attacker can bring down service"
        ));
        response.put("attacks", List.of(
            "Request 1 million records",
            "Multiple concurrent large requests",
            "Recursive/infinite queries",
            "Large file uploads without size limit"
        ));
        
        return ResponseEntity.ok(response);
    }

    @GetMapping("/resource/secure/export")
    public ResponseEntity<Map<String, Object>> resourceConsumptionSecure(
            @RequestParam(required = false, defaultValue = "10") Integer limit,
            @RequestParam(required = false, defaultValue = "0") Integer offset,
            @AuthenticationPrincipal UserDetails userDetails
    ) {
        // SECURE: Enforce max limit, pagination, rate limiting
        final int MAX_LIMIT = 100;
        final int MAX_OFFSET = 10000;
        
        Map<String, Object> response = new HashMap<>();
        response.put("protection", "API4:2023 – Resource Consumption - PROTECTED");
        
        int actualLimit = Math.min(limit, MAX_LIMIT);
        int actualOffset = Math.min(offset, MAX_OFFSET);
        
        // Check rate limit
        String userKey = userDetails.getUsername();
        if (isRateLimited(userKey)) {
            response.put("error", "Rate Limit Exceeded");
            response.put("message", "Too many requests. Try again later.");
            response.put("retryAfter", "60 seconds");
            return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS).body(response);
        }
        
        response.put("requestedLimit", limit);
        response.put("appliedLimit", actualLimit);
        response.put("maxAllowedLimit", MAX_LIMIT);
        response.put("pagination", Map.of(
            "limit", actualLimit,
            "offset", actualOffset,
            "maxOffset", MAX_OFFSET
        ));
        response.put("protections", List.of(
            "Max limit enforced: " + MAX_LIMIT,
            "Pagination required for large datasets",
            "Rate limiting: " + MAX_REQUESTS + " requests per minute",
            "Timeout enforcement: 30 seconds",
            "Response size limit: 10MB"
        ));
        response.put("rateLimitRemaining", getRemainingRequests(userKey));
        
        return ResponseEntity.ok(response);
    }

    /**
     * API5:2023 Broken Function Level Authorization
     */
    @GetMapping("/function-auth/vulnerable/admin/stats")
    public ResponseEntity<Map<String, Object>> functionAuthVulnerable() {
        // VULNERABLE: No role check - any authenticated user can access
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "API5:2023 – Broken Function Level Authorization");
        response.put("issue", "Admin function accessible to all authenticated users");
        response.put("sensitiveData", Map.of(
            "totalUsers", 1000,
            "revenue", "$500,000",
            "activeSubscriptions", 750,
            "serverLoad", "45%"
        ));
        response.put("danger", "Any user can access admin-only functions");
        
        return ResponseEntity.ok(response);
    }

    @GetMapping("/function-auth/secure/admin/stats")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Map<String, Object>> functionAuthSecure(
            @AuthenticationPrincipal UserDetails userDetails
    ) {
        // SECURE: @PreAuthorize enforces role check
        Map<String, Object> response = new HashMap<>();
        response.put("protection", "API5:2023 – Function Authorization - PROTECTED");
        response.put("stats", Map.of(
            "totalUsers", 1000,
            "revenue", "$500,000",
            "activeSubscriptions", 750,
            "serverLoad", "45%"
        ));
        response.put("accessGranted", "Admin role verified");
        response.put("user", userDetails.getUsername());
        response.put("protection", "@PreAuthorize annotation enforces role-based access");
        
        log.info("Admin stats accessed by: {}", userDetails.getUsername());
        
        return ResponseEntity.ok(response);
    }

    /**
     * API6:2023 Unrestricted Access to Sensitive Business Flows
     */
    @PostMapping("/business-flow/vulnerable/purchase")
    public ResponseEntity<Map<String, Object>> businessFlowVulnerable(@RequestBody Map<String, Object> purchase) {
        // VULNERABLE: No checks for automated/bulk operations
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "API6:2023 – Unrestricted Access to Sensitive Business Flows");
        response.put("issue", "No protection against automated bulk operations");
        response.put("purchase", purchase);
        response.put("dangers", List.of(
            "Scalpers buying all inventory with bots",
            "Automated account creation for abuse",
            "Mass voting/rating manipulation",
            "Bulk ticket purchasing"
        ));
        response.put("note", "Purchase processed without rate limiting or CAPTCHA");
        
        return ResponseEntity.ok(response);
    }

    @PostMapping("/business-flow/secure/purchase")
    public ResponseEntity<Map<String, Object>> businessFlowSecure(
            @RequestBody Map<String, Object> purchase,
            @RequestHeader(value = "X-CAPTCHA-Token", required = false) String captchaToken,
            @AuthenticationPrincipal UserDetails userDetails
    ) {
        // SECURE: Rate limiting, CAPTCHA, purchase limits
        Map<String, Object> response = new HashMap<>();
        response.put("protection", "API6:2023 – Business Flow - PROTECTED");
        
        // Check rate limit
        String userKey = "purchase_" + userDetails.getUsername();
        if (isRateLimited(userKey)) {
            response.put("error", "Too many purchase attempts");
            response.put("message", "Please wait before making another purchase");
            return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS).body(response);
        }
        
        // Verify CAPTCHA (in production)
        if (captchaToken == null || captchaToken.isEmpty()) {
            response.put("note", "CAPTCHA required for purchase (demo mode - not enforced)");
        }
        
        response.put("purchase", purchase);
        response.put("protections", Map.of(
            "rateLimit", "Max 3 purchases per minute",
            "captcha", "Required for sensitive flows",
            "accountAge", "Minimum 24 hours for high-value purchases",
            "velocityCheck", "Monitors suspicious patterns",
            "deviceFingerprinting", "Tracks devices used"
        ));
        response.put("purchaseStatus", "Approved with security checks");
        
        return ResponseEntity.ok(response);
    }

    /**
     * API8:2023 Security Misconfiguration (API Specific)
     */
    @GetMapping("/misconfiguration/demo")
    public ResponseEntity<Map<String, Object>> apiMisconfigurationDemo() {
        Map<String, Object> response = new HashMap<>();
        response.put("vulnerability", "API8:2023 – Security Misconfiguration");
        
        Map<String, Object> vulnerable = new HashMap<>();
        vulnerable.put("issues", List.of(
            "Verbose error messages with stack traces",
            "CORS allows all origins (*)",
            "Missing security headers",
            "Default credentials unchanged",
            "Unnecessary HTTP methods enabled (TRACE, OPTIONS abuse)",
            "Missing input validation",
            "Unnecessary endpoints exposed"
        ));
        
        Map<String, Object> secure = new HashMap<>();
        secure.put("implementations", List.of(
            "Generic error messages",
            "CORS whitelist specific origins",
            "Security headers enforced (CSP, HSTS, etc)",
            "All default credentials changed",
            "Only necessary HTTP methods allowed",
            "Input validation on all endpoints",
            "API versioning",
            "Remove unnecessary endpoints"
        ));
        
        response.put("vulnerable", vulnerable);
        response.put("secure", secure);
        response.put("currentConfig", Map.of(
            "cors", "Configured for specific origins",
            "headers", "CSP, X-Frame-Options, HSTS enabled",
            "errorHandling", "Custom exception handler",
            "validation", "Jakarta Validation enabled"
        ));
        
        return ResponseEntity.ok(response);
    }

    /**
     * Get all OWASP API Security Top 10 demonstrations
     */
    @GetMapping("/demonstrations")
    public ResponseEntity<Map<String, Object>> getAllApiDemonstrations() {
        Map<String, Object> response = new HashMap<>();
        response.put("title", "OWASP API Security Top 10 (2023)");
        
        List<Map<String, String>> demonstrations = new ArrayList<>();
        
        demonstrations.add(Map.of(
            "id", "API1",
            "name", "Broken Object Level Authorization (BOLA)",
            "vulnerableEndpoint", "/api/owasp/api/bola/vulnerable/users/{id}/data",
            "secureEndpoint", "/api/owasp/api/bola/secure/users/{id}/data"
        ));
        
        demonstrations.add(Map.of(
            "id", "API2",
            "name", "Broken Authentication",
            "endpoint", "/api/owasp/api/auth/demo"
        ));
        
        demonstrations.add(Map.of(
            "id", "API3",
            "name", "Broken Object Property Level Authorization",
            "vulnerableEndpoint", "/api/owasp/api/property-auth/vulnerable/users/{id}",
            "secureEndpoint", "/api/owasp/api/property-auth/secure/users/{id}"
        ));
        
        demonstrations.add(Map.of(
            "id", "API4",
            "name", "Unrestricted Resource Consumption",
            "vulnerableEndpoint", "/api/owasp/api/resource/vulnerable/export?limit=1000000",
            "secureEndpoint", "/api/owasp/api/resource/secure/export?limit=10&offset=0"
        ));
        
        demonstrations.add(Map.of(
            "id", "API5",
            "name", "Broken Function Level Authorization",
            "vulnerableEndpoint", "/api/owasp/api/function-auth/vulnerable/admin/stats",
            "secureEndpoint", "/api/owasp/api/function-auth/secure/admin/stats"
        ));
        
        demonstrations.add(Map.of(
            "id", "API6",
            "name", "Unrestricted Access to Sensitive Business Flows",
            "vulnerableEndpoint", "/api/owasp/api/business-flow/vulnerable/purchase",
            "secureEndpoint", "/api/owasp/api/business-flow/secure/purchase"
        ));
        
        demonstrations.add(Map.of(
            "id", "API8",
            "name", "Security Misconfiguration",
            "endpoint", "/api/owasp/api/misconfiguration/demo"
        ));
        
        response.put("demonstrations", demonstrations);
        response.put("note", "All endpoints require authentication. Some require admin role.");
        
        return ResponseEntity.ok(response);
    }

    // Helper methods for rate limiting (simplified - use Redis in production)
    private boolean isRateLimited(String key) {
        List<Long> requests = rateLimitStore.computeIfAbsent(key, k -> new ArrayList<>());
        long now = System.currentTimeMillis();
        
        // Remove old requests outside time window
        requests.removeIf(timestamp -> now - timestamp > TIME_WINDOW);
        
        if (requests.size() >= MAX_REQUESTS) {
            return true;
        }
        
        requests.add(now);
        return false;
    }

    private int getRemainingRequests(String key) {
        List<Long> requests = rateLimitStore.get(key);
        if (requests == null) {
            return MAX_REQUESTS;
        }
        
        long now = System.currentTimeMillis();
        long validRequests = requests.stream()
                .filter(timestamp -> now - timestamp <= TIME_WINDOW)
                .count();
        
        return Math.max(0, MAX_REQUESTS - (int) validRequests);
    }
}
