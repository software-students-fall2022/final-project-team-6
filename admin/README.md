# How to Install and Run the admin with Venv

1. Setup a Python virtual environment
   ```
   python3 -m venv .venv
   ```

2. Activate the virtual environment
   ```
   .venv\Scripts\activate.bat
   ```
   If the above one doesn't work, try this:
   ```
   .venv\Scripts\activate.ps1
   ```


3. Install requirements.txt
   ```
   pip3 install -r requirements.txt
   ```

4. Run the App
   ```
   set FLASK_APP=app.py
   set FLASK_ENV=development
   python -m flask run
   ```