##LooksSus – A System State Monitoring Project


## Overview
This project detects security configuration drift in systems by comparing a secure baseline
with the current system state. It is designed for ERP and payment systems where silent
misconfigurations can lead to security risks.

## Features
- Detects open network ports
- Detects administrator user changes
- Checks firewall status
- Compares current state with baseline
- Alerts on configuration drift

## Use Case
- ERP systems
- Payment platforms
- Financial servers
- Security auditing

## Technologies Used
- Python
- System Commands
- JSON

## How It Works
1. Create a secure baseline
2. Make system changes (open ports, add admin, etc.)
3. Compare current system with baseline
4. Detect drift

## Demo Commands
```bash
python baseline.py
python compare.py
