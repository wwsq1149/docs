import requests
import json
import urllib.parse
import api.admin
import api.ini
def Retry_request(url): #远程下载
    i = 0
    for i in range(2):
        try:
            res = requests.get(url) # verify =false 防止请求时因为代理导致证书不安全
            return res.text
        except Exception as e:
            i = i+1
    return 'erro'

ip = api.ini.getvalue('SET','dashboard').split('ui')[0]

def getallproxies(address):
    allproxies=Retry_request(ip+'proxies')
    allproxies= json.loads(allproxies)['proxies']
    
    load = ''
    for key in allproxies.keys():
        if allproxies[key]['type'] == 'Selector':
            load += urllib.parse.quote(key) + '='+allproxies[key]['now']+'@'
    
    api.admin.writefile(load,address)

def setproxies(address):
    a = api.admin.getfile(address)
    a = a.split('@')
    for b in a:
        if b == '':
            continue
        b = b.split('=')
        requests.put(ip+'proxies/'+ b[0], data=json.dumps({'name': b[1]}))

def setconfig(address):
    requests.put(ip+'configs/'+address)


def setmode(mode):
    requests.patch(ip+'configs/',data=json.dumps({'mode':mode}))
