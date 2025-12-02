#!/usr/bin/env python3
"""Analyze security findings and categorize for visual analysis"""

import json
from collections import Counter

def analyze_findings():
    with open('security_findings_all.json', 'r') as f:
        findings = json.load(f)
    
    categories = []
    titles = []
    severities = []
    
    for item in findings:
        finding = item['detail']['findings'][0]
        title = finding.get('Title', '')
        severity = finding.get('Severity', {}).get('Label', 'UNKNOWN')
        
        titles.append(title)
        severities.append(severity)
        
        # Categorize by keywords
        title_lower = title.lower()
        if 'encryption' in title_lower or 'kms' in title_lower:
            categories.append('Encryption & Key Management')
        elif 'public' in title_lower or 'internet' in title_lower or '0.0.0.0' in title:
            categories.append('Public Exposure')
        elif 'iam' in title_lower or 'permission' in title_lower or 'policy' in title_lower:
            categories.append('IAM & Access Control')
        elif 'cloudtrail' in title_lower or 'logging' in title_lower or 'audit' in title_lower:
            categories.append('Logging & Monitoring')
        elif 's3' in title_lower:
            categories.append('S3 Storage Security')
        elif 'rds' in title_lower or 'database' in title_lower:
            categories.append('Database Security')
        elif 'lambda' in title_lower:
            categories.append('Serverless Security')
        elif 'vpc' in title_lower or 'security group' in title_lower or 'network' in title_lower:
            categories.append('Network Security')
        elif 'llm' in title_lower or 'ai' in title_lower or 'bedrock' in title_lower or 'jailbreak' in title_lower:
            categories.append('AI/ML Security')
        elif 'dns' in title_lower or 'dga' in title_lower:
            categories.append('DNS Security')
        else:
            categories.append('Other')
    
    print(f"\n{'='*60}")
    print(f"SECURITY FINDINGS ANALYSIS")
    print(f"{'='*60}\n")
    
    print(f"Total Findings: {len(findings)}\n")
    
    print("SEVERITY DISTRIBUTION:")
    for sev, count in Counter(severities).most_common():
        print(f"  {sev:12s}: {count:3d} ({count/len(findings)*100:.1f}%)")
    
    print("\n\nTOP CATEGORIES:")
    for cat, count in Counter(categories).most_common():
        print(f"  {cat:30s}: {count:3d} ({count/len(findings)*100:.1f}%)")
    
    print("\n\nTOP 20 MOST COMMON ISSUES:")
    for i, (title, count) in enumerate(Counter(titles).most_common(20), 1):
        print(f"  {i:2d}. [{count:2d}x] {title[:80]}")
    
    # Get unique titles for visual analysis
    unique_titles = list(set(titles))
    
    print(f"\n\nUNIQUE FINDING TYPES: {len(unique_titles)}")
    
    # Recommend top issues for visual analysis
    print(f"\n{'='*60}")
    print("RECOMMENDED FOR VISUAL ANALYSIS (High Impact):")
    print(f"{'='*60}\n")
    
    priority_keywords = [
        ('Public Exposure', ['public', '0.0.0.0', 'internet']),
        ('Encryption', ['encryption', 'kms', 'encrypted']),
        ('IAM Overprivileges', ['iam', 'policy', 'privileges', 'permission']),
        ('Logging Gaps', ['cloudtrail', 'logging', 'audit']),
        ('Database Security', ['rds', 'database', 'sql']),
        ('Network Security', ['security group', 'vpc', 'network']),
        ('AI/ML Security', ['llm', 'jailbreak', 'bedrock', 'guardrail']),
        ('S3 Security', ['s3 bucket', 's3 object'])
    ]
    
    for category, keywords in priority_keywords:
        matching = [t for t in unique_titles if any(kw in t.lower() for kw in keywords)]
        if matching:
            print(f"\n{category}:")
            for title in matching[:3]:
                print(f"  • {title}")

if __name__ == '__main__':
    analyze_findings()
