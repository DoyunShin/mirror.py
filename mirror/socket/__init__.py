import mirror

import socket
from pathlib import Path

# unix socket server
socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockPath = Path("/var/run/mirror.sock")
if sockPath.exists():
    sockPath.unlink()

socket.bind(str(sockPath))
socket.listen(1)

while True:
    connection, address = socket.accept()
    data = connection.recv(1024)
    if data:
        data = data.decode("utf-8")
        if data == "reload":
            mirror.reload()
            connection.sendall(b"reload")
        elif data == "save":
            mirror.status.save()
            connection.sendall(b"save")
        elif data == "exit":
            connection.sendall(b"exit")
            break
        else:
            connection.sendall(b"unknown")
    else:
        connection.sendall(b"unknown")
    connection.close()