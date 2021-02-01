import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc


class TypicalityRatingsLoader():
    def __init__(self, parent_dataset):
        self.parent_dataset = parent_dataset

    def load(self, directory):
        dir_name = 'exemplarTypicalityRatings'

        ratings = {}

        for csv_f in glob(os.path.join(directory, dir_name, '*.CSV')):
            result = re.search(
                '^exemplarTypicalityRatings-(.*).CSV$', os.path.basename(csv_f))
            concept_name = result.group(1)

            df = pd.read_csv(csv_f, encoding=dc.DutchConcepts.ENCODING)
            reliability = self.__extract_reliability(df)

            df = self.__clean_dataframe(df)

            ratings[concept_name] = {
                'data': df, 'reliability': reliability}

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

        if self.parent_dataset.dataset.language == 'en':
            index_col = 1
        else:
            index_col = 0

        df.index = df.iloc[:, index_col]
        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        df.index.name = 'object'

        new_columns = []
        for i, name in enumerate(df.columns):
            if 'Unnamed' in name:
                new_columns.append(f"subject {i}")
            else:
                new_columns.append(name)

        df.columns = new_columns

        return df
