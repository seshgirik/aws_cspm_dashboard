#!/bin/bash
# Upload generated findings to S3 bucket created by CloudFormation template
# Usage: ./upload_to_s3.sh <bucket-name>

if [ -z "$1" ]; then
    echo "Usage: $0 <bucket-name>"
    echo "Example: $0 securityhubfindingsbucket-abc123"
    exit 1
fi

BUCKET_NAME=$1

echo "🚀 Uploading security findings to S3..."
echo "Bucket: $BUCKET_NAME"
echo ""

# Upload the date-organized findings
echo "📂 Uploading date-organized findings..."
aws s3 sync findings_by_date/ s3://$BUCKET_NAME/raw/firehose/ \
    --exclude "*.DS_Store" \
    --content-type "application/json"

if [ $? -eq 0 ]; then
    echo "✅ Upload complete!"
    echo ""
    echo "📊 You can now query the findings in Athena using:"
    echo "   SELECT * FROM SecurityHub.securityhubfindingsview"
    echo "   WHERE Severity = 'CRITICAL'"
    echo "   ORDER BY CreatedAt DESC;"
else
    echo "❌ Upload failed!"
    exit 1
fi
