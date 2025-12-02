# AWS VPC Security - Cybersecurity Architect Interview Questions

**Comprehensive collection of AWS VPC security interview questions with detailed answers, code examples, and architecture patterns for cybersecurity architect roles.**

---

## Table of Contents

1. [VPC Security Layers - Defense in Depth](#vpc-security-layers---defense-in-depth)
2. [Security Groups vs. Network ACLs](#security-groups-vs-network-acls)
3. [VPC Peering vs. Transit Gateway vs. PrivateLink](#vpc-peering-vs-transit-gateway-vs-privatelink)
4. [VPC Flow Logs Analysis](#vpc-flow-logs-analysis)
5. [AWS Network Firewall](#aws-network-firewall)
6. [VPC Endpoint Policies for S3](#vpc-endpoint-policies-for-s3)
7. [PrivateLink for Cross-Account Access](#privatelink-for-cross-account-access)
8. [IPv6 Security](#ipv6-security)
9. [VPC Sharing with AWS RAM](#vpc-sharing-with-aws-ram)
10. [VPC Reachability Analyzer](#vpc-reachability-analyzer)
11. [Summary & Key Takeaways](#summary--key-takeaways)

---

# VPC Security Layers - Defense in Depth

## Question 1: Multi-Layer Security Architecture

**Scenario:**
Your company runs a 3-tier web application in AWS:
- **Public Subnet:** Application Load Balancer (ALB)
- **Private Subnet 1:** Web servers (EC2 instances)
- **Private Subnet 2:** Database servers (RDS)

Security team mandates: "Implement defense in depth - multiple security layers at network, subnet, and instance level."

**Question:** What's the complete security architecture?

**Options:**
- A) Security Groups only - they're stateful and sufficient
- B) Network ACLs (NACLs) at subnet level + Security Groups at instance level + VPC Flow Logs for monitoring
- C) AWS WAF on ALB + Security Groups + Private subnets (no internet access)
- D) All of the above: NACLs + Security Groups + WAF + Flow Logs + Private subnets + optional VPC endpoints

**Answer:** D

---

## Explanation: Complete Defense in Depth Architecture

### Security Layer Model:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Perimeter Security                                 │
├─────────────────────────────────────────────────────────────┤
│ AWS WAF (Web Application Firewall)                          │
│ ├── SQL injection protection                                │
│ ├── XSS prevention                                          │
│ ├── Rate limiting                                           │
│ ├── Geo-blocking                                            │
│ └── Bot detection                                           │
│              ↓                                              │
│ Application Load Balancer                                   │
│ └── SSL/TLS termination                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Network Segmentation                               │
├─────────────────────────────────────────────────────────────┤
│ Public Subnet (10.0.1.0/24)                                │
│ ├── Internet Gateway attached                              │
│ ├── Route: 0.0.0.0/0 → IGW                                │
│ └── NACL: Allow 80/443 inbound, deny all else             │
│                                                             │
│ Private Subnet - Web Tier (10.0.2.0/24)                    │
│ ├── NAT Gateway for outbound only                          │
│ ├── Route: 0.0.0.0/0 → NAT Gateway                        │
│ └── NACL: Allow from ALB subnet only                       │
│                                                             │
│ Private Subnet - Database Tier (10.0.3.0/24)               │
│ ├── No internet access (no NAT/IGW route)                  │
│ ├── VPC Endpoints for AWS services                         │
│ └── NACL: Allow from web tier subnet only                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Instance-Level Security                            │
├─────────────────────────────────────────────────────────────┤
│ ALB Security Group                                          │
│ ├── Inbound: 0.0.0.0/0:443 (HTTPS)                        │
│ └── Outbound: Web SG:8080                                  │
│                                                             │
│ Web Server Security Group                                   │
│ ├── Inbound: ALB-SG:8080                                   │
│ └── Outbound: DB-SG:3306                                   │
│                                                             │
│ Database Security Group                                     │
│ ├── Inbound: Web-SG:3306                                   │
│ └── Outbound: None (deny all)                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Monitoring & Detection                             │
├─────────────────────────────────────────────────────────────┤
│ VPC Flow Logs → CloudWatch Logs → Athena analysis          │
│ GuardDuty → Threat detection                                │
│ AWS Network Firewall → IDS/IPS (optional)                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Layer 5: Data Protection                                    │
├─────────────────────────────────────────────────────────────┤
│ VPC Endpoints (PrivateLink)                                 │
│ ├── S3 Gateway Endpoint                                     │
│ ├── DynamoDB Gateway Endpoint                               │
│ └── Systems Manager Interface Endpoint                      │
└─────────────────────────────────────────────────────────────┘
```

### Complete Implementation:

```python
import boto3
import json

ec2 = boto3.client('ec2')
elbv2 = boto3.client('elbv2')
wafv2 = boto3.client('wafv2')

# Create VPC with DNS support
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc['Vpc']['VpcId']

ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})

# Create subnets
public_subnet = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.1.0/24',
    AvailabilityZone='us-east-1a'
)

private_web_subnet = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.2.0/24',
    AvailabilityZone='us-east-1a'
)

private_db_subnet = ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock='10.0.3.0/24',
    AvailabilityZone='us-east-1a'
)

# Create Security Groups with strict isolation
alb_sg = ec2.create_security_group(
    GroupName='alb-sg',
    Description='ALB Security Group',
    VpcId=vpc_id
)

ec2.authorize_security_group_ingress(
    GroupId=alb_sg['GroupId'],
    IpPermissions=[{
        'IpProtocol': 'tcp',
        'FromPort': 443,
        'ToPort': 443,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }]
)

web_sg = ec2.create_security_group(
    GroupName='web-sg',
    Description='Web Server Security Group',
    VpcId=vpc_id
)

ec2.authorize_security_group_ingress(
    GroupId=web_sg['GroupId'],
    IpPermissions=[{
        'IpProtocol': 'tcp',
        'FromPort': 8080,
        'ToPort': 8080,
        'UserIdGroupPairs': [{'GroupId': alb_sg['GroupId']}]
    }]
)

db_sg = ec2.create_security_group(
    GroupName='db-sg',
    Description='Database Security Group',
    VpcId=vpc_id
)

ec2.authorize_security_group_ingress(
    GroupId=db_sg['GroupId'],
    IpPermissions=[{
        'IpProtocol': 'tcp',
        'FromPort': 3306,
        'ToPort': 3306,
        'UserIdGroupPairs': [{'GroupId': web_sg['GroupId']}]
    }]
)

# Enable VPC Flow Logs
logs = boto3.client('logs')
iam = boto3.client('iam')

logs.create_log_group(logGroupName='/aws/vpc/flowlogs')

flow_log = ec2.create_flow_logs(
    ResourceType='VPC',
    ResourceIds=[vpc_id],
    TrafficType='ALL',
    LogDestinationType='cloud-watch-logs',
    LogGroupName='/aws/vpc/flowlogs'
)

print("✅ Complete defense in depth architecture deployed")
```

---

# Security Groups vs. Network ACLs

## Question 2: IP Blocking for Security Incidents

**Scenario:**
You notice unusual SSH attempts from IP `203.0.113.50` targeting your web servers. You need to block this IP immediately.

**Question:** Where should you implement the block, and why?

**Options:**
- A) Security Group - add deny rule for 203.0.113.50:22
- B) Network ACL - add explicit deny rule with low rule number (before allow rules)
- C) Both Security Group and Network ACL for redundancy
- D) AWS WAF with IP set blocking

**Answer:** B

---

## Explanation: Network ACLs for IP Blocking

### The Critical Difference:

```
┌─────────────────────────────────────────────┐
│ Security Groups (Stateful)                  │
├─────────────────────────────────────────────┤
│ ✅ CAN:                                     │
│ ├── Allow specific sources                  │
│ ├── Reference other security groups         │
│ ├── Stateful (return traffic automatic)     │
│ └── Instance-level protection               │
│                                             │
│ ❌ CANNOT:                                  │
│ ├── Explicit DENY rules                     │
│ ├── Block specific IPs                      │
│ └── Rule ordering                           │
└─────────────────────────────────────────────┘

vs.

┌─────────────────────────────────────────────┐
│ Network ACLs (Stateless)                    │
├─────────────────────────────────────────────┤
│ ✅ CAN:                                     │
│ ├── Explicit DENY rules                     │
│ ├── Block specific IP addresses/ranges      │
│ ├── Rule ordering (lowest # first)          │
│ └── Subnet-level protection                 │
│                                             │
│ ⚠️  Must handle:                            │
│ ├── Return traffic (stateless)             │
│ └── Ephemeral ports (1024-65535)           │
└─────────────────────────────────────────────┘
```

### Implementation:

```python
import boto3

ec2 = boto3.client('ec2')

def block_malicious_ip(subnet_id, malicious_ip):
    """
    Block malicious IP using Network ACL
    """
    # Find NACL for subnet
    nacls = ec2.describe_network_acls(
        Filters=[{
            'Name': 'association.subnet-id',
            'Values': [subnet_id]
        }]
    )
    
    nacl_id = nacls['NetworkAcls'][0]['NetworkAclId']
    
    # Add DENY rule with LOW rule number (evaluated first)
    ec2.create_network_acl_entry(
        NetworkAclId=nacl_id,
        RuleNumber=10,  # LOW number = highest priority
        Protocol='6',   # TCP
        RuleAction='deny',  # EXPLICIT DENY
        Egress=False,
        CidrBlock=f'{malicious_ip}/32',
        PortRange={'From': 22, 'To': 22}
    )
    
    print(f"✅ Blocked {malicious_ip} at NACL level")
    
    # Block outbound as well (complete isolation)
    ec2.create_network_acl_entry(
        NetworkAclId=nacl_id,
        RuleNumber=10,
        Protocol='-1',  # All protocols
        RuleAction='deny',
        Egress=True,
        CidrBlock=f'{malicious_ip}/32'
    )
    
    return nacl_id

# Block attacker
block_malicious_ip('subnet-abc123', '203.0.113.50')
```

### Rule Ordering Example:

```
Rule #  | Type  | Protocol | Port | Source         | Action
--------|-------|----------|------|----------------|--------
10      | SSH   | TCP (6)  | 22   | 203.0.113.50/32| DENY ✅
100     | SSH   | TCP (6)  | 22   | 0.0.0.0/0      | ALLOW
200     | HTTP  | TCP (6)  | 80   | 0.0.0.0/0      | ALLOW
*       | ALL   | ALL      | ALL  | 0.0.0.0/0      | DENY

Rule 10 evaluated first → blocks 203.0.113.50
Other IPs hit rule 100 → allowed
```

### Automated Threat Response:

```python
# Lambda function: Auto-block IPs from GuardDuty findings
def lambda_handler(event, context):
    """
    Auto-block malicious IPs detected by GuardDuty
    """
    finding = event['detail']
    
    if finding['type'].startswith('UnauthorizedAccess'):
        remote_ip = finding['service']['action']['networkConnectionAction']['remoteIpDetails']['ipAddressV4']
        instance_id = finding['resource']['instanceDetails']['instanceId']
        
        # Get instance subnet
        ec2 = boto3.client('ec2')
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        subnet_id = instance['Reservations'][0]['Instances'][0]['SubnetId']
        
        # Block the IP
        nacl_id = block_malicious_ip(subnet_id, remote_ip)
        
        # Notify security team
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:123456:security-alerts',
            Subject=f'Auto-blocked malicious IP: {remote_ip}',
            Message=f'GuardDuty detected attack. IP {remote_ip} blocked via NACL {nacl_id}'
        )
        
        return {'statusCode': 200, 'blocked_ip': remote_ip}
```

---

# VPC Peering vs. Transit Gateway vs. PrivateLink

## Question 3: Hub-and-Spoke Architecture

**Scenario:**
Your organization has:
- 50 VPCs across multiple AWS accounts
- Shared services VPC (Active Directory, DNS, monitoring)
- Need: All VPCs must access shared services, but VPCs should NOT communicate with each other

**Question:** What's the most scalable and secure architecture?

**Options:**
- A) VPC Peering mesh (50 VPCs peer with shared services VPC)
- B) Transit Gateway with route table isolation per VPC
- C) AWS PrivateLink with VPC endpoint services in shared services VPC
- D) VPN connections from each VPC to shared services VPC

**Answer:** B

---

## Explanation: Transit Gateway with Route Isolation

### Architecture:

```
┌─────────────────────────────────────────────────────────────┐
│ AWS Transit Gateway (Central Hub)                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────┐              │
│  │ Shared Services Route Table              │              │
│  │ ├── Routes TO all spoke VPCs             │              │
│  │ └── Attached: Shared Services VPC        │              │
│  └──────────────────────────────────────────┘              │
│                                                             │
│  ┌──────────────────────────────────────────┐              │
│  │ Spoke Route Table                        │              │
│  │ ├── Routes TO Shared Services ONLY       │              │
│  │ ├── NO routes to other spokes            │              │
│  │ └── Attached: VPC-1, VPC-2, ... VPC-50   │              │
│  └──────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────┘

          ↓                    ↓                    ↓
    
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Shared      │     │   VPC-1     │     │   VPC-2     │
│ Services    │     │ (App Team A)│     │ (App Team B)│
│ VPC         │     │             │     │             │
│ ├── AD      │     │ 10.1.0.0/16 │     │ 10.2.0.0/16 │
│ ├── DNS     │     │             │     │             │
│ └── Monitor │     │ ✅ → Shared │     │ ✅ → Shared │
│ 10.0.0.0/16 │     │ ❌ → VPC-2  │     │ ❌ → VPC-1  │
└─────────────┘     └─────────────┘     └─────────────┘

Benefits:
✅ Scalable: 5,000 VPCs per TGW
✅ Centralized routing
✅ Isolated: Spokes can't reach each other
✅ Cross-account support
```

### Implementation:

```python
import boto3

ec2 = boto3.client('ec2')

# Create Transit Gateway
tgw = ec2.create_transit_gateway(
    Description='Hub for 50 VPCs',
    Options={
        'DefaultRouteTableAssociation': 'disable',
        'DefaultRouteTablePropagation': 'disable',
        'DnsSupport': 'enable'
    }
)

tgw_id = tgw['TransitGateway']['TransitGatewayId']

# Create route tables
shared_rt = ec2.create_transit_gateway_route_table(
    TransitGatewayId=tgw_id,
    TagSpecifications=[{
        'ResourceType': 'transit-gateway-route-table',
        'Tags': [{'Key': 'Name', 'Value': 'shared-services-rt'}]
    }]
)

spoke_rt = ec2.create_transit_gateway_route_table(
    TransitGatewayId=tgw_id,
    TagSpecifications=[{
        'ResourceType': 'transit-gateway-route-table',
        'Tags': [{'Key': 'Name', 'Value': 'spoke-rt'}]
    }]
)

# Attach shared services VPC
shared_attachment = ec2.create_transit_gateway_vpc_attachment(
    TransitGatewayId=tgw_id,
    VpcId='vpc-shared123',
    SubnetIds=['subnet-shared1', 'subnet-shared2']
)

# Associate with shared services RT
ec2.associate_transit_gateway_route_table(
    TransitGatewayRouteTableId=shared_rt['TransitGatewayRouteTable']['TransitGatewayRouteTableId'],
    TransitGatewayAttachmentId=shared_attachment['TransitGatewayVpcAttachment']['TransitGatewayAttachmentId']
)

# Attach spoke VPCs
def attach_spoke_vpc(vpc_id, vpc_cidr):
    attachment = ec2.create_transit_gateway_vpc_attachment(
        TransitGatewayId=tgw_id,
        VpcId=vpc_id,
        SubnetIds=['subnet-1', 'subnet-2']
    )
    
    # Associate with SPOKE RT (isolated)
    ec2.associate_transit_gateway_route_table(
        TransitGatewayRouteTableId=spoke_rt['TransitGatewayRouteTable']['TransitGatewayRouteTableId'],
        TransitGatewayAttachmentId=attachment['TransitGatewayVpcAttachment']['TransitGatewayAttachmentId']
    )
    
    # Propagate to shared services RT (so shared can reach spoke)
    ec2.enable_transit_gateway_route_table_propagation(
        TransitGatewayRouteTableId=shared_rt['TransitGatewayRouteTable']['TransitGatewayRouteTableId'],
        TransitGatewayAttachmentId=attachment['TransitGatewayVpcAttachment']['TransitGatewayAttachmentId']
    )

# Attach all 50 spokes
for i in range(1, 51):
    attach_spoke_vpc(f'vpc-spoke{i:03d}', f'10.{i}.0.0/16')

print("✅ Transit Gateway configured with route isolation")
```

---

# VPC Flow Logs Analysis

## Question 4: Security Incident Investigation

**Scenario:**
Security team detected a potential data exfiltration attempt. VPC Flow Logs show:
```
2 123456789012 eni-abc123 172.31.16.5 203.0.113.50 49152 22 6 20 4000 1620000000 1620000300 REJECT OK
```

**Question:** What does this flow log entry indicate?

**Options:**
- A) Outbound SSH connection from 172.31.16.5 to 203.0.113.50 was successful
- B) Inbound SSH connection attempt from 203.0.113.50 to 172.31.16.5 was rejected
- C) Outbound connection on ephemeral port 49152 to SSH port 22 was rejected - potential compromise blocked
- D) Bidirectional SSH traffic totaling 4000 bytes

**Answer:** C

---

## Explanation: Reading VPC Flow Logs

### Flow Log Format:

```
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status

2 123456789012 eni-abc123 172.31.16.5 203.0.113.50 49152 22 6 20 4000 1620000000 1620000300 REJECT OK
```

### Breaking It Down:

```python
flow_log = {
    'srcaddr': '172.31.16.5',      # INTERNAL (RFC 1918)
    'dstaddr': '203.0.113.50',     # EXTERNAL (public IP)
    'srcport': '49152',            # EPHEMERAL PORT
    'dstport': '22',               # SSH (well-known port)
    'protocol': '6',               # TCP
    'action': 'REJECT'             # BLOCKED!
}

# Analysis
print("Direction: OUTBOUND (internal → external)")
print("Pattern: Internal host trying to SSH to external server")
print("Result: REJECTED by Security Group/NACL")
print("⚠️  Indicates potential compromise (even though blocked)")
```

### Threat Analysis:

```
Compromise Scenario:
┌─────────────────────────────────────────────┐
│ 1. Attacker compromises EC2 (172.31.16.5)  │
│ 2. Attempts reverse shell to C2 server     │
│ 3. Tries SSH to 203.0.113.50:22            │
│ 4. Security controls BLOCK it ✅            │
│ 5. BUT: Instance IS compromised ⚠️          │
└─────────────────────────────────────────────┘
```

### Automated Investigation:

```python
def investigate_compromised_instance(internal_ip, external_ip):
    """
    Automated response to suspected compromise
    """
    ec2 = boto3.client('ec2')
    
    # Find instance
    instances = ec2.describe_instances(
        Filters=[{'Name': 'private-ip-address', 'Values': [internal_ip]}]
    )
    
    instance_id = instances['Reservations'][0]['Instances'][0]['InstanceId']
    
    # 1. Isolate instance
    forensic_sg = ec2.create_security_group(
        GroupName=f'forensic-{instance_id}',
        Description='Forensic isolation',
        VpcId='vpc-12345'
    )
    
    # Remove all egress rules
    ec2.revoke_security_group_egress(
        GroupId=forensic_sg['GroupId'],
        IpPermissions=[{'IpProtocol': '-1', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]
    )
    
    # Apply to instance
    ec2.modify_instance_attribute(
        InstanceId=instance_id,
        Groups=[forensic_sg['GroupId']]
    )
    
    # 2. Create snapshot
    volumes = [vol['Ebs']['VolumeId'] for vol in 
               instances['Reservations'][0]['Instances'][0]['BlockDeviceMappings']]
    
    for volume_id in volumes:
        ec2.create_snapshot(
            VolumeId=volume_id,
            Description=f'Forensic snapshot - {instance_id}'
        )
    
    # 3. Block external IP at NACL
    # 4. Notify security team
    
    print(f"✅ Instance {instance_id} isolated and forensics preserved")
```

### Athena Queries:

```sql
-- Find outbound SSH attempts (potential compromises)
SELECT 
    sourceaddress,
    destinationaddress,
    COUNT(*) as attempts
FROM vpc_flow_logs
WHERE 
    destinationport = 22
    AND action = 'REJECT'
    AND sourceaddress LIKE '172.31.%'  -- Internal
    AND destinationaddress NOT LIKE '172.31.%'  -- External
GROUP BY sourceaddress, destinationaddress
HAVING COUNT(*) > 10
ORDER BY attempts DESC;
```

---

# AWS Network Firewall

## Question 5: Layer 7 Security

**Scenario:**
Security team requires deep packet inspection (DPI), domain filtering, and IDS/IPS. Current setup uses Security Groups and NACLs.

**Question:** Which capabilities does AWS Network Firewall provide that Security Groups and NACLs cannot?

**Options:**
- A) Stateful firewall rules and port-based filtering
- B) Domain name filtering, intrusion detection/prevention, and deep packet inspection with Suricata rules
- C) Instance-level traffic control and security group referencing
- D) Blocking specific IP addresses and CIDR ranges

**Answer:** B

---

## Explanation: Layer 7 Deep Inspection

### Comparison:

```
Security Groups / NACLs: Layer 3/4
├── IP addresses/CIDR
├── Port/protocol
└── ❌ No domain filtering
    ❌ No payload inspection
    ❌ No IDS/IPS

AWS Network Firewall: Layer 3/4/7
├── Everything above PLUS:
├── ✅ Domain name filtering
├── ✅ URL filtering
├── ✅ Deep packet inspection
├── ✅ Suricata rules
├── ✅ IDS/IPS
└── ✅ TLS inspection
```

### Implementation:

```python
import boto3

nfw = boto3.client('network-firewall')

# Create firewall policy
policy = nfw.create_firewall_policy(
    FirewallPolicyName='production-policy',
    FirewallPolicy={
        'StatelessDefaultActions': ['aws:forward_to_sfe'],
        'StatelessFragmentDefaultActions': ['aws:forward_to_sfe'],
        'StatefulDefaultActions': ['aws:drop_strict']
    }
)

# Domain filtering rule group
domain_rules = nfw.create_rule_group(
    RuleGroupName='block-malicious-domains',
    Type='STATEFUL',
    RuleGroup={
        'RulesSource': {
            'RulesSourceList': {
                'TargetTypes': ['HTTP_HOST', 'TLS_SNI'],
                'Targets': [
                    '.malicious-domain.com',
                    '.phishing-site.net',
                    '.cryptominer.org',
                    # Block data exfiltration
                    '.dropbox.com',
                    'drive.google.com'
                ],
                'GeneratedRulesType': 'DENYLIST'
            }
        }
    },
    Capacity=100
)

# Suricata IDS/IPS rules
suricata_rules = """
# SQL Injection
alert http any any -> any any (msg:"SQL Injection"; content:"SELECT"; http_uri; content:"FROM"; http_uri; sid:1000001;)

# Command Injection
alert http any any -> any any (msg:"Command Injection"; pcre:"/(\||;|`)/"; http_uri; sid:1000002;)

# Log4Shell
alert http any any -> any any (msg:"Log4Shell Exploit"; content:"${jndi:ldap://"; nocase; sid:1000003;)

# Crypto Mining
alert tcp any any -> any any (msg:"Crypto Mining"; content:"mining.subscribe"; sid:1000004;)

# AWS Metadata SSRF
alert http any any -> any 169.254.169.254 (msg:"SSRF to Metadata"; content:"169.254.169.254"; sid:1000005;)
"""

suricata_rule_group = nfw.create_rule_group(
    RuleGroupName='ids-ips-rules',
    Type='STATEFUL',
    Rules=suricata_rules,
    Capacity=500
)

# Create firewall
firewall = nfw.create_firewall(
    FirewallName='production-firewall',
    FirewallPolicyArn=policy['FirewallPolicyResponse']['FirewallPolicyArn'],
    VpcId='vpc-12345',
    SubnetMappings=[
        {'SubnetId': 'subnet-fw1'},
        {'SubnetId': 'subnet-fw2'}
    ]
)

print("✅ Network Firewall with Layer 7 inspection enabled")
```

### Use Cases:

**1. Block Malware C2:**
```json
{
  "alert": {
    "signature": "Malware C2 Communication",
    "severity": 1
  },
  "http": {
    "hostname": "malicious-c2.example.com"
  },
  "action": "blocked"
}
```

**2. Detect SQL Injection:**
```json
{
  "alert": {
    "signature": "SQL Injection Attempt"
  },
  "http": {
    "url": "/api/users?id=1' OR '1'='1"
  }
}
```

---

# VPC Endpoint Policies for S3

## Question 6: Preventing Data Exfiltration

**Scenario:**
Requirements:
- EC2 instances must access S3
- Traffic must NOT traverse internet
- Only company-owned S3 buckets allowed
- Prevent exfiltration to personal buckets

**Question:** What's the most secure architecture?

**Options:**
- A) NAT Gateway with S3 bucket policies
- B) S3 Gateway Endpoint with endpoint policy restricting to specific bucket ARNs
- C) S3 Interface Endpoint with security groups
- D) VPN connection to S3

**Answer:** B

---

## Explanation: S3 Gateway Endpoint Security

### Architecture:

```
┌─────────────────────────────────────────────┐
│ VPC                                         │
│                                             │
│ EC2 Instance → S3 Gateway Endpoint          │
│                     ↓                       │
│              Endpoint Policy:               │
│              Allow ONLY:                    │
│              - arn:aws:s3:::company-bucket  │
│              Deny: all others               │
└─────────────────────────────────────────────┘
              ↓ (AWS backbone)
        ┌──────────────────┐
        │ Amazon S3        │
        │ ✅ company-bucket │
        │ ❌ personal-bucket│
        └──────────────────┘
```

### Implementation:

```python
import boto3
import json

ec2 = boto3.client('ec2')

# Restrictive endpoint policy
endpoint_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCompanyBucketsOnly",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::company-data-bucket",
                "arn:aws:s3:::company-data-bucket/*",
                "arn:aws:s3:::company-logs-bucket",
                "arn:aws:s3:::company-logs-bucket/*"
            ]
        }
    ]
}

