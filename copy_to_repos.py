# copies the contents of Labor and Skripts to all sibling folders


# first detect all sibling folders of this skript

import os
import shutil

src_base_path = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(src_base_path, '..'))

siblings = os.listdir(parent_dir)

folders_to_copy = ['build', 'templates', 'modules/aboutme', 'modules/_includes', '.vscode']


def make_copy_function(name):
    """Liefert eine Kopierfunktion fuer copytree, die in tasks.json
    den Platzhalter [LECTURE_NAME] durch `name` ersetzt."""
    def copy_with_replace(src, dst, *, follow_symlinks=True):
        if os.path.basename(src) == 'tasks.json':
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('[LECTURE_NAME]', name)
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [LECTURE_NAME] in {dst} durch '{name}' ersetzt")
            return dst
        return shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
    return copy_with_replace


print(f"Looking for sibling folders in {parent_dir}...")

for sibling in siblings:
    sibling_path = os.path.join(parent_dir, sibling)
    if not os.path.isdir(sibling_path) or sibling == os.path.basename(src_base_path):
        continue

    print(f"Found sibling folder: {sibling_path}")
    # get contents of sibling folder
    subdirs = os.listdir(sibling_path)
    for dir in subdirs:

        if os.path.isdir(os.path.join(sibling_path, dir)):
            if dir == 'Labor' or dir == 'Skript':
                # copy contents of Labor and Skripts to this sibling folder

                for folder in folders_to_copy:
                    src_path = os.path.join(src_base_path, dir, folder)
                    target_path = os.path.join(sibling_path, dir, folder)

                    # recursively copy contents of src_path to target_path

                    if os.path.exists(src_path):
                        print(f"Copying contents of {src_path} to {target_path}...")
                        shutil.copytree(
                            src_path,
                            target_path,
                            dirs_exist_ok=True,
                            copy_function=make_copy_function(sibling),
                        )