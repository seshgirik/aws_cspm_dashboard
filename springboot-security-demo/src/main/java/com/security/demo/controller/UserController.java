package com.security.demo.controller;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/user")
public class UserController {

    @GetMapping("/profile")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public Map<String, Object> getUserProfile(@AuthenticationPrincipal UserDetails userDetails) {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "User Profile");
        response.put("username", userDetails.getUsername());
        response.put("authorities", userDetails.getAuthorities());
        return response;
    }

    @GetMapping("/dashboard")
    public Map<String, Object> getUserDashboard(@AuthenticationPrincipal UserDetails userDetails) {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "Welcome to User Dashboard");
        response.put("user", userDetails.getUsername());
        response.put("features", new String[]{
            "View Profile",
            "Update Settings",
            "View Activity History"
        });
        return response;
    }

    @PutMapping("/settings")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public Map<String, Object> updateSettings(
            @RequestBody Map<String, Object> settings,
            @AuthenticationPrincipal UserDetails userDetails
    ) {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "Settings updated successfully");
        response.put("user", userDetails.getUsername());
        response.put("updatedSettings", settings);
        return response;
    }

    @GetMapping("/data")
    @PreAuthorize("hasAuthority('USER:READ')")
    public Map<String, Object> getUserData() {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "User data retrieved");
        response.put("data", Map.of(
            "recent_activity", "Logged in 2 hours ago",
            "last_update", "2026-01-08",
            "status", "Active"
        ));
        return response;
    }
}