# Create S3 Gateway Endpoint
endpoint = ec2.create_vpc_endpoint(
    VpcId='vpc-12345',
    ServiceName='com.amazonaws.us-east-1.s3',
    RouteTableIds=['rtb-abc123'],
    PolicyDocument=json.dumps(endpoint_policy),
    VpcEndpointType='Gateway'
)

print(f"✅ S3 Gateway Endpoint: {endpoint['VpcEndpoint']['VpcEndpointId']}")
print("✅ Traffic stays on AWS backbone")
print("✅ Only company buckets accessible")
print("✅ FREE (no Gateway Endpoint charges)")
```

### Benefits:

✅ **Private** - No internet traversal  
✅ **Secure** - Whitelist specific buckets  
✅ **Cost-effective** - Gateway endpoints FREE  
✅ **Compliant** - Meets data governance requirements

---

# PrivateLink for Cross-Account Access

## Question 7: Secure Service Sharing

**Scenario:**
- Company A (111111) provides microservice API
- Company B (222222) needs to consume it
- No public internet exposure
- No VPC peering
- Traffic stays within AWS

**Question:** What's the correct architecture?

**Options:**
- A) VPC Peering with security groups
- B) AWS PrivateLink - Company A creates Endpoint Service, Company B creates Interface Endpoint
- C) Internet-facing ALB with IP whitelist
- D) Transit Gateway

**Answer:** B

---

## Explanation: AWS PrivateLink

### Architecture:

```
Provider Account (111111)
┌─────────────────────────────────┐
│ NLB → Microservice API          │
│  ↓                              │
│ VPC Endpoint Service            │
│ Whitelist: Account 222222       │
└─────────────────────────────────┘
        ↓ (PrivateLink)
