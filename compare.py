import json
import subprocess

with open("baseline.json", "r") as f:
    baseline = json.load(f)

current_ports = subprocess.check_output("netstat -an", shell=True).decode()
current_admins = subprocess.check_output(
    "net localgroup administrators", shell=True
).decode()

drift_found = False
risk_score = 0

print("\n--- Drift Analysis ---\n")

baseline_ports = set(baseline["open_ports"])

current_result = subprocess.check_output("netstat -an", shell=True).decode()
current_ports = set(
    line.strip() for line in current_result.splitlines()
    if "LISTENING" in line
)

new_ports = current_ports - baseline_ports

if new_ports:
    drift_found = True
    risk_score += 40
    print("[!] New open ports detected:")
    for p in new_ports:
        print("    ", p)
