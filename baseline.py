import subprocess
import platform
import os

# Function to get admin users (cross-platform)
def get_admin_users():
    system = platform.system()
    try:
        if system == "Windows":
            # Windows: list administrators
            result = subprocess.check_output("net localgroup administrators", shell=True).decode()
            users = [line.strip() for line in result.splitlines() if line.strip() and line.strip() != "Administrators"]
            return users
        else:
            # Linux: get users in sudo group
            result = subprocess.check_output("getent group sudo", shell=True).decode()
            users = result.strip().split(":")[-1].split(",")
            return [u for u in users if u]
    except Exception as e:
        print(f"Error fetching admin users: {e}")
        return []

# Function to check if firewall is enabled (cross-platform)
def check_firewall():
    system = platform.system()
    try:
        if system == "Windows":
            result = subprocess.check_output("netsh advfirewall show allprofiles", shell=True).decode()
            return "ON" in result
        else:
            # Linux: check ufw status
            result = subprocess.check_output("ufw status", shell=True).decode()
            return "active" in result.lower()
    except Exception as e:
        print(f"Error checking firewall: {e}")
        return False

# Function to check disk usage
def check_disk_usage():
    try:
        if platform.system() == "Windows":
            result = subprocess.check_output("wmic logicaldisk get size,freespace,caption", shell=True).decode()
            return result
        else:
            result = subprocess.check_output("df -h", shell=True).decode()
            return result
    except Exception as e:
        print(f"Error checking disk usage: {e}")
        return ""

# Function to check system updates (Linux only)
def check_updates():
    if platform.system() != "Linux":
        return "Not applicable for Windows"
    try:
        result = subprocess.check_output("apt list --upgradable", shell=True, stderr=subprocess.DEVNULL).decode()
        return result if result else "No updates available"
    except Exception as e:
        return f"Error checking updates: {e}"

# Main function to gather baseline info
def main():
    print("=== Security Baseline Report ===\n")
    
    print("Admin Users:")
    admins = get_admin_users()
    print(admins if admins else "No admin users found")
    print("\nFirewall Enabled:", check_firewall())
    
    print("\nDisk Usage:")
    print(check_disk_usage())
    
    print("\nPending Updates:")
    print(check_updates())

if __name__ == "__main__":
    main()
