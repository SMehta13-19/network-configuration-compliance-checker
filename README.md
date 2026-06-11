# 🔒 Network Configuration Compliance Checker

A Python-based Network Automation Tool that performs automated security compliance audits on Cisco network devices using SSH. The tool connects to multiple devices concurrently, validates configurations against predefined compliance rules, and generates detailed CSV reports.

---

## 📌 Overview

Network engineers often spend hours manually verifying device configurations to ensure they meet organizational security standards. This process is repetitive, time-consuming, and prone to human error.

The Network Configuration Compliance Checker automates this process by:

* Connecting to Cisco devices using SSH
* Executing compliance verification commands
* Validating outputs using Regex-based rules
* Generating detailed compliance reports
* Supporting concurrent checks across multiple devices

This project demonstrates practical Network Automation concepts using Python, Netmiko, JSON, Regex, and Multithreading.

---

## 🚀 Features

### ✅ Automated Compliance Validation

Checks device configurations against predefined security policies.

### ✅ SSH-Based Device Access

Uses Netmiko to securely connect to Cisco IOS devices.

### ✅ Concurrent Device Auditing

Uses ThreadPoolExecutor to audit multiple devices simultaneously.

### ✅ Dynamic Rule Engine

Compliance rules are stored in JSON and can be modified without changing the code.

### ✅ Regex-Based Verification

Flexible pattern matching allows validation of different configuration standards.

### ✅ CSV Report Generation

Creates both detailed and summary compliance reports.

### ✅ Error Handling & Retry Logic

Handles authentication failures, timeouts, and unreachable devices gracefully.

### ✅ Mock Testing Environment

Allows testing without requiring physical network devices.

---

## 🏗️ Project Architecture

```text
Network Configuration Compliance Checker
│
├── config/
│   └── rules.json
│
├── devices/
│   ├── devices.csv
│   └── devices.csv.example
│
├── reports/
│
├── src/
│   ├── compliance_checker.py
│   ├── device_connector.py
│   └── report_generator.py
│
├── tests/
│   ├── mock_data.py
│   └── test_compliance_checker.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Technologies Used

| Technology         | Purpose                     |
| ------------------ | --------------------------- |
| Python             | Core Development            |
| Netmiko            | SSH Connectivity            |
| Cisco IOS          | Device Platform             |
| Regex              | Configuration Validation    |
| JSON               | Compliance Rule Definitions |
| CSV                | Report Generation           |
| Pytest             | Unit Testing                |
| ThreadPoolExecutor | Concurrent Processing       |

---

## 📋 Compliance Checks Implemented

The tool currently validates:

### SSH Version Check

Ensures SSH Version 2 is enabled.

### Password Encryption

Verifies service password encryption is configured.

### Login Banner Verification

Checks for security warning banners.

### Console Timeout Validation

Ensures session timeout policies are enforced.

### SNMP Security Check

Detects insecure default SNMP community strings.

---

## 🛠 Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/network-configuration-compliance-checker.git
cd network-configuration-compliance-checker
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📝 Device Inventory Configuration

Edit:

```text
devices/devices.csv
```

Example:

```csv
hostname,device_type,ip,username,password,port,secret
R1,cisco_ios,192.168.1.1,admin,password123,22,enable123
R2,cisco_ios,192.168.1.2,admin,password123,22,enable123
```

---

## ▶️ Running the Application

```bash
python main.py
```

Example Output:

```text
✓ Loaded 2 devices

Running compliance checks...

R1: PASS
R2: FAIL

Compliance Report Generated Successfully
```

---

## 📊 Generated Reports

### Detailed Report

Contains:

* Device Name
* Rule ID
* Rule Status
* Severity
* Actual Value
* Expected Value
* Validation Message

### Summary Report

Contains:

* Device Name
* Overall Compliance Status
* Timestamp
* Error Details

---

## 🧪 Running Unit Tests

```bash
pytest tests/
```

Or run mock testing:

```bash
python test_mock.py
```

---

## 🎯 Skills Demonstrated

* Network Automation
* Python Programming
* Cisco IOS Operations
* SSH Automation
* Multithreading
* Regex Pattern Matching
* OOP Design
* JSON Data Processing
* CSV Report Generation
* Software Testing

---

## 📈 Future Enhancements

* HTML Dashboard Reporting
* Email Alert Notifications
* YAML-Based Configuration Support
* REST API Integration
* Multi-Vendor Device Support (Cisco, Juniper, Arista)
* Compliance Score Visualization

---

## 👨‍💻 Author

Harshibar Mehta

Electronics Engineering Student | CCNA Certified

Interested in Network Automation, Network Engineering, and Infrastructure Automation.

---

## 📄 License

This project is released under the MIT License.