Consumer Account (222222)
┌─────────────────────────────────┐
│ Interface Endpoint              │
│ eni-xyz (10.1.2.50)            │
│  ↑                              │
│ App calls 10.1.2.50             │
└─────────────────────────────────┘
```

### Implementation:

```python
# Provider: Create Endpoint Service
elbv2 = boto3.client('elbv2')
ec2 = boto3.client('ec2')

# Create NLB
nlb = elbv2.create_load_balancer(
    Name='api-nlb',
    Subnets=['subnet-1', 'subnet-2'],
    Type='network',
    Scheme='internal'
)

# Create Endpoint Service
endpoint_service = ec2.create_vpc_endpoint_service_configuration(
    NetworkLoadBalancerArns=[nlb['LoadBalancers'][0]['LoadBalancerArn']],
    AcceptanceRequired=True
)

service_name = endpoint_service['ServiceConfiguration']['ServiceName']

# Whitelist consumer account
ec2.modify_vpc_endpoint_service_permissions(
    ServiceId=endpoint_service['ServiceConfiguration']['ServiceId'],
    AddAllowedPrincipals=['arn:aws:iam::222222222222:root']
)

print(f"✅ Service: {service_name}")

# Consumer: Create Interface Endpoint
consumer_ec2 = boto3.client('ec2', region_name='us-east-1')

