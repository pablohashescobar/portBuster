import socket
import sys
import threading
from queue import Queue
import time

host = '10.10.88.120'

print_lock = threading.Lock()


def scanner(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        con = s.connect((host, port))

        with print_lock:
            print('port', port)
        con.close()
    except:
        pass


def threader():
    while True:
        worker = q.get()
        scanner(worker)
        q.task_done()


q = Queue()

start = time.time()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in range(1, 100):
    q.put(worker)

q.join()

end = time.time()

totalTime = end - start

print(f"Scan completed in {round(totalTime)} second(s)")
