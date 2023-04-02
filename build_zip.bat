set /p version=<version.txt
echo version=%version%

del susumu_toolbox_*.zip
cd dist
rename susumu_toolbox susumu_toolbox_%version%
7z a -tzip ../susumu_toolbox_%version%.zip susumu_toolbox_%version%
cd ..
