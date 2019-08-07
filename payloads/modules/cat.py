def module_classification():
    return 'admin/cat'


def module_description():
    return 'Read the content of a file.'


def run(fname):
    plugin = '''
def run():
    try:
        f = open("%s", "r")
        return f.read()
    except Exception, e:
        return "[-] Error: " + str(e)
''' % fname
    return plugin
