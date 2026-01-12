import json
import subprocess
import platform
import shutil

BASELINE_FILE = "baseline_report.json"


def load_baseline():
    with open(BASELINE_FILE, "r") as f:
        return json.load(f)


def get_linux_admin_users():
    """
    Extract sudo users only (clean usernames)
    """
    if not shutil.which("getent"):
        return []

    output = subprocess.check_output(
        "getent group sudo",
        shell=True,
        stderr=subprocess.DEVNULL
    ).decode().strip()

    # Format: sudo:x:27:user1,user2
    if ":" in output:
        users_part = output.split(":")[-1]
        if users_part:
            return users_part.split(",")
    return []


def get_windows_admin_users():
    output = subprocess.check_output(
        "net localgroup administrators",
        shell=True,
        stderr=subprocess.DEVNULL
    ).decode()

    users = []
    for line in output.splitlines():
        line = line.strip()
        if line and not line.startswith(("Alias", "Comment", "Members", "---", "The command")):
            users.append(line)
    return users


def get_current_admin_users():
    os_name = platform.system().lower()

    if os_name == "linux":
        return get_linux_admin_users()
    elif os_name == "windows":
        return get_windows_admin_users()
    else:
        return []


def main():
    baseline = load_baseline()

    baseline_admins = sorted(baseline.get("admin_users", []))
    current_admins = sorted(get_current_admin_users())

    print("\n--- Drift Analysis ---")

    if baseline_admins == current_admins:
        print("No Drift Detected. System Secure.")
    else:
        print("Admin Drift Detected")

        print("\n[Baseline Admins]")
        for user in baseline_admins:
            print(f"- {user}")

        print("\n[Current Admins]")
        for user in current_admins:
            print(f"- {user}")


if __name__ == "__main__":
    main()
