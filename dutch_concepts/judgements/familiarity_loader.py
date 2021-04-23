import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc
import dutch_concepts.tools as tools


class FamiliarityLoader():
    def __init__(self, parent_dataset):
        self.parent_dataset = parent_dataset

    def load(self):
        dir_name = 'exemplarFamiliarityRatings'

        ratings = {}

        for csv_f in glob(os.path.join(self.parent_dataset.sub_dataset_dir, dir_name, '*.CSV')):
            result = re.search(
                '^exemplarFamiliarityRatings-(.*).CSV$', os.path.basename(csv_f))
            concept_name = result.group(1)

            if concept_name == 'amphibians':
                continue

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, skipinitialspace=True, dtype='unicode')
            reliability = self.__extract_reliability(df)

            df = self.__clean_dataframe(df)

            ratings[concept_name] = FamiliarityDataset(
                df, reliability, concept_name)

        return ratings

    def __extract_reliability(self, df):
        reliability = -1
        for col in df.columns:
            match = re.search('^reliability=(.*)$', col)

            if match:
                reliability = float(match.group(1).replace(',', '.'))

        return reliability

    def __clean_dataframe(self, df):
        df = tools.drop_all_nan(df)

        df.index = df.iloc[:, 0]
        df.index = map(str.strip, df.index)

        # Exemplar names fix
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        if self.parent_dataset.dataset.language == 'en':
            exemplar_translation = tools.get_fixed_translation(
                df.index, df.iloc[:, 1], dc.EXEMPLAR_TRANSLATION_FIXES)

        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        df.index.name = 'object'

        if self.parent_dataset.dataset.language == 'en':
            df.rename(index=exemplar_translation, inplace=True)

        new_columns = []
        for i, name in enumerate(df.columns):
            if 'Unnamed' in name:
                new_columns.append(f"respondent {i}")
            else:
                new_columns.append(name)

        df.columns = new_columns

        df = df.astype(float)

        df = tools.sort_index_and_columns(df)

        return df


class FamiliarityDataset():
    def __init__(self, data, reliability, name):
        self.name = name
        self.reliability = reliability
        self.data = data

    def __str__(self):
        return "FamiliarityDataset({})".format(self.name)

    def __repr__(self):
        return "FamiliarityDataset({})".format(self.name)

    def __len__(self):
        return len(self.data)
