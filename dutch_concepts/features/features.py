import os
import re

import pandas as pd
from glob import glob

import dutch_concepts as dc
import dutch_concepts.tools as tools


class Features():
    def __init__(self, dataset):
        self.dataset = dataset
        self.sub_dataset_dir = os.path.join(
            self.dataset.dataset_dir, dc.DutchConcepts.CSV_DIR, 'exemplar feature judgments')

        self.domain_category_based, self.domain_exemplar_based = self.__domains_features_loader()
        self.semantic_category_based, self.semantic_exemplar_based = self.__semantic_concepts_features_loader()

    def __semantic_concepts_features_loader(self):
        features = {'exemplar': {}, 'category': {}}

        for csv_f in glob(os.path.join(self.sub_dataset_dir, '*', '*', '*-sum.CSV')):
            result = re.search(
                '^(category|exemplar)(Label)*(.*)Diagonal(.*).CSV$', os.path.basename(csv_f))

            concept_name = ' '.join(re.findall(
                '[A-Z][^A-Z]*', result.group(3))).lower()
            data_type = result.group(1).lower()

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None, skipinitialspace=True)

            df = self.__clean_dataframe(df)
            frequencies = df['freq']
            df.drop('freq', axis=1, inplace=True)
            data = df.transpose()

            features[data_type][concept_name] = FeaturesDataset(
                data, frequencies, f"{concept_name.capitalize()}{data_type.capitalize()}")

        return features['category'], features['exemplar']

    def __domains_features_loader(self):
        features = {'exemplar': {}, 'category': {}}
        translate = {'animal': 'animals', 'artifacts': 'artifacts'}

        for csv_f in glob(os.path.join(self.sub_dataset_dir, '*', '*-sum.CSV')):
            result = re.search(
                '^(.*)(Animal|Artifacts)(Category|Exemplar)(.*).CSV$', os.path.basename(csv_f))
            concept_name = result.group(2).lower()
            concept_name = translate[concept_name]
            data_type = result.group(3).lower()

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None)

            df = self.__clean_dataframe(df)
            frequencies = df['freq']
            df.drop('freq', axis=1, inplace=True)
            data = df.transpose()

            # Translation
            data.rename(index=dc.TRANSLATION_OBJECTS, inplace=True)
            data.rename(columns=dc.TRANSLATION_FEATURES, inplace=True)

            features[data_type][concept_name] = FeaturesDataset(
                data, frequencies, f"{concept_name.capitalize()}{data_type.capitalize()}")

        return features['category'], features['exemplar']

    def __clean_dataframe(self, df):
        df = df.dropna(how='all', axis=0)
        df = df.dropna(how='all', axis=1)

        # if self.dataset.language == 'en':
        # index_col = 1
        # column_row = 0
        # elif self.dataset.language == 'nl':
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

        # Deduplicate and ensure lowercase
        new_columns = [label.lower() for label in df.columns]
        tools.uniquify(new_columns)
        df.columns = new_columns

        new_index = [label.lower() for label in df.index]
        tools.uniquify(new_index)
        df.index = new_index

        # Name columns and index
        df.index.name = 'attribute'
        df.columns.name = 'object'

        df = df.astype(int)

        return df


class FeaturesDataset():
    def __init__(self, data, frequencies, name):
        self.name = name
        self.frequencies = frequencies
        self.data = data