interface_endpoint = consumer_ec2.create_vpc_endpoint(
    VpcId='vpc-consumer',
    ServiceName=service_name,
    VpcEndpointType='Interface',
    SubnetIds=['subnet-consumer-1'],
    PrivateDnsEnabled=False
)

print(f"✅ Consumer endpoint: {interface_endpoint['VpcEndpoint']['VpcEndpointId']}")
```

---

# IPv6 Security

## Question 8: Dual-Stack VPC Security

**Scenario:**
VPC has dual-stack (IPv4 + IPv6) enabled. Security team asks: "How do we secure IPv6?"

**Question:** What's TRUE about IPv6 security?

**Options:**
- A) IPv6 not supported in Security Groups
- B) Security Groups and NACLs both support IPv6 with ::/0 notation
- C) IPv6 bypasses Security Groups
- D) IPv6 requires separate VPC

**Answer:** B

---

## Explanation: IPv6 Security Controls

### Implementation:

```python
# Security Group - IPv6
ec2.authorize_security_group_ingress(
    GroupId='sg-12345',
    IpPermissions=[{
        'IpProtocol': 'tcp',
        'FromPort': 443,
        'ToPort': 443,
        'Ipv6Ranges': [{'CidrIpv6': '::/0'}]  # All IPv6
    }]
)

