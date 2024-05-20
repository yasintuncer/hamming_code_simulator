@echo off
:: Get the directory of the batch file
set "BATCH_DIR=%~dp0"

:: Check if Python is installed
python --version >nul 2>&1

:: If Python is installed, %ERRORLEVEL% will be 0
if %ERRORLEVEL% == 0 (
    echo Python is installed on this system.
    echo Creating virtual environment in the current directory...

    :: Create virtual environment in the current directory
    python -m venv "%BATCH_DIR%venv"

    :: Check if the virtual environment was created successfully
    if exist "%BATCH_DIR%venv" (
        echo Virtual environment created successfully.
        
        :: Debug: Check if the activate script exists in Scripts
        if exist "%BATCH_DIR%venv\bin\activate" (
            echo Activating virtual environment from Scripts...
            
            :: Activate the virtual environment
            .\venv\bin\activate
            
            echo Virtual environment activated.
        ) else (
            echo Activation script not found.
            goto end
        )

        :: Install setuptools in the virtual environment
        .\venv\bin\python.exe -m pip install setuptools

        :: Run setup.py if it exists
        if exist "%BATCH_DIR%setup.py" (
            echo Running setup.py...
            call .\venv\bin\python.exe setup.py
        ) else (
            echo setup.py not found in the current directory.
        )
    ) else (
        echo Failed to create the virtual environment.
    )
) else (
    echo Python is not installed on this system.
)

:end
:: Pause the script to view the output
pause
