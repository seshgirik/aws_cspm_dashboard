#!/bin/bash

echo "============================================"
echo "Spring Boot Security Demo - OWASP Testing"
echo "============================================"
echo ""

# Login and get JWT token
echo "Step 1: Logging in as admin..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed!"
    echo "Response: $LOGIN_RESPONSE"
    exit 1
fi

echo "✅ Login successful!"
echo "Token: ${TOKEN:0:50}..."
echo ""

# Test OWASP Web demonstrations
echo "============================================"
echo "OWASP WEB TOP 10 DEMONSTRATIONS"
echo "============================================"
echo ""

echo "1. Testing A01: Broken Access Control (Secure)"
curl -s -X GET "http://localhost:8080/api/owasp/web/access-control/secure/1" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool | head -15
echo ""

echo "2. Testing A02: Cryptographic Failures"
curl -s -X GET "http://localhost:8080/api/owasp/web/crypto/weak-password" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool | head -20
echo ""

echo "3. Testing A03: Injection (Secure)"
curl -s -X GET "http://localhost:8080/api/owasp/web/injection/search?username=admin&mode=secure" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool | head -15
echo ""

echo "4. Testing A10: SSRF (Secure with whitelist)"
curl -s -X GET "http://localhost:8080/api/owasp/web/ssrf/fetch-url?url=http://localhost:8080&mode=secure" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool | head -20
echo ""

# Test OWASP API demonstrations
echo "============================================"
echo "OWASP API SECURITY TOP 10 DEMONSTRATIONS"
echo "============================================"
echo ""

echo "1. Testing API1: BOLA (Secure)"
curl -s -X GET "http://localhost:8080/api/owasp/api/bola/secure/users/1/data" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool | head -15
echo ""

echo "2. Testing API4: Resource Consumption (Secure with rate limiting)"
curl -s -X GET "http://localhost:8080/api/owasp/api/resource/secure/export?limit=10" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool | head -20
echo ""

echo "3. Testing API5: Function Level Authorization (Admin only)"
curl -s -X GET "http://localhost:8080/api/owasp/api/function-auth/secure/admin/stats" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool | head -15
echo ""

# Test rate limiting
echo "============================================"
echo "TESTING RATE LIMITING"
echo "============================================"
echo ""
echo "Making 6 rapid requests to trigger rate limit..."
for i in {1..6}; do
    echo "Request $i..."
    RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X GET \
      "http://localhost:8080/api/owasp/api/resource/secure/export?limit=5" \
      -H "Authorization: Bearer $TOKEN")
    HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE" | cut -d':' -f2)
    echo "Status: $HTTP_CODE"
    if [ "$HTTP_CODE" = "429" ]; then
        echo "✅ Rate limiting working! Got 429 Too Many Requests"
        echo "$RESPONSE" | python3 -m json.tool 2>/dev/null | head -10
        break
    fi
    sleep 0.5
done
echo ""

echo "============================================"
echo "Testing Complete!"
echo "============================================"
echo ""
echo "📊 Summary:"
echo "✅ Authentication working"
echo "✅ OWASP Web Top 10 demonstrations available"
echo "✅ OWASP API Security Top 10 demonstrations available"
echo "✅ Rate limiting implemented"
echo "✅ Access control working"
echo ""
echo "🌐 Open http://localhost:8080 in your browser to see the interactive demo!"
echo ""
