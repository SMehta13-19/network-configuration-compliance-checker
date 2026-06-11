import csv
from datetime import datetime
import os

class ReportGenerator:
    """Generates CSV reports from compliance results"""
    
    @staticmethod
    def generate_csv_report(results, output_dir='reports'):
        """Generate detailed CSV report"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/compliance_report_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [
                'hostname', 'timestamp', 'rule_id', 'rule_name', 'severity',
                'command', 'status', 'actual', 'expected', 'message'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for device_result in results:
                if 'rules' not in device_result:
                    continue
                    
                for rule_result in device_result['rules']:
                    row = {
                        'hostname': device_result['hostname'],
                        'timestamp': device_result.get('timestamp', ''),
                        'rule_id': rule_result.get('rule_id', ''),
                        'rule_name': rule_result.get('rule_name', ''),
                        'severity': rule_result.get('severity', ''),
                        'command': rule_result.get('command', ''),
                        'status': rule_result.get('status', ''),
                        'actual': rule_result.get('actual', ''),
                        'expected': rule_result.get('expected', ''),
                        'message': rule_result.get('message', '')
                    }
                    writer.writerow(row)
        
        print(f"\n📊 CSV Report generated: {filename}")
        return filename
    
    @staticmethod
    def generate_summary_csv(results, output_dir='reports'):
        """Generate summary CSV with device-level results"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/summary_report_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['hostname', 'overall_status', 'timestamp', 'error']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for device_result in results:
                row = {
                    'hostname': device_result.get('hostname', ''),
                    'overall_status': device_result.get('overall_status', ''),
                    'timestamp': device_result.get('timestamp', ''),
                    'error': device_result.get('error', '')
                }
                writer.writerow(row)
        
        print(f"📊 Summary Report generated: {filename}")
        return filename