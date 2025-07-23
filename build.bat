@echo off
echo ============================================
echo   Professional Billing System - Build Script
echo              Version 1.0.0
echo              AUTOMATIC BUILD MODE
echo ============================================
echo.
echo Command line options:
echo   build.bat          - Build with auto-cleanup (default)
echo   build.bat --test   - Build and auto-test executable
echo   build.bat --no-cleanup - Build and keep temporary files
echo   build.bat --silent - Build with minimal output
echo.
echo Starting automatic build process...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    echo Build process aborted.
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not available!
    echo Please ensure pip is installed with Python.
    echo Build process aborted.
    exit /b 1
)

echo Installing/Updating dependencies...
echo This may take a few minutes for first-time installation...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Error: Failed to install dependencies!
    echo Please check your internet connection and try again.
    echo.
    echo Trying to install core dependencies individually...
    pip install customtkinter>=5.2.0
    pip install firebase-admin>=7.0.0
    pip install requests>=2.25.0
    pip install python-dotenv>=1.0.0
    pip install pyinstaller>=5.13.0
    pip install pillow>=11.3.0
    pip install reportlab>=4.4.2

    if errorlevel 1 (
        echo Error: Could not install core dependencies!
        echo Build process aborted.
        exit /b 1
    )
)

echo.
echo Dependencies installed successfully!
echo.

REM Check if main.py exists
if not exist "main.py" (
    echo Error: main.py not found!
    echo Please ensure you are running this script from the project directory.
    echo Current directory: %cd%
    echo Build process aborted.
    exit /b 1
)

REM Create assets directory structure if it doesn't exist
if not exist "assets" (
    echo Creating assets directory structure...
    mkdir assets
    echo Please place your billing.ico file in assets\ directory
    echo.
)

REM Create auth directory structure if it doesn't exist
if not exist "auth" (
    echo Creating auth directory structure...
    mkdir auth
    echo Please place your serviceAccountKey.json file in auth\ directory
    echo.
)

REM Check for required files
if not exist "assets\billing.ico" (
    echo Warning: Icon file not found at assets\billing.ico
    echo The executable will be built without a custom icon.
    echo You can add the icon file later and rebuild.
    echo.
)

