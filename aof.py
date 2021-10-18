import threading
import time
from collections import deque

aof_buf = deque()


def aof_handle():
    f = open('backup.aof', 'a+')
    while True:
        if len(aof_buf) > 0:
            req = aof_buf.popleft()
            f.write(str(req) + "\n")
            f.flush()
        else:
            time.sleep(0.1)

def start():
    t = threading.Thread(target=aof_handle, daemon=True)
    t.start()


def write_aof(data):
    aof_buf.append(data)
