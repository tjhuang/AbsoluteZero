from core.color import color
import viewbag


def ShowOptions():
    srv = None
    prts = ""

    if viewbag.SERVER_STATUS:
        srv = color.ReturnBold(color.color.GREEN + 'Online' + color.color.END)
    else:
        srv = color.ReturnBold(color.color.RED + 'Offline' + color.color.END)

    if viewbag.PORT_LIST:
        for port in viewbag.PORT_LIST:
            prts += str(port) + ","
        prts = prts[:-1]

    opts = [('SERVER_STATUS', srv),
            ('CALLBACK_IP', viewbag.CALLBACK_IP),
            ('CALLBACK_PORTS', prts),
            ('MAX_CONN', str(viewbag.MAX_CONN)),
            ('MESSAGE_LENGTH_SHOW', str(viewbag.MESSAGE_LENGTH_SHOW)),
            ('ENVIRONMENT_FOLDER', viewbag.ENVIRONMENT_FOLDER),
            ('IMPLANTS CONNECTED', str(len(viewbag.all_connections)))]

    return "\n" + color.ReturnTabulate(opts, ['Option', 'Value'], "simple") + "\n"
