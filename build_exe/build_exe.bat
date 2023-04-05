rem GUIの場合、--onefile付きだとexeの起動に失敗する
rem tclフォルダを強引にコピーすれば動くため、他の解決方法もあると思うが
rem 現状は--onefileを使わないことで回避
rmdir /s /q build
rmdir /s /q dist
pyinstaller  --clean susumu_ai_dialogue_system.spec
