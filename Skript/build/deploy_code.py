import os
import shutil

ZIP_EXT = ".zip"

def deploy(base_dir: str, dist_name: str, dest_dir: str): 
    base_dir = os.path.abspath(base_dir)
    if dest_dir is None or len(dest_dir) == 0:
        raise ValueError("No destination directory given")
    if not os.path.exists(dest_dir):
        raise ValueError("Destination directory does not exist: " + dest_dir)

    src_dirs: list[str] = []
    for root, dirs, _ in os.walk(base_dir):
        if dist_name in dirs:
            src_dirs.append(os.path.join(root, dist_name))
            
    for src_dir in src_dirs:
        chapter = src_dir.split(os.sep)[-2]
        print(chapter)        
    
        src = os.path.join(src_dir)
        #dest = os.path.join(dest_dir, dist_name, chapter)
        dest = os.path.join(dest_dir, dist_name)

        zipfile_dir = os.path.abspath(os.path.join(src, '..'))
        zipfile_name = os.path.join(zipfile_dir, chapter+ZIP_EXT)
        shutil.make_archive(base_name = zipfile_name.replace(ZIP_EXT, ""), format="zip", root_dir = src)
        print(zipfile_name + "->" + dest)
        os.makedirs(dest, exist_ok=True)         
        shutil.copy(zipfile_name, dest)
        #shutil.copytree(src, dest, dirs_exist_ok=True)
    

base_dir = 'modules'
# TODO: set your destination directory here, e.g. 'P:/mmunz/Lehre/MALE/lecture_notes'
dest_dir = None 

print("Deploying notebooks...")
deploy(base_dir, 'notebooks', dest_dir)
print("Deploying examples...")
deploy(base_dir, 'examples', dest_dir)