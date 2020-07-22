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


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="host",
                      help="Target Host (required)")
    parser.add_option("-p", "--ping", dest="ping",
                      help="Ping The Host 0 or 1 default 1 (optional)")
    parser.add_option("-T", "--ping", dest="threads",
                      help="No. of threads default 100 (optional)")
    (options, arguments) = parser.parse_args()
    if not options.host:
        parser.error("[-] Please specify a target host")
    if not options.ping:
        options.ping = 1
    if not options.threads:
        options.threads = 100
    return options


def ping_scan(host):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = host
    transmitter.count = 5
    result = transmitter.ping()

    output = json.loads(json.dumps(ping_parser.parse(result).as_dict()))

    return output["rtt_max"]*0.001


def mapper(host, timeout):
    print(
        f'Performing port scan on {host} with default timeout set to {str(timeout)}')

    def scanner(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(timeout)
        try:
            con = s.connect((host, port))

            with print_lock:
                print(f'port {port} is open')
            con.close()
        except:
            pass

    def threader():
        while True:
            worker = q.get()
            scanner(worker)
            q.task_done()

    q = Queue()

    for x in range(500):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for worker in range(1, 65535):
        q.put(worker)

    q.join()


def main():
    options = get_arguments()
    host = options.host
    ping = options.ping
    threads = options.threads
    print('Starting Ping Scan')
    print("-"*60)
    timeout = round(ping_scan(host), 3)
    print(f'Ping scan finished timeout set to {round(timeout, 3)} ms')
    print('-'*60)
    ans = input('Press y/n to set default timeout: ')
    if ans == 'y' or ans == 'Y':
        print('Starting Port scan')
        mapper(host, timeout)
    elif ans == 'n' or ans == 'N':
        timeout = None
        mapper(host, timeout)
    else:
        print('Invalid Input')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Quitting')
        sys.exit()
