set /p version=<build_exe/version.txt
echo version=%version%

del susumu_toolbox_*.zip
cd dist
rename susumu_ai_dialogue_system susumu_ai_dialogue_system_%version%
7z a -tzip ../susumu_ai_dialogue_system_%version%.zip susumu_ai_dialogue_system_%version%
cd ..
