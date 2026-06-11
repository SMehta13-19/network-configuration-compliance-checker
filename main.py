#!/usr/bin/env python3
"""
Network Configuration Compliance Checker
Main entry point for the application
"""

import csv
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.compliance_checker import ComplianceChecker
from src.report_generator import ReportGenerator

def load_devices_from_csv(csv_file='devices/devices.csv'):
    """Load device list from CSV file"""
    devices = []
    
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found!")
        print(f"   Please create the file with the following format:")
        print(f"   hostname,device_type,ip,username,password,port,secret")
        return []
    
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip empty rows
                if not row.get('ip'):
                    continue
                    
                device = {
                    'device_type': row.get('device_type', 'cisco_ios'),
                    'host': row.get('ip', '').strip(),
                    'ip': row.get('ip', '').strip(),
                    'username': row.get('username', '').strip(),
                    'password': row.get('password', '').strip(),
                    'port': int(row.get('port', 22)) if row.get('port') else 22,
                }
                
                # Add secret if provided
                if row.get('secret'):
                    device['secret'] = row.get('secret', '').strip()
                
                # Add hostname for display
                device['hostname'] = row.get('hostname', device['host'])
                
                if device['ip'] and device['username'] and device['password']:
                    devices.append(device)
                else:
                    print(f"⚠️  Warning: Skipping incomplete device entry: {row.get('hostname', 'Unknown')}")
        
        print(f"✓ Loaded {len(devices)} device(s) from {csv_file}")
        return devices
    except Exception as e:
        print(f"❌ Error reading {csv_file}: {e}")
        return []

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║     NETWORK CONFIGURATION COMPLIANCE CHECKER v1.0               ║
    ║     Python + Netmiko + Regex + CSV Reports                      ║
    ║                                                                  ║
    ║     Developed for Network Automation Portfolio                   ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Check for required files
    if not os.path.exists('config/rules.json'):
        print("❌ Error: config/rules.json not found!")
        print("   Please ensure the rules configuration file exists.")
        sys.exit(1)
    
    # Load devices
    devices = load_devices_from_csv()
    if not devices:
        print("\n❌ No valid devices found. Please check devices/devices.csv")
        print("\nExample CSV format:")
        print("hostname,device_type,ip,username,password,port,secret")
        print("R1,cisco_ios,192.168.1.1,admin,cisco123,22,enable123")
        sys.exit(1)
    
    print(f"\n📡 Found {len(devices)} device(s) to check")
    
    # Initialize checker
    try:
        checker = ComplianceChecker('config/rules.json')
    except Exception as e:
        print(f"❌ Failed to initialize compliance checker: {e}")
        sys.exit(1)
    
    # Run concurrent checks
    print("\n🔄 Running compliance checks concurrently...\n")
    print("-" * 70)
    
    try:
        results = checker.check_devices_concurrent(devices, max_workers=5)
        
        # Print summary
        checker.print_summary()
        
        # Generate reports
        report_gen = ReportGenerator()
        csv_file = report_gen.generate_csv_report(results)
        summary_file = report_gen.generate_summary_csv(results)
        
        print(f"\n✅ Compliance check complete!")
        if csv_file:
            print(f"   📄 Detailed Report: {csv_file}")
        if summary_file:
            print(f"   📊 Summary Report: {summary_file}")
        
        # Determine exit code
        failed_devices = sum(1 for r in results if r.get('overall_status') in ['FAIL', 'CONNECTION_FAILED'])
        if failed_devices > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()