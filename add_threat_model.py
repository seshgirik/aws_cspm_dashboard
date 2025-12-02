#!/usr/bin/env python3
"""
Add STRIDE and MITRE ATT&CK threat modeling to security findings
"""

import json
import re

# MITRE ATT&CK mapping based on finding types
MITRE_ATTACK_MAPPING = {
    'CloudTrail': {
        'tactics': ['Defense Evasion', 'Discovery'],
        'techniques': ['T1562.008', 'T1518'],
        'description': 'Disable Cloud Logs, Software Discovery'
    },
    'KMS': {
        'tactics': ['Impact', 'Credential Access'],
        'techniques': ['T1486', 'T1552.001'],
        'description': 'Data Encrypted for Impact, Credentials in Files'
    },
    'S3': {
        'tactics': ['Collection', 'Exfiltration'],
        'techniques': ['T1530', 'T1537'],
        'description': 'Data from Cloud Storage Object, Transfer Data to Cloud Account'
    },
    'IAM': {
        'tactics': ['Privilege Escalation', 'Persistence'],
        'techniques': ['T1078.004', 'T1098'],
        'description': 'Cloud Accounts, Account Manipulation'
    },
    'VPC': {
        'tactics': ['Defense Evasion', 'Command and Control'],
        'techniques': ['T1562.007', 'T1071'],
        'description': 'Disable or Modify Cloud Firewall, Application Layer Protocol'
    },
    'Lambda': {
        'tactics': ['Execution', 'Persistence'],
        'techniques': ['T1204.003', 'T1546'],
        'description': 'Malicious Cloud Function, Event Triggered Execution'
    },
    'RDS': {
        'tactics': ['Collection', 'Impact'],
        'techniques': ['T1530', 'T1485'],
        'description': 'Data from Cloud Storage, Data Destruction'
    },
    'EC2': {
        'tactics': ['Initial Access', 'Lateral Movement'],
        'techniques': ['T1190', 'T1021'],
        'description': 'Exploit Public-Facing Application, Remote Services'
    },
    'EKS': {
        'tactics': ['Execution', 'Privilege Escalation'],
        'techniques': ['T1610', 'T1611'],
        'description': 'Deploy Container, Escape to Host'
    },
    'Secrets': {
        'tactics': ['Credential Access'],
        'techniques': ['T1552', 'T1555'],
        'description': 'Unsecured Credentials, Credentials from Password Stores'
    },
    'GuardDuty': {
        'tactics': ['Defense Evasion', 'Discovery'],
        'techniques': ['T1562', 'T1580'],
        'description': 'Impair Defenses, Cloud Infrastructure Discovery'
    },
    'Config': {
        'tactics': ['Defense Evasion'],
        'techniques': ['T1562.008'],
        'description': 'Disable Cloud Logs'
    }
}

# MITRE ATLAS mapping for AI/ML findings
MITRE_ATLAS_MAPPING = {
    'vectordb': {
        'tactics': ['ML Model Access'],
        'techniques': ['AML.T0018', 'AML.T0020'],
        'description': 'Data Poisoning, Backdoor ML Model'
    },
    'llm': {
        'tactics': ['LLM Exploitation'],
        'techniques': ['AML.T0051', 'AML.T0054'],
        'description': 'Prompt Injection, LLM Jailbreak'
    },
    'modelhost': {
        'tactics': ['ML Model Access'],
        'techniques': ['AML.T0024', 'AML.T0043'],
        'description': 'Model Extraction, Craft Adversarial Data'
    }
}

# STRIDE categorization
STRIDE_MAPPING = {
    'authentication': {
        'category': 'Spoofing',
        'description': 'Identity impersonation or credential theft'
    },
    'authorization': {
        'category': 'Tampering',
        'description': 'Unauthorized modification of data or configuration'
    },
    'encryption': {
        'category': 'Information Disclosure',
        'description': 'Exposure of sensitive information'
    },
    'logging': {
        'category': 'Repudiation',
        'description': 'Inability to prove actions occurred'
    },
    'network': {
        'category': 'Denial of Service',
        'description': 'Service availability disruption'
    },
    'access': {
        'category': 'Elevation of Privilege',
        'description': 'Gaining unauthorized access rights'
    }
}


