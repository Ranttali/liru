@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo Building liru wheels for all Python versions
echo ==========================================
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist liru.egg-info rmdir /s /q liru.egg-info
echo.

REM Check if Spout SDK exists
if not exist "external\Spout2\SPOUTSDK" (
    echo ERROR: Spout SDK not found at external\Spout2\SPOUTSDK
    echo Please download Spout 2.007 from:
    echo https://github.com/leadedge/Spout2/releases/tag/2.007g
    echo and extract to external\Spout2\
    exit /b 1
)

REM Build for each Python version
set "VERSIONS=3.13"
REM TODO: Add 3.14 3.15 when available

for %%v in (%VERSIONS%) do (
    echo ==========================================
    echo Building for Python %%v
    echo ==========================================

    py -%%v -m build --wheel

    if errorlevel 1 (
        echo ERROR: Build failed for Python %%v
        exit /b 1
    )

    echo.
)

echo ==========================================
echo All wheels built successfully!
echo ==========================================
echo.

dir /b dist\*.whl

endlocal
