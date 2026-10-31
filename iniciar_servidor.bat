@echo off
title Servidor Django - Consultoria Novo Varejo Portugal
color 0A
echo =========================================================================
echo   NOVO VAREJO - INTELIGENCIA DE MERCADO / REGIS COSTA (PT-PT)
echo   Plataforma de Consultoria Especializada em Retalho Alimentar
echo =========================================================================
echo.
echo Servidor a iniciar em:
echo   - Local:    http://127.0.0.1:8000/
echo   - Hostname: http://localhost:8000/
echo.
echo Pressione CTRL+C para encerrar o servidor.
echo =========================================================================
echo.
python manage.py runserver 0.0.0.0:8000
pause
