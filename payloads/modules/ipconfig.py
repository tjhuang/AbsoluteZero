def module_classification():
    return 'admin/ipconfig'


def module_description():
    return 'Get a list of all network interfaces.'


def run(command=None):
    plugin = '''def run():    
    import netifaces
    interfc = netifaces.interfaces()
    buffer = ''
    for interface in interfc:
        buffer += interface + "xxx"
        addr = netifaces.ifaddresses(interface)
        mac = addr[netifaces.AF_LINK]
        mac1 = mac[0].get('addr')
        buffer += "Harware MAC::::::" + str(mac1) + "xxx"
        try:
            lan = addr[netifaces.AF_INET]
            lan1 = lan[0].get('addr')
            buffer += "IP Address::::::" + str(lan1) + "xxx"
        except KeyError:
            buffer += "IP Address::::::-" + "xxx"
        try:
            net = addr[netifaces.AF_INET]
            net1 = net[0].get('netmask')
            buffer += "Netmask   ::::::" + str(net1) + "xxx"
        except KeyError:
            buffer += "Netmask   ::::::" + "-" + "xxx"
        buffer += "xxx"
    return buffer'''
    return plugin
