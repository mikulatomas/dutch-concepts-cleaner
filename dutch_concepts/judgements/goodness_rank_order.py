import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc
import dutch_concepts.tools as tools


class GoodnessRankOrderLoader():
    def __init__(self, parent_dataset):
        self.parent_dataset = parent_dataset

    def load(self):
        dir_name = 'exemplarGoodnessRankOrder'

        ratings = {}

        for csv_f in glob(os.path.join(self.parent_dataset.sub_dataset_dir, dir_name, '*.CSV')):
            result = re.search(
                '^exemplarGoodnessRankOrder-(.*).CSV$', os.path.basename(csv_f))
            concept_name = result.group(1)

            if concept_name == 'amphibians':
                continue

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, dtype='unicode', index_col=0, header=None)

            df = self.__clean_dataframe(df)

            ratings[concept_name] = GoodnessRankOrderDataset(
                df, concept_name)

        return ratings

    def __clean_dataframe(self, df):
        df = tools.drop_all_nan(df)

        # Exemplar names fix
        df.index = map(str.strip, df.index)
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        original_english_exemplars = df.iloc[:, 0]

        if self.parent_dataset.dataset.language == 'en':
            exemplars_translation = tools.get_fixed_translation(
                df.index, original_english_exemplars, dc.EXEMPLAR_TRANSLATION_FIXES)

        df.drop(df.columns[0], axis=1, inplace=True)

        if self.parent_dataset.dataset.language == 'en':
            df.rename(index=exemplars_translation, inplace=True)

        df.columns = range(df.shape[1])

        df.index.name = 'object'
        df.columns.name = 'respondent'

        df = tools.sort_index_and_columns(df)

        return df


class GoodnessRankOrderDataset():
    def __init__(self, data, name):
        self.name = name
        self.data = data

    def __str__(self):
        return "GoodnessRankOrderDataset({})".format(self.name)

    def __repr__(self):
        return "GoodnessRankOrderDataset({})".format(self.name)

    def __len__(self):
        return len(self.data)
