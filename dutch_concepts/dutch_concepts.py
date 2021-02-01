import urllib.request
import os
import zipfile
import re

from glob import glob

import dutch_concepts.exemplar_judgements as ej
import dutch_concepts.exemplar_features as ef


class DutchConcepts():
    URL = 'https://static-content.springer.com/esm/art%3A10.3758%2FBRM.40.4.1030/MediaObjects/DeDeyne-BRM-2008b.zip'
    DIR_NAME = 'dutch_concepts'
    ZIP_NAME = 'archive.zip'
    CSV_DIR = 'cvsdata'
    ENCODING = 'ISO-8859-1'

    def __init__(self, root, download=False, language='en'):
        self.root = root
        if language not in ['en', 'nl']:
            raise ValueError("Wrong language, 'en' and 'nl' is supported.")
        self.language = language
        self.dataset_dir = os.path.join(self.root, DutchConcepts.DIR_NAME)

        self.exemplar_judgements = ej.ExemplarJudgements(self)
        self.exemplar_features = ef.ExemplarFeatures(self)

        if not os.path.exists(self.dataset_dir):
            os.makedirs(self.dataset_dir)

        if download:
            if not os.listdir(self.dataset_dir):
                print("Downloading dataset.")
                self.__download()
                print("Downloading is done.")
                print("Extracting dataset.")
                self.__extract()
                print("Extracting done.")
            else:
                print("Dataset directory is not empty, skipping download.")

    def __download(self):
        with urllib.request.urlopen(DutchConcepts.URL) as f:
            with open(os.path.join(self.root, DutchConcepts.ZIP_NAME), 'wb') as out_f:
                out_f.write(f.read())

    def __extract(self):
        with zipfile.ZipFile(os.path.join(self.root, DutchConcepts.ZIP_NAME), 'r') as zip_f:
            zip_f.extractall(self.dataset_dir)

        for subdir, _, files in os.walk(self.dataset_dir):
            for file in files:
                zip_path = os.path.join(subdir, file)
                if '.zip' in zip_path:
                    print(f"Extracting: {os.path.basename(zip_path)}")

                    new_dir_name = file.replace('.zip', '')
                    if not os.path.exists(os.path.join(subdir, new_dir_name)):
                        os.makedirs(os.path.join(subdir, new_dir_name))

                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(os.path.join(subdir, new_dir_name))

                    os.remove(zip_path)

        os.remove(os.path.join(self.root, DutchConcepts.ZIP_NAME))
