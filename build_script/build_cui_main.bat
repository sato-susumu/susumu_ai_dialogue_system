copy cui_main.py ..
cd ..
pyinstaller cui_main.py --name cui_main.exe --onefile --clean
del cui_main.py
