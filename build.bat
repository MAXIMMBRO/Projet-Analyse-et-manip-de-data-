Copy

@echo off
title Build IMC.exe
echo ============================================
echo   Build de l'application IMC en .exe
echo ============================================
echo.
 
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH.
    echo Telecharge Python sur https://python.org
    pause
    exit /b
)
 echo [1/3] Installation de PyInstaller...
pip install pyinstaller --quiet
 
echo [2/3] Compilation en cours...
pyinstaller --onefile --windowed --name "CalculateurIMC" imc_app.py
 
echo.
echo [3/3] Termine !
echo Le fichier IMC.exe se trouve dans le dossier : dist\
echo.
pause
 