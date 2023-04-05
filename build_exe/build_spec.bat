pyi-makespec main.py --name susumu_ai_dialogue_system  --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock  --copy-metadata numpy --copy-metadata tokenizers --collect-data ipadic --hidden-import ipadic --collect-all torch
echo import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5) > temp.txt
type susumu_ai_dialogue_system.spec >> temp.txt
move /Y temp.txt susumu_ai_dialogue_system.spec
