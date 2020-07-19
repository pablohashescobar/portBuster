import socket
import sys
import threading
from queue import Queue

host = '10.10.88.120'


def scanner():
    for port in range(1, 65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = s.connect((host, port))
            if con == 0:
                print(f'Port {port} is open')
            s.close()
        except socket.error:
            pass
        except KeyboardInterrupt:
            print('Quitting....')
            sys.exit()


scanner()
