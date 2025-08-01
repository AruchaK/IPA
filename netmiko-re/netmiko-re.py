from netmiko import ConnectHandler
import time
from pathlib import Path
import re

def matchRegex(output : str, reg=None):
    '''RegEx Search'''
    temp = output.split("\n")
    output = temp
    ans = []
    if reg is None:
        reg = input("Input your pattern that want to search: ")
    for searchTerm in output:
        match = re.search(reg, searchTerm)
        if match:
            ans.append(match.groups())
    return ans
    

def connectDevice(ip : str, username="admin", password="cisco", command=None):
    '''Connect to Cisco device with IP, username and password (you can choose your username and password)'''
    BASE_DEVICE_PARAMS = {
        "device_type": "cisco_ios",
        "username": username,
        "secret": password,
        "use_keys": True,
        "key_file": str(Path.home() / ".ssh" / "id_rsa"),
        "allow_agent": False
    }

    print(f"Connecting to {ip}...")

    device_params = BASE_DEVICE_PARAMS.copy()
    device_params["ip"] = ip

    if command is None:
        command = input("(Global Configuration Mode) Input your command: ")
    command_set = str(command)

    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        print(f"Connected to {ip}")
        result = ssh.send_config_set(command_set)
        temp = matchRegex(result)
        result = temp
        print(f"Configuration result for {ip}:\n{result}")
        time.sleep(2)
        print(f"Finished configuration for {ip}")

# connectDevice("172.31.36.5")