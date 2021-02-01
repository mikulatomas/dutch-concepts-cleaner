import os
import re

import pandas as pd
from glob import glob

import dutch_concepts as dc


class ExemplarFeatures():
    def __init__(self, dataset):
        self.dataset = dataset
        self.sub_dataset_dir = os.path.join(
            self.dataset.dataset_dir, dc.DutchConcepts.CSV_DIR, 'exemplar feature judgments')

        self.category_based, self.exemplar_based = self.__loader()

    def __loader(self):
        category_based_part_1, exemplar_based_part_1 = self.__other_concepts_loader()

        category_based_part_2, exemplar_based_part_2 = self.__animals_artifacts_loader()

        # Join the dicts
        category_based = {**category_based_part_1, **category_based_part_2}
        exemplar_based = {**exemplar_based_part_1, **exemplar_based_part_2}

        return category_based, exemplar_based

    def __other_concepts_loader(self):
        features = {'exemplar': {}, 'category': {}}

        for csv_f in glob(os.path.join(self.sub_dataset_dir, '*', '*', '*-sum.CSV')):
            result = re.search(
                '^(category|exemplar)(Label)*(.*)Diagonal(.*).CSV$', os.path.basename(csv_f))

            concept_name = ' '.join(re.findall(
                '[A-Z][^A-Z]*', result.group(3))).lower()
            data_type = result.group(1).lower()

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None)

            df = self.__clean_dataframe(df)
            frequencies = df['freq']
            df.drop('freq', axis=1, inplace=True)
            data = df.transpose()

            features[data_type][concept_name] = {
                'data': data, 'frequencies': frequencies}

        return features['category'], features['exemplar']

    def __animals_artifacts_loader(self):
        features = {'exemplar': {}, 'category': {}}
        translate = {'animal': 'animals', 'artifacts': 'artifacts'}

        for csv_f in glob(os.path.join(self.sub_dataset_dir, '*', '*-sum.CSV')):
            result = re.search(
                '^(.*)(Animal|Artifacts)(Category|Exemplar)(.*).CSV$', os.path.basename(csv_f))
            concept_name = result.group(2).lower()
            data_type = result.group(3).lower()

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None)

            df = self.__clean_dataframe(df)
            frequencies = df['freq']
            df.drop('freq', axis=1, inplace=True)
            data = df.transpose()

            features[data_type][translate[concept_name]] = {
                'data': data, 'frequencies': frequencies}

        return features['category'], features['exemplar']

    def __clean_dataframe(self, df):
        df = df.dropna(how='all', axis=0)
        df = df.dropna(how='all', axis=1)

        if self.dataset.language == 'en':
            index_col = 1
            column_row = 0
        elif self.dataset.language == 'nl':
            index_col = 0
            column_row = 1

        # Set the right column
        df.columns = df.iloc[column_row]
        df.drop(df.index[0], axis=0, inplace=True)
        df.drop(df.index[0], axis=0, inplace=True)

        # Set the right index
        df.index = df.iloc[:, index_col]
        new_columns = list(df.columns)
        new_columns[2] = 'freq'
        df.columns = new_columns
        df.columns = df.columns.fillna('drop')
        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        # Name columns and index
        df.index.name = 'attribute'
        df.columns.name = 'object'

        return df
