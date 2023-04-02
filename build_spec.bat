pyi-makespec main.py --name susumu_toolbox  --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock  --copy-metadata numpy --copy-metadata tokenizers --collect-data ipadic --hidden-import ipadic --collect-all torch
echo import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5) > temp.txt
type susumu_toolbox.spec >> temp.txt
move /Y temp.txt susumu_toolbox.spec
