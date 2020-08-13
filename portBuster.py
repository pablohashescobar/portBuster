#!/usr/bin/env python3

#------------------------------------------------DISCLAIMER----------------------------------------------------------
#
#Usage of this tool for attacking targets without 
#prior mutual consent is illegal. It is the end user’s responsibility
#to obey all applicable local, state and federal laws.
#I assume no liability and are not responsible for any misuse or damage caused by this tool.
#
#--------------------------------------------------------------------------------------------------------------------

import socket
import sys
import os
import threading
from queue import Queue
import time
import subprocess
import pyfiglet
import json
import pingparsing
from datetime import datetime


print_lock = threading.Lock()
toolbar_width = 40
open_ports = []
nmap_ports = []
host  = ""
ping = 1
threads = 200
#get user input
def get_arguments():
    ascii_banner = pyfiglet.figlet_format("Port Buster")
    print(ascii_banner)
    print("="*100)
    print("Enter the required values..")
    print()
    host = input("Target Machine IP Address: ")
    ping = int(input("Ping Scan (0 or 1): "))
    threads = int(input("Amount of threads : "))
    return host, ping, threads


#ping scan
def ping_scan(host):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = host
    transmitter.count = 5
    try:
        result = transmitter.ping()
        output = json.loads(json.dumps(ping_parser.parse(result).as_dict()))
        return output["rtt_max"]*0.001 #return output in seconds
    except:
        pass

#Intro Banner
def intro(host, ping, threads):
    print("="*68 + " PORT BUSTER " +"="*69)
    print(f"Target machine set to: {host}")
    print(f"Ping is set to:        {ping}")
    print(f"Total threads set to:  {threads}")

#Progress Bar
def update_progress(progress):
    barLength = 40 # Modify this to change the length of the progress bar
    status = ""
 
    
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\r[{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress*100.0,2), status)
    sys.stdout.write(text)
    sys.stdout.flush()

#Port Scanner
def mapper(host, timeout, threads):
    print(
        f'Performing port scan on {host} with default timeout set to {str(timeout)}')
    print('='*100)
    def scanner(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(timeout)

        try:
           
            con = s.connect((host, port))
            
            with print_lock:
                print(f"     port {port} is OPEN")
                #Print the ports with the progress bar
                open_ports.append(str(port))
            if con: 
                con.close()
        except socket.error:
            pass
    #Threading
    def threader():
        while True:
            worker = q.get()
            scanner(worker)
            update_progress((worker/65535))
            q.task_done()

    q = Queue()

    for x in range(int(threads)):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()
  

    for worker in range(1, 65535):
        q.put(worker)
   

    q.join()


#Nmap
def nmap_scanner(host):
    print("="*150)
    mc_ports = ",".join(nmap_ports)
    print(f"Starting nmap scans on ports {mc_ports}")
    print("="*150)
    os.mkdir("nmap")
    subprocess.call(["nmap", "-p", mc_ports, "-A", "-oN", "nmap/initial", host])


#Print Ports
def print_open_ports(open_ports):
    
    port_list = [int(i) for i in (open_ports)]
    length = len(port_list)
    port_list.sort()
    print(f"Total {length} ports are open")
    print()
   
    for p in port_list:
        print(f"Port {p} is open")
        nmap_ports.append(str(p))

#Main
def main():
    host, ping, threads = get_arguments()

    intro(host, ping, threads)
    print("="*100)
    if int(ping):
        print('Starting Ping Scan...')

        timeout = ping_scan(host)

        if timeout == None:
            print("="*100)
            print("Target Machine isn't up or isn't responding to ping")
            print('Please try with -p 0 to skip ping scan')
            print('Quitting...')
        else:
            print(
                f'Ping scan finished average timeout: {round(timeout, 3)} ms')
            ans = input('Press y/n to set default timeout: ')
            timeout = round(timeout, 3)
            print('='*100)
            t1 = datetime.now()
            print(f'Starting Port scan on {t1}')
            
            # Port Scan
            if ans == 'y' or ans == 'Y':
                mapper(host, timeout, threads)
                print()
                t2 = datetime.now()
                print(f"Scan Completed in {t2-t1}")
                print('='*100)
                print_open_ports(open_ports)
                nmap_scanner(host)
            elif ans == 'n' or ans == 'N':
                timeout = None
                mapper(host, timeout, threads)
                print()
                t2 = datetime.now()
                print()
                print(f"Scan Completed {t2-t1}")
                print('='*100)
                print_open_ports(open_ports)
                nmap_scanner(host)
            else:
                print('Invalid Input')
    else:
        t1 = datetime.now()
        mapper(host, None, threads)
        print()
        t2 = datetime.now()
        print()
        print(f"Scan Completed {t2-t1}")
        print('='*100)
        print_open_ports(open_ports)
        nmap_scanner(host)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('Keyboard Interruption detected')
        sys.exit('Quitting....')