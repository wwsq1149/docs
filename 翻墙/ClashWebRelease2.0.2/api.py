# coding=utf-8
import sys
import flask_restful
from flask import redirect, url_for,flash
import  re
import  requests
import urllib3
import urllib
import urllib.parse
import json
import time
import codecs
import subprocess
import base64
import api.admin
import api.subconverter
import api.airport
import api.togist
import api.clashapi
import api.currentmode
import api.ini
import os
from flask import Flask,render_template,request
urllib3.disable_warnings()

def safe_base64_decode(s): # 解密
    try:
        if len(s) % 4 != 0:
            s = s + '=' * (4 - len(s) % 4)
        base64_str = base64.urlsafe_b64decode(s)
        return bytes.decode(base64_str)
    except Exception as e:
        print('解码错误') 

def safe_base64_encode(s): # 加密
    try:
        return base64.urlsafe_b64encode(bytes(s, encoding='utf8'))
    except Exception as e:
        print('加密错误',e)

app = Flask(__name__)
ip = 'http://127.0.0.1:'+api.ini.getvalue('SET','clashweb')
subconverterurl = api.ini.getvalue('SET','subconverter')
clashapi = api.ini.getvalue('SET','dashboard').split('ui')[0]
dashboard = api.ini.getvalue('SET','dashboard')
app.secret_key = 'some_secret'
mypath = os.getcwd().replace('\\','/')
sysflag = ''

