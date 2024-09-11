import socket
import psutil
import uuid
import platform
import subprocess
import json

def check_system_components():
    # List of components to check
    components = [
        "Mac address", "Motherboard", "HDD", "SSD",
        "IP Address", "Network Card / MAC", "Router",
        "Other HWID keys on your PC", "Monitor",
        "Peripherals", "MacOS unique identifiers"
    ]

    # Simulate gathering system information
    system_info = {}
    system_info["Mac address"] = get_mac_address()
    system_info["Motherboard"] = get_motherboard_info()
    system_info["HDD"] = psutil.disk_usage('/').total
    system_info["SSD"] = check_if_ssd()
    system_info["IP Address"] = get_ip_address()
    system_info["Network Card / MAC"] = get_network_card_info()
    system_info["Router"] = get_router_info()
    system_info["Other HWID keys on your PC"] = get_hwid_keys()
    system_info["Monitor"] = get_monitor_info()
    system_info["Peripherals"] = get_peripherals_info()
    system_info["MacOS unique identifiers"] = get_macos_unique_ids()

    return system_info

def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                    for elements in range(0, 2*6, 2)][::-1])
    return mac

def get_motherboard_info():
    if platform.system() == "Darwin":  # MacOS platform identifier
        try:
            output = subprocess.check_output("ioreg -l | grep board-id", shell=True).decode()
            return output.split('"')[-2]  # Extract the motherboard ID
        except subprocess.CalledProcessError:
            return "Could not retrieve motherboard info"
    else:
        return "Unavailable on non-MacOS platforms"

def check_if_ssd():
    if platform.system() == "Darwin":  # For MacOS
        try:
            output = subprocess.check_output(["system_profiler", "SPSerialATADataType"], universal_newlines=True)
            if "Solid State" in output:
                return True
            return False
        except Exception:
            return "Could not determine if SSD or not"
    else:
        return "Unavailable on non-MacOS platforms"

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_network_card_info():
    net_cards = psutil.net_if_addrs()
    net_info = {}
    for interface_name, interface_addresses in net_cards.items():
        net_info[interface_name] = {}  # Initialize the dictionary for each interface
        for address in interface_addresses:
            if address.family == socket.AF_INET:
                net_info[interface_name]["IP"] = address.address
            elif address.family == psutil.AF_LINK:
                net_info[interface_name]["MAC"] = address.address
    return net_info


def get_router_info():
    if platform.system() == "Darwin":  # MacOS specific command to get the router IP
        try:
            output = subprocess.check_output("netstat -rn | grep 'default'", shell=True).decode().split()
            router_ip = output[1]
            return router_ip
        except Exception:
            return "Could not retrieve router information"
    else:
        return "Unavailable on non-MacOS platforms"

def get_hwid_keys():
    hwid = uuid.UUID(int=uuid.getnode())
    return str(hwid)

def get_monitor_info():
    if platform.system() == "Darwin":  # MacOS specific command to get monitor info
        try:
            output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"], universal_newlines=True)
            return output
        except subprocess.CalledProcessError:
            return "Could not retrieve monitor info"
    else:
        return "Unavailable on non-MacOS platforms"

def get_peripherals_info():
    if platform.system() == "Darwin":
        try:
            output = subprocess.check_output(["system_profiler", "SPUSBDataType"], universal_newlines=True)
            return output
        except subprocess.CalledProcessError:
            return "Could not retrieve peripherals info"
    else:
        return "Unavailable on non-MacOS platforms"

def get_macos_unique_ids():
    if platform.system() == "Darwin":  # MacOS unique identifier
        return uuid.UUID(int=uuid.getnode()).hex
    return "Not available on non-MacOS platforms"

# Simulating the system component check
system_components_info = check_system_components()
print(json.dumps(system_components_info, indent=4))
