from core.color import color

core_commands = [(color.ReturnCommandHighLight('sessions'), '-v\n-i [index]\n-k [index]', 'Show all active implants.\nInteract with an implant.\nKill a specific session by its index.'),
                 (color.ReturnCommandHighLight('payloadgen'), '[host]\n[port]\n[debug]\n[implantName]\n[output]\n[console]', 'Callback ip.\nCallback port.\nDebug mode (bool).\nId.\n".py" or ".exe" file.\nShow the payload.'),
                 (color.ReturnCommandHighLight('run'), 'tcp', 'Start the reverse TCP handler.'),
                 (color.ReturnCommandHighLight('background'), '-', 'Move current session interaction to the background.'),
                 (color.ReturnCommandHighLight('set'), 'CALLBACK_IP [value]\nCALLBACK_PORTS [value]\nMAX_CONN [value]\nMESSAGE_LENGTH_SHOW [value]\nENVIRONMENT_FOLDER [value]', 'Set the callback ip.\nSet the callback ports.\nSet maximum connections to accept.\nShow/Hide the packet length of each message (bool).\nSet the AbsoluteZero environment folder.'),
                 (color.ReturnCommandHighLight('exec'), '[module name]::[module arguments]', 'Execute a payload passing with "::" the arguments\nAdd "::" anyway and leave blank to not passing arguments.'),
                 (color.ReturnCommandHighLight('modules'), '-', 'Show all modules.'),
                 (color.ReturnCommandHighLight('download'), '[remote file path] [destination path]', 'Download a file from the remote target.'),
                 (color.ReturnCommandHighLight('upload'), '[local file path] [remote destination path]', 'Upload a file on the remote target.'),
                 (color.ReturnCommandHighLight('show'), 'options', 'Show environment system variables.'),
                 (color.ReturnCommandHighLight('screenshot'), '-', 'Grab a screenshot from the remote target.'),
                 (color.ReturnCommandHighLight('exit'), '-', 'Quit.')
                 ]


def Extract(lst):
    return list(list(zip(*lst))[0])


def help():
    headers = ['Command', 'Argument', 'Description']
    butterfly_headers = []

    for head in headers:
        butterfly_headers.append(head)

    return "\n" + color.ReturnTabulate(core_commands, butterfly_headers, "simple") + "\n"
