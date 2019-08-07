import os
from datetime import datetime
from tabulate import tabulate
from colorama import Fore, Back, Style, init


class color:
    def __init__(self):
        pass

    if os.name == "posix":
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
    else:
        PURPLE = Fore.MAGENTA
        CYAN = Fore.CYAN
        DARKCYAN = ''  # Unsupported
        BLUE = Fore.BLUE
        GREEN = Fore.GREEN
        YELLOW = Fore.YELLOW
        RED = Fore.RED
        BOLD = Style.BRIGHT
        UNDERLINE = ''  # Unsupported
        END = Style.RESET_ALL


def PrintTabulate(list_c, headr, style):
    print tabulate(list_c, headers=headr, tablefmt=style)


def ReturnTabulate(list_c, headr, style):
    return tabulate(list_c, headers=headr, tablefmt=style)


def ReturnInfo(string):
    return color.BLUE + color.BOLD + '[*] ' + color.END + string


def ReturnError(string):
    return color.RED + color.BOLD + '[-] ' + color.END + string


def ReturnWarning(string):
    return color.YELLOW + color.BOLD + '[!] ' + color.END + string


def ReturnSuccess(string):
    return color.GREEN + color.BOLD + '[+] ' + color.END + string


def ReturnQuestion(string):
    return color.BLUE + color.BOLD + '[?] ' + color.END + string


def ReturnMsgLength(string):
    return "[Packet-Length: " + color.YELLOW + color.BOLD + string + color.END + "]"


def ReturnBold(string):
    return color.BOLD + string + color.END


def ReturnCommandHighLight(string):
    return color.BOLD + color.BLUE + string + color.END


def ClearConsole():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")


def ReturnConsole(string):
    return color.END + string + color.BLUE + color.BOLD + ' >> ' + color.END


def ReturnImplantConsole(string):
    return color.END + color.UNDERLINE + color.BOLD + string + color.END + color.BOLD + color.BLUE + ' >> ' + color.END
