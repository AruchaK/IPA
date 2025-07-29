from netmiko import ConnectHandler
import time


DEVICES_IP = ["172.31.36.5"]
USERNAME = "admin"
PASSWORD = "cisco"

BASE_DEVICE_PARAMS = {
    "device_type": "cisco_ios",
    "username": USERNAME,
    "secret": PASSWORD,
    "use_keys": True,
    "key_file": "/home/devasc/.ssh/id_rsa",
    "allow_agent": False
}

COMMAND_SET_VLAN = [
    "vlan 101",
    "name control-data",
    "exit",
    "int range Gi0/1, Gi1/1",
    "switchport mode access",
    "switchport access vlan 101"
]

COMMAND_SET_OSPF_R1 = [
    "int lo0",
    "ip add 1.1.1.1 255.255.255.255",
    "router ospf 10 vrf control-data",
    "network 192.168.1.0 0.0.0.255 area 0",
    "network 192.168.3.0 0.0.0.255 area 0",
    "network 1.1.1.1 0.0.0.0 area 0"
]

COMMAND_SET_OSPF_R2 = [
    "int Gi0/3",
    "ip vrf forwarding control-data",
    "no shut",
    "ip add dhcp",
    "int lo0",
    "ip add 2.2.2.2 255.255.255.255",
    "exit",
    "ip route vrf control-data 0.0.0.0 0.0.0.0 192.168.122.1",
    "router ospf 10 vrf control-data",
    "network 192.168.2.0 0.0.0.255 area 0",
    "network 192.168.3.0 0.0.0.255 area 0",
    "network 2.2.2.2 0.0.0.0 area 0",
    "default-information originate always"
]

COMMAND_SET_PART2 = [
    "int g0/3",
    "ip nat outside",
    "int range Gi0/1-2",
    "ip nat inside",
    "exit",
    "access-list 1 permit 192.168.1.0 0.0.0.255",
    "access-list 1 permit 192.168.2.0 0.0.0.255",
    "access-list 1 permit 192.168.3.0 0.0.0.255",
    "ip nat inside source list 1 interface g0/3 vrf control-data overload"
]

COMMAND_SET_REMOTE = [
    "ip access-list standard SECURE-REMOTE",
    "permit 172.31.36.0 0.0.0.255",
    "permit 10.30.6.0 0.0.0.255",
    "deny any",
    "line vty 0 4",
    "access-class SECURE-REMOTE in",
    "transport input ssh telnet",
    "login local"
]

for ip in DEVICES_IP:
    print("Connecting to " + ip + "...")

    device_params = BASE_DEVICE_PARAMS.copy()
    device_params["ip"] = ip

    if ip == "172.31.36.3":
        command_set = COMMAND_SET_VLAN
    elif ip == "172.31.36.4":
        command_set = COMMAND_SET_OSPF_R1
    elif ip == "172.31.36.5":
        command_set = COMMAND_SET_OSPF_R2


    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        print("Connected to " + ip)
        result = ssh.send_config_set(command_set)
        print(f"Configuration result for {ip}:\n{result}")
        time.sleep(3)
        command_set = COMMAND_SET_REMOTE
        result = ssh.send_config_set(command_set)
        print(f"Configuration telnet/ssh result for {ip}:\n{result}")
        if device_params["ip"] == "172.31.36.5":
            command_set = COMMAND_SET_PART2
            result = ssh.send_config_set(command_set)
            print(f"PAT Configuration result for {ip}:\n{result}")
        time.sleep(1)
        print(ip + " Finished")
