import re
import os

from glob import glob
import pandas as pd
import numpy as np

import dutch_concepts as dc
import dutch_concepts.tools as tools


class AgeOfAcquisitionLoader():
    def __init__(self, parent_dataset):
        self.parent_dataset = parent_dataset

    def load(self):
        dir_name = 'exemplarWFAoAPercKnownRatings'

        ratings = {}

        for csv_f in glob(os.path.join(self.parent_dataset.sub_dataset_dir, dir_name, '*.CSV')):
            result = re.search(
                '^exemplarWFAoAPercKnownRatings-(.*).CSV$', os.path.basename(csv_f))
            concept_name = result.group(1)

            if concept_name == 'amphibians':
                continue

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, dtype='unicode', usecols=range(6))

            reliability = self.__extract_reliability(df)

            df = self.__clean_dataframe(df)

            ratings[concept_name] = AgeOfAcquisitionDataset(
                df, reliability, concept_name)

        return ratings

    def __extract_reliability(self, df):
        reliability = -1
        for col in df.columns:
            match = re.search('^\(estimated reliability = (.*)\)$', col)

            if match:
                reliability = float(match.group(1).replace(',', '.'))

        return reliability

    def __clean_dataframe(self, df):
        df = tools.drop_all_nan(df)

        df.index = df.iloc[:, 0]
        df.index = df.index.fillna('tmp')
        df.index = map(str.strip, df.index)

        if 'tmp' in df.index:
            df.drop('tmp', axis=0, inplace=True)

        # Exemplar names fix
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        if self.parent_dataset.dataset.language == 'en':
            exemplar_translation = tools.get_fixed_translation(
                df.index, df.iloc[:, 1], dc.EXEMPLAR_TRANSLATION_FIXES)
            df.rename(index=exemplar_translation, inplace=True)

        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        df.index.name = 'object'

        df = df.replace('??', np.nan)
        df = df.astype(float)

        df = tools.sort_index_and_columns(df)

        return df


class AgeOfAcquisitionDataset():
    def __init__(self, data, reliability, name):
        self.name = name
        self.reliability = reliability
        self.data = data

    def __str__(self):
        return "AgeOfAcquisitionDataset({})".format(self.name)

    def __repr__(self):
        return "AgeOfAcquisitionDataset({})".format(self.name)

    def __len__(self):
        return len(self.data)
