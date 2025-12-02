#!/usr/bin/env python3
"""
AWS Security Findings Sample Data Generator
Generates realistic sample data for various AWS security issues
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
import uuid

class AWSSecurityDataGenerator:
    """Generate sample AWS security findings data"""
    
    def __init__(self):
        self.account_ids = ["123456789012", "987654321098", "456789012345"]
        self.regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]
        
        # Define various security issue types
        self.security_issues = {
            "S3": [
                {
                    "title": "S3 bucket does not have server-side encryption enabled",
                    "description": "The S3 bucket does not have server-side encryption enabled. Data at rest should be encrypted to protect sensitive information.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/S3.4",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "S3 bucket does not have public access blocks configured",
                    "description": "The S3 bucket does not have public access block settings enabled. This could allow unintended public access to bucket contents.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/S3.8",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "S3 bucket versioning is not enabled",
                    "description": "S3 bucket versioning should be enabled to help recover from both unintended user actions and application failures.",
                    "severity": "LOW",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/S3.15",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "S3 bucket allows public READ access",
                    "description": "The S3 bucket policy allows public read access to the bucket contents. This is a critical security risk.",
                    "severity": "CRITICAL",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/S3.2",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                }
            ],
            "EC2": [
                {
                    "title": "EC2 instance is not managed by Systems Manager",
                    "description": "EC2 instances should be managed by AWS Systems Manager to provide visibility and control.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/SSM.1",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "Security group allows unrestricted SSH access (0.0.0.0/0)",
                    "description": "The security group allows SSH access from 0.0.0.0/0. This is a significant security risk and should be restricted.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/EC2.13",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "EC2 instance has public IP address",
                    "description": "EC2 instances should not have a public IPv4 address associated. Use VPC endpoints or NAT gateways instead.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/EC2.9",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "EBS volumes are not encrypted",
                    "description": "Attached EBS volumes should be encrypted at rest for data protection.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/EC2.7",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "Security group allows unrestricted RDP access (0.0.0.0/0)",
                    "description": "The security group allows RDP access from 0.0.0.0/0 on port 3389.",
                    "severity": "CRITICAL",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/EC2.19",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                }
            ],
            "IAM": [
                {
                    "title": "IAM root account access keys exist",
                    "description": "Root account access keys should not exist. Remove access keys and use IAM users instead.",
                    "severity": "CRITICAL",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/IAM.4",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "IAM password policy does not meet recommended configuration",
                    "description": "The IAM password policy should require minimum length, complexity, and rotation.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/IAM.15",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "IAM user has not used credentials for 90 days",
                    "description": "IAM users with unused credentials for 90 days or more should be removed or deactivated.",
                    "severity": "LOW",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/IAM.22",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "IAM policy allows full administrative privileges",
                    "description": "IAM policy grants full administrative privileges (*:*). Follow principle of least privilege.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/IAM.1",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "MFA is not enabled for IAM user with console password",
                    "description": "Multi-factor authentication (MFA) should be enabled for all IAM users that have a console password.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/IAM.5",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                }
            ],
            "RDS": [
                {
                    "title": "RDS DB instance is not encrypted",
                    "description": "RDS DB instances should have encryption at rest enabled for data protection.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/RDS.3",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "RDS DB instance has public accessibility enabled",
                    "description": "RDS instances should not be publicly accessible to minimize security risks.",
                    "severity": "CRITICAL",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/RDS.2",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "RDS DB instance automated backups are not enabled",
                    "description": "Automated backups should be enabled for RDS instances to ensure data recovery.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/RDS.1",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                }
            ],
            "CloudTrail": [
                {
                    "title": "CloudTrail trail is not enabled in all regions",
                    "description": "CloudTrail should be enabled in all regions to ensure complete API activity logging.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/CloudTrail.1",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "CloudTrail log file validation is not enabled",
                    "description": "CloudTrail log file validation should be enabled to verify log integrity.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/CloudTrail.4",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                }
            ],
            "Lambda": [
                {
                    "title": "Lambda function is not configured with a dead-letter queue",
                    "description": "Lambda functions should be configured with a dead-letter queue for failed invocations.",
                    "severity": "LOW",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/Lambda.1",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "Lambda function is not in a VPC",
                    "description": "Lambda functions should run within a VPC to access private resources securely.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/Lambda.2",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                }
            ],
            "GuardDuty": [
                {
                    "title": "EC2 instance is communicating with known malicious IP",
                    "description": "GuardDuty detected EC2 instance communicating with a known malicious IP address.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/guardduty",
                    "types": ["TTPs/Command and Control/Backdoor:EC2-C&CActivity.B!DNS"]
                },
                {
                    "title": "Unusual API call detected",
                    "description": "GuardDuty detected an unusual API call pattern that deviates from baseline behavior.",
                    "severity": "MEDIUM",
                    "compliance": "WARNING",
                    "generator_id": "aws/guardduty",
                    "types": ["TTPs/Discovery/Recon:IAMUser-UnusualBehavior"]
                },
                {
                    "title": "Possible cryptocurrency mining activity detected",
                    "description": "EC2 instance is querying a domain associated with cryptocurrency mining.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/guardduty",
                    "types": ["TTPs/Impact/CryptoCurrency:EC2-BitcoinTool.B!DNS"]
                }
            ],
            "KMS": [
                {
                    "title": "KMS key rotation is not enabled",
                    "description": "KMS customer-managed keys should have automatic key rotation enabled.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/KMS.4",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                }
            ],
            "ELB": [
                {
                    "title": "Application Load Balancer is not configured to drop invalid headers",
                    "description": "ALB should be configured to drop HTTP headers with invalid header fields.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/ELB.13",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                },
                {
                    "title": "Classic Load Balancer does not have connection draining enabled",
                    "description": "Classic Load Balancers should have connection draining enabled.",
                    "severity": "LOW",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws-foundational-security-best-practices/v/1.0.0/ELB.5",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"]
                }
            ],
            "Inspector": [
                {
                    "title": "EC2 instance has critical CVE vulnerabilities",
                    "description": "Inspector found 3 critical CVE vulnerabilities (CVE-2024-1234, CVE-2024-5678) on EC2 instance. Immediate patching required.",
                    "severity": "CRITICAL",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/inspector",
                    "types": ["Software and Configuration Checks/Vulnerabilities/CVE"]
                },
                {
                    "title": "Lambda function has outdated runtime with known vulnerabilities",
                    "description": "Inspector detected Lambda function using Python 3.7 runtime which has reached end of support and contains known security vulnerabilities.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/inspector",
                    "types": ["Software and Configuration Checks/Vulnerabilities/Runtime"]
                },
                {
                    "title": "ECR image contains high severity vulnerabilities",
                    "description": "Container image in ECR has 12 high severity and 5 critical vulnerabilities in base packages.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/inspector",
                    "types": ["Software and Configuration Checks/Vulnerabilities/Container"]
                },
                {
                    "title": "Network path allows exposure to internet",
                    "description": "Inspector network reachability analysis found EC2 instance with unnecessary internet exposure through security group configuration.",
                    "severity": "MEDIUM",
                    "compliance": "WARNING",
                    "generator_id": "aws/inspector",
                    "types": ["Software and Configuration Checks/Network Reachability"]
                }
            ],
            "Macie": [
                {
                    "title": "S3 bucket contains unencrypted PII data",
                    "description": "Macie discovered 1,247 objects containing unencrypted personally identifiable information (PII) including credit card numbers, SSNs, and email addresses.",
                    "severity": "CRITICAL",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/macie",
                    "types": ["Sensitive Data Identifications/PII/Credentials"]
                },
                {
                    "title": "S3 bucket contains sensitive financial data",
                    "description": "Macie detected 342 files containing financial data including bank account numbers and credit card information without proper access controls.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/macie",
                    "types": ["Sensitive Data Identifications/Financial"]
                },
                {
                    "title": "S3 bucket exposed with sensitive API credentials",
                    "description": "Macie found AWS access keys, API tokens, and private keys in publicly readable S3 objects.",
                    "severity": "CRITICAL",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/macie",
                    "types": ["Sensitive Data Identifications/Credentials"]
                },
                {
                    "title": "S3 bucket contains PHI/healthcare data",
                    "description": "Macie identified protected health information (PHI) in S3 bucket without proper HIPAA controls.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/macie",
                    "types": ["Sensitive Data Identifications/PII/Healthcare"]
                }
            ],
            "AccessAnalyzer": [
                {
                    "title": "S3 bucket allows public access from internet",
                    "description": "IAM Access Analyzer detected S3 bucket policy allowing anonymous public access from any AWS account or internet user.",
                    "severity": "CRITICAL",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/access-analyzer",
                    "types": ["Effects/Data Exposure/Access Analyzer"]
                },
                {
                    "title": "IAM role allows cross-account access from external account",
                    "description": "Access Analyzer found IAM role trust policy allowing assume role from external AWS account 999888777666.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/access-analyzer",
                    "types": ["Effects/Data Exposure/Access Analyzer"]
                },
                {
                    "title": "Lambda function has public resource-based policy",
                    "description": "Lambda function resource policy allows invocation from public principal (*), enabling unauthorized execution.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/access-analyzer",
                    "types": ["Effects/Data Exposure/Access Analyzer"]
                },
                {
                    "title": "KMS key allows external account access",
                    "description": "KMS key policy grants decrypt and encrypt permissions to external AWS account, potential data exfiltration risk.",
                    "severity": "MEDIUM",
                    "compliance": "WARNING",
                    "generator_id": "aws/access-analyzer",
                    "types": ["Effects/Data Exposure/Access Analyzer"]
                }
            ],
            "VPCFlowLogs": [
                {
                    "title": "Unusual outbound traffic to suspicious IP address",
                    "description": "VPC Flow Logs analysis detected abnormal outbound traffic pattern to known malicious IP 203.0.113.45 from private subnet.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/vpc-flow-logs",
                    "types": ["TTPs/Command and Control/Network Traffic"]
                },
                {
                    "title": "High volume of rejected connection attempts",
                    "description": "VPC Flow Logs show 15,000+ rejected connection attempts to port 22 from multiple source IPs, indicating potential SSH brute force attack.",
                    "severity": "MEDIUM",
                    "compliance": "WARNING",
                    "generator_id": "aws/vpc-flow-logs",
                    "types": ["TTPs/Initial Access/Brute Force"]
                },
                {
                    "title": "Data transfer to unexpected geographic location",
                    "description": "Detected large data transfer (50GB) to IP addresses in restricted geographic region not matching normal traffic patterns.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/vpc-flow-logs",
                    "types": ["Effects/Data Exfiltration"]
                },
                {
                    "title": "Port scanning activity detected",
                    "description": "VPC Flow Logs indicate systematic port scanning from instance attempting connections to multiple ports across subnet range.",
                    "severity": "MEDIUM",
                    "compliance": "WARNING",
                    "generator_id": "aws/vpc-flow-logs",
                    "types": ["TTPs/Discovery/Network Service Scanning"]
                }
            ],
            "WAF": [
                {
                    "title": "WAF detected SQL injection attack attempts",
                    "description": "AWS WAF blocked 234 SQL injection attempts targeting application endpoint /api/users in the last hour.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/waf",
                    "types": ["TTPs/Initial Access/Exploit Public-Facing Application"]
                },
                {
                    "title": "WAF detected XSS attack patterns",
                    "description": "Cross-site scripting (XSS) attack patterns detected in request parameters, 89 requests blocked by WAF rules.",
                    "severity": "MEDIUM",
                    "compliance": "WARNING",
                    "generator_id": "aws/waf",
                    "types": ["TTPs/Initial Access/Exploit Public-Facing Application"]
                },
                {
                    "title": "DDoS attack mitigated by AWS Shield",
                    "description": "AWS Shield detected and mitigated volumetric DDoS attack with peak of 2.3 Tbps targeting ALB endpoint.",
                    "severity": "CRITICAL",
                    "compliance": "WARNING",
                    "generator_id": "aws/shield",
                    "types": ["TTPs/Impact/Network Denial of Service"]
                },
                {
                    "title": "WAF rule violations exceeding threshold",
                    "description": "Rate limiting rule exceeded with 5,000 requests from single IP in 5 minutes, potential credential stuffing attack.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/waf",
                    "types": ["TTPs/Credential Access/Brute Force"]
                }
            ],
            "Route53": [
                {
                    "title": "DNS queries to known malicious domains",
                    "description": "Route53 DNS logs show queries to 15 domains associated with malware C2 infrastructure from EC2 instances in production VPC.",
                    "severity": "CRITICAL",
                    "compliance": "WARNING",
                    "generator_id": "aws/route53",
                    "types": ["TTPs/Command and Control/Application Layer Protocol"]
                },
                {
                    "title": "DNS tunneling activity detected",
                    "description": "Abnormal DNS query patterns suggest data exfiltration via DNS tunneling with unusually long TXT record queries.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/route53",
                    "types": ["TTPs/Exfiltration/Exfiltration Over Alternative Protocol"]
                },
                {
                    "title": "High volume DNS queries indicating DGA activity",
                    "description": "Route53 logs show domain generation algorithm (DGA) patterns with rapid queries to non-existent random domains.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/route53",
                    "types": ["TTPs/Command and Control/Dynamic Resolution"]
                },
                {
                    "title": "DNS queries to newly registered domains",
                    "description": "Multiple DNS queries to domains registered within last 24 hours, common indicator of phishing or malware infrastructure.",
                    "severity": "MEDIUM",
                    "compliance": "WARNING",
                    "generator_id": "aws/route53",
                    "types": ["TTPs/Initial Access/Phishing"]
                }
            ],
            "Config": [
                {
                    "title": "Resource configuration drift detected",
                    "description": "AWS Config detected configuration drift on 12 resources that deviate from approved baseline configuration.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/config",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards"]
                },
                {
                    "title": "Non-compliant resource detected by Config rule",
                    "description": "Security group allows inbound traffic on prohibited port 23 (Telnet), violating organization security policy.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/config",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards"]
                },
                {
                    "title": "Unapproved resource changes detected",
                    "description": "AWS Config recorded unauthorized modifications to production S3 bucket policy outside change management window.",
                    "severity": "HIGH",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/config",
                    "types": ["Software and Configuration Checks/Change Management"]
                },
                {
                    "title": "Required tags missing on resources",
                    "description": "Config compliance check found 47 EC2 instances missing required tags (Environment, Owner, CostCenter) for governance.",
                    "severity": "LOW",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/config",
                    "types": ["Software and Configuration Checks/Industry and Regulatory Standards"]
                }
            ],
            "CloudTrail-Events": [
                {
                    "title": "Unauthorized API calls from unusual location",
                    "description": "CloudTrail logs show API calls (DescribeInstances, DescribeSecurityGroups) from IP address in restricted country not matching user baseline.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/cloudtrail",
                    "types": ["TTPs/Discovery/Cloud Service Discovery"]
                },
                {
                    "title": "IAM policy changes by unauthorized user",
                    "description": "CloudTrail detected IAM policy modification (PutUserPolicy) by user account without administrative privileges.",
                    "severity": "CRITICAL",
                    "compliance": "WARNING",
                    "generator_id": "aws/cloudtrail",
                    "types": ["TTPs/Privilege Escalation/Valid Accounts"]
                },
                {
                    "title": "Disabled CloudTrail logging detected",
                    "description": "CloudTrail event shows StopLogging API call, attempt to disable audit logging and evade detection.",
                    "severity": "CRITICAL",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/cloudtrail",
                    "types": ["TTPs/Defense Evasion/Impair Defenses"]
                },
                {
                    "title": "Suspicious console login from new device",
                    "description": "CloudTrail ConsoleLogin event from unrecognized device and location for privileged IAM user without MFA.",
                    "severity": "HIGH",
                    "compliance": "WARNING",
                    "generator_id": "aws/cloudtrail",
                    "types": ["TTPs/Initial Access/Valid Accounts"]
                },
                {
                    "title": "Root account activity detected",
                    "description": "CloudTrail recorded root account usage for routine operations, violating security best practices.",
                    "severity": "MEDIUM",
                    "compliance": "NON_COMPLIANT",
                    "generator_id": "aws/cloudtrail",
                    "types": ["Software and Configuration Checks/Best Practices"]
                }
            ]
        }
    
    def generate_resource_id(self, resource_type: str) -> str:
        """Generate a realistic resource ID based on type"""
        resource_patterns = {
            "AwsS3Bucket": lambda: f"arn:aws:s3:::{random.choice(['prod', 'dev', 'staging'])}-{random.choice(['data', 'logs', 'backups', 'uploads'])}-bucket-{random.randint(1000, 9999)}",
            "AwsEc2Instance": lambda: f"arn:aws:ec2:{random.choice(self.regions)}:{random.choice(self.account_ids)}:instance/i-{uuid.uuid4().hex[:17]}",
            "AwsEc2SecurityGroup": lambda: f"arn:aws:ec2:{random.choice(self.regions)}:{random.choice(self.account_ids)}:security-group/sg-{uuid.uuid4().hex[:17]}",
            "AwsEc2Volume": lambda: f"arn:aws:ec2:{random.choice(self.regions)}:{random.choice(self.account_ids)}:volume/vol-{uuid.uuid4().hex[:17]}",
            "AwsIamUser": lambda: f"arn:aws:iam::{random.choice(self.account_ids)}:user/{random.choice(['admin', 'developer', 'analyst', 'service'])}-user-{random.randint(1, 100)}",
            "AwsIamPolicy": lambda: f"arn:aws:iam::{random.choice(self.account_ids)}:policy/{random.choice(['Admin', 'PowerUser', 'ReadOnly', 'Custom'])}-Policy",
            "AwsRdsDbInstance": lambda: f"arn:aws:rds:{random.choice(self.regions)}:{random.choice(self.account_ids)}:db:{random.choice(['prod', 'dev'])}-{random.choice(['mysql', 'postgres', 'oracle'])}-{random.randint(1, 50)}",
            "AwsLambdaFunction": lambda: f"arn:aws:lambda:{random.choice(self.regions)}:{random.choice(self.account_ids)}:function:{random.choice(['process', 'transform', 'notify', 'validate'])}-{random.choice(['data', 'events', 'logs'])}-function",
            "AwsKmsKey": lambda: f"arn:aws:kms:{random.choice(self.regions)}:{random.choice(self.account_ids)}:key/{uuid.uuid4()}",
            "AwsElbLoadBalancer": lambda: f"arn:aws:elasticloadbalancing:{random.choice(self.regions)}:{random.choice(self.account_ids)}:loadbalancer/{random.choice(['app', 'net'])}/{random.choice(['prod', 'dev'])}-lb-{random.randint(1, 100)}",
            "AwsCloudTrailTrail": lambda: f"arn:aws:cloudtrail:{random.choice(self.regions)}:{random.choice(self.account_ids)}:trail/{random.choice(['organization', 'account'])}-trail"
        }
        
        return resource_patterns.get(resource_type, lambda: f"arn:aws:::resource-{uuid.uuid4().hex[:12]}")()
    
    def get_resource_type_for_service(self, service: str) -> str:
        """Map service to resource type"""
        resource_type_map = {
            "S3": "AwsS3Bucket",
            "EC2": random.choice(["AwsEc2Instance", "AwsEc2SecurityGroup", "AwsEc2Volume"]),
            "IAM": random.choice(["AwsIamUser", "AwsIamPolicy"]),
            "RDS": "AwsRdsDbInstance",
            "CloudTrail": "AwsCloudTrailTrail",
            "Lambda": "AwsLambdaFunction",
            "GuardDuty": "AwsEc2Instance",
            "KMS": "AwsKmsKey",
            "ELB": "AwsElbLoadBalancer",
            "Inspector": random.choice(["AwsEc2Instance", "AwsLambdaFunction"]),
            "Macie": "AwsS3Bucket",
            "AccessAnalyzer": random.choice(["AwsS3Bucket", "AwsIamUser", "AwsLambdaFunction", "AwsKmsKey"]),
            "VPCFlowLogs": "AwsEc2Instance",
            "WAF": "AwsElbLoadBalancer",
            "Route53": "AwsEc2Instance",
            "Config": random.choice(["AwsEc2SecurityGroup", "AwsS3Bucket", "AwsEc2Instance"]),
            "CloudTrail-Events": "AwsIamUser"
        }
        return resource_type_map.get(service, "AwsAccount")
    
    def generate_finding(self, service: str, issue: Dict) -> Dict:
        """Generate a single security finding"""
        now = datetime.utcnow()
        created_at = now - timedelta(days=random.randint(1, 30))
        updated_at = created_at + timedelta(hours=random.randint(1, 48))
        
        resource_type = self.get_resource_type_for_service(service)
        resource_id = self.generate_resource_id(resource_type)
        
        finding = {
            "id": str(uuid.uuid4()),
            "detail": {
                "findings": [
                    {
                        "AwsAccountId": random.choice(self.account_ids),
                        "CreatedAt": created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "UpdatedAt": updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "Description": issue["description"],
                        "ProductArn": f"arn:aws:securityhub:{random.choice(self.regions)}::product/aws/securityhub",
                        "GeneratorId": issue["generator_id"],
                        "Region": random.choice(self.regions),
                        "Compliance": {
                            "status": issue["compliance"]
                        },
                        "Workflow": {
                            "status": random.choice(["NEW", "NOTIFIED", "SUPPRESSED"])
                        },
                        "Types": issue["types"],
                        "Title": issue["title"],
                        "Severity": {
                            "Label": issue["severity"]
                        },
                        "Resources": [
                            {
                                "Id": resource_id,
                                "Type": resource_type
                            }
                        ]
                    }
                ]
            }
        }
        
        return finding
    
    def generate_all_findings(self, count_per_service: int = 5) -> List[Dict]:
        """Generate findings for all services"""
        all_findings = []
        
        for service, issues in self.security_issues.items():
            # Generate multiple findings for each service
            for _ in range(count_per_service):
                issue = random.choice(issues)
                finding = self.generate_finding(service, issue)
                all_findings.append(finding)
        
        return all_findings
    
    def save_findings(self, findings: List[Dict], output_file: str = "security_findings.json"):
        """Save findings to a JSON file"""
        with open(output_file, 'w') as f:
            json.dump(findings, f, indent=2)
        print(f"✅ Generated {len(findings)} security findings")
        print(f"📁 Saved to: {output_file}")
    
    def save_findings_by_date(self, findings: List[Dict], output_dir: str = "findings_by_date"):
        """Save findings organized by date (matching the S3 structure)"""
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Group findings by date
        findings_by_date = {}
        for finding in findings:
            created_at = finding["detail"]["findings"][0]["CreatedAt"]
            date_str = created_at.split("T")[0].replace("-", "/")
            
            if date_str not in findings_by_date:
                findings_by_date[date_str] = []
            findings_by_date[date_str].append(finding)
        
        # Save each date's findings
        for date_str, date_findings in findings_by_date.items():
            date_dir = os.path.join(output_dir, date_str)
            os.makedirs(date_dir, exist_ok=True)
            
            output_file = os.path.join(date_dir, f"findings_{date_str.replace('/', '_')}.json")
            with open(output_file, 'w') as f:
                for finding in date_findings:
                    f.write(json.dumps(finding) + '\n')
        
        print(f"📂 Organized {len(findings)} findings into {len(findings_by_date)} date directories")
        print(f"📁 Saved to: {output_dir}/")
    
    def generate_summary_report(self, findings: List[Dict]) -> Dict:
        """Generate a summary report of findings"""
        summary = {
            "total_findings": len(findings),
            "by_severity": {},
            "by_service": {},
            "by_compliance_status": {},
            "by_region": {},
            "by_account": {}
        }
        
        for finding in findings:
            detail = finding["detail"]["findings"][0]
            
            # Count by severity
            severity = detail["Severity"]["Label"]
            summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
            
            # Count by service (extract from generator ID)
            generator_id = detail["GeneratorId"]
            service = generator_id.split("/")[-1].split(".")[0] if "/" in generator_id else "GuardDuty"
            summary["by_service"][service] = summary["by_service"].get(service, 0) + 1
            
            # Count by compliance status
            compliance = detail["Compliance"]["status"]
            summary["by_compliance_status"][compliance] = summary["by_compliance_status"].get(compliance, 0) + 1
            
            # Count by region
            region = detail["Region"]
            summary["by_region"][region] = summary["by_region"].get(region, 0) + 1
            
            # Count by account
            account = detail["AwsAccountId"]
            summary["by_account"][account] = summary["by_account"].get(account, 0) + 1
        
        return summary
    
    def save_summary(self, summary: Dict, output_file: str = "findings_summary.json"):
        """Save summary report"""
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📊 SUMMARY REPORT")
        print(f"=" * 50)
        print(f"Total Findings: {summary['total_findings']}")
        print(f"\n🔴 By Severity:")
        for severity, count in sorted(summary['by_severity'].items()):
            print(f"  {severity}: {count}")
        print(f"\n☁️  By Service:")
        for service, count in sorted(summary['by_service'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {service}: {count}")
        print(f"\n✅ By Compliance Status:")
        for status, count in summary['by_compliance_status'].items():
            print(f"  {status}: {count}")
        print(f"\n🌍 By Region:")
        for region, count in summary['by_region'].items():
            print(f"  {region}: {count}")
        print(f"\n📝 Saved summary to: {output_file}")


def main():
    """Main function to generate sample AWS security findings"""
    print("🔐 AWS Security Findings Sample Data Generator")
    print("=" * 50)
    
    generator = AWSSecurityDataGenerator()
    
    # Generate findings (5 per service by default)
    findings = generator.generate_all_findings(count_per_service=5)
    
    # Save all findings to a single file
    generator.save_findings(findings, "security_findings_all.json")
    
    # Save findings organized by date (for S3/Athena compatibility)
    generator.save_findings_by_date(findings, "findings_by_date")
    
    # Generate and save summary report
    summary = generator.generate_summary_report(findings)
    generator.save_summary(summary, "findings_summary.json")
    
    print(f"\n✨ Generation complete!")
    print(f"📦 Files generated:")
    print(f"   - security_findings_all.json (all findings)")
    print(f"   - findings_by_date/ (organized by date)")
    print(f"   - findings_summary.json (summary report)")


if __name__ == "__main__":
    main()