# NACL - IPv6
ec2.create_network_acl_entry(
    NetworkAclId='acl-12345',
    RuleNumber=100,
    Protocol='6',
    RuleAction='allow',
    Egress=False,
    Ipv6CidrBlock='::/0',
    PortRange={'From': 443, 'To': 443}
)
```

### Key Points:
- ✅ IPv4 and IPv6 coexist
- ✅ Same security model
- ✅ ::/0 = all IPv6
- ✅ Dual rules needed

---

# VPC Sharing with AWS RAM

## Question 9: Centralized Network Management

**Scenario:**
100 AWS accounts. Central networking team manages VPCs. Application teams need their own subnets.

**Question:** Best architecture?

**Options:**
- A) VPC Peering mesh
- B) AWS RAM to share VPC - teams get dedicated subnets
- C) Each account creates own VPC
- D) All teams in one account

**Answer:** B

---

## Explanation: VPC Sharing

### Architecture:

```
Central Network Account
├── Shared VPC (10.0.0.0/16)
├── Manages: IGW, NAT, Routes
└── Shares via AWS RAM
      ↓
App Team A (Account 111111)
└── Subnet 10.0.1.0/24

App Team B (Account 222222)
└── Subnet 10.0.2.0/24
```

### Implementation:

```python
ram = boto3.client('ram')

