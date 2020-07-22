# import socket
# import sys
# import threading
# from queue import Queue
# import time
# import subprocess
# import optparse


# print_lock = threading.Lock()


# def get_arguments():
#     parser = optparse.OptionParser()
#     parser.add_option("-t", "--target", dest="host", help="Target Host")
#     (options, arguments) = parser.parse_args()
#     if not options.host:
#         parser.error("[-] Please specify a target host")
#     return options


# options = get_arguments()
# host = options.host


# def scanner(port):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     try:
#         con = s.connect((host, port))

#         with print_lock:
#             print('port', port)
#         con.close()
#     except:
#         pass


# def threader():
#     while True:
#         worker = q.get()
#         scanner(worker)
#         q.task_done()


# q = Queue()

# start = time.time()

# for x in range(500):
#     t = threading.Thread(target=threader)
#     t.daemon = True
#     t.start()

# for worker in range(1, 65535):
#     q.put(worker)

# q.join()


# end = time.time()

# totalTime = end - start

# print(f"Scan completed in {round(totalTime)} second(s)")

# import platform    # For getting the operating system name
# import subprocess  # For executing a shell command


# def ping(host):
#     """
#     Returns True if host (str) responds to a ping request.
#     Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
#     """

#     # Option for the number of packets as a function of
#     param = '-n' if platform.system().lower() == 'windows' else '-c'

#     # Building the command. Ex: "ping -c 1 google.com"
#     command = ['pingparsing', param, '3', host]

#     return subprocess.call(command)


# s = ping('10.10.106.250')
# print(s)


import json
import pingparsing

ping_parser = pingparsing.PingParsing()
transmitter = pingparsing.PingTransmitter()
transmitter.destination = "google.com"
transmitter.count = 10
result = transmitter.ping()

print(json.dumps(ping_parser.parse(result).as_dict(), indent=4))
