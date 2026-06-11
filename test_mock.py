"""Test compliance checker with mock data - No network required!"""
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import your checker
from src.compliance_checker import ComplianceChecker

# Mock device responses
MOCK_RESPONSES = {
    "show ip ssh": "SSH Enabled - version 2.0",
    "show running-config | include service password-encryption": "service password-encryption",
    "show running-config | include banner": "banner motd ^C Welcome ^C",
    "show running-config | include exec-timeout": "exec-timeout 10 0",
    "show running-config | include snmp-server community": "",
}

def test_with_mock_data():
    """Test compliance rules with mock data"""
    print("\n" + "="*60)
    print("COMPLIANCE CHECKER - MOCK TEST MODE")
    print("Testing without network devices")
    print("="*60)
    
    # Load rules
    with open('config/rules.json', 'r') as f:
        rules = json.load(f)['rules']
    
    checker = ComplianceChecker('config/rules.json')
    
    print("\n📋 Testing each rule with mock data:\n")
    
    results = []
    for rule in rules:
        command = rule['command']
        mock_output = MOCK_RESPONSES.get(command, "")
        
        print(f"Rule: {rule['id']} - {rule['name']}")
        print(f"  Command: {command}")
        print(f"  Mock Output: {mock_output[:80]}...")
        
        result = checker.check_rule(mock_output, rule)
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        
        print(f"  {status_icon} Status: {result['status']}")
        print(f"  Message: {result.get('message', 'N/A')}")
        print()
        
        results.append(result)
    
    # Summary
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    
    print("="*60)
    print(f"TEST SUMMARY: {passed} PASSED, {failed} FAILED")
    print("="*60)
    
    return results

if __name__ == "__main__":
    test_with_mock_data()