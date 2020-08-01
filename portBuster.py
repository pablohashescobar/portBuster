import socket
import sys
import threading
from queue import Queue
import time
import subprocess
import optparse
import json
import pingparsing

print_lock = threading.Lock()
toolbar_width = 40
open_ports = []

#get user input
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="host",
                      help="Target Host (required)")
    parser.add_option("-p", "--ping", dest="ping",
                      help="Ping The Host 0 or 1 default 1 (optional)")
    parser.add_option("-T", "--threads", dest="threads",
                      help="No. of threads default 200 (optional)")
    (options, arguments) = parser.parse_args()
    if not options.host:
        parser.error(
            "[-] Please specify a target host as -t <TARGET_MACHINE_IP>")
    if not options.ping:
        options.ping = 1
    if not options.threads:
        options.threads = 200
    return options

#ping scan
def ping_scan(host):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = host
    transmitter.count = 5
    try:
        result = transmitter.ping()
        output = json.loads(json.dumps(ping_parser.parse(result).as_dict()))
        return output["rtt_max"]*0.001
    except:
        pass

#Banner
def intro(host, ping, threads):
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

    def scanner(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(timeout)

        try:
           
            con = s.connect((host, port))
            
            with print_lock:
                print(f"port {port} is OPEN")

                open_ports.append(port)
            if con: 
                con.close()
        except socket.error:
            pass

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
    # setup toolbar

    for worker in range(1, 65535):
        q.put(worker)
   

    q.join()

#Main
def main():
    options = get_arguments()
    host = options.host
    ping = options.ping
    threads = options.threads
    intro(host, ping, threads)
    print("-"*60)
    if int(ping):
        print('Starting Ping Scan...')

        timeout = ping_scan(host)

        if timeout == None:
            print("-"*60)
            print("Target Machine isn't up or isn't responding to ping")
            print('Please try with -p 0 to skip ping scan')
            print('Quitting...')
        else:
            print(
                f'Ping scan finished average timeout: {round(timeout, 3)} ms')
            ans = input('Press y/n to set default timeout: ')
            timeout = round(timeout, 3)
            print('-'*60)
            # Port Scan
            if ans == 'y' or ans == 'Y':
                print('Starting Port scan')
                mapper(host, timeout, threads)
                print(open_ports)
            elif ans == 'n' or ans == 'N':
                timeout = None
                mapper(host, timeout, threads)
                print(open_ports)
            else:
                print('Invalid Input')
    else:
        mapper(host, None, threads)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('Keyboard Interruption detected')
        sys.exit('Quitting....')
