compile:
	pyinstaller --onefile .\uvm.py --icon="installer/favicon.ico"
source:
	echo venv\Scripts\activate.bat
