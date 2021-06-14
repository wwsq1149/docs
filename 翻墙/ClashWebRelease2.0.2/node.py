# coding=utf-8
import sys
import json
import time
import codecs
import subprocess
import requests
import api.admin
import api.subconverter
import api.airport
import api.togist
import api.currentmode
import api.clashapi
import api.ini
import os
import yaml

clashapi = api.ini.getvalue('SET','dashboard').split('ui')[0]
dashboard = api.ini.getvalue('SET','dashboard')
mypath = os.getcwd().replace('\\','/')

if __name__ == '__main__':
    gpus = sys.argv[1]
    #gpus = 'updateruleprovider'
    if gpus == 'save':
        try:
            currentconfig = api.admin.getfile('./App/tmp.vbs')
            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.yaml','.txt').replace('.\\Profile\\','')     
            api.clashapi.getallproxies('./Profile/save/'+currentconfig)                                 
        except Exception as e:
            pass       

    if gpus == 'saveandclose':
        try:
            currentconfig = api.admin.getfile('./App/tmp.vbs')
            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.yaml','.txt').replace('.\\Profile\\','')     
            api.clashapi.getallproxies('./Profile/save/'+currentconfig)                     
            p=subprocess.Popen(mypath+'/bat/stop.bat',shell=False)
            p.wait()                
        except Exception as e:
            pass

    if gpus == 'startandset':
        try:
            currentconfig = api.admin.getfile('./App/tmp.vbs')
            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')
            p=subprocess.Popen(mypath+'/bat/start.bat',shell=False)            
            p.wait() 
            path=mypath+'/Profile/'+currentconfig
            path=path.replace('/','\\')
            p=requests.put(clashapi+'configs',data=json.dumps({'path':path}))   
            print(p.text)  
            if '' == p.text:                      
                api.clashapi.setproxies('./Profile/save/'+currentconfig.replace('.yaml','.txt'))              
                if api.ini.getvalue('SET','opensysafterstartclash') == 'True':
                    p=subprocess.Popen(mypath+'/bat/setsys.bat',shell=False)
                    p.wait()
            else:
                    s=p.text.split('\":\"')[1][0:-3]
                    s='\"'+"启动失败："+s+'\"'
                    print(s)
                    p=subprocess.Popen(mypath+'/bat/startclasherro.bat '+s,shell=False)
                
            api.admin.writefile('currentmode=\'nomal\'','./api/currentmode.py')
        except Exception as e:
            pass

    if gpus == 'restart':
        try:
            mode=api.currentmode.currentmode
            if mode == 'nomal':
                currentconfig = api.admin.getfile('./App/tmp.vbs')
                currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')
                p=subprocess.Popen(mypath+'/bat/start.bat',shell=False)            
                p.wait() 
                path=mypath+'/Profile/'+currentconfig
                path=path.replace('/','\\')
                p=requests.put(clashapi+'configs',data=json.dumps({'path':path}))   
                print(p.text)  
                if '' == p.text:  
                    print(gpus)                     
                    api.clashapi.setproxies('./Profile/save/'+currentconfig.replace('.yaml','.txt'))              
                    if api.ini.getvalue('SET','opensysafterstartclash') == 'True' :
                        print(gpus)
                        p=subprocess.Popen(mypath+'/bat/setsys.bat',shell=False)
                        p.wait()
                else:
                    s=p.text.split('\":\"')[1][0:-3]
                    s='\"'+"启动失败："+s+'\"'
                    print(s)
                    p=subprocess.Popen(mypath+'/bat/startclasherro.bat '+s,shell=False)
            else:
                currentconfig = api.admin.getfile('./App/tmp.vbs')                      #获取当前文件
                currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')

                #把普通配置重写为tun配置
                tapconfig=api.admin.getfile('./Profile/defaultconfig/tunconfig.yaml')
                config=api.admin.getfile('./Profile/'+currentconfig)
                config=tapconfig+'\nproxies:'+config.split('proxies:',1)[1]       
                api.admin.writefile(config,'./Profile/tunconfig/'+currentconfig)         
                #重写完成

                p=subprocess.Popen(mypath+'/bat/tunstart.bat',shell=False)              #启动默认tun文件    
                p.wait() 
                path=mypath+'/Profile/tunconfig/'+currentconfig
                path=path.replace('/','\\')
                p=requests.put(clashapi+'configs',data=json.dumps({'path':path}))       #切换成tun模式配置文件
                print(p.text)  
                if '' == p.text:  
                    print(gpus)                     
                    api.clashapi.setproxies('./Profile/save/'+currentconfig.replace('.yaml','.txt'))       #设置节点  
                else:
                    s=p.text.split('\":\"')[1][0:-3]
                    s='\"'+"启动失败："+s+'\"'
                    print(s)
                    p=subprocess.Popen(mypath+'/bat/startclasherro.bat '+s,shell=False)    
                p=subprocess.Popen(mypath+'/bat/dissys.bat',shell=False)
                p.wait()  
        except Exception as e:
            pass

    if gpus == 'tunstart':
        try:
            currentconfig = api.admin.getfile('./App/tmp.vbs')                      #获取当前文件
            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')

            #把普通配置重写为tun配置
            tapconfig=api.admin.getfile('./Profile/defaultconfig/tunconfig.yaml')
            config=api.admin.getfile('./Profile/'+currentconfig)
            config=tapconfig+'\nproxies:'+config.split('proxies:',1)[1]       
            api.admin.writefile(config,'./Profile/tunconfig/'+currentconfig)         
            #重写完成

            p=subprocess.Popen(mypath+'/bat/tunstart.bat',shell=False)              #启动默认tun文件    
            p.wait() 
            path=mypath+'/Profile/tunconfig/'+currentconfig
            path=path.replace('/','\\')
            p=requests.put(clashapi+'configs',data=json.dumps({'path':path}))       #切换成tun模式配置文件
            print(p.text)  
            if '' == p.text:  
                print(gpus)                     
                api.clashapi.setproxies('./Profile/save/'+currentconfig.replace('.yaml','.txt'))       #设置节点  
            else:
                s=p.text.split('\":\"')[1][0:-3]
                s='\"'+"启动失败："+s+'\"'
                print(s)
                p=subprocess.Popen(mypath+'/bat/startclasherro.bat '+s,shell=False)    
            p=subprocess.Popen(mypath+'/bat/dissys.bat',shell=False)
            p.wait()  
            api.admin.writefile('currentmode=\'tun\'','./api/currentmode.py')
        except Exception as e:
            pass

    if gpus == 'opendashboard':
        try:
            os.system('start '+dashboard)
        except Exception as e:
            pass

    if gpus == 'ipipupdate':
        try:
            #r = requests.get("https://cdn.jsdelivr.net/gh/alecthw/mmdb_china_ip_list@release/Country.mmdb") 
            r = requests.get("https://cdn.jsdelivr.net/gh/Hackl0us/GeoIP2-CN@release/Country.mmdb")
            with open("./Profile/tmp.mmdb",'wb') as f:
                f.write(r.content)
                print('1')
            p=subprocess.Popen(mypath+'/bat/ipipgeoip.bat',shell=False)
            p.wait()
        except Exception as e:
            pass

    if gpus == 'geoipupdate':
        try:
            url = "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key={key}&suffix=tar.gz".format(key=api.ini.getvalue('SET','key'))
            print(url)
            r = requests.get(url) 
            with open("./Profile/GeoLite2-Country.tar.gz",'wb') as f:
                f.write(r.content)
            p=subprocess.Popen(mypath+'/bat/geoip.bat',shell=False)
            p.wait()
        except Exception as e:
            pass

    if gpus == 'updateconfig':
        try:
            currentconfig = api.admin.getfile('./App/tmptmp.vbs')
            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')
            print(currentconfig)
            url=str(api.admin.getfile('./Profile/'+currentconfig)).split('NicoNewBeee的Clash控制台')[0].split('#托管地址:')[1]
        except:
            print('未查到托管地址，请在输入框输入托管地址')
        if '127.0.0.1' in url or 'localhost' in url:
            p=subprocess.Popen(mypath+'/bat/subconverter.bat',shell=False) 
            p.wait()
        content = api.subconverter.Retry_request(url)
        p=subprocess.Popen(mypath+'/bat/stopsubconverter.bat',shell=False)
        p.wait()
        print(content)
        if 'proxies:' in content and 'proxy-groups:' in content:
            api.ini.setvalue('SET','configdownload','success')
            content = '#托管地址:'+url+'NicoNewBeee的Clash控制台\n'+content  #下载  
            api.admin.writefile(content,'./Profile/'+currentconfig)           #写入
        else:
            api.ini.setvalue('SET','configdownload','erro')

    if gpus == 'closeclashweb':
        try:
            currentconfig = api.admin.getfile('./App/tmp.vbs')
            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.yaml','.txt').replace('.\\Profile\\','')     
            api.clashapi.getallproxies('./Profile/save/'+currentconfig)                                          
            p=subprocess.Popen(mypath+'/bat/stop.bat',shell=False)
            p.wait()                   
        except:
            pass

    if gpus == 'rulemode':
        try:  
            api.clashapi.setmode('Rule')                 
                 
        except:
            pass
        
    if gpus == 'directmode':
        try:
            api.clashapi.setmode('Direct')                  
        except:
            pass

    if gpus == 'globalmode':
        try:
            api.clashapi.setmode('Global')    
        except:
            pass

    if gpus == 'updateruleprovider':
        try:
            currentconfig = api.admin.getfile('./App/tmp.vbs')
            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')
            print(currentconfig)
            #currentconfig='config2.yaml'
            current_path = os.path.abspath(os.path.dirname(__file__))
            print(current_path + '/Profile/' + currentconfig)
            
            with open(current_path + '/Profile/' + currentconfig, 'rb') as f:
                temp = yaml.load(f.read())['rule-providers']
                for key in temp:
                    print(key)                
                    print(temp[key]['url'])
                    url = temp[key]['url']
                    content = api.subconverter.Retry_request(url)
                    if 'payload' in content :
                        api.admin.writefile(content,'./Profile/ruleset/'+key+'.yaml')  
                    else:
                        print('规则集下载失败')
                

        except Exception as e:
            print(e)

    if gpus == 'updateproxyprovider':
        try:
            currentconfig = api.admin.getfile('./App/tmp.vbs')
            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')
            print(currentconfig)
            #currentconfig='config2.yaml'
            current_path = os.path.abspath(os.path.dirname(__file__))
            print(current_path + '/Profile/' + currentconfig)
            
            with open(current_path + '/Profile/' + currentconfig, 'rb') as f:
                temp = yaml.load(f.read())['proxy-providers']
                for key in temp:
                    #利用api更新
                    p=requests.put(clashapi+'providers/proxies/'+key)
                    #保存最新节点集
                    print(temp[key]['url'])
                    url = temp[key]['url']
                    path = temp[key]['path'].split('./')[1]
                    print(path)
                    content = api.subconverter.Retry_request(url)
                    if 'name' in content :
                        api.admin.writefile(content,'./Profile/'+path)  
                    else:
                        print('节点集下载失败')         
        except Exception as e:
            print(e)
