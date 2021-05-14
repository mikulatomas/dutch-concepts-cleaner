import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc
import dutch_concepts.tools as tools
from dutch_concepts.experiment_data import ExperimentData


class ImageabilityLoader():
    def __init__(self, experiment_set):
        self.experiment_set = experiment_set

    def load(self):
        dir_name = 'exemplarImageabilityRatings'

        ratings = {}

        for csv_f in glob(os.path.join(self.experiment_set.sub_dataset_dir, dir_name, '*.CSV')):
            result = re.search(
                f'^{dir_name}-(.*).CSV$', os.path.basename(csv_f))
            category_name = result.group(1)

            if category_name == 'amphibians':
                continue

            try:
                df = pd.read_csv(
                    csv_f, encoding=dc.DutchConcepts.ENCODING, skipinitialspace=True, dtype='unicode')
            except:
                df = pd.read_csv(
                    csv_f, encoding=dc.DutchConcepts.ENCODING, skipinitialspace=True, dtype='unicode', usecols=range(42))

            df = self.__clean_dataframe(df)

            category_enum = dc.Category.from_str(category_name)
            ratings[category_enum] = ImageabilityData(
                df, category_enum)

        return ratings

    def __clean_dataframe(self, df):
        df = tools.drop_all_nan(df)

        df.index = df.iloc[:, 0]
        df.index = map(str.strip, df.index)
        # Exemplar names fix
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        if self.experiment_set.dataset.language == 'en':
            exemplar_translation = tools.get_fixed_translation(
                df.index, df.iloc[:, 1], dc.EXEMPLAR_TRANSLATION_FIXES)

        df.drop(df.columns[:-4], axis=1, inplace=True)

        df = df.rename(columns={'average': 'mean',
                                'standard deviation': 'std',
                                'number of participants who know the item': 'nonmissing',
                                "number of 'don't know'-responses": 'missing'
                                })

        df.index.name = 'exemplar'

        if self.experiment_set.dataset.language == 'en':
            df.rename(index=exemplar_translation, inplace=True)

        column_types = {'missing': int, 'nonmissing': int, 'mean': float, 'std': float}
        df = df.astype(column_types)

        df = tools.sort_index_and_columns(df)

        return df


class ImageabilityData(ExperimentData):
    pass
