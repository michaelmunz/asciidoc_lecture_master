import os
import shutil
import sys
import argparse
from tkinter import filedialog


ZIP_EXT = ".zip"

SERVER_URL = "su765390@5016756940.ssh.w2.strato.hosting"
PATH_TO_KEY = "../../strato_key.ppko"
WEB_ROOT = "/home/www/public/teaching/"

def makedirs_ssh(dest_dir: str):
    # use ssh via shell to create the directory on the remote server
    import subprocess
    dest_dir = dest_dir.replace("\\", "/")
    print("Creating directory on remote server: " + dest_dir)
    subprocess.run(["ssh", "-i", PATH_TO_KEY, f"{SERVER_URL}", "mkdir", "-p", dest_dir], check=False)
    
    
def copyfile_ssh(src_file: str, dest_file: str):
    # use scp via shell to copy the file to the remote server
    import subprocess
    dest_file = dest_file.replace("\\", "/")
    print("Copying file to remote server: " + src_file + " -> " + dest_file)
    
    
    subprocess.run(["ssh", "-i", PATH_TO_KEY, f"{SERVER_URL}", "rm", dest_file], check=False)
    subprocess.run(["scp", "-i", PATH_TO_KEY, src_file, f"{SERVER_URL}:{dest_file}"], check=True)


def deploy_docs(base_dir: str, dest_dir: str):
    if dest_dir is None or len(dest_dir) == 0:
        raise ValueError("No destination directory given")
        
    base_dir = os.path.abspath(base_dir)    
        
    makedirs_ssh(dest_dir)    
    
    # iterate over all files in the base_dir and copy them to the dest_dir
    for file in os.listdir(base_dir):
        src = os.path.join(base_dir, file)        
        dest = os.path.join(dest_dir, file)    
        print(f"Copying file: {src} -> {dest}")                
        copyfile_ssh(src, dest)



def deploy_code(base_dir: str, dist_name: str, dest_dir: str): 
    if dest_dir is None or len(dest_dir) == 0:
        raise ValueError("No destination directory given")
        
    base_dir = os.path.abspath(base_dir)    
    
    
    src_dirs: list[str] = []
    
    # if single directory
    if dist_name in base_dir:
        src_dirs.append(base_dir)       
    else:    
        # recurse into the subdirectories of base_dir and check if "dist_name" exists there. If yes, zip it and copy it to the destination directory
        for root, dirs, _ in os.walk(base_dir):
            if dist_name in dirs:
                src_dirs.append(os.path.join(root, dist_name))
                
    for src_dir in src_dirs:
        chapter = src_dir.split(os.sep)[-2]
        print(chapter)        
    
        src = os.path.join(src_dir)
        

        zipfile_dir = os.path.abspath(os.path.join(src, '..'))
        zipfile_name = f"{chapter}_{dist_name}{ZIP_EXT}"
        zipfile_path = os.path.join(zipfile_dir, zipfile_name)        
        shutil.make_archive(base_name = zipfile_path.replace(ZIP_EXT, ""), format="zip", root_dir = src)
        dest = os.path.join(dest_dir, zipfile_name)    
        print(f"Copying file: {zipfile_path} -> {dest}")                
                
        makedirs_ssh(dest_dir)        
        copyfile_ssh(zipfile_path, dest)
        
    
  


if __name__ == "__main__":    

    parser = argparse.ArgumentParser(description="Deploy files on remote server")
    parser.add_argument("--destdir", help="Destination directory on remote server")
    parser.add_argument("--basedir", default="./modules", help="Base directory containing the files to deploy")
    parser.add_argument("--type", choices=["docs", "examples", "solution", "input"], help="Type of files to deploy (docs, examples, solution, input)")
    args = parser.parse_args()

    dest_dir = args.destdir
    base_dir = args.basedir
    type = args.type
    
    #dest_dir = "SOTE2/lab/inputs"
    #type = "input"
    
    dest_dir = os.path.join( WEB_ROOT, dest_dir)          
    base_dir = os.path.abspath(base_dir).replace("\\", "/")  



    # differentiate the deployment based on the type of files to deploy
    if type == "docs":
        print("Deploying documentation...")                
        # iterate over all subdirectores in the base dir and deploy the html and pdf files to the destination directory
        for docs_dir in os.listdir(base_dir):            
            deploy_docs(os.path.join(base_dir, docs_dir), dest_dir)
        

    elif type == "examples":
        print("Deploying notebooks...")
        deploy_code(base_dir, 'notebooks', dest_dir)
        print("Deploying examples...")
        deploy_code(base_dir, 'examples', dest_dir)
        
    elif type == "solution" or type == "input":
        print(f"Deploying {type}...")
        # ask the user to select the solution directory to deploy. allow multi-selection of directories. For each selected directory, deploy the solution or input files to the destination directory
        
        base_dir = filedialog.askdirectory(initialdir=base_dir, title='Select solution to publish')
        if base_dir is None or len(base_dir) == 0:
            print("No solution directory selected. Exiting.")
            sys.exit(1)
        deploy_code(base_dir, type, dest_dir)
    

