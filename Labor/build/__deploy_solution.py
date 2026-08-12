import os
import shutil
import sys

from tkinter import filedialog

ZIP_EXT = ".zip"

def deploy_solution(root_dir: str, dist_name: str, dest_dir: str): 
    root_dir = os.path.abspath(root_dir)

    src = os.path.join(root_dir, dist_name)
    if not os.path.exists(src):
        print(f"Solution directory {src} does not exist.")
        return
    
    exercise_name = os.path.basename(root_dir)
    
    dest = os.path.join(dest_dir)
    print(src + " -> " + dest) 
    
    zipfile_name = os.path.join(root_dir, exercise_name+"_solution"+ZIP_EXT)
    shutil.make_archive(base_name = zipfile_name.replace(ZIP_EXT, ""), format="zip", root_dir = src)
    
    #shutil.copytree(src, dest, dirs_exist_ok=True)
    os.makedirs(dest_dir, exist_ok=True)    
    shutil.copy(zipfile_name, dest)


args = sys.argv[1:]
if len(args) >= 1:
    dest_dir = args[0]
else:
    print("Missing destination directory as argument.")
    sys.exit(1)
    
#dest_dir = r'P:\mmunz\Lehre\MALE\lab\solutions'

base_dir = './modules/'
root_dir = filedialog.askdirectory(initialdir=base_dir, title='Select solution to publish')
#root_dir = r'C:\Users\micha\THU\Lehre\SOMD\Labor\docs\python_exercises'

dist_name = 'solution'

deploy_solution(root_dir, dist_name, dest_dir)