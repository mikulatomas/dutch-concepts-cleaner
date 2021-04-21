import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc
import dutch_concepts.tools as tools


class TypicalityRatingsLoader():
    def __init__(self, parent_dataset):
        self.parent_dataset = parent_dataset

    def load(self):
        dir_name = 'exemplarTypicalityRatings'

        ratings = {}

        for csv_f in glob(os.path.join(self.parent_dataset.sub_dataset_dir, dir_name, '*.CSV')):
            result = re.search(
                '^exemplarTypicalityRatings-(.*).CSV$', os.path.basename(csv_f))
            concept_name = result.group(1)

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, skipinitialspace=True, dtype='unicode')
            reliability = self.__extract_reliability(df)

            df = self.__clean_dataframe(df)

            ratings[concept_name] = TypicalityJudgementsDataset(
                df, reliability, f"{concept_name.capitalize()}TypicalityRatings")

        return ratings

    def __extract_reliability(self, df):
        reliability = -1
        for col in df.columns:
            match = re.search('^reliability=(.*)$', col)

            if match:
                reliability = float(match.group(1).replace(',', '.'))

        return reliability

    def __clean_dataframe(self, df):
        df = df.dropna(how='all', axis=0)
        df = df.dropna(how='all', axis=1)

        df.index = df.iloc[:, 0]

        # Exemplar names fix
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        if self.parent_dataset.dataset.language == 'en':
            exemplar_translation = dict(
                zip(df.index.values, map(str.strip, df.iloc[:, 1].values)))

            # Apply translation fixes
            for original, english in dc.EXEMPLAR_NAMES_TRANSLATION_FIXES.items():
                if exemplar_translation.get(original):
                    exemplar_translation[original] = english

        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        new_index = [label.lower() for label in df.index]
        tools.uniquify(new_index)

        df.index = new_index
        df.index.name = 'object'

        if self.parent_dataset.dataset.language == 'en':
            # Translation
            df.rename(index=exemplar_translation, inplace=True)

        new_columns = []
        for i, name in enumerate(df.columns):
            if 'Unnamed' in name:
                new_columns.append(f"subject {i}")
            else:
                new_columns.append(name)

        df.columns = new_columns

        df = df.astype(float)

        return df


class TypicalityJudgementsDataset():
    def __init__(self, data, reliability, name):
        self.name = name
        self.reliability = reliability
        self.data = data
