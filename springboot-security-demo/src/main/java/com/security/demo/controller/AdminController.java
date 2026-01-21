package com.security.demo.controller;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.security.Principal;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    @GetMapping("/dashboard")
    @PreAuthorize("hasRole('ADMIN')")
    public Map<String, Object> getAdminDashboard(Principal principal) {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "Welcome to Admin Dashboard");
        response.put("user", principal.getName());
        response.put("role", "ADMIN");
        response.put("features", new String[]{
            "User Management",
            "System Configuration",
            "Security Audit Logs",
            "Performance Metrics"
        });
        return response;
    }

    @GetMapping("/users")
    @PreAuthorize("hasAuthority('ADMIN:READ')")
    public Map<String, Object> getAllUsers() {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "List of all users");
        response.put("users", new String[]{"admin", "user1", "user2"});
        return response;
    }

    @GetMapping("/audit-logs")
    @PreAuthorize("hasRole('ADMIN')")
    public Map<String, Object> getAuditLogs() {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "Security audit logs");
        response.put("logs", new String[]{
            "2026-01-09 10:15:23 - User 'admin' logged in",
            "2026-01-09 10:20:45 - User 'user1' accessed /api/user/profile",
            "2026-01-09 10:25:12 - Failed login attempt for 'unknown'"
        });
        return response;
    }

    @GetMapping("/system-config")
    @PreAuthorize("hasRole('ADMIN') and hasAuthority('ADMIN:WRITE')")
    public Map<String, Object> getSystemConfig() {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "System configuration");
        response.put("config", Map.of(
            "jwt_expiration", "24h",
            "max_sessions", "1",
            "password_policy", "Strong",
            "rate_limiting", "60 req/min"
        ));
        return response;
    }
}
