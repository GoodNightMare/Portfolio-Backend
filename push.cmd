@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

where git >nul 2>nul
if errorlevel 1 (
    echo ERROR: Git is not installed or is not available in PATH.
    exit /b 1
)

git rev-parse --is-inside-work-tree >nul 2>nul
if errorlevel 1 (
    echo ERROR: This folder is not a Git repository.
    exit /b 1
)

git ls-files --error-unmatch .env >nul 2>nul
if not errorlevel 1 (
    echo ERROR: .env is tracked by Git. Remove it from tracking before pushing.
    echo Run: git rm --cached .env
    exit /b 1
)

git add -A
if errorlevel 1 exit /b 1

git diff --cached --quiet
if errorlevel 1 (
    set "COMMIT_MESSAGE=%~1"
    if not defined COMMIT_MESSAGE set "COMMIT_MESSAGE=Update portfolio backend"

    git commit -m "!COMMIT_MESSAGE!"
    if errorlevel 1 exit /b 1
) else (
    echo No new changes to commit.
)

for /f "delims=" %%B in ('git branch --show-current') do set "CURRENT_BRANCH=%%B"
if not defined CURRENT_BRANCH (
    echo ERROR: Could not determine the current branch.
    exit /b 1
)

git push origin "%CURRENT_BRANCH%"
if errorlevel 1 exit /b 1

echo Successfully pushed branch !CURRENT_BRANCH! to GitHub.
endlocal
