import re
import os

from glob import glob
import pandas as pd

import dutch_concepts as dc
import dutch_concepts.tools as tools


class SimilarityJudgementsLoader():
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
            subject_number = result.group(2)

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None, skipinitialspace=True, error_bad_lines=False)

            df = self.__clean_dataframe(df, concept_name)
            name = f"{concept_name.capitalize()}PairwiseSimilarities-{subject_number}"

            if similarities.get(concept_name):
                similarities.get(concept_name)[name] = df
            else:
                similarities[concept_name] = {name: df}

        similarities_filtered = {}

        for concept_name, datasets in similarities.items():
            similarities_filtered[concept_name] = SimilarityJudgementsDataset(
                self.__calculate_mean(datasets), datasets, f"{concept_name.capitalize()}PairwiseSimilarities")

        return similarities_filtered

    def __calculate_mean(self, datasets):
        datasets = list(datasets.values())
        mean = datasets[0]
        for df in datasets[1:]:
            mean += df

        mean /= len(datasets)

        return mean

    def __clean_dataframe(self, df, concept_name):
        df = df.dropna(how='all', axis=0)
        df = df.dropna(how='all', axis=1)

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

        # Exemplar names fix
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        if self.parent_dataset.dataset.language == 'en':
            exemplar_translation = dict(
                zip(df.index.values[2:], map(str.strip, df.iloc[0 if column_row == 1 else 1][2:])))

            # Apply translation fixes
            for original, english in dc.EXEMPLAR_NAMES_TRANSLATION_FIXES.items():
                if exemplar_translation.get(original):
                    exemplar_translation[original] = english

        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)
        df.index = df.index.fillna('drop')

        # Set the columns
        df.columns = df.iloc[column_row]
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

        return df


class SimilarityJudgementsDataset():
    def __init__(self, data, respondents, name):
        self.name = name
        self.data = data
        self.respondents = respondents
