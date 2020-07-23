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
    parser.add_option("-T", "--threads", dest="threads",
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


def intro(host, ping, threads):
    print(f"Target machine set to: {host}")
    print(f"Ping is set to:        {ping}")
    print(f"Total threads set to:  {threads}")


def mapper(host, timeout, threads):
    print(
        f'Performing port scan on {host} with default timeout set to {str(timeout)}')

    def scanner(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(timeout)
        try:
            con = s.connect((host, port))

            with print_lock:
                print(f"{port} is OPEN")
            con.close()
        except:
            pass

    def threader():
        while True:
            worker = q.get()
            scanner(worker)
            q.task_done()

    q = Queue()

    for x in range(int(threads)):
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
    intro(host, ping, threads)
    if ping:
        print('Starting Ping Scan...')
        print("-"*60)
        timeout = round(ping_scan(host), 3)
        print(f'Ping scan finished average timeout: {round(timeout, 3)} ms')
        ans = input('Press y/n to set default timeout: ')

    print('-'*60)
    # Port Scan
    if ans == 'y' or ans == 'Y':
        print('Starting Port scan')
        mapper(host, timeout, threads)
    elif ans == 'n' or ans == 'N':
        timeout = None
        mapper(host, timeout, threads)
    else:
        print('Invalid Input')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Quitting')
        sys.exit()
