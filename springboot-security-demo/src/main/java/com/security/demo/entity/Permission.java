package com.security.demo.entity;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public enum Permission {
    
    ADMIN_READ("ADMIN:READ"),
    ADMIN_WRITE("ADMIN:WRITE"),
    ADMIN_DELETE("ADMIN:DELETE"),
    USER_READ("USER:READ"),
    USER_WRITE("USER:WRITE");

    @Getter
    private final String permission;
}
