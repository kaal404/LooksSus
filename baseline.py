import subprocess
import json
import datetime

def get_open_ports():
    result = subprocess.check_output("netstat -an", shell=True).decode()
    ports = []
    for line in result.splitlines():
        if "LISTENING" in line:
            ports.append(line.strip())
    return ports

def get_admin_users():
    result = subprocess.check_output("net localgroup administrators", shell=True).decode()
    users = []
    for line in result.splitlines():
        if line.strip() and "----" not in line and "command" not in line.lower():
            users.append(line.strip())
    return users

def get_firewall_status():
    result = subprocess.check_output(
        "netsh advfirewall show allprofiles",
        shell=True
    ).decode()
    return result

baseline_data = {
    "timestamp": str(datetime.datetime.now()),
    "open_ports": get_open_ports(),
    "admin_users": get_admin_users(),
    "firewall_status": get_firewall_status()
}

with open("baseline.json", "w") as f:
    json.dump(baseline_data, f, indent=4)

print("Baseline created successfully.")
