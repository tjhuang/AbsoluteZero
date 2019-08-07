def module_classification():
    return 'admin/shell_exec'


def module_description():
    return 'Execute a cmd/bash command and get the output.'


def run(command):
    plugin = '''
def run():
    import os
    import subprocess

    cmd = subprocess.Popen("%s", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) 
    output_bytes = cmd.stdout.read() + cmd.stderr.read()
    return output_bytes''' % command
    return plugin