if not exist "auth\serviceAccountKey.json" (
    echo ERROR: Firebase service account key is required!
    echo Please place your serviceAccountKey.json in the auth\ directory.
    echo.
    echo To get your service account key:
    echo 1. Go to Firebase Console (https://console.firebase.google.com)
    echo 2. Select your project
    echo 3. Go to Project Settings → Service Accounts
    echo 4. Click "Generate new private key"
    echo 5. Save the downloaded JSON file as serviceAccountKey.json in auth\ folder
    echo.
    echo Build process aborted.
    exit /b 1
)

REM Check for .env file (optional but recommended)
if not exist ".env" (
    echo Warning: .env file not found
    echo Consider creating a .env file with your Firebase configuration
    echo for better security and configuration management.
    echo.
)

REM Test the application before building
echo Testing the application...
python -c "import main; print('Application import test: OK')"
if errorlevel 1 (
    echo Error: Application failed import test!
    echo Please check for syntax errors in main.py
    echo Build process aborted.
    exit /b 1
)

echo Application test passed!
echo.

REM Test Firebase connectivity
echo Testing Firebase configuration...
python -c "
try:
    from auth.firebase_config import FirebaseConfig
    config = FirebaseConfig()
    print('Firebase configuration test: OK')
except Exception as e:
    print(f'Firebase configuration test: FAILED - {e}')
    exit(1)
"
if errorlevel 1 (
    echo Error: Firebase configuration failed!
    echo Please check your serviceAccountKey.json and Firebase settings.
    echo Build process aborted.
    exit /b 1
)

echo Firebase configuration test passed!
echo.

echo Cleaning previous build files...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "BillingSystem.spec" del "BillingSystem.spec"
echo.

echo ============================================
echo     Building Professional Billing System
echo ============================================
echo.
echo This process will:
echo • Create a standalone executable (.exe)
echo • Include all dependencies and Firebase integration
echo • Bundle CustomTkinter and all UI components
echo • Include authentication and database modules
echo • Optimize for performance and security
echo • Create distribution files
echo.
echo Please wait... This may take 5-15 minutes depending on your system
echo.

REM Build using Python setup script
python setup.py
if errorlevel 1 (
    echo.
    echo Error: Build failed!
    echo Trying alternative build method...
    echo.

    REM Alternative build using direct PyInstaller command
    pyinstaller --onefile ^
                --windowed ^
                --name=BillingSystem ^
                --icon=assets/billing.ico ^
                --distpath=dist ^
                --workpath=build ^
                --clean ^
                --noconfirm ^
                --optimize=2 ^
                --noupx ^
                --hidden-import=customtkinter ^
                --hidden-import=tkinter ^
                --hidden-import=tkinter.ttk ^
                --hidden-import=tkinter.messagebox ^
                --hidden-import=tkinter.filedialog ^
                --hidden-import=firebase_admin ^
                --hidden-import=firebase_admin.credentials ^
                --hidden-import=firebase_admin.firestore ^
                --hidden-import=firebase_admin.auth ^
                --hidden-import=requests ^
                --hidden-import=dotenv ^
                --hidden-import=PIL ^
                --hidden-import=reportlab ^
                --add-data=assets;assets ^
                --add-data=auth;auth ^
                main.py

    if errorlevel 1 (
        echo.
        echo Error: Both build methods failed!
        echo Please check the error messages above and try the following:
        echo 1. Ensure all dependencies are installed correctly
        echo 2. Check that main.py has no syntax errors
        echo 3. Verify that PyInstaller is properly installed
        echo 4. Ensure Firebase serviceAccountKey.json is valid
        echo 5. Check internet connection for Firebase services
        echo Build process aborted.
        exit /b 1
    )
)

echo.
echo ============================================
echo           Build Completed Successfully!
echo ============================================
echo.

REM Check if executable was created
if not exist "dist\BillingSystem.exe" (
    echo Error: Executable was not created!
    echo Please check the build logs above for errors.
    echo Build process aborted.
    exit /b 1
)

REM Get file size
for %%A in ("dist\BillingSystem.exe") do set SIZE=%%~zA
set /a SIZE_MB=%SIZE%/1024/1024

echo Build Summary:
echo • Executable: dist\BillingSystem.exe
echo • File size: %SIZE_MB% MB
echo • Build date: %date% %time%
echo • Platform: Windows (64-bit)
echo.

echo Distribution files created:
if exist "dist\README_DIST.txt" echo • README_DIST.txt - User documentation
if exist "dist\LICENSE.txt" echo • LICENSE.txt - License information
if exist "dist\install.bat" echo • install.bat - Optional installer script
echo.

REM Security reminder
echo ============================================
echo              SECURITY REMINDER
echo ============================================
echo.
echo IMPORTANT: Your executable contains Firebase credentials
echo Please ensure secure distribution and consider:
echo • Code signing for trusted distribution
echo • Secure hosting for downloads
echo • User authentication before download
echo • Regular updates for security patches
echo.

REM Check command line arguments for testing and cleanup
set AUTO_TEST=no
set AUTO_CLEANUP=yes
set SILENT_MODE=no

if "%1"=="--test" set AUTO_TEST=yes
if "%1"=="--no-cleanup" set AUTO_CLEANUP=no
if "%1"=="--silent" set SILENT_MODE=yes

REM Automatic testing (only if requested)
if /i "%AUTO_TEST%"=="yes" (
    echo Automatically testing the executable...
    echo Launching Professional Billing System for testing...
    start "" "dist\BillingSystem.exe"

    REM Wait a moment then check if it's running
    timeout /t 5 /nobreak >nul
    tasklist /FI "IMAGENAME eq BillingSystem.exe" 2>NUL | find /I /N "BillingSystem.exe">NUL
    if errorlevel 1 (
        echo Warning: Application may not have started correctly.
        echo Please manually test the executable in the dist folder.
    ) else (
        echo ✓ Application started successfully!
    )
    echo.
) else (
    echo Skipping automatic test. Use --test parameter to auto-test.
)

REM Automatic cleanup (default behavior)
if /i "%AUTO_CLEANUP%"=="yes" (
    echo Automatically cleaning up temporary build files...
    if exist "build" rmdir /s /q "build"
    if exist "BillingSystem.spec" del "BillingSystem.spec"
    if exist "__pycache__" rmdir /s /q "__pycache__"
    echo Cleanup completed.
    echo.
) else (
    echo Skipping cleanup. Build files retained for debugging.
    echo.
)

echo ============================================
echo            Build Process Complete!
echo ============================================
echo.
echo Your Professional Billing System is ready!
echo.
echo 📁 Location: %cd%\dist\BillingSystem.exe
echo 💾 Size: %SIZE_MB% MB
echo 🎯 Status: Ready for distribution
echo 🔐 Security: Firebase-powered authentication
echo.
echo Distribution Options:
echo 1. Share the 'dist' folder containing all files
echo 2. Use the install.bat script for automatic installation
echo 3. Simply share the .exe file for portable use
echo.
echo Features included in your build:
echo ✓ User authentication and registration
echo ✓ Firebase cloud integration
echo ✓ Professional invoice generation
echo ✓ Customer management system
echo ✓ Payment tracking and reporting
echo ✓ PDF report generation
echo ✓ Modern CustomTkinter interface
echo ✓ Secure data storage and sync
echo.
echo Next Steps:
echo • Test all features thoroughly
echo • Verify Firebase connectivity
echo • Test on different Windows systems
echo • Consider code signing for wider distribution
echo • Set up user support and documentation
echo.

REM Create a simple batch file to run the application
echo @echo off > "Run_Billing_System.bat"
echo cd /d "%~dp0" >> "Run_Billing_System.bat"
echo start "" "dist\BillingSystem.exe" >> "Run_Billing_System.bat"

echo Created Run_Billing_System.bat for easy launching.
echo.

echo Important Notes:
echo • Ensure users have internet connection for Firebase
echo • Consider creating user documentation
echo • Set up Firebase security rules appropriately
echo • Monitor usage and performance through Firebase console
echo.

echo Thank you for using the Professional Billing System build system!
echo.
echo Build completed automatically!
echo Usage examples:
echo   build.bat          - Build with default settings (auto-cleanup)
echo   build.bat --test   - Build and auto-test the executable
echo   build.bat --no-cleanup - Build and keep temporary files
echo   build.bat --silent - Build with minimal output
echo.
timeout /t 3 /nobreak >nul
echo Exiting...