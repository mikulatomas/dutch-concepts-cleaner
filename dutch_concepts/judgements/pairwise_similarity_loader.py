import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc
import dutch_concepts.tools as tools
from dutch_concepts.experiment_data import ExperimentData


class PairwiseSimilarityLoader():
    def __init__(self, experiment_set):
        self.experiment_set = experiment_set

    def load(self):
        dir_name = 'pairwise similarities'

        similarities = {}

        load_dir = os.path.join(
            self.experiment_set.dataset.dataset_dir, dc.DutchConcepts.CSV_DIR, dir_name)

        for csv_f in glob(os.path.join(load_dir, '*', '*.CSV')):
            result = re.search(
                '^pairwiseSimilarities(.*)-(.*).CSV$', os.path.basename(csv_f))

            category_name = tools.format_category_name(result.group(1))

            if category_name == 'amphibians':
                continue

            subject_number = result.group(2)

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None, skipinitialspace=True, error_bad_lines=False, dtype='unicode', warn_bad_lines=False)

            df = self.__clean_dataframe(df, category_name)
            name = f"{category_name.capitalize()}PairwiseSimilarities-{subject_number}"

            if similarities.get(category_name):
                similarities.get(category_name)[name] = df
            else:
                similarities[category_name] = {name: df}

        similarities_filtered = {}

        for category_name, datasets in similarities.items():
            category_enum = dc.Category.from_str(category_name)
            similarities_filtered[category_enum] = SimilarityJudgementsData(
                self.__calculate_mean(datasets), datasets, category_enum)

        return similarities_filtered

    def __calculate_mean(self, datasets):
        datasets = list(datasets.values())
        mean = datasets[0]
        for df in datasets[1:]:
            mean += df

        mean /= len(datasets)

        return mean

    def __clean_dataframe(self, df, category_name):
        df = tools.drop_all_nan(df)

        # hack because csv are messy
        if category_name in ['birds', 'clothing', 'fish', 'musical instruments', 'vehicles']:
            index_col = 1
            column_row = 1
        elif category_name in ['fruit', 'professions', 'sports', 'vegetables']:
            index_col = 0
            column_row = 0
        else:
            index_col = 0
            column_row = 1

        # Set the index
        df.index = df.iloc[:, index_col]
        df.index = df.index.fillna('tmp')
        df.index = map(str.strip, df.index)

        # Exemplar names fix
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        if self.experiment_set.dataset.language == 'en':
            exemplar_translation = tools.get_fixed_translation(
                df.index[2:], df.iloc[0 if column_row == 1 else 1][2:], dc.EXEMPLAR_TRANSLATION_FIXES)

        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        # Set the columns
        df.columns = df.iloc[column_row]
        df.columns = map(str.strip, df.columns)

        # Exemplar names fix
        df.rename(columns=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        df.drop(df.index[0], axis=0, inplace=True)
        df.drop(df.index[0], axis=0, inplace=True)

        if self.experiment_set.dataset.language == 'en':
            # Translation
            df.rename(index=exemplar_translation, inplace=True)
            df.rename(columns=exemplar_translation, inplace=True)

        # Name columns and index
        df.index.name = 'exemplar'
        df.columns.name = 'exemplar'

        # Retype to int
        df = df.astype(int)

        df = tools.sort_index_and_columns(df)

        return df


class SimilarityJudgementsData(ExperimentData):
    def __init__(self, data, respondents, name):
        super().__init__(data, name)
        self.respondents = respondents
