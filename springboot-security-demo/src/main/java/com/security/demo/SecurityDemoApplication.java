package com.security.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;

@SpringBootApplication
@EnableMethodSecurity(prePostEnabled = true, securedEnabled = true, jsr250Enabled = true)
@EnableAsync
@EnableScheduling
public class SecurityDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(SecurityDemoApplication.class, args);
        System.out.println("\n==============================================");
        System.out.println("Spring Boot Security Demo Application Started");
        System.out.println("==============================================");
        System.out.println("Access the application at: http://localhost:8080");
        System.out.println("H2 Console: http://localhost:8080/h2-console");
        System.out.println("\nDefault Users:");
        System.out.println("  Admin - username: admin, password: admin123");
        System.out.println("  User  - username: user, password: user123");
        System.out.println("==============================================\n");
    }
}
