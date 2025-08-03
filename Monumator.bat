@echo off
chcp 65001 >nul
title Monumator - Monumental Markets Automation System
color 0A
cd /d "%~dp0"
mode con: cols=120 lines=50

REM Activate environment silently before showing startup screen
call venv\Scripts\activate.bat >nul 2>&1

cls
echo.
echo.
echo          ███╗   ███╗ ██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗ █████╗ ████████╗ ██████╗ ██████╗ 
echo          ████╗ ████║██╔═══██╗████╗  ██║██║   ██║████╗ ████║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
echo          ██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║██╔████╔██║███████║   ██║   ██║   ██║██████╔╝
echo          ██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██║   ██║██╔══██╗
echo          ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
echo          ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
echo.
echo ════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo                            MONUMENTAL MARKETS AUTOMATION SYSTEM                              
echo ════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo                                        Version 1.0 - Production Ready                                    
echo ════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo.
echo                            Press any key to continue to main menu...
pause >nul

python main.py

pause

