import mirror
import mirror.structure
import json

import socket
import time
from pathlib import Path

from threading import Thread

workers: list[Thread] = []

def setup():
    pass

def cleaner():
    global workers
    while True:
        time.sleep(1)
        workers = [i for i in workers if i.is_alive()]

def server():
    # unix socket server
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockPath = Path("/var/run/mirror.sock")
    if sockPath.exists():
        sockPath.unlink()

    sock.bind(str(sockPath))
    sock.listen(10)

    while True:
        conn, addr = sock.accept()
        


def worker(conn: socket.socket):
    while True:
        data = conn.recv(1024)
        if not data:
            # log error
            conn.close()
        
        pk = mirror.structure.Packet()
        pk.load(json.loads(data.decode(encoding="UTF-8")))

        # command checker

