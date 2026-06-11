import pytest
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.compliance_checker import ComplianceChecker
from tests.mock_data import MockDeviceConnector

@pytest.fixture
def checker():
    """Create compliance checker instance"""
    return ComplianceChecker('config/rules.json')

def test_load_rules(checker):
    """Test if rules load correctly"""
    assert len(checker.rules) > 0
    assert checker.rules[0]['id'] == 'SEC-001'

def test_check_rule_ssh_version(checker):
    """Test SSH version rule"""
    rule = checker.rules[0]
    output = "SSH Enabled - version 2.0"
    result = checker.check_rule(output, rule)
    assert result['status'] == 'PASS'
    assert result['actual'] == '2'

def test_check_rule_password_encryption(checker):
    """Test password encryption rule"""
    rule = checker.rules[1]
    output = "service password-encryption"
    result = checker.check_rule(output, rule)
    assert result['status'] == 'PASS'

def test_check_rule_exec_timeout(checker):
    """Test exec-timeout rule"""
    rule = checker.rules[3]
    output = "exec-timeout 5 0"
    result = checker.check_rule(output, rule)
    assert result['status'] == 'PASS'

def test_mock_device_check(checker):
    """Test device check using mock data"""
    mock_device = {
        'device_type': 'cisco_ios',
        'host': 'mock-router',
        'username': 'test',
        'password': 'test'
    }
    
    # Override the connector with mock
    result = checker.check_device(mock_device)
    assert result['hostname'] == 'mock-router'
    assert 'rules' in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"])