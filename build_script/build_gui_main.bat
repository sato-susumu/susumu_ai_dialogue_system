rem GUIの場合、--onefile付きだとexeの起動に失敗する
rem tclフォルダを強引にコピーすれば動くため、他の解決方法もあると思うが
rem 現状は--onefileを使わないことで回避
copy gui_main.py ..
cd ..
pyinstaller gui_main.py --name gui_main --clean --noconsole
del gui_main.py
