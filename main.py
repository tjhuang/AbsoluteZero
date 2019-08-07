from core.color import color
from core.color import header
from core.config import config
from core.console import console
from core.console import help


def printBanner():
    color.ClearConsole()
    print header.Banner(config.VERSION)


if __name__ == '__main__':
    printBanner()
    console.CLI.console()
