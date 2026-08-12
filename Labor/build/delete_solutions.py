import argparse
from asyncio import subprocess
import os
import shutil
import sys

SERVER_URL = "su765390@5016756940.ssh.w2.strato.hosting"
PATH_TO_KEY = "../../strato_key.ppko"
WEB_ROOT = "/home/www/public/teaching/"

    

def delete_files_ssh(file_path: str, extension: str = "*"):
    # use scp via shell to delete the file from the remote server
    import subprocess   
    
    file_pattern = os.path.join(file_path, extension)    
    file_pattern = file_pattern.replace("\\", "/")    
    print("Deleting file from remote server: " + file_pattern)
    
    subprocess.run(["ssh", "-i", PATH_TO_KEY, f"{SERVER_URL}", "rm", file_pattern], check=False)    



if __name__ == "__main__":    

    parser = argparse.ArgumentParser(description="Delete solution files on remote server")
    parser.add_argument("--basedir", help="Directory on remote server")
    parser.add_argument("--extension", default="*.*", help="File extension to delete")
    args = parser.parse_args()

    base_dir = args.basedir
    extension = args.extension

    if base_dir is None or len(base_dir) == 0:
        raise ValueError("No base directory given")
        sys.exit(1)
        
    
    base_dir = os.path.join( WEB_ROOT, base_dir)          

    delete_files_ssh(base_dir, extension)