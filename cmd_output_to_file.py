from netmiko import Netmiko
from netmiko.ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException
from getpass import getpass
from pprint import pprint
import signal
import os
from queue import Queue
import threading

ip_addrs_file = open('ListOfIPs.txt')
ip_addrs = ip_addrs_file.read().splitlines()
num_threads = 8
enclosure_queue = Queue()
print_lock = threading.Lock()
command = "sh ver"

def deviceconnector(i,q):
    while True:
        print("{}: Waiting for IP address...".format(i))
        ip = q.get()
        print("{}: Acquired IP: {}".format(i,ip))
        device_dict =  {
            'host': ip,
            'username': 'user',
            'password': 'pass',
            'device_type': 'cisco_ios',
            'secret' : 'secret'
        }

        try:
            net_connect = Netmiko(**device_dict)
        except NetMikoTimeoutException:
            with print_lock:
                print("\n{}: ERROR **** Connection to {} timed-out.\n".format(i,ip))
            q.task_done()
            continue
        except NetMikoAuthenticationException:
            with print_lock:
                print("\n{}: ERROR **** Authenticaftion failed for {}. Stopping script. \n".format(i,ip))
            q.task_done()
            
        output = net_connect.send_command(command)
        with print_lock:
            print("{}: Printing ...".format(i))
            pprint(output)
            file = open(ip +'_config.txt', 'w')
            file.write(output)
            file.close()
            
        net_connect.disconnect

        q.task_done()

def main():

    for i in range(num_threads):
        thread = threading.Thread(target=deviceconnector, args=(i,enclosure_queue,))
        thread.setDaemon(True)
        thread.start()

    for ip_addr in ip_addrs:
        enclosure_queue.put(ip_addr)

    enclosure_queue.join()
    print("**** End ****")

if __name__ == '__main__':
    
    main()
