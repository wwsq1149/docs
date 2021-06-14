taskkill /IM EnableLoopback.exe >NUL 2>NUL
cd ./App
EnableLoopback.exe
CD /D %~DP0