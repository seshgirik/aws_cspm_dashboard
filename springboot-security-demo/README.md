# Spring Boot Security Demo Application

A comprehensive demonstration of Spring Boot Security features including JWT authentication, role-based access control, method-level security, and various security best practices.

## 🚀 Features

### Authentication & Authorization
- **JWT (JSON Web Token)** authentication with custom token provider
- **BCrypt password encoding** with strength level 12
- **Role-Based Access Control (RBAC)** with USER and ADMIN roles
- **Permission-based authorization** with fine-grained access control
- **Method-level security** using @PreAuthorize annotations

### Security Features
- **CSRF Protection** (configurable per endpoint)
- **CORS Configuration** with allowlist
- **Security Headers**:
  - Content Security Policy (CSP)
  - X-Frame-Options
  - X-XSS-Protection
  - X-Content-Type-Options
  - Strict-Transport-Security (HSTS)
  - Referrer-Policy
  - Permissions-Policy
- **Session Management** with stateless JWT-based authentication
- **Input Validation** using Jakarta Validation API
- **Custom Exception Handling** for authentication failures

### Application Features
- RESTful API with JSON responses
- Interactive web UI for testing
- H2 in-memory database for easy testing
- Pre-configured test users
- Thymeleaf templates for frontend
- Actuator endpoints for monitoring (admin-only)

## 📋 Prerequisites

- Java 17 or higher
- Maven 3.6 or higher
- Your favorite IDE (IntelliJ IDEA, Eclipse, VS Code)

## 🛠️ Installation & Setup

### 1. Clone or navigate to the project directory

```bash
cd springboot-security-demo
```

### 2. Build the project

```bash
mvn clean install
```

### 3. Run the application

```bash
mvn spring-boot:run
```

Or run the JAR directly:

```bash
java -jar target/springboot-security-demo-1.0.0.jar
```

The application will start on `http://localhost:8080`

## 🔐 Default Credentials

The application comes with two pre-configured users:

### Admin User
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: ADMIN
- **Permissions**: Full access to all endpoints

### Regular User
- **Username**: `user`
- **Password**: `user123`
- **Role**: USER
- **Permissions**: Access to user endpoints only

## 📡 API Endpoints

### Public Endpoints (No Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with interactive UI |
| GET | `/public/info` | Public information page |
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | User authentication |
| GET | `/auth/test` | Test authentication endpoint |

### User Endpoints (USER or ADMIN role)

| Method | Endpoint | Description | Required Permission |
|--------|----------|-------------|-------------------|
| GET | `/api/user/profile` | Get user profile | USER or ADMIN role |
| GET | `/api/user/dashboard` | User dashboard | USER or ADMIN role |
| PUT | `/api/user/settings` | Update user settings | USER or ADMIN role |
| GET | `/api/user/data` | Get user data | USER:READ permission |

### Admin Endpoints (ADMIN role only)

| Method | Endpoint | Description | Required Permission |
|--------|----------|-------------|-------------------|
| GET | `/api/admin/dashboard` | Admin dashboard | ADMIN role |
| GET | `/api/admin/users` | List all users | ADMIN:READ permission |
| GET | `/api/admin/audit-logs` | View security audit logs | ADMIN role |
| GET | `/api/admin/system-config` | System configuration | ADMIN:WRITE permission |

### Actuator Endpoints (ADMIN only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/actuator/health` | Application health status |
| GET | `/actuator/info` | Application information |
| GET | `/actuator/metrics` | Application metrics |

## 🧪 Testing the Application

### Using the Web UI

1. Open your browser and navigate to `http://localhost:8080`
2. You'll see an interactive demo page with:
   - Login form
   - Registration form
   - API testing buttons
   - Available endpoints list
   - Security features overview

3. Login with one of the default users
4. Test the protected endpoints using the provided buttons

### Using cURL

#### 1. Register a new user

