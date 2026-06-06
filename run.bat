@echo off

cd /d "C:\Users\GULSHAN\Desktop\Project\Booking Website"

start cmd /k "venv\Scripts\activate && uvicorn main:app --reload"

start cmd /k "python -m http.server 5500"

timeout /t 3 >nul

start http://127.0.0.1:5500/index.html