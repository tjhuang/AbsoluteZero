def module_classification():
    return 'admin/ps'


def module_description():
    return 'Get process list.'


def run(command=None):
    plugin = '''def run():
    import psutil
    buffer = ''
    for proc in psutil.process_iter():
        try:
            processName = proc.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            processName = "ACCESS DENIED"
        try:
            processID = proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            processID = "ACCESS DENIED"
        try:
            processPath = proc.exe()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            processPath = "-"
        if processPath == "":
            processPath = "-"
        buffer += processName + '###' + str(processID) + '###' + processPath + ":::::"
    return buffer'''
    return plugin
