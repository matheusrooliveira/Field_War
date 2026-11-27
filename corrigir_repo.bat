@echo off
chcp 65001 >nul
cd /d "%~dp0"

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
  echo ERRO: coloque este arquivo dentro da pasta Field_War_git e rode de novo.
  pause
  exit /b 1
)

echo.
echo [1/4] Criando .gitignore...
echo venv/>> .gitignore
echo database/>> .gitignore
echo __pycache__/>> .gitignore

echo.
echo [2/4] Tirando banco e cache do Git (os arquivos continuam na sua maquina)...
git rm -r --cached --ignore-unmatch database __pycache__ sistemas/__pycache__

echo.
echo [3/4] Fazendo commit...
git add .gitignore
git commit -m "Remove banco e cache do versionamento"

echo.
echo [4/4] Enviando para o GitHub...
git push

echo.
echo ===== Arquivos alterados no commit anterior (copie e me mande) =====
git diff --stat 18c652b 4d29381

echo.
pause
