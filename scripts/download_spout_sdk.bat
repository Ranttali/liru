@echo off
setlocal

REM Change to project root (parent of scripts directory)
cd /d "%~dp0\.."

echo ==========================================
echo Downloading Spout SDK 2.007
echo ==========================================
echo.

REM Check if already downloaded
if exist "external\Spout2\Spout-SDK-binaries\Libs_2-007-017\include\SpoutGL\Spout.h" (
    echo Spout SDK already exists at external\Spout2\Spout-SDK-binaries
    echo Skipping download.
    exit /b 0
)

echo Creating external directory...
if not exist "external" mkdir external

echo Downloading Spout 2.007...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/leadedge/Spout2/releases/download/2.007.017/Spout-SDK-binaries_2-007-017_1.zip' -OutFile 'Spout2.zip'"

if errorlevel 1 (
    echo ERROR: Failed to download Spout SDK
    exit /b 1
)

echo Extracting Spout SDK...
powershell -Command "Expand-Archive -Path 'Spout2.zip' -DestinationPath 'external\Spout2' -Force"

if errorlevel 1 (
    echo ERROR: Failed to extract Spout SDK
    del Spout2.zip
    exit /b 1
)

echo Cleaning up...
del Spout2.zip

echo.
echo ==========================================
echo Spout SDK installed successfully!
echo Location: external\Spout2\Spout-SDK-binaries
echo ==========================================
echo.
echo You can now build liru with: python -m build --wheel

endlocal