```bash
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### 2. Login and get JWT token

```bash
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "username": "admin",
  "role": "ADMIN",
  "message": "Authentication successful"
}
```

#### 3. Access protected endpoint with JWT

```bash
curl -X GET http://localhost:8080/api/user/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### 4. Try admin endpoint (will fail if not admin)

```bash
curl -X GET http://localhost:8080/api/admin/dashboard \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Using Postman

1. Create a new request
2. Set method to POST and URL to `http://localhost:8080/auth/login`
3. In Body tab, select "raw" and "JSON"
4. Enter credentials:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
5. Send the request and copy the token from response
6. For protected endpoints:
   - Add header: `Authorization: Bearer YOUR_TOKEN`
   - Test different endpoints

## 🗄️ Database Access

The application uses H2 in-memory database. You can access the H2 console:

1. Navigate to: `http://localhost:8080/h2-console`
2. Use these settings:
   - JDBC URL: `jdbc:h2:mem:securitydb`
   - Username: `sa`
   - Password: (leave empty)

## 🔧 Configuration

### JWT Configuration

Edit `application.yml`:

```yaml
jwt:
  secret: your-secret-key-here  # Base64 encoded secret
  expiration: 86400000          # Token expiration (24 hours)
```

### Security Headers

Customize security headers in `SecurityConfig.java`:

```java
.headers(headers -> headers
    .contentSecurityPolicy(csp -> csp
        .policyDirectives("your-csp-policy")
    )
    // ... other headers
)
```

### CORS Configuration

Modify allowed origins in `SecurityConfig.java`:

```java
configuration.setAllowedOrigins(List.of(
    "http://localhost:3000",
    "https://your-domain.com"
));
```

## 📊 Security Features Explained

### 1. JWT Authentication
- Stateless authentication using JSON Web Tokens
- Token contains user information and authorities
- 24-hour expiration (configurable)
- Signature verification on every request

### 2. Password Security
- BCrypt hashing with strength 12
- Passwords never stored in plain text
- Salting automatically handled by BCrypt

### 3. Role-Based Access Control
- Hierarchical role system (USER < ADMIN)
- Fine-grained permissions (READ, WRITE, DELETE)
- Method-level security with @PreAuthorize

### 4. Security Headers
- **CSP**: Prevents XSS attacks by controlling resource loading
- **X-Frame-Options**: Prevents clickjacking attacks
- **HSTS**: Forces HTTPS connections
- **X-XSS-Protection**: Browser XSS protection
- **Referrer-Policy**: Controls referrer information

### 5. CSRF Protection
- Enabled for form-based requests
- Disabled for stateless API endpoints (JWT)
- Automatic token generation and validation

### 6. Session Management
- Stateless sessions (no server-side storage)
- Maximum 1 concurrent session per user
- Session timeout: 30 minutes

## 🏗️ Project Structure

```
springboot-security-demo/
├── src/
│   ├── main/
│   │   ├── java/com/security/demo/
│   │   │   ├── config/
│   │   │   │   ├── SecurityConfig.java          # Main security configuration
│   │   │   │   └── DataInitializer.java         # Initialize test users
│   │   │   ├── controller/
│   │   │   │   ├── AuthenticationController.java # Auth endpoints
│   │   │   │   ├── UserController.java          # User endpoints
│   │   │   │   ├── AdminController.java         # Admin endpoints
│   │   │   │   └── PublicController.java        # Public endpoints
│   │   │   ├── entity/
│   │   │   │   ├── User.java                    # User entity
│   │   │   │   ├── Role.java                    # Role enum
│   │   │   │   └── Permission.java              # Permission enum
│   │   │   ├── repository/
│   │   │   │   └── UserRepository.java          # User data access
│   │   │   ├── security/
│   │   │   │   ├── JwtTokenProvider.java        # JWT utilities
│   │   │   │   ├── JwtAuthenticationFilter.java # JWT filter
│   │   │   │   └── JwtAuthenticationEntryPoint.java
│   │   │   ├── service/
│   │   │   │   ├── AuthenticationService.java   # Auth logic
│   │   │   │   └── CustomUserDetailsService.java
│   │   │   ├── dto/
│   │   │   │   ├── RegisterRequest.java
│   │   │   │   ├── AuthenticationRequest.java
│   │   │   │   └── AuthenticationResponse.java
│   │   │   └── SecurityDemoApplication.java     # Main application
│   │   └── resources/
│   │       ├── application.yml                  # Application config
│   │       └── templates/
│   │           └── index.html                   # Demo UI
│   └── test/
│       └── java/com/security/demo/
│           └── SecurityDemoApplicationTests.java
└── pom.xml                                       # Maven dependencies
```

