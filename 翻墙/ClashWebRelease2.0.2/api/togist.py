import  base64
import  re
import  requests
import urllib3
import json
import time
urllib3.disable_warnings()

def getrules(file):             # 自定义规则
    
    try:       
        with open(file, "r",encoding = 'utf-8') as f:
            p_rule = f.read() + '\n'            
        return  p_rule
    except Exception as e:
        print('读取文件错误'+e)

def togist(fileadd,username,id,auth):    #togist
    try:  
        rule = './Profile/'+str(fileadd)
        rule = getrules(rule)      
        gistname = str(fileadd)
        currenttime = '# 更新时间为（UTC时区）：'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'
        content = "#!MANAGED-CONFIG https://gist.githubusercontent.com/{userid}/{id1}/raw/".format(userid=username,id1=id)+gistname+"\n"+currenttime+rule
        payload ={
            "description": "Hello World Examples",
            "files": {
                gistname: {
                "content": content
                }
            }
        }
        r = requests.patch(url="https://api.github.com/gists/{id1}".format(id1=id), data=json.dumps(payload), auth=auth)   
        return "https://gist.githubusercontent.com/{userid}/{id1}/raw/".format(userid=username,id1=id)+gistname 
        
    except Exception as e:
        print('上传文件错误:',e)
        return 'erro'

 