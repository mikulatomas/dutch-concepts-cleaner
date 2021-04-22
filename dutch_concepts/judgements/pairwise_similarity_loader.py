import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc
import dutch_concepts.tools as tools


class PairwiseSimilarityLoader():
    def __init__(self, parent_dataset):
        self.parent_dataset = parent_dataset

    def load(self):
        dir_name = 'pairwise similarities'

        similarities = {}

        load_dir = os.path.join(
            self.parent_dataset.dataset.dataset_dir, dc.DutchConcepts.CSV_DIR, dir_name)

        for csv_f in glob(os.path.join(load_dir, '*', '*.CSV')):
            result = re.search(
                '^pairwiseSimilarities(.*)-(.*).CSV$', os.path.basename(csv_f))

            concept_name = tools.format_concept_name(result.group(1))

            if concept_name == 'amphibians':
                continue

            subject_number = result.group(2)

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None, skipinitialspace=True, error_bad_lines=False, dtype='unicode')

            df = self.__clean_dataframe(df, concept_name)
            name = f"{concept_name.capitalize()}PairwiseSimilarities-{subject_number}"

            if similarities.get(concept_name):
                similarities.get(concept_name)[name] = df
            else:
                similarities[concept_name] = {name: df}

        similarities_filtered = {}

        for concept_name, datasets in similarities.items():
            similarities_filtered[concept_name] = SimilarityJudgementsDataset(
                self.__calculate_mean(datasets), datasets, concept_name)

        return similarities_filtered

    def __calculate_mean(self, datasets):
        datasets = list(datasets.values())
        mean = datasets[0]
        for df in datasets[1:]:
            mean += df

        mean /= len(datasets)

        return mean

    def __clean_dataframe(self, df, concept_name):
        df = tools.drop_all_nan(df)

        # hack because csv are messy
        if concept_name in ['birds', 'clothing', 'fish', 'musical instruments', 'vehicles']:
            index_col = 1
            column_row = 1
        elif concept_name in ['fruit', 'professions', 'sports', 'vegetables']:
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

        if self.parent_dataset.dataset.language == 'en':
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

        if self.parent_dataset.dataset.language == 'en':
            # Translation
            df.rename(index=exemplar_translation, inplace=True)
            df.rename(columns=exemplar_translation, inplace=True)

        # Name columns and index
        df.index.name = 'object'
        df.columns.name = 'object'

        # Retype to int
        df = df.astype(int)

        df = tools.sort_index_and_columns(df)

        return df


class SimilarityJudgementsDataset():
    def __init__(self, data, respondents, name):
        self.name = name
        self.data = data
        self.respondents = respondents

    def __str__(self):
        return "SimilarityJudgementsDataset({})".format(self.name)

    def __repr__(self):
        return "SimilarityJudgementsDataset({})".format(self.name)

    def __len__(self):
        return len(self.data)
