@ECHO OFF & TITLE 添加 clash 开机启动
>NUL 2>&1 REG.exe query "HKU\S-1-5-19" || (
    ECHO SET UAC = CreateObject^("Shell.Application"^) > "%TEMP%\Getadmin.vbs"
    ECHO UAC.ShellExecute "%~f0", "%1", "", "runas", 1 >> "%TEMP%\Getadmin.vbs"
    "%TEMP%\Getadmin.vbs"
    DEL /f /q "%TEMP%\Getadmin.vbs" 2>NUL
    Exit /b
)
CD /D %~DP0\..\
SET PATH="%~dp0";"%~dp0App";%PATH%

:menu
cls
echo.&echo.
echo -------------------------------------
echo.
echo.
echo 请选择
echo.
echo.  [1] 开机启动
echo.
echo.  [2] 删除开机启动
echo.
echo.  [X] 退出
echo.
choice /C:12X /N /M  "输入您的选项："

if errorlevel 3 exit
if errorlevel 2 goto :delete
if errorlevel 1 goto :startup

:startup
Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "clashweb" /t REG_SZ /d "\"%~dp0startupclash.bat\"" /f
echo 添加成功，按任意键退出 &pause >NUL
exit

:delete
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "clashweb"  /f>NUL 2>NUL
echo 删除成功，按任意键退出&pause >NUL
exit