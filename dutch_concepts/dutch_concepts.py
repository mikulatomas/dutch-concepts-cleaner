import urllib.request
import os
import zipfile
import re
import logging

from glob import glob

import dutch_concepts.judgements as ej
import dutch_concepts.features as ef

from .enums import FeatureType


class DutchConcepts():
    URL = 'https://static-content.springer.com/esm/art%3A10.3758%2FBRM.40.4.1030/MediaObjects/DeDeyne-BRM-2008b.zip'
    DIR_NAME = 'dutch_concepts'
    ZIP_NAME = 'archive.zip'
    CSV_DIR = 'cvsdata'
    ENCODING = 'ISO-8859-1'

    def __init__(self, root, download=False, language='en'):
        self.root = os.path.abspath(root)
        if language not in ['en', 'nl']:
            raise ValueError("Wrong language, 'en' and 'nl' is supported.")
        self.language = language
        self.dataset_dir = os.path.join(self.root, DutchConcepts.DIR_NAME)

        if not os.path.exists(self.dataset_dir):
            os.makedirs(self.dataset_dir)

        if download:
            if not os.listdir(self.dataset_dir):
                logging.info("Downloading dataset.")
                self.__download()
                logging.info("Downloading is done.")
                logging.info("Extracting dataset.")
                self.__extract()
                logging.info("Extracting done.")
            else:
                logging.info(
                    "Dataset directory is not empty, skipping download.")

        self.judgements = ej.Judgements(self)
        self.exemplar_features = ef.Features(
            self, feature_type=FeatureType.EXEMPLAR)
        self.category_features = ef.Features(
            self, feature_type=FeatureType.CATEGORY)

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
                    logging.info(f"Extracting: {os.path.basename(zip_path)}")

                    new_dir_name = file.replace('.zip', '')
                    if not os.path.exists(os.path.join(subdir, new_dir_name)):
                        os.makedirs(os.path.join(subdir, new_dir_name))

                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(os.path.join(subdir, new_dir_name))

                    os.remove(zip_path)

        os.remove(os.path.join(self.root, DutchConcepts.ZIP_NAME))
