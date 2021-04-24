import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc
import dutch_concepts.tools as tools


class ImageabilityLoader():
    def __init__(self, parent_dataset):
        self.parent_dataset = parent_dataset

    def load(self):
        dir_name = 'exemplarImageabilityRatings'

        ratings = {}

        for csv_f in glob(os.path.join(self.parent_dataset.sub_dataset_dir, dir_name, '*.CSV')):
            result = re.search(
                '^exemplarImageabilityRatings-(.*).CSV$', os.path.basename(csv_f))
            concept_name = result.group(1)

            if concept_name == 'amphibians':
                continue

            try:
                df = pd.read_csv(
                    csv_f, encoding=dc.DutchConcepts.ENCODING, skipinitialspace=True, dtype='unicode')
            except:
                df = pd.read_csv(
                    csv_f, encoding=dc.DutchConcepts.ENCODING, skipinitialspace=True, dtype='unicode', usecols=range(42))

            df = self.__clean_dataframe(df)

            ratings[concept_name] = ImageabilityDataset(
                df, concept_name)

        return ratings

    def __clean_dataframe(self, df):
        df = tools.drop_all_nan(df)

        df.index = df.iloc[:, 0]
        df.index = map(str.strip, df.index)
        # Exemplar names fix
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        if self.parent_dataset.dataset.language == 'en':
            exemplar_translation = tools.get_fixed_translation(
                df.index, df.iloc[:, 1], dc.EXEMPLAR_TRANSLATION_FIXES)

        # df.drop(df.columns[0], axis=1, inplace=True)
        # df.drop(df.columns[0], axis=1, inplace=True)

        df.drop(df.columns[:-4], axis=1, inplace=True)

        df = df.rename(columns={'average': 'mean',
                                'standard deviation': 'std',
                                'number of participants who know the item': 'nonmissing',
                                "number of 'don't know'-responses": 'missing'
                                })

        df.index.name = 'object'

        if self.parent_dataset.dataset.language == 'en':
            df.rename(index=exemplar_translation, inplace=True)

        df = df.astype(float)

        df = tools.sort_index_and_columns(df)

        return df


class ImageabilityDataset():
    def __init__(self, data, name):
        self.name = name
        self.data = data

    def __str__(self):
        return "ImageabilityDataset({})".format(self.name)

    def __repr__(self):
        return "ImageabilityDataset({})".format(self.name)

    def __len__(self):
        return len(self.data)