@app.route('/',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if request.form['submit'] == 'clash': 
            clash = request.form.get('clash')
            sysproxy = request.form.get('sysproxy')
            if '开启' in sysproxy:
                issys = '系统代理：关闭'
            else:
                issys = '系统代理：开启'

            if clash == '启动Clash':
                try:
                        mode=api.admin.getfile('./api/currentmode.py')
                        if 'nomal' in mode:
                            mode = '普通模式'
                            print(mode)
                            currentconfig = api.admin.getfile('./App/tmp.vbs')
                            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')
                            p=subprocess.Popen(mypath+'/bat/start.bat',shell=False)            
                            p.wait() 
                            path=mypath+'/Profile/'+currentconfig
                            path=path.replace('/','\\')
                            p=requests.put(clashapi+'configs',data=json.dumps({'path':path}))   
                            print(p.text)  
                            if '' == p.text: 
                                clash = '关闭Clash'
                                isclash = 'Clash 正在运行'                                                    
                                api.clashapi.setproxies('./Profile/save/'+currentconfig.replace('.yaml','.txt'))              
                                if api.ini.getvalue('SET','opensysafterstartclash') == 'True':
                                    p=subprocess.Popen(mypath+'/bat/setsys.bat',shell=False)
                                    p.wait()
                                    issys = '系统代理：开启'
                                    sysproxy = '关闭系统代理'
                            else:
                                clash = '启动Clash'
                                isclash = 'Clash启动失败:'+p.text+'   '
                        else:
                            mode = 'Tap模式'
                            print(mode)
                            currentconfig = api.admin.getfile('./App/tmp.vbs')                      #获取当前文件
                            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')
                            #把普通配置重写为tap配置
                            tapconfig=api.admin.getfile('./Profile/defaultconfig/tapconfig.txt')
                            config=api.admin.getfile('./Profile/'+currentconfig)
                            config=tapconfig+'\nproxies:'+config.split('proxies:',1)[1]       
                            api.admin.writefile(config,'./Profile/tapconfig/'+currentconfig)         
                            #重写完成
                            p=subprocess.Popen(mypath+'/App/tap/ahktapstart.bat',shell=False)              #启动tap    
                            p.wait() 
                            p=subprocess.Popen(mypath+'/bat/tapstart.bat',shell=False)              #启动默认tap文件    
                            p.wait() 
                            path=mypath+'/Profile/tapconfig/'+currentconfig
                            path=path.replace('/','\\')
                            p=requests.put(clashapi+'configs',data=json.dumps({'path':path}))       #切换成默认文件
                            print(p.text)  
                            if '' == p.text: 
                                print('1') 
                                clash = '关闭Clash'
                                isclash = 'Clash 正在运行'                    
                                api.clashapi.setproxies('./Profile/save/'+currentconfig.replace('.yaml','.txt'))       #设置节点   
                            else:
                                print('2')
                                clash = '启动Clash'
                                isclash = 'Clash启动失败:'+p.text+'   '
                            p=subprocess.Popen(mypath+'/bat/dissys.bat',shell=False)
                            p.wait()  
                            issys = '系统代理：关闭'
                            sysproxy = '开启系统代理'
                        flash(isclash+' '+issys+'   当前模式:'+mode)
                        return render_template('login.html',clash=clash,sysproxy=sysproxy)

                except Exception as e:
                    print(e)
                    flash('未知错误，启动Clash失败')    
                    return redirect(ip)


            if clash == '关闭Clash':
                try:
                    mode=api.admin.getfile('./api/currentmode.py')
                    if 'tap' in mode:
                        p=subprocess.Popen(mypath+'/App/tap/ahktapstop.bat',shell=False)
                        p.wait()  
                    currentconfig = api.admin.getfile('./App/tmp.vbs')
                    currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.yaml','.txt').replace('.\\Profile\\','')     
                    try:
                        api.clashapi.getallproxies('./Profile/save/'+currentconfig)    
                    except:
                        pass                    
                    p=subprocess.Popen(mypath+'/bat/stop.bat',shell=False)
                    p.wait()     
                    flash('Clash 未运行 '+'系统代理：关闭')
                    return render_template('login.html',clash='启动Clash',sysproxy='开启系统代理')
                except :
                    flash('关闭Clash失败')
                    return redirect(ip)           
        if request.form['submit'] == '切换 节点':
            clash = request.form.get('clash')
            sysproxy = request.form.get('sysproxy')
            if clash == '启动Clash':
                flash('请先启动Clash')
                return render_template('login.html',clash=clash,sysproxy=sysproxy)
            try:
                currentconfig = api.admin.getfile('./App/tmp.vbs')
                currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','')
                isDashboard = api.admin.getfile(currentconfig)
                os.system('start '+dashboard)
                return redirect(ip)
            except:
                flash('查看代理失败')
                return redirect(request.url)
        if request.form['submit'] == '订阅  管理':
            return redirect('profiles')
    a = os.popen(mypath+'/bat/check.bat')
    a = a.read()
    if 'Console' in str(a):   #检查是否正常运行，console in 表示在运行。
        clash = '关闭Clash'
        isclash = 'Clash 正在运行'
    else:
        clash = '启动Clash' 
        isclash = 'Clash 未运行'   
    a = os.popen(mypath+'/bat/checksys.bat')
    a = a.read().replace(' ','').replace('\n','')
    if str(a).endswith('0x0'):
        sysproxy = '开启系统代理'
        issys = '系统代理：关闭'   
    else:
        sysproxy = '关闭系统代理'
        issys = '系统代理：开启'
    mode= api.admin.getfile('./api/currentmode.py')
    if 'tun' in mode:
        mode = 'Tun模式'
    else:
        mode = '普通模式'
    flash(isclash+'\n'+issys+'  当前模式：'+mode) 
    return render_template('login.html',clash=clash,sysproxy=sysproxy)

@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
    try:
        if request.method == "POST":
                if request.form['submit'] == '更新  配置':            
                    url = request.form.get('url')  
                    fileadd = './Profile/'+request.form.get('configselect')    
                    configtype =request.values.get('customRadioInline1')         
                    if '://' in url:
                        if configtype == 'notclash':
                            url = urllib.parse.quote(url)
                            url = '{ip}/sub?target=clashr&url={sub}'.format(ip=subconverterurl,sub=url)    #非Clash进行拼接 
                        if '127.0.0.1' in url or 'localhost' in url:
                            p=subprocess.Popen(mypath+'/bat/subconverter.bat',shell=False) 
                            p.wait()
                        content = api.subconverter.Retry_request(url)
                        p=subprocess.Popen(mypath+'/bat/stopsubconverter.bat',shell=False)
                        p.wait()
                        if 'proxies:' in content and 'proxy-groups:' in content:
                            content = '#托管地址:'+url+'NicoNewBeee的Clash控制台\n'+content  #下载  
                            api.admin.writefile(content,fileadd)           #写入
                            flash('下载配置成功。注意查看内容是否正常，无误后请点击重启Clash以应用！')
                            return render_template('content.html',content=content,file=fileadd,sub=url) 
                        else:
                            flash('下载失败')
                            return redirect('profiles')

                    else:
                        try:
                            url=str(api.admin.getfile(fileadd)).split('NicoNewBeee的Clash控制台')[0].split('#托管地址:')[1]
                        except:
                            return '未查到托管地址，请在输入框输入托管地址'
                        if '127.0.0.1' in url or 'localhost' in url:
                            p=subprocess.Popen(mypath+'/bat/subconverter.bat',shell=False) 
                            p.wait()
                        content = api.subconverter.Retry_request(url)
                        p=subprocess.Popen(mypath+'/bat/stopsubconverter.bat',shell=False)
                        p.wait()
                        if 'proxies:' in content and 'proxy-groups:' in content:
                            content = '#托管地址:'+url+'NicoNewBeee的Clash控制台\n'+content  #下载  
                            api.admin.writefile(content,fileadd)          #写入
                            flash('下载配置成功。注意查看内容是否正常，无误后请点击重启Clash以应用！')
                            return render_template('content.html',content=content,file=fileadd,sub=url) 
                        else:
                            flash('下载失败')
                            return redirect('profiles')                      
                if request.form['submit'] == '查看  配置': 
                    fileadd = './Profile/'+request.form.get('configselect')              
                    content= api.admin.getfile(fileadd)
                    try:
                        url=content.split('NicoNewBeee的Clash控制台')[0].split('#托管地址:')[1]
                        content
                    except:
                        url='erro'
                        content=''
                    flash('查看配置成功！')
                    return render_template('content.html',content=content,file=fileadd,sub=url) 
                if  request.form['submit'] == '重启/切换' :
                    currentconfig = api.admin.getfile('./App/tmp.vbs')
                    currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.yaml','.txt').replace('.\\Profile\\','')
                    try:
                        api.clashapi.getallproxies('./Profile/save/'+currentconfig)  
                        print('保存当前节点选择成功,开始重启') 
                    except:
                        pass   
                    fileadd = './Profile/'+request.form.get('configselect')
                    fileadd2 = './Profile/save/'+request.form.get('configselect') 
                    fileadd = str(fileadd).replace('/','\\')
                    script = 'CreateObject("WScript.Shell").Run "clash-win64 -d .\Profile -f {file}",0'.format(file=fileadd)
                    api.admin.writefile(script,'./App/tmp.vbs')       #更新所选文件到本地
                    try:
                        mode=api.admin.getfile('./api/currentmode.py')
                        if 'nomal' in mode:
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
                                flash('重启/切换普通模式配置文件成功')
                            else:
                                flash('重启失败： '+p.text)
                        else:
                            currentconfig = api.admin.getfile('./App/tmp.vbs')                      #获取当前文件
                            currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')
                            #把普通配置重写为tap配置
                            tapconfig=api.admin.getfile('./Profile/defaultconfig/tapconfig.txt')
                            config=api.admin.getfile('./Profile/'+currentconfig)
                            config=tapconfig+'\nproxies:'+config.split('proxies:',1)[1]       
                            api.admin.writefile(config,'./Profile/tapconfig/'+currentconfig)         
                            #重写完成
                            p=subprocess.Popen(mypath+'/App/tap/ahktapstart.bat',shell=False)              #启动tap    
                            p.wait() 
                            p=subprocess.Popen(mypath+'/bat/tapstart.bat',shell=False)              #启动默认tap文件    
                            p.wait() 
                            path=mypath+'/Profile/tapconfig/'+currentconfig
                            path=path.replace('/','\\')
                            p=requests.put(clashapi+'configs',data=json.dumps({'path':path}))       #切换成默认文件
                            print(p.text)  
                            if '' == p.text:                      
                                api.clashapi.setproxies('./Profile/save/'+currentconfig.replace('.yaml','.txt'))       #设置节点   
                                flash('重启/切换tap模式配置文件成功')
                            else:
                                flash('重启失败： '+p.text)   
                            p=subprocess.Popen(mypath+'/bat/dissys.bat',shell=False)
                            p.wait()  
                    except Exception as e:
                        print(e)
                        flash('失败')
                    return redirect(ip)
                if  request.form['submit'] == '返回  主页' or request.form['submit'] == '返回主页' :
                    return redirect(ip)
                if  request.form['submit'] == '修改订阅/修改配置' :
                    sub = request.form.get('sub')
                    content = request.form.get('content')
                    content = '#托管地址:'+sub+'NicoNewBeee的Clash控制台'+content.split('NicoNewBeee的Clash控制台')[1]
                    fileadd = request.form.get('file')
                    print('当前配置文件地址：'+fileadd)
                    api.admin.writefile(content,fileadd)
                    content= api.admin.getfile(fileadd)
                    try:
                        url=content.split('NicoNewBeee的Clash控制台')[0].split('#托管地址:')[1]
                        content
                    except:
                        url='erro'
                        content=''
                    flash('修改配置成功！点击重启以应用！')
                    return render_template('content.html',content=content,file=fileadd,sub=url)  
                if  request.form['submit'] == '返回上页' :
                    return redirect(request.referrer) 
                if  request.form['submit'] == '重启Clash' :
                    currentconfig = api.admin.getfile('./App/tmp.vbs')
                    currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.yaml','.txt').replace('.\\Profile\\','')
                    try:
                        api.clashapi.getallproxies('./Profile/save/'+currentconfig)    
                        print('保存当前节点选择成功，开始重启')  
                    except:
                        pass
                    fileadd = request.form.get('file')
                    fileadd2 = './Profile/save/'+request.form.get('file').split('./Profile/')[1] 
                    fileadd = str(fileadd).replace('/','\\')
                    script = 'CreateObject("WScript.Shell").Run "clash-win64 -d .\Profile -f {file}",0'.format(file=fileadd)
                    api.admin.writefile(script,'./App/tmp.vbs')  #更新所选文件到本地
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
                            flash('重启/切换普通模式配置文件成功')
                        else:
                            flash('重启失败： '+p.text)
                    except Exception as e:
                        flash('失败')
                    return redirect(ip)
                if  request.form['submit'] == '订阅转换' :   
                    os.system('explorer file:///{path}/Profile/sub-web/index.html'.format(path=mypath)) 
                    flash('订阅转换')
                    return redirect('profiles')   
                if request.form['submit'] == '上传 gist':
                    return redirect('togist')    
                if request.form['submit'] == '打开目录':
                    os.system('explorer file:///{path}/Profile'.format(path=mypath)) 
                    return redirect('profiles') 
                if request.form['submit'] == '修改名称':
                    filename = './Profile/'+request.form.get('filename')
                    if filename == "./Profile/":
                        return '请先输入名称'
                    if '.yaml' not in filename:
                        filename += '.yaml'                    
                    currentconfig = api.admin.getfile('./App/tmp.vbs')
                    currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','') 
                    fileadd =request.form.get('configselect')
                    fileadd = './Profile/'+fileadd 
                    try: 
                        os.rename(fileadd, filename)
                    except:
                        return "重名了！！！"   
                    currentconfig = './Profile/' + currentconfig                
                    if fileadd == currentconfig:
                        filetmp = str(filename).replace('/','\\')
                        script = 'CreateObject("WScript.Shell").Run "clash-win64 -d .\Profile -f {file}",0'.format(file=filetmp)
                        api.admin.writefile(script,'./App/tmp.vbs')                                            
                    flash('重命名成功')
                    return redirect('profiles')    
        currentconfig = api.admin.getfile('./App/tmp.vbs')
        currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')
        filelist = os.listdir('./Profile')
        config = []
        config.append(currentconfig)
        for i in range(len(filelist)):
            if filelist[i].endswith('.yaml'):
                if filelist[i] == 'notchangeme.yaml':
                    continue
                if filelist[i] != currentconfig: 
                    config.append(filelist[i])    
        return render_template('profiles.html',cates=config)
    except Exception as e:
        flash('发生错误，重新操作'+e)
        return redirect(ip)


@app.route('/airport',methods=['GET', 'POST'])
def airport():
    if request.method == "POST":
        email = request.form.get('email')
        passwd = request.form.get('passwd')
        suburl = api.airport.stc(email,passwd)   #ssr订阅
        totalurl = suburl+'|'+suburl+'?mu=2'     #ssr+V2订阅
        sub = urllib.parse.quote(totalurl)
        clash = '{ip}/sub?target=clashr&url={sub}'.format(ip=subconverterurl,sub=sub)  #Clash订阅
        currentconfig = api.admin.getfile('./App/tmp.vbs')
        currentconfig = str(currentconfig).split('-f')[1].split('\"')[0].replace(' ','').replace('.\\Profile\\','')   #获取当前配置文件
        currentconfig = './Profile/'+currentconfig
        currentconfig2 = './Profile/save/'+currentconfig
        if '127.0.0.1' in clash or 'localhost' in clash:
            p=subprocess.Popen(mypath+'/bat/subconverter.bat',shell=False) 
            p.wait()        
        content = '#托管地址:'+clash+'NicoNewBeee的Clash控制台\n'+api.admin.Retry_request(clash)
        p=subprocess.Popen(mypath+'/bat/stopsubconverter.bat',shell=False)
        p.wait()
        api.admin.writefile(content,currentconfig) 
        p=subprocess.Popen(mypath+'/bat/start.bat',shell=False)            
        p.wait()
        path = mypath+currentconfig
        path = path.replace('/','\\').replace('.\\','\\')
        p=requests.put(clashapi+'configs',data=json.dumps({'path':path}))
        if '' == p.text:
            try:
                api.clashapi.setproxies(currentconfig2.replace('.yaml','.txt'))
            except:
                pass
            flash('重启成功')
        else:
            flash('重启失败： '+p.text)
        return redirect(ip)
        flash('尊敬的STC用户，您可以使用了！！！')
        return redirect(ip)                    
    return render_template('airport.html')


@app.route('/togist',methods=['GET', 'POST'])
def togist():
    if request.method == "POST":
        email = request.form.get('email')
        passwd = request.form.get('passwd')
        fileadd = request.form.get('file')
        gist = request.form.get('gist')
        if email =='' or passwd == '' or fileadd == '' or gist == '':
            flash('检查是否漏填了或者忘记选择文件了？')
            return redirect(request.referrer)
        try:
            gist = gist.split('/')
            usrname = gist[3]
            id = gist[4]
        except:
            flash('请输入正确gist地址')
            return redirect(request.referrer)
        auth=requests.auth.HTTPBasicAuth(email,passwd)
        flag=api.togist.togist(fileadd,usrname,id,auth)
        if flag == 'erro':
            flash('发生错误')
            return redirect(request.referrer)
        else:
            return '成功上传，Gist托管地址为：'+flag                
    return render_template('togist.html')

@app.route('/start',methods=['GET', 'POST'])
def start(): 
    try:
        if sysflag == '':
            return redirect(ip)    
        return redirect(sysflag)             
    except Exception as e:
        pass    

if __name__ == '__main__':
    port = api.ini.getvalue('SET','clashweb')
    try:
        sysflag = sys.argv[1]
    except:
        sysflag = ''
    print(sysflag)
    os.system('start '+ip+'/start')
    app.run(host='127.0.0.1',debug=False,port=port)            #自定义端口   

#  os.system('wscript ".\App\tmp.vbs" ')