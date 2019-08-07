def module_classification():
    return 'admin/ls'


def module_description():
    return 'List all files and folders in a directory.'


def run(command=None):
    plugin = """
def run():
    import os
    from datetime import datetime
    list_directory = ""
    f_list = os.listdir(os.getcwd())
    for file_ in f_list:
        statbuf = os.stat(file_)
        try:
            sizef = str(os.path.getsize(file_))
        except:
            sizef = 'ACCESS DENIED'
        if os.path.isfile(file_):
            list_directory += file_ + '::'
            list_directory += 'fil' + '::'
            list_directory += sizef + '::'
            list_directory += str(datetime.utcfromtimestamp(statbuf.st_mtime).strftime('%Y-%m-%d %H:%M:%S')) + ';;;;'
        else:
            list_directory += file_ + '::'
            list_directory += 'dir' + '::'
            list_directory += '0' + '::'
            list_directory += str(datetime.utcfromtimestamp(statbuf.st_mtime).strftime('%Y-%m-%d %H:%M:%S')) + ';;;;'
    return list_directory"""
    return plugin
