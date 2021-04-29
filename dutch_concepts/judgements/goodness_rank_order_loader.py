import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc
import dutch_concepts.tools as tools
from dutch_concepts.experiment_data import ExperimentData


class GoodnessRankOrderLoader():
    def __init__(self, experiment_set):
        self.experiment_set = experiment_set

    def load(self):
        dir_name = 'exemplarGoodnessRankOrder'

        ratings = {}

        for csv_f in glob(os.path.join(self.experiment_set.sub_dataset_dir, dir_name, '*.CSV')):
            result = re.search(
                f'^{dir_name}-(.*).CSV$', os.path.basename(csv_f))
            category_name = result.group(1)

            if category_name == 'amphibians':
                continue

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, dtype='unicode', index_col=0, header=None)

            df = self.__clean_dataframe(df)

            category_enum = dc.Category.from_str(category_name)
            ratings[category_enum] = GoodnessRankOrderData(
                df, category_enum)

        return ratings

    def __clean_dataframe(self, df):
        df = tools.drop_all_nan(df)

        # Exemplar names fix
        df.index = map(str.strip, df.index)
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        original_english_exemplars = df.iloc[:, 0]

        if self.experiment_set.dataset.language == 'en':
            exemplars_translation = tools.get_fixed_translation(
                df.index, original_english_exemplars, dc.EXEMPLAR_TRANSLATION_FIXES)

        df.drop(df.columns[0], axis=1, inplace=True)

        if self.experiment_set.dataset.language == 'en':
            df.rename(index=exemplars_translation, inplace=True)

        df.columns = range(df.shape[1])

        df.index.name = 'exemplar'
        df.columns.name = 'respondent'

        df = tools.sort_index_and_columns(df)

        return df


class GoodnessRankOrderData(ExperimentData):
    pass
