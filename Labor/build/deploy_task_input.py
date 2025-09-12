import os
import shutil

from tkinter import filedialog

ZIP_EXT = ".zip"


## currently not used!
def deploy_html(task_dir: str, dest_dir: str):
    task_dir = os.path.abspath(task_dir)

    
    if not os.path.exists(task_dir):
        print(f"Task directory {task_dir} does not exist.")
        return
    
    exercise_name = os.path.basename(task_dir)

        
    dest_dir_task = os.path.join(dest_dir, exercise_name)    
    # copy html file to the destination directory    
    html_dir = os.path.join(task_dir, "../../out/html")    
    html_file = os.path.abspath(os.path.join(html_dir, exercise_name + ".doc.html"))    
    os.makedirs(dest_dir_task, exist_ok=True)    
    if os.path.exists(html_file):
        print(html_file + " -> " + dest_dir_task)             
        shutil.copy(html_file, dest_dir_task)
    else:
        print(f"HTML file {html_file} does not exist.")
        return
    

def deploy_task_inputs(task_dir: str, dest_dir: str): 
    task_dir = os.path.abspath(task_dir)

    
    if not os.path.exists(task_dir):
        print(f"Task directory {task_dir} does not exist.")
        return
    
    exercise_name = os.path.basename(task_dir)

    
    # check if input directory exists. If yes, zip it and copy it to the destination directory
    input_dir = os.path.join(task_dir, "input")
    
    if os.path.exists(input_dir):
        zipfile_name = os.path.join(task_dir, exercise_name+ZIP_EXT)
        shutil.make_archive(base_name = zipfile_name.replace(ZIP_EXT, ""), format="zip", root_dir = input_dir)
        print(zipfile_name + " -> " + dest_dir)            
        # make directory for the zip file in the destination directory (if not exits)
        os.makedirs(dest_dir, exist_ok=True)    
        shutil.copy(zipfile_name, dest_dir)  
     
    
    
    
    
    
    


base_dir = './modules/'

task_dir = filedialog.askdirectory(initialdir=base_dir, title='Select task to publish')
#task_dir = r'C:\Users\micha\THU\Lehre\SOMD\Labor\docs\python_exercises'
#task_dir = r'C:\Users\micha\THU\Lehre\SOMD\Labor\docs\simple_patient_monitor'
dest_dir = r'P:\mmunz\Lehre\SOMD\lab\inputs'


deploy_task_inputs(task_dir, dest_dir)