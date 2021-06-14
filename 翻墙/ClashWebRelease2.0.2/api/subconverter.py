# coding=utf-8
import  sys
import  base64
import  re
import  requests
import  urllib3
import  urllib
import  json
import  time
import codecs
urllib3.disable_warnings()
def Retry_request(url): #远程下载
    i = 0
    headers = {
        "User-Agent": "ClashforWindows/<0.11.3>"
    }
    proxies = { "http": None, "https": None}
    for i in range(2):
        try:
            print("download with proxy")
            res = requests.get(url, headers = headers) 
            return res.text
        except Exception as e:
            try: 
                print("download without proxy")
                res = requests.get(url, headers = headers, proxies=proxies) 
                return res.text
            except Exception as e:
                print(e)
                i = i+1
    return 'erro'

