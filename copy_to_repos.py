# copies the contents of Labor and Skripts to all sibling folders


# first detect all sibling folders of this skript

import os
import shutil

src_base_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(src_base_path, '..'))

siblings = os.listdir(parent_dir)

folders_to_copy = ['build', 'templates', 'modules/aboutme', 'modules/_includes', '.vscode']

print(f"Looking for sibling folders in {parent_dir}...")

for sibling in siblings:
    sibling_path = os.path.join(parent_dir, sibling)
    if not os.path.isdir(sibling_path) or sibling == os.path.basename(src_base_path):
        continue
    
    print(f"Found sibling folder: {sibling_path}")
    # get contents of sibling folder
    subdirs = os.listdir(sibling_path)
    for dir in subdirs:    
    
        if os.path.isdir(dir):
            if dir == 'Labor' or dir == 'Skript':
                # copy contents of Labor and Skripts to this sibling folder
                
                for folder in folders_to_copy:
                    src_path = os.path.join(src_base_path, dir, folder)
                    target_path = os.path.join(sibling_path, dir, folder)
                    
                    # recursively copy contents of src_path to target_path

                    if os.path.exists(src_path):
                        shutil.copytree(src_path, target_path, dirs_exist_ok=True)
                        print(f"Copying contents of {src_path} to {target_path}...")
                        
