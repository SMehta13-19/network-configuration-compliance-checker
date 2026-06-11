"""
Compliance Checker Module - Main compliance checking engine
"""
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from src.device_connector import DeviceConnector
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComplianceChecker:
    """Main compliance checking engine"""
    
    def __init__(self, rules_file='config/rules.json'):
        try:
            with open(rules_file, 'r') as f:
                self.rules = json.load(f)['rules']
            logger.info(f"Loaded {len(self.rules)} compliance rules")
        except FileNotFoundError:
            logger.error(f"Rules file not found: {rules_file}")
            self.rules = []
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in rules file: {e}")
            self.rules = []
        
        self.results = []
        
    def check_rule(self, command_output, rule):
        """Check a single rule against command output"""
        pattern = rule['regex_pattern']
        expected = rule['expected_value']
        comparison = rule.get('comparison', 'exact')
        
        # Handle empty output
        if not command_output:
            return {
                'status': 'FAIL',
                'actual': 'NO_OUTPUT',
                'expected': expected,
                'message': f"Command returned no output for rule: {rule['name']}"
            }
        
        # Search for pattern
        try:
            match = re.search(pattern, command_output, re.IGNORECASE | re.MULTILINE)
        except re.error as e:
            return {
                'status': 'ERROR',
                'actual': 'INVALID_REGEX',
                'expected': expected,
                'message': f"Invalid regex pattern: {e}"
            }
        
        # Handle no match
        if not match:
            if comparison == 'absent':
                return {
                    'status': 'PASS',
                    'actual': 'NOT_FOUND',
                    'expected': expected,
                    'message': f"Pattern not found (expected absent) - GOOD"
                }
            return {
                'status': 'FAIL',
                'actual': 'NOT_FOUND',
                'expected': expected,
                'message': f"Pattern '{pattern}' not found in output"
            }
        
        # Extract actual value
        actual = match.group(1) if match.groups() else 'present'
        
        # Compare based on comparison type
        try:
            if comparison == 'exact':
                passed = str(actual).strip() == str(expected).strip()
            elif comparison == 'less_equal':
                passed = int(actual) <= int(expected)
            elif comparison == 'greater_equal':
                passed = int(actual) >= int(expected)
            elif comparison == 'present':
                passed = True
            elif comparison == 'absent':
                passed = False  # Found when it should be absent = FAIL
            else:
                passed = False
            
            # For absent comparison, we need to flip logic
            if comparison == 'absent':
                passed = False  # Found something that should be absent
                actual = f"FOUND: {actual}"
        except (ValueError, TypeError) as e:
            passed = False
            actual = f"COMPARISON_ERROR: {actual}"
        
        return {
            'status': 'PASS' if passed else 'FAIL',
            'actual': str(actual),
            'expected': str(expected),
            'message': f"Actual: {actual}, Expected: {expected} (comparison: {comparison})"
        }
    
    def check_device(self, device_info):
        """Check compliance for a single device"""
        device_result = {
            'hostname': device_info.get('host', device_info.get('ip', 'Unknown')),
            'timestamp': datetime.now().isoformat(),
            'rules': [],
            'overall_status': 'PASS',
            'passed_rules': 0,
            'failed_rules': 0,
            'error_rules': 0
        }
        
        connector = DeviceConnector(device_info)
        
        if not connector.connect():
            device_result['overall_status'] = 'CONNECTION_FAILED'
            device_result['error'] = 'Could not establish SSH connection'
            logger.error(f"Connection failed for {device_result['hostname']}")
            return device_result
        
        logger.info(f"Checking compliance on {device_result['hostname']}")
        
        for rule in self.rules:
            try:
                # Send command to device
                output = connector.send_command(rule['command'])
                
                # Check rule compliance
                rule_result = self.check_rule(output, rule)
                
                # Add metadata
                rule_result['rule_id'] = rule['id']
                rule_result['rule_name'] = rule['name']
                rule_result['severity'] = rule['severity']
                rule_result['command'] = rule['command']
                rule_result['description'] = rule.get('description', '')
                
                device_result['rules'].append(rule_result)
                
                # Update counters
                if rule_result['status'] == 'PASS':
                    device_result['passed_rules'] += 1
                elif rule_result['status'] == 'FAIL':
                    device_result['failed_rules'] += 1
                    if rule['severity'] == 'HIGH':
                        device_result['overall_status'] = 'FAIL'
                else:
                    device_result['error_rules'] += 1
                    device_result['overall_status'] = 'PARTIAL'
                    
            except Exception as e:
                logger.error(f"Rule check failed for {rule['id']} on {device_result['hostname']}: {str(e)}")
                device_result['rules'].append({
                    'rule_id': rule['id'],
                    'rule_name': rule['name'],
                    'status': 'ERROR',
                    'message': str(e)
                })
                device_result['error_rules'] += 1
        
        connector.disconnect()
        logger.info(f"Completed check for {device_result['hostname']} - Passed: {device_result['passed_rules']}, Failed: {device_result['failed_rules']}")
        
        return device_result
    
    def check_devices_concurrent(self, devices_list, max_workers=5):
        """Check multiple devices concurrently"""
        self.results = []
        
        logger.info(f"Starting concurrent checks on {len(devices_list)} devices with {max_workers} workers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_device = {
                executor.submit(self.check_device, device): device 
                for device in devices_list
            }
            
            for future in as_completed(future_to_device):
                device = future_to_device[future]
                try:
                    result = future.result()
                    self.results.append(result)
                except Exception as e:
                    logger.error(f"Failed to check {device.get('host', 'Unknown')}: {str(e)}")
                    self.results.append({
                        'hostname': device.get('host', 'Unknown'),
                        'error': str(e),
                        'overall_status': 'ERROR'
                    })
        
        return self.results
    
    def print_summary(self):
        """Print summary statistics to terminal"""
        if not self.results:
            print("\nNo results to display")
            return
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get('overall_status') == 'PASS')
        failed = sum(1 for r in self.results if r.get('overall_status') == 'FAIL')
        conn_failed = sum(1 for r in self.results if r.get('overall_status') == 'CONNECTION_FAILED')
        partial = sum(1 for r in self.results if r.get('overall_status') == 'PARTIAL')
        errors = sum(1 for r in self.results if r.get('overall_status') == 'ERROR')
        
        print("\n" + "="*70)
        print("COMPLIANCE CHECK SUMMARY REPORT")
        print("="*70)
        print(f"Total Devices Checked:     {total}")
        print(f"✅ Fully Compliant:        {passed}")
        print(f"❌ Non-Compliant:          {failed}")
        print(f"⚠️  Partial Compliance:    {partial}")
        print(f"🔌 Connection Failed:      {conn_failed}")
        print(f"💥 Errors:                 {errors}")
        print(f"\nCompliance Rate: {(passed/total)*100:.1f}%" if total > 0 else "N/A")
        print("="*70)
        
        # Detailed device status
        print("\n📊 DEVICE DETAILS:")
        print("-"*70)
        for result in self.results:
            status_icon = {
                'PASS': '✅',
                'FAIL': '❌',
                'CONNECTION_FAILED': '🔌',
                'PARTIAL': '⚠️',
                'ERROR': '💥'
            }.get(result.get('overall_status'), '❓')
            
            print(f"\n{status_icon} {result['hostname']}: {result.get('overall_status', 'UNKNOWN')}")
            
            if 'passed_rules' in result:
                print(f"   📈 Rules: {result['passed_rules']} passed, {result['failed_rules']} failed, {result['error_rules']} errors")
            
            # Show failed high-severity rules
            if result.get('rules'):
                high_failures = [r for r in result['rules'] 
                               if r.get('status') == 'FAIL' and r.get('severity') == 'HIGH']
                if high_failures:
                    print(f"   🔴 HIGH SEVERITY FAILURES:")
                    for rule in high_failures[:3]:  # Show top 3
                        print(f"      - {rule.get('rule_name')}: {rule.get('message', 'No details')[:60]}")
        
        print("\n" + "="*70)