# Share VPC
ram.create_resource_share(
    name='shared-vpc',
    resourceArns=['arn:aws:ec2:us-east-1:999999:vpc/vpc-abc123'],
    principals=['111111111111', '222222222222']
)
```

---

# VPC Reachability Analyzer

## Question 10: Network Troubleshooting

**Scenario:**
"Can't connect from EC2 to RDS. Security Groups look correct!"

**Question:** Fastest way to diagnose?

**Options:**
- A) Manually check all components
- B) VPC Reachability Analyzer - analyzes all components automatically
- C) Wait for VPC Flow Logs
- D) Use AWS Config

**Answer:** B

---

## Explanation: Automated Path Analysis

### Implementation:

```python
ec2 = boto3.client('ec2')

# Create path
path = ec2.create_network_insights_path(
    Source='eni-ec2-abc',
    Destination='eni-rds-xyz',
    Protocol='tcp',
    DestinationPort=3306
)

# Analyze
analysis = ec2.start_network_insights_analysis(
    NetworkInsightsPathId=path['NetworkInsightsPath']['NetworkInsightsPathId']
)

# Result
"""
❌ NOT REACHABLE
Blocking: NACL acl-12345
Rule: 100 DENY port 3306
"""
```

---

# Summary & Key Takeaways

## Your Performance:
- **Total Questions:** 10
- **Correct Answers:** 9
- **Score:** 90%

### Questions Breakdown:
1. ✅ Defense in Depth
2. ✅ Security Groups vs NACLs
3. ✅ Transit Gateway
4. ❌ VPC Flow Logs (direction)
5. ✅ Network Firewall
6. ✅ VPC Endpoint Policies
7. ✅ PrivateLink
8. ✅ IPv6 Security
9. ✅ VPC Sharing
10. ✅ Reachability Analyzer

## Key Security Principles:

### 1. Defense in Depth
- Multiple security layers
- NACL (subnet) + Security Group (instance) + WAF (application)
- VPC Flow Logs for monitoring

### 2. Blocking Strategy
- Security Groups: Allow only (implicit deny)
- NACLs: Explicit deny (block specific IPs)
- Network Firewall: Layer 7 (domains, IDS/IPS)

### 3. Connectivity Patterns
- **Transit Gateway:** Hub-and-spoke, route isolation
- **VPC Peering:** 1-to-1, no transitive routing
- **PrivateLink:** Service sharing, no VPC peering

### 4. VPC Endpoints
- **Gateway:** S3, DynamoDB (FREE)
- **Interface:** AWS services, PrivateLink (hourly fee)
- Endpoint policies restrict access

### 5. Monitoring
- VPC Flow Logs: Network traffic analysis
- Reachability Analyzer: Path troubleshooting
- GuardDuty: Threat detection

## Architecture Decision Tree:

```
Need to block specific IP?
└── Use NACL (explicit deny)

