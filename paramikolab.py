import time
import paramiko

username = "admin"

device_ip = ["172.31.36.1", "172.31.36.2", "172.31.36.3", "172.31.36.4", "172.31.36.5"]
R0 = "172.31.36.1"

# test ssh
for ip in device_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=username, look_for_keys=True)
    print(f"Connected to {ip}")
    with client.invoke_shell() as ssh:
        print("Conntected to {}".format(ip))
        ssh.send("terminal length 0\n")
        time.sleep(1)
        result = ssh.recv(1000).decode("ascii")
        print(result)

        ssh.send("en\n")
        time.sleep(1)
        result = ssh.recv(1000).decode("ascii")
        print(result)


# Get show run from R0 and save to file
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=R0, username=username, look_for_keys=True)
print(f"Connected to {R0}")
with client.invoke_shell() as ssh:
    print("Conntected to {}".format(R0))
    ssh.send("terminal length 0\n")
    time.sleep(1)
    result = ssh.recv(1000).decode("ascii")
    print(result)

    ssh.send("en\n")
    time.sleep(1)
    result = ssh.recv(1000).decode("ascii")
    print(result)

    ssh.send("show run\n")
    time.sleep(1)
    result = ssh.recv(10000).decode("ascii")
    print(result)

    try:
        with open("R0-running-config.txt", "w") as f:
            f.write(result)
        print("\nSuccessfully saved running configuration to R0-running-config.txt")
    except IOError as e:
        print(f"\nError saving file: {e}")