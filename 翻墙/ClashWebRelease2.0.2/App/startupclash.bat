@echo off
:: 切换的软件根目录
CD /D %~dp0\..\
:: 设置环境变量
PATH="%CD%\";"%CD%\App";"%CD%\Python";"%CD%\Python\Scripts";"%CD%\Python\Lib\distutils\command";"%CD%\Python\Lib\site-packages\pip\_vendor\distlib";"%CD%\Python\Lib\site-packages\setuptools";%PATH%
taskkill /IM clash-win64.exe >NUL 2>NUL
start ClashWeb.exe