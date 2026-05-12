@echo off
curl -s --max-time 1 http://localhost:5000 >nul 2>&1
if %errorlevel% equ 0 goto open

start "Convertidor" /min cmd /k "python "%~dp0app.py" >> "%~dp0server.log" 2>&1"

set intentos=0
:wait
timeout /t 1 /nobreak >nul
set /a intentos+=1
if %intentos% geq 15 goto error
curl -s --max-time 1 http://localhost:5000 >nul 2>&1
if %errorlevel% neq 0 goto wait
goto open

:error
echo No se pudo iniciar el servidor. Revisa server.log
pause
exit /b 1

:open
start http://localhost:5000
