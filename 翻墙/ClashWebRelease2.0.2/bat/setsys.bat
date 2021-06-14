for /F "tokens=1,2 delims=:" %%a in ('findstr /x /I "^mixed-port:.*[0-9].*$" ".\Profile\defaultconfig\default.yaml"') do set "http_port=%%~nxb"
set http_port=%http_port: =%
cd ./App
sysproxy global 127.0.0.1:%http_port% localhost;127.*;10.*