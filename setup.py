"""
Setup script for building the Professional Billing System executable
Author: Praveen Yadav
Version: 1.0.0
"""

import os
import shutil
import sys

import PyInstaller.__main__


def build_executable():
    """Build the executable using PyInstaller"""

    # Application information
    APP_NAME = 'BillingSystem'
    APP_VERSION = '1.0.0'
    APP_DESCRIPTION = 'Professional Billing System with Firebase Integration'
    APP_AUTHOR = 'Praveen Yadav'

    # Define the build arguments
    args = [
        '--onefile',  # Create a one-file bundled executable
        '--windowed',  # Hide console window (GUI app)
        '--name=' + APP_NAME,  # Name of the executable
        '--distpath=dist',  # Output directory
        '--workpath=build',  # Temporary build directory
        '--specpath=.',  # Spec file location
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace output directory without asking
        '--optimize=2',  # Optimize bytecode
        '--noupx',  # Don't use UPX compression

        # Icon (if available)
        '--icon=assets/billing.ico',

        # Hidden imports for modules PyInstaller might miss
        '--hidden-import=customtkinter',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=firebase_admin',
        '--hidden-import=firebase_admin.credentials',
        '--hidden-import=firebase_admin.firestore',
        '--hidden-import=firebase_admin.auth',
        '--hidden-import=requests',
        '--hidden-import=json',
        '--hidden-import=datetime',
        '--hidden-import=os',
        '--hidden-import=sys',
        '--hidden-import=dotenv',
        '--hidden-import=platformdirs',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=reportlab',
        '--hidden-import=reportlab.pdfgen',
        '--hidden-import=reportlab.lib',

        # Add data files
        '--add-data=assets;assets',
        '--add-data=auth;auth',

        # Main Python file
        'main.py'
    ]

    print("=" * 60)
    print(f"Building {APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print(f"Platform: {sys.platform}")
    print(f"Python version: {sys.version}")
    print()

    try:
        # Check if required files exist
        required_files = [
            'assets/billing.ico',
            'auth/serviceAccountKey.json'
        ]

        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)

        if missing_files:
            print("Warning: The following files are missing:")
            for file_path in missing_files:
                print(f"  - {file_path}")
            print()

            if 'assets/billing.ico' in missing_files:
                print("Building without custom icon.")
                args = [arg for arg in args if not arg.startswith('--icon=')]

            if 'auth/serviceAccountKey.json' in missing_files:
                print("ERROR: Firebase service account key is required!")
                print("Please place your serviceAccountKey.json in the auth/ directory.")
                return False

        # Run PyInstaller
        print("Starting build process...")
        PyInstaller.__main__.run(args)

        print()
        print("=" * 60)
        print("Build completed successfully!")
        print("=" * 60)
        print(f"Executable location: {os.path.abspath('dist/' + APP_NAME + '.exe')}")

        # Create distribution files
        create_distribution_files(APP_NAME, APP_VERSION, APP_AUTHOR)

        print("\nDistribution files created successfully!")
        print("\nYour Professional Billing System is ready to distribute!")
        return True

    except Exception as e:
        print(f"Build failed: {e}")
        return False


