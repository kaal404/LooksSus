import subprocess

def scan_ports():
    return subprocess.check_output("netstat -an", shell=True).decode()

def scan_admins():
    return subprocess.check_output("net localgroup administrators", shell=True).decode()

def scan_firewall():
    return subprocess.check_output("netsh advfirewall show allprofiles", shell=True).decode()

print("Current Open Ports:")
print(scan_ports())

print("\nAdmin Users:")
print(scan_admins())

print("\nFirewall Status:")
print(scan_firewall())
