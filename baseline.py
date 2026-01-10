import subprocess
import platform
import json

def get_admin_users():
    system = platform.system()
    try:
        if system == "Windows":
            result = subprocess.check_output("net localgroup administrators", shell=True).decode()
            users = [line.strip() for line in result.splitlines() if line.strip() and line.strip() != "Administrators"]
            return users
        else:
            result = subprocess.check_output("getent group sudo", shell=True).decode()
            users = result.strip().split(":")[-1].split(",")
            return [u for u in users if u]
    except Exception as e:
        return [f"Error fetching admin users: {e}"]

def check_firewall():
    system = platform.system()
    try:
        if system == "Windows":
            result = subprocess.check_output("netsh advfirewall show allprofiles", shell=True).decode()
            return "ON" in result
        else:
            # Linux: check ufw safely
            result = subprocess.run("ufw status", shell=True, capture_output=True, text=True)
            return "active" in result.stdout.lower()
    except Exception:
        return "ufw not installed"

def check_disk_usage():
    try:
        if platform.system() == "Windows":
            return subprocess.check_output("wmic logicaldisk get size,freespace,caption", shell=True).decode()
        else:
            return subprocess.check_output("df -h --total", shell=True).decode()
    except Exception as e:
        return str(e)

def check_updates():
    if platform.system() != "Linux":
        return "Not applicable for Windows"
    try:
        result = subprocess.check_output("apt list --upgradable 2>/dev/null", shell=True).decode()
        lines = result.splitlines()
        # Only show first 10 upgradable packages to avoid huge output
        return lines[:10] if len(lines) > 10 else lines
    except Exception as e:
        return f"Error checking updates: {e}"

def main():
    report = {
        "admin_users": get_admin_users(),
        "firewall": check_firewall(),
        "disk_usage": check_disk_usage(),
        "pending_updates": check_updates()
    }

    # Print report
    print("=== Security Baseline Report ===\n")
    for key, value in report.items():
        print(f"{key}:")
        if isinstance(value, list):
            for v in value:
                print(f" - {v}")
        else:
            print(value)
        print()

    # Save report to JSON for users
    with open("baseline_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print("Report saved to baseline_report.json")

if __name__ == "__main__":
    main()
