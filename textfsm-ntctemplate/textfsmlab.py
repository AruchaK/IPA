import textfsm
import os
from netmiko import ConnectHandler
from pathlib import Path
from typing import Dict, Any, List


def get_base_device_params(ip: str, username: str = "admin", password: str = "cisco") -> Dict[str, Any]:
    """Base device parameters for connecting to a Cisco IOS device using password auth."""
    return {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": username,
        "password": password,
        "secret": password,
    }

TEMPLATE_PATH = os.getenv("NTC_TEMPLATES_PATH", "templates")

def get_interface_descriptions(interfaces_description_output: str) -> Dict[str, str]:
    """
    Parses the output of 'show interfaces description' and returns a dictionary
    of interfaces and their descriptions.
    """
    template_path = Path(TEMPLATE_PATH) / "cisco_ios_show_interfaces_description.template"
    if not template_path.is_file():
        raise FileNotFoundError(f"Template file not found at: {template_path}")

    with open(template_path) as template_file:
        fsm = textfsm.TextFSM(template_file)
        parsed_data: List[List[str]] = fsm.ParseText(interfaces_description_output)

    descriptions = {}
    for row in parsed_data:
        interface = row[0]
        description = row[3]
        if description != "":
            descriptions[interface] = description

    return descriptions

def generate_interface_descriptions(cdp_output: str, device_ip: str = None):
    template_path = Path(TEMPLATE_PATH) / "cisco_ios_show_cdp_neighbors.template"
    if not template_path.is_file():
        raise FileNotFoundError(f"Template file not found at: {template_path}")

    with open(template_path) as template_file:
        fsm = textfsm.TextFSM(template_file)
        parsed_data = fsm.ParseText(cdp_output)

    descriptions = {}

    for row in parsed_data:
        remote_device = row[0]
        local_intf = row[1]
        remote_intf = row[3] + " " + row[4]

        if "PC" in remote_device:
            descriptions[local_intf] = "Connect to PC"
        elif remote_device == "DHCP":
            descriptions[local_intf] = "Connect to WAN"
        else:
            descriptions[local_intf] = f"Connect to {remote_intf} of {remote_device}"

    live_int_desc_output = get_int_desc_from_device(device_ip)

    show_interface_description = get_interface_descriptions(live_int_desc_output)

    descriptions.update(show_interface_description)

    return descriptions

def get_int_desc_from_device(ip: str) -> str:
    """
    Execute 'show interfaces description' and get existing descriptions.
    """
    device_params = get_base_device_params(ip)
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        int_desc_output = ssh.send_command("show interfaces description")
        return int_desc_output


def get_cdp_from_device(ip: str) -> str:
    """
    Connects to a network device and retrieves the output of 'show cdp neighbors'.
    """
    device_params = get_base_device_params(ip)
    print("Connecting to " + ip)
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        print(f"Connected to {ip}")
        cdp_output = ssh.send_command("show cdp neighbors")
        return cdp_output
    
if __name__ == "__main__":
    device_ip = "172.31.36.5"
    live_cdp_output = get_cdp_from_device(device_ip)

    if "Error" in live_cdp_output:
        print(live_cdp_output)
    else:
        interface_descriptions = generate_interface_descriptions(live_cdp_output)
        print(interface_descriptions)