import json
import subprocess
import platform
import shutil

BASELINE_FILE = "baseline_report.json"


def load_baseline():
    try:
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[!] Baseline file not found. Run baseline.py first.")
        exit(1)


def get_current_admins():
    os_name = platform.system().lower()

    # Windows admin check
    if os_name == "windows":
        try:
            output = subprocess.check_output(
                "net localgroup administrators",
                shell=True,
                stderr=subprocess.DEVNULL
            ).decode()
            return output.strip()
        except subprocess.CalledProcessError:
            return "ERROR: Unable to fetch Windows administrators"

    # Linux admin (sudo users)
    elif os_name == "linux":
        if shutil.which("getent"):
            try:
                output = subprocess.check_output(
                    "getent group sudo",
                    shell=True,
                    stderr=subprocess.DEVNULL
                ).decode()
                return output.strip()
            except subprocess.CalledProcessError:
                return "ERROR: Unable to fetch sudo group"
        else:
            return "ERROR: getent command not found"

    else:
        return "Unsupported OS"


def compare_admins(baseline_admins, current_admins):
    if baseline_admins == current_admins:
        return "No Drift Detected"
    else:
        return "Admin Drift Detected"


def main():
    baseline = load_baseline()

    baseline_admins = baseline.get("admins", "")
    current_admins = get_current_admins()

    result = compare_admins(baseline_admins, current_admins)

    print("\n--- Drift Analysis ---")
    print(result)

    if result != "No Drift Detected":
        print("\n[Baseline Admins]")
        print(baseline_admins)

        print("\n[Current Admins]")
        print(current_admins)


if __name__ == "__main__":
    main()