def get_mitre_attack_for_finding(generator_id, title, description):
    """Determine MITRE ATT&CK techniques based on finding content"""
    
    # Check for AWS service in GeneratorId
    for service, mapping in MITRE_ATTACK_MAPPING.items():
        if service.lower() in generator_id.lower() or service.lower() in title.lower():
            return mapping
    
    # Check for AI/ML specific findings
    if any(term in generator_id.lower() for term in ['vectordb', 'llm', 'modelhost', 'aisupply']):
        for key, mapping in MITRE_ATLAS_MAPPING.items():
            if key in generator_id.lower():
                return {
                    'tactics': mapping['tactics'],
                    'techniques': mapping['techniques'],
                    'description': mapping['description'],
                    'framework': 'MITRE ATLAS'
                }
    
    # Default mapping based on severity and type
    if 'unauthorized' in description.lower() or 'authentication' in description.lower():
        return MITRE_ATTACK_MAPPING['IAM']
    elif 'encryption' in description.lower() or 'kms' in description.lower():
        return MITRE_ATTACK_MAPPING['KMS']
    elif 'logging' in description.lower() or 'cloudtrail' in description.lower():
        return MITRE_ATTACK_MAPPING['CloudTrail']
    
    # Generic default
    return {
        'tactics': ['Initial Access'],
        'techniques': ['T1190'],
        'description': 'Exploit Public-Facing Application'
    }


def get_stride_categories(finding):
    """Determine STRIDE categories based on finding content"""
    title = finding.get('Title', '').lower()
    description = finding.get('Description', '').lower()
    
    categories = []
    
    # Spoofing
    if any(term in title + description for term in ['authentication', 'mfa', 'password', 'credential', 'identity']):
        categories.append({
            'category': 'Spoofing',
            'description': 'Authentication and identity threats',
            'risk': 'HIGH' if finding.get('Severity', {}).get('Label') in ['CRITICAL', 'HIGH'] else 'MEDIUM'
        })
    
    # Tampering
    if any(term in title + description for term in ['integrity', 'modification', 'tampering', 'unauthorized change']):
        categories.append({
            'category': 'Tampering',
            'description': 'Data or configuration integrity threats',
            'risk': 'HIGH' if finding.get('Severity', {}).get('Label') in ['CRITICAL', 'HIGH'] else 'MEDIUM'
        })
    
    # Repudiation
    if any(term in title + description for term in ['logging', 'audit', 'trail', 'monitoring']):
        categories.append({
            'category': 'Repudiation',
            'description': 'Audit trail and logging threats',
            'risk': 'MEDIUM'
        })
    
    # Information Disclosure
    if any(term in title + description for term in ['encryption', 'exposure', 'public', 'disclosure', 'leak', 'sensitive']):
        categories.append({
            'category': 'Information Disclosure',
            'description': 'Sensitive data exposure threats',
            'risk': 'HIGH' if finding.get('Severity', {}).get('Label') == 'CRITICAL' else 'MEDIUM'
        })
    
    # Denial of Service
    if any(term in title + description for term in ['availability', 'backup', 'redundancy', 'failover']):
        categories.append({
            'category': 'Denial of Service',
            'description': 'Service availability threats',
            'risk': 'MEDIUM'
        })
    
    # Elevation of Privilege
    if any(term in title + description for term in ['privilege', 'permission', 'authorization', 'access control', 'policy']):
        categories.append({
            'category': 'Elevation of Privilege',
            'description': 'Unauthorized privilege escalation threats',
            'risk': 'HIGH' if finding.get('Severity', {}).get('Label') in ['CRITICAL', 'HIGH'] else 'MEDIUM'
        })
    
    # If no categories matched, add a default based on severity
    if not categories:
        categories.append({
            'category': 'Information Disclosure',
            'description': 'Security configuration weakness',
            'risk': finding.get('Severity', {}).get('Label', 'MEDIUM')
        })
    
    return categories


