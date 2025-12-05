1. Download the Codeflix.Zip file and extract it.

2 . Delete any Previous Venv. folder(virtual Environment folder) if initially seen in the main file.

3. Then open the folder in VS Code.

4. Install Python 3.12 on the device with the run pathway while installing(https://www.python.org/downloads/release/python-3120/)

5. Then run the following commands chronologically, opening a new Terminal: 

1. py -3.12 -m venv .venv
2. Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
3. .\.venv\Scripts\Activate.ps1
4. pip install streamlit
5. python.exe -m pip install --upgrade pip
6. pip install requests
7. pip install plotly
8. pip install matplotlib
9. python seed.py
10. streamlit run app.py

Please run these commands carefully and in chronological order. Otherwise, it will not work.
