\# Network Configuration Compliance Checker 🔒



\[!\[Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)

\[!\[Netmiko](https://img.shields.io/badge/Netmiko-4.7+-green.svg)](https://github.com/ktbyers/netmiko)

\[!\[License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)



A production-ready network automation tool that validates device configurations against security compliance rules. Built for network engineers to automate compliance checking across multiple devices.



\## 🎯 Problem Solved



Manual network compliance checking is:

\- ⏱️ \*\*Time-consuming\*\* - 4+ hours for 50 devices

\- ❌ \*\*Error-prone\*\* - Human misses critical misconfigurations

\- 📋 \*\*Inconsistent\*\* - Different engineers apply different standards



\*\*This tool automates the entire process\*\* - 50 devices in under 5 minutes with consistent, accurate results.



\## ✨ Features



| Feature           | Description                                         |

|-------------------|-----------------------------------------------------|

|\*\*Multi-threaded\*\* | Check 50+ devices concurrently (5-10x faster)       |

|\*\*Dynamic Rules\*\*  | JSON-based rules - update without code changes      |

|\*\*CSV Reports\*\*    | Detailed compliance reports with pass/fail analysis |

|\*\*Regex Patterns\*\* | Flexible configuration validation                   |

|\*\*Mock Testing\*\*   | Test without physical lab devices                   |

|\*\*Error Handling\*\* | Graceful failure handling with retry logic          |



\## 🏗️ System Architecture



\### Component Details



| Layer          | Component          | Technology         | Responsibility                             |

|----------------|--------------------|--------------------|--------------------------------------------|

| \*\*Input\*\*      | Device Inventory   | CSV                | Stores device hostnames, IPs, credentials  |

| \*\*Input\*\*      | Rules Engine       | JSON               | Defines compliance rules and expectations  |

| \*\*Processing\*\* | Connection Manager | Netmiko            | Handles SSH connections to network devices |

| \*\*Processing\*\* | Thread Pool        | concurrent.futures | Manages concurrent device checks           |

| \*\*Processing\*\* | Regex Engine       | Python `re`        | Pattern matching on device outputs         |

| \*\*Output\*\*     | Report Generator   | CSV module         | Creates detailed compliance reports        |

| \*\*Output\*\*     | Terminal UI        | Print/logging      | Displays real-time progress and summary    |





\## 📋 Prerequisites



\- Python 3.8+

\- Network devices with SSH access

\- Device credentials (read-only recommended)



\## 🛠️ Installation



```bash

\# Clone repository

git clone https://github.com/YOUR\_USERNAME/network-compliance-checker.git

cd network-compliance-checker



\# Install dependencies

pip install -r requirements.txt



\# Configure devices (copy example and edit)

cp devices/devices.csv.example devices/devices.csv

\# Edit devices.csv with your device information



\# Run compliance check

python main.py