def add_threat_model(findings_data):
    """Add threat model to all findings"""
    
    updated_findings = []
    
    for item in findings_data:
        finding = item['detail']['findings'][0]
        
        # Get MITRE ATT&CK mapping
        mitre_data = get_mitre_attack_for_finding(
            finding.get('GeneratorId', ''),
            finding.get('Title', ''),
            finding.get('Description', '')
        )
        
        # Get STRIDE categories
        stride_categories = get_stride_categories(finding)
        
        # Create threat model section
        threat_model = {
            'STRIDE': stride_categories,
            'MITRE_ATTACK': {
                'framework': mitre_data.get('framework', 'MITRE ATT&CK for Cloud'),
                'tactics': mitre_data['tactics'],
                'techniques': [
                    {
                        'id': tech,
                        'name': mitre_data['description']
                    } for tech in mitre_data['techniques']
                ],
                'url': f"https://attack.mitre.org/techniques/{mitre_data['techniques'][0].replace('.', '/')}"
            },
            'risk_score': calculate_risk_score(finding, stride_categories),
            'attack_surface': determine_attack_surface(finding)
        }
        
        # Add threat model to finding
        finding['ThreatModel'] = threat_model
        
        updated_findings.append(item)
    
    return updated_findings


def calculate_risk_score(finding, stride_categories):
    """Calculate overall risk score (0-100)"""
    severity_weights = {
        'CRITICAL': 100,
        'HIGH': 75,
        'MEDIUM': 50,
        'LOW': 25,
        'INFORMATIONAL': 10
    }
    
    base_score = severity_weights.get(finding.get('Severity', {}).get('Label', 'MEDIUM'), 50)
    
    # Increase score if multiple STRIDE categories apply
    stride_multiplier = 1 + (len(stride_categories) * 0.1)
    
    # Adjust for compliance status
    if finding.get('Compliance', {}).get('Status') == 'FAILED':
        compliance_multiplier = 1.2
    else:
        compliance_multiplier = 1.0
    
    final_score = min(100, int(base_score * stride_multiplier * compliance_multiplier))
    
    return final_score


def determine_attack_surface(finding):
    """Determine the attack surface exposed"""
    title = finding.get('Title', '').lower()
    description = finding.get('Description', '').lower()
    
    surfaces = []
    
    if 'public' in title + description or 'internet' in title + description:
        surfaces.append('External/Internet-facing')
    
    if 'vpc' in title + description or 'network' in title + description:
        surfaces.append('Network Layer')
    
    if 'api' in title + description or 'endpoint' in title + description:
        surfaces.append('API/Application Layer')
    
    if 'iam' in title + description or 'access' in title + description:
        surfaces.append('Identity & Access Management')
    
    if 'data' in title + description or 's3' in title + description or 'rds' in title + description:
        surfaces.append('Data Layer')
    
    if 'llm' in title + description or 'ai' in title + description or 'ml' in title + description:
        surfaces.append('AI/ML Services')
    
    return surfaces if surfaces else ['Infrastructure']


def main():
    """Main function to process findings"""
    
    # Read the existing findings
    with open('security_findings_all.json', 'r') as f:
        findings_data = json.load(f)
    
    print(f"Processing {len(findings_data)} findings...")
    
    # Add threat model to findings
    updated_findings = add_threat_model(findings_data)
    
    # Write updated findings
    with open('security_findings_all.json', 'w') as f:
        json.dump(updated_findings, f, indent=2)
    
    print(f"✓ Successfully added threat models to {len(updated_findings)} findings")
    
    # Print summary
    print("\n=== Threat Model Summary ===")
    stride_counts = {}
    mitre_techniques = set()
    
    for item in updated_findings:
        finding = item['detail']['findings'][0]
        threat_model = finding.get('ThreatModel', {})
        
        for stride in threat_model.get('STRIDE', []):
            category = stride['category']
            stride_counts[category] = stride_counts.get(category, 0) + 1
        
        for tech in threat_model.get('MITRE_ATTACK', {}).get('techniques', []):
            mitre_techniques.add(tech['id'])
    
    print("\nSTRIDE Coverage:")
    for category, count in sorted(stride_counts.items()):
        print(f"  - {category}: {count} findings")
    
    print(f"\nMITRE ATT&CK Techniques: {len(mitre_techniques)} unique techniques")
    print(f"Average Risk Score: {sum(item['detail']['findings'][0]['ThreatModel']['risk_score'] for item in updated_findings) / len(updated_findings):.1f}")


if __name__ == '__main__':
    main()
