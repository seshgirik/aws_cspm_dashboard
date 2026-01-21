package com.security.demo.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.security.Key;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;
import java.util.Base64;

@Component
public class JwtTokenProvider {

    private static final Logger logger = LoggerFactory.getLogger(JwtTokenProvider.class);

    @Value("${jwt.secret}")
    private String jwtSecret;

    @Value("${jwt.expiration}")
    private long jwtExpirationMs;

    /**
     * Generate JWT token from UserDetails
     */
    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        return createToken(claims, userDetails.getUsername());
    }

    /**
     * Generate token with custom claims
     */
    public String generateToken(Map<String, Object> extraClaims, UserDetails userDetails) {
        return createToken(extraClaims, userDetails.getUsername());
    }

    /**
     * Create JWT token
     */
    private String createToken(Map<String, Object> claims, String subject) {
        return Jwts.builder()
                .setClaims(claims)
                .setSubject(subject)
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + jwtExpirationMs))
                .signWith(getSignInKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    /**
     * Extract username from token
     */
    public String extractUsername(String token) {
        logger.info("========================================");
        logger.info("STEP 1: EXTRACTING USERNAME FROM TOKEN");
        logger.info("========================================");
        logger.info("Token (first 50 chars): {}", token.substring(0, Math.min(50, token.length())) + "...");
        
        String username = extractClaim(token, Claims::getSubject);
        
        logger.info("✓ Username extracted successfully: {}", username);
        logger.info("");
        return username;
    }

    /**
     * Extract expiration date from token
     */
    public Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }

    /**
     * Extract specific claim from token
     */
    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    /**
     * Extract all claims from token
     */
    private Claims extractAllClaims(String token) {
        logger.info("========================================");
        logger.info("STEP 2: EXTRACTING ALL CLAIMS FROM TOKEN");
        logger.info("========================================");
        
        // Split token into parts
        String[] tokenParts = token.split("\\.");
        logger.info("Token Structure:");
        logger.info("  - Parts count: {}", tokenParts.length);
        
        if (tokenParts.length == 3) {
            // Decode header
            try {
                String header = new String(Base64.getUrlDecoder().decode(tokenParts[0]));
                logger.info("  - Header: {}", header);
            } catch (Exception e) {
                logger.warn("  - Could not decode header: {}", e.getMessage());
            }
            
            // Decode payload
            try {
                String payload = new String(Base64.getUrlDecoder().decode(tokenParts[1]));
                logger.info("  - Payload: {}", payload);
            } catch (Exception e) {
                logger.warn("  - Could not decode payload: {}", e.getMessage());
            }
            
            logger.info("  - Signature (first 20 chars): {}", tokenParts[2].substring(0, Math.min(20, tokenParts[2].length())) + "...");
        }
        
        logger.info("");
        logger.info("========================================");
        logger.info("STEP 3: GETTING SIGNING KEY");
        logger.info("========================================");
        Key signingKey = getSignInKey();
        logger.info("✓ Signing key retrieved successfully");
        logger.info("  - Algorithm: HMAC-SHA256");
        logger.info("  - Key format: {}", signingKey.getFormat());
        logger.info("");
        
        logger.info("========================================");
        logger.info("STEP 4: VERIFYING TOKEN SIGNATURE");
        logger.info("========================================");
        logger.info("Process:");
        logger.info("  1. Parsing JWT token...");
        logger.info("  2. Verifying signature with secret key...");
        logger.info("  3. Extracting claims from validated token...");
        
        try {
            Claims claims = Jwts.parser()
                    .verifyWith((javax.crypto.SecretKey) signingKey)
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();
            
            logger.info("✓ SIGNATURE VERIFICATION SUCCESSFUL!");
            logger.info("");
            logger.info("========================================");
            logger.info("STEP 5: EXTRACTED CLAIMS DETAILS");
            logger.info("========================================");
            logger.info("Claims found in token:");
            logger.info("  - Subject (username): {}", claims.getSubject());
            logger.info("  - Issued At: {}", claims.getIssuedAt());
            logger.info("  - Expiration: {}", claims.getExpiration());
            logger.info("  - Time until expiration: {} ms", claims.getExpiration().getTime() - System.currentTimeMillis());
            
            // Print all claims
            logger.info("  - All claims: {}", claims);
            logger.info("");
            
            return claims;
            
        } catch (io.jsonwebtoken.security.SignatureException e) {
            logger.error("✗ SIGNATURE VERIFICATION FAILED!");
            logger.error("  - Reason: Invalid signature - token may have been tampered with");
            logger.error("  - Error: {}", e.getMessage());
            throw e;
        } catch (io.jsonwebtoken.ExpiredJwtException e) {
            logger.error("✗ TOKEN EXPIRED!");
            logger.error("  - Token expired at: {}", e.getClaims().getExpiration());
            logger.error("  - Current time: {}", new Date());
            throw e;
        } catch (io.jsonwebtoken.MalformedJwtException e) {
            logger.error("✗ MALFORMED TOKEN!");
            logger.error("  - Reason: Invalid JWT token format");
            logger.error("  - Error: {}", e.getMessage());
            throw e;
        } catch (Exception e) {
            logger.error("✗ TOKEN VALIDATION FAILED!");
            logger.error("  - Error: {}", e.getMessage());
            throw e;
        }
    }

    /**
     * Check if token is expired
     */
    private Boolean isTokenExpired(String token) {
        Date expiration = extractExpiration(token);
        boolean expired = expiration.before(new Date());
        
        logger.info("========================================");
        logger.info("STEP 6: CHECKING TOKEN EXPIRATION");
        logger.info("========================================");
        logger.info("  - Token expiration: {}", expiration);
        logger.info("  - Current time: {}", new Date());
        logger.info("  - Is expired: {}", expired);
        logger.info("");
        
        return expired;
    }

    /**
     * Validate token against UserDetails
     */
    public Boolean validateToken(String token, UserDetails userDetails) {
        logger.info("========================================");
        logger.info("STARTING JWT TOKEN VALIDATION");
        logger.info("========================================");
        logger.info("Validating token for user: {}", userDetails.getUsername());
        logger.info("");
        
        final String username = extractUsername(token);
        
        boolean usernameMatches = username.equals(userDetails.getUsername());
        boolean notExpired = !isTokenExpired(token);
        
        logger.info("========================================");
        logger.info("STEP 7: FINAL VALIDATION CHECKS");
        logger.info("========================================");
        logger.info("Validation Results:");
        logger.info("  - Username from token: {}", username);
        logger.info("  - Username from UserDetails: {}", userDetails.getUsername());
        logger.info("  - Username matches: {}", usernameMatches);
        logger.info("  - Token not expired: {}", notExpired);
        logger.info("");
        
        boolean isValid = usernameMatches && notExpired;
        
        logger.info("========================================");
        logger.info("VALIDATION RESULT: {}", isValid ? "✓ VALID" : "✗ INVALID");
        logger.info("========================================");
        logger.info("");
        
        return isValid;
    }

    /**
     * Get signing key from secret
     */
    private Key getSignInKey() {
        logger.info("  - Secret (Base64, first 20 chars): {}...", jwtSecret.substring(0, Math.min(20, jwtSecret.length())));
        logger.info("  - Secret length: {} characters", jwtSecret.length());
        
        byte[] keyBytes = Decoders.BASE64.decode(jwtSecret);
        logger.info("  - Decoded key bytes length: {} bytes", keyBytes.length);
        logger.info("  - Required minimum for HS256: 256 bits (32 bytes)");
        
        if (keyBytes.length < 32) {
            logger.warn("  ⚠ WARNING: Key is shorter than recommended 256 bits!");
        }
        
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
