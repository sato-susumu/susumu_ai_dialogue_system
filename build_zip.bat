set /p version=<version.txt
echo version=%version%

del susumu_toolbox_*.zip
cd dist
rename susumu_toolbox susumu_toolbox_%version%
wsl zip -r ../susumu_toolbox_%version%.zip susumu_toolbox_%version%
cd ..
