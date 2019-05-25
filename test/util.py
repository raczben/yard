import os
import shutil

def copy_to_work_dir(work_dir, filepath):
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    dst = os.path.join(work_dir, os.path.basename(filepath))
    shutil.copyfile(filepath, dst)
    