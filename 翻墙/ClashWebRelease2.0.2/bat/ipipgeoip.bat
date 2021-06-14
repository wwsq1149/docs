cd ./Profile
del "Country.mmdb" /f /q
ren tmp.mmdb Country.mmdb
echo.&echo.
echo -------------------------------------
echo.
echo success
ping -n 3 127.0.0.1 > nul