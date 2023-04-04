rmdir /s /q build
rmdir /s /q dist
del susumu_toolbox.spec
pip freeze > freeze.txt
pip uninstall -y -r freeze.txt
pip install -r requirements.txt
del freeze.txt
