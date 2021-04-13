from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException
from netmiko.ssh_exception import NetMikoAuthenticationException
from getpass import getpass
from queue import Queue
import threading
ip = '192.168.X.X'
device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': 'user',
        'password': 'Password',
        'secret' : 'Password'
    }
try:
    Connect = ConnectHandler(**device)
    print(Connect.find_prompt())
    Connect.enable()
    print(Connect.find_prompt())
    Command = Connect.send_command_timing("terminal datadump")
    Command1 = Connect.send_command("sh run")
    print(Command1)
    file = open(ip +'_config.txt', 'w')
    file.write(Command1)
except (NetMikoAuthenticationException, NetMikoAuthenticationException) as error:
    print(error)