## 🔍 Testing Security Features

### 1. Test JWT Expiration
- Login and get token
- Wait for token to expire (default 24 hours)
- Try to access protected endpoint
- Should receive 401 Unauthorized

### 2. Test Role-Based Access
- Login as regular user
- Try to access admin endpoint
- Should receive 403 Forbidden

### 3. Test Invalid Token
- Try accessing protected endpoint with invalid/malformed token
- Should receive 401 Unauthorized

### 4. Test Missing Token
- Try accessing protected endpoint without Authorization header
- Should receive 401 Unauthorized

## 📚 Technologies Used

- **Spring Boot 3.2.0** - Application framework
- **Spring Security 6** - Security framework
- **JWT (jjwt 0.12.3)** - Token-based authentication
- **Spring Data JPA** - Data persistence
- **H2 Database** - In-memory database
- **Thymeleaf** - Template engine
- **Lombok** - Boilerplate code reduction
- **Jakarta Validation** - Input validation
- **Spring Boot Actuator** - Monitoring and management

## 🚨 Security Best Practices Implemented

1. ✅ Never store passwords in plain text
2. ✅ Use strong password hashing (BCrypt)
3. ✅ Implement proper token expiration
4. ✅ Validate all user inputs
5. ✅ Use HTTPS in production (configured HSTS)
6. ✅ Implement proper CORS policy
7. ✅ Set security headers
8. ✅ Use method-level security
9. ✅ Implement proper error handling
10. ✅ Limit session concurrency
11. ✅ Enable audit logging
12. ✅ Protect against CSRF attacks

## ⚠️ Important Notes

- **Development Only**: H2 console and default credentials are for development
- **Production**: Use environment variables for secrets (JWT secret, database credentials)
- **HTTPS**: Always use HTTPS in production
- **Secret Key**: Generate a strong random secret key for JWT signing
- **Database**: Replace H2 with a production database (PostgreSQL, MySQL)
- **Monitoring**: Configure proper logging and monitoring in production

## 🔐 Environment Variables for Production

```bash
export JWT_SECRET=your-base64-encoded-secret-key
export SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/yourdb
export SPRING_DATASOURCE_USERNAME=dbuser
export SPRING_DATASOURCE_PASSWORD=dbpassword
```

## 📖 Additional Resources

- [Spring Security Documentation](https://docs.spring.io/spring-security/reference/)
- [JWT.io](https://jwt.io/) - JWT debugger
- [OWASP Security Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)

## 🤝 Contributing

Feel free to fork this project and customize it for your needs. This is a demo application meant for learning purposes.

## 📝 License

This project is provided as-is for educational purposes.

## 🎯 Learning Objectives

After exploring this demo, you should understand:

1. How to implement JWT authentication in Spring Boot
2. How to configure Spring Security
3. How to implement role-based access control
4. How to use method-level security
5. How to configure security headers
6. How to handle CORS and CSRF
7. How to validate user inputs
8. How to structure a secure Spring Boot application

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in application.yml
server:
  port: 8081
```

### JWT Token Issues
- Check if secret is properly configured
- Verify token format (Bearer prefix)
- Check token expiration

### Database Connection Issues
- Verify H2 console configuration
- Check database URL in application.yml

### Access Denied Issues
- Verify JWT token is valid
- Check user role and permissions
- Review @PreAuthorize annotations

---

**Happy Learning! 🎓**

For questions or issues, please review the code comments and Spring Security documentation.
