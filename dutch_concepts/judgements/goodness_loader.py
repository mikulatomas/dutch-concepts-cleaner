import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc
import dutch_concepts.tools as tools
from dutch_concepts.experiment_data import ExperimentData


class GoodnessLoader():
    def __init__(self, experiment_set):
        self.experiment_set = experiment_set

    def load(self):
        dir_name = 'exemplarGoodnessRatings'

        ratings = {}

        for csv_f in glob(os.path.join(self.experiment_set.sub_dataset_dir, dir_name, '*.CSV')):
            result = re.search(
                f'^{dir_name}-(.*).CSV$', os.path.basename(csv_f))
            category_name = result.group(1)

            if category_name == 'amphibians':
                continue

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, skipinitialspace=True, dtype='unicode')
            reliability = self.__extract_reliability(df)

            df = self.__clean_dataframe(df)

            category_enum = dc.Category.from_str(category_name)
            ratings[category_enum] = GoodnessData(
                df, reliability, category_enum)

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

        if self.experiment_set.dataset.language == 'en':
            exemplar_translation = tools.get_fixed_translation(
                df.index, df.iloc[:, 1], dc.EXEMPLAR_TRANSLATION_FIXES)

        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        df.index.name = 'exemplar'

        if self.experiment_set.dataset.language == 'en':
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


class GoodnessData(ExperimentData):
    def __init__(self, data, reliability, name):
        super().__init__(data, name)
        self.reliability = reliability
