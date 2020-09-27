import zipfile
from glob import glob
import os

if not os.path.exists('dataset'):
    os.makedirs('dataset')

for filepath in glob(os.path.join('download', '*.zip')):
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall('dataset')

for subdir, dirs, files in os.walk('dataset'):
    for file in files:
        zippath = os.path.join(subdir, file)
        print(zippath)
        if '.zip' in zippath:
            new_dir_name = file.replace('.zip', '')
            if not os.path.exists(os.path.join(subdir, new_dir_name)):
                os.makedirs(os.path.join(subdir, new_dir_name))

            with zipfile.ZipFile(zippath, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(subdir, new_dir_name))

            os.remove(zippath)