Need Layer 7 inspection?
└── Use Network Firewall

Need to connect VPCs?
├── Same organization → Transit Gateway
├── Service sharing → PrivateLink
└── 1-to-1 connection → VPC Peering

Need private S3 access?
└── S3 Gateway Endpoint + policy

Need to troubleshoot connectivity?
└── VPC Reachability Analyzer
```

## Cost Optimization:

| Service | Cost Model | When to Use |
|---------|-----------|-------------|
| Security Groups | FREE | Always |
| NACLs | FREE | Always |
| VPC Flow Logs | Storage cost | Monitoring/forensics |
| Network Firewall | $0.395/hour + data | Layer 7 security |
| Transit Gateway | $0.05/hour/attachment + data | Multi-VPC (50+) |
| VPC Peering | Data transfer only | 1-to-1 connections |
| Gateway Endpoints | FREE | S3/DynamoDB access |
| Interface Endpoints | $0.01/hour + data | AWS service access |

## Best Practices:

1. **Always enable VPC Flow Logs** - invaluable for security investigations
2. **Use NACLs for IP blocking** - Security Groups don't support deny
3. **Implement defense in depth** - multiple layers, not single point of failure
4. **Use VPC endpoints** - avoid internet traversal when possible
5. **Leverage Transit Gateway** - for multi-VPC architectures (50+ VPCs)
6. **Apply endpoint policies** - restrict which resources can be accessed
7. **Automate threat response** - GuardDuty + Lambda for auto-blocking
8. **Use Reachability Analyzer** - faster than manual troubleshooting
9. **Tag everything** - cost allocation and security tracking
10. **Regular security audits** - review NACLs, Security Groups, Flow Logs

## Interview Talking Points:

**For VPC Security Architect roles, emphasize:**

1. **Layered security model** - NACL + SG + WAF + Network Firewall
2. **Difference between stateful/stateless** - SG vs NACL
3. **When to use each connectivity option** - TGW vs Peering vs PrivateLink
4. **How to read VPC Flow Logs** - direction, action, interpretation
5. **Network Firewall capabilities** - Layer 7 vs Layer 3/4
6. **VPC endpoint types and use cases** - Gateway vs Interface
7. **Security automation** - GuardDuty + Lambda for threat response
8. **Troubleshooting methodology** - Reachability Analyzer first
9. **Cost considerations** - free vs paid services
10. **Compliance requirements** - private connectivity, data governance

---

*Generated: November 30, 2024*
*Total Questions: 10*
*Your Score: 90%*
*Focus Area: VPC Flow Logs direction analysis*

**You're ready for AWS Security Specialty certification and cybersecurity architect interviews!**
