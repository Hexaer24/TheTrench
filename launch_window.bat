@echo off
REM Activate virtual environment (edit this path to match yours)
call .venv\Scripts\activate.bat

REM Run pytest with SeleniumBase using selected browser and seleniumwire
python theTrench.py --browser=firefox --wire

pause