def create_distribution_files(app_name, app_version, app_author):
    """Create additional distribution files"""

    # Create README for distribution
    dist_readme = f"""Professional Billing System - Distribution Package

Application: {app_name}
Version: {app_version}
Author: {app_author}
Build Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

FEATURES:
✓ User Authentication & Registration
✓ Firebase Integration for Data Storage
✓ Professional Invoice Generation
✓ Customer Management System
✓ Product/Service Catalog
✓ Payment Tracking
✓ PDF Report Generation
✓ Modern CustomTkinter UI
✓ Secure Login System
✓ Email Verification
✓ Password Reset Functionality
✓ Data Export Capabilities

CONTENTS:
- {app_name}.exe         : Main application executable
- README_DIST.txt        : This file
- LICENSE.txt            : License information
- User_Guide.pdf         : Detailed user manual (if available)

SYSTEM REQUIREMENTS:
- Windows 7/8/10/11 (64-bit recommended)
- Minimum 4GB RAM
- 200MB free disk space
- Internet connection (required for Firebase)

INSTALLATION:
1. Simply run {app_name}.exe
2. No additional installation required
3. Application will create config files automatically

FIRST TIME SETUP:
1. Launch the application
2. Create a new account or login with existing credentials
3. Verify your email address
4. Start managing your billing operations

FEATURES OVERVIEW:

🔐 AUTHENTICATION:
• Secure user registration and login
• Email verification system
• Password reset functionality
• Firebase-powered authentication

📋 BILLING MANAGEMENT:
• Create professional invoices
• Manage customer information
• Track payments and due dates
• Generate detailed reports

💼 BUSINESS FEATURES:
• Product/service catalog management
• Tax calculations and compliance
• Multi-currency support
• Data backup and sync

📊 REPORTING:
• PDF invoice generation
• Financial reports and analytics
• Export data in various formats
• Historical transaction tracking

🛡️ SECURITY:
• Encrypted data transmission
• Secure cloud storage with Firebase
• User session management
• Data privacy compliance

USAGE TIPS:
• Keep your internet connection active for cloud sync
• Regularly backup important data
• Use strong passwords for account security
• Verify all calculations before finalizing invoices

SUPPORT:
For technical support or feature requests:
• Email: support@example.com
• GitHub: https://github.com/yourusername/billing_system
• Documentation: See built-in help system

COPYRIGHT:
© 2025 {app_author}. All rights reserved.
Licensed under MIT License - see LICENSE.txt for details.

DISCLAIMER:
This software is provided for business use.
Always verify calculations and comply with local tax regulations.
Consult with accounting professionals for important financial decisions.
Ensure compliance with data protection laws in your jurisdiction.

TECHNICAL NOTES:
• Built with Python and CustomTkinter
• Powered by Google Firebase
• PDF generation via ReportLab
• Cross-platform compatibility
"""

    try:
        with open('dist/README_DIST.txt', 'w') as f:
            f.write(dist_readme)
    except Exception as e:
        print(f"Warning: Could not create dist README: {e}")

    # Copy additional files to dist
    files_to_copy = [
        ('LICENSE', 'LICENSE.txt'),
        ('README.md', 'README.md'),
    ]

    for src, dst in files_to_copy:
        try:
            if os.path.exists(src):
                shutil.copy2(src, f'dist/{dst}')
        except Exception as e:
            print(f"Warning: Could not copy {src}: {e}")

    # Create a simple installer batch file
    installer_content = f"""@echo off
echo ============================================
echo     Professional Billing System Installer
echo ============================================
echo.

echo Installing Professional Billing System...
echo.

set INSTALL_DIR=%PROGRAMFILES%\\Professional Billing System

echo Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Copying application files...
copy "{app_name}.exe" "%INSTALL_DIR%\\"
copy "README_DIST.txt" "%INSTALL_DIR%\\"
copy "LICENSE.txt" "%INSTALL_DIR%\\"

echo Creating desktop shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\\Desktop\\Professional Billing System.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\\{app_name}.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "Professional Billing System - Complete Business Solution" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo Creating start menu entry...
set START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs
if not exist "%START_MENU%\\Professional Billing System" mkdir "%START_MENU%\\Professional Billing System"

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateStartMenu.vbs
echo sLinkFile = "%START_MENU%\\Professional Billing System\\Professional Billing System.lnk" >> CreateStartMenu.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateStartMenu.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\\{app_name}.exe" >> CreateStartMenu.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateStartMenu.vbs
echo oLink.Description = "Professional Billing System" >> CreateStartMenu.vbs
echo oLink.Save >> CreateStartMenu.vbs
cscript CreateStartMenu.vbs
del CreateStartMenu.vbs

echo.
echo ============================================
echo     Installation Completed Successfully!
echo ============================================
echo.
echo Professional Billing System has been installed to:
echo %INSTALL_DIR%
echo.
echo Shortcuts created:
echo • Desktop shortcut
echo • Start Menu entry
echo.
echo You can now launch the application from:
echo 1. Desktop shortcut
echo 2. Start Menu → Professional Billing System
echo 3. Direct execution from: %INSTALL_DIR%
echo.

set /p launch="Launch Professional Billing System now? (y/n): "
if /i "%launch%"=="y" (
    echo Launching Professional Billing System...
    start "" "%INSTALL_DIR%\\{app_name}.exe"
)

echo.
echo Thank you for using Professional Billing System!
echo.
pause
"""

    try:
        with open('dist/install.bat', 'w') as f:
            f.write(installer_content)
        print("Installer script created: dist/install.bat")
    except Exception as e:
        print(f"Warning: Could not create installer script: {e}")


def clean_build_files():
    """Clean up build files"""
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['BillingSystem.spec']

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"Cleaned up: {dir_name}")
            except Exception as e:
                print(f"Warning: Could not remove {dir_name}: {e}")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"Cleaned up: {file_name}")
            except Exception as e:
                print(f"Warning: Could not remove {file_name}: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Build Professional Billing System executable')
    parser.add_argument('--clean', action='store_true', help='Clean build files after building')
    parser.add_argument('--test', action='store_true', help='Test the built executable')

    args = parser.parse_args()

    # Check if required files exist
    if not os.path.exists('main.py'):
        print("Error: main.py not found!")
        print("Please ensure you are running this script from the project directory.")
        sys.exit(1)

    # Check for required directories
    if not os.path.exists('assets'):
        print("Warning: assets directory not found. Creating assets structure...")
        os.makedirs('assets', exist_ok=True)
        print("Please place your billing.ico file in assets/ directory")

    if not os.path.exists('auth'):
        print("Error: auth directory not found!")
        print("Please ensure your Firebase serviceAccountKey.json is in the auth/ directory")
        sys.exit(1)

    # Build the executable
    success = build_executable()

    if not success:
        sys.exit(1)

    # Test the executable if requested
    if args.test:
        print("\nTesting the executable...")
        try:
            import subprocess

            exe_path = 'dist/BillingSystem.exe'
            if os.path.exists(exe_path):
                print(f"Launching {exe_path} for testing...")
                subprocess.Popen([exe_path])
                print("Executable launched successfully!")
            else:
                print("Error: Executable not found for testing.")
        except Exception as e:
            print(f"Error testing executable: {e}")

    # Clean up if requested
    if args.clean:
        print("\nCleaning up build files...")
        clean_build_files()

    print("\n" + "=" * 60)
    print("Build process completed!")
    print("=" * 60)
    print("\nFiles created in 'dist' directory:")
    print("• BillingSystem.exe - Main application")
    print("• README_DIST.txt - User documentation")
    print("• LICENSE.txt - License information")
    print("• install.bat - Optional installer script")
    print("\nYour Professional Billing System is ready for distribution!")