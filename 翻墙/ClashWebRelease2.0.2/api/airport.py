# -*- coding: utf-8 -*-
import requests
import re


def stc(account, password):
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    header = {
        #"origin": "https://stc-beta4.com",
        "Referer": "https://stc-beta4.com/auth/login",
        'User-Agent': userAgent,
    }    
    print ("登录STC")
    postUrl = "https://stc-beta4.com/auth/login"
    postData = {
        "email": account,
        "passwd": password,
    }
    response = requests.post(postUrl, data = postData, headers = header)
    cookies=response.cookies.get_dict()
    print(cookies)
    text=requests.get('https://stc-beta4.com/user',cookies=cookies).text
    match = re.search(r'data-clipboard-text="(.*)">复制链接',text)
    url = match.group(1).split('">复制链接')[0]
    print(url)
    return url

