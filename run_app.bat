@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AI Скорая — Астана
echo ============================================================
echo   AI Скорая помощь · Астана
echo   Запуск операционной системы диспетчеризации...
echo.
echo   Браузер откроется автоматически.
echo   Чтобы остановить — закройте это окно.
echo ============================================================
echo.

"C:\Python314\python.exe" -m streamlit run "%~dp0app.py"
if errorlevel 1 (
  echo.
  echo [!] Не удалось запустить через C:\Python314. Пробую python из PATH...
  python -m streamlit run "%~dp0app.py"
)
if errorlevel 1 (
  echo.
  echo [!] Пробую через лаунчер py...
  py -m streamlit run "%~dp0app.py"
)

echo.
pause
