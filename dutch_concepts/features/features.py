import os
import re

import numpy as np
import pandas as pd
from glob import glob

import dutch_concepts as dc
import dutch_concepts.tools as tools


class Features():
    def __init__(self, dataset, feature_type):
        self.feature_type = feature_type
        self.dataset = dataset

        self._features_dir = os.path.join(
            self.dataset.dataset_dir, dc.DutchConcepts.CSV_DIR, 'exemplar feature judgments')

        self.domain = self.__domains_features_loader()
        self.category = self.__semantic_concepts_features_loader()
        self.importance = self.__features_importance_loader()

    def __features_importance_loader(self):
        categories = {}

        for csv_f in glob(os.path.join(self._features_dir, '*', f'{self.feature_type.value}*.CSV')):

            result = re.search(
                f'^{self.feature_type.value}FeatureImportanceRatings-(.*).CSV$', os.path.basename(csv_f))

            concept_name = result.group(1)
            # TODO generalize to all
            if dc.CATEGORY_NAMES_FIXES.get(concept_name):
                concept_name = dc.CATEGORY_NAMES_FIXES.get(concept_name)

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None, dtype='unicode', index_col=0)

            df = self.__clean_importance_dataframe(df)

            categories[concept_name] = FeatureImportanceDataset(
                df, concept_name, self.feature_type)

        return categories

    def __semantic_concepts_features_loader(self):
        features = {}

        for csv_f in glob(os.path.join(self._features_dir, '*', '*', f'*{self.feature_type.value}*-sum.CSV')):
            result = re.search(
                f'^({self.feature_type.value})(Label)*(.*)Diagonal(.*).CSV$', os.path.basename(csv_f))

            concept_name = tools.format_concept_name(result.group(3))

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None, skipinitialspace=True, dtype='unicode')

            df = self.__clean_features_dataframe(df)
            frequencies = df['freq']
            df.drop('freq', axis=1, inplace=True)
            df = df.transpose()

            features[concept_name] = FeaturesDataset(
                df,
                frequencies,
                concept_name,
                self.feature_type)

        return features

    def __domains_features_loader(self):
        features = {}
        # translate = {'animal': 'animal', 'artifacts': 'artifact'}

        for csv_f in glob(os.path.join(self._features_dir, '*', f'*{self.feature_type.value.capitalize()}*-sum.CSV')):
            result = re.search(
                f'^(.*)(Animal|Artifacts)({self.feature_type.value.capitalize()})(.*).CSV$', os.path.basename(csv_f))

            concept_name = result.group(2).lower()

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None)

            df = self.__clean_features_dataframe(df)
            frequencies = df['freq']
            df.drop('freq', axis=1, inplace=True)
            df = df.transpose()

            features[concept_name] = FeaturesDataset(
                df,
                frequencies,
                concept_name,
                self.feature_type)

        return features

    def __clean_importance_dataframe(self, df):
        df = tools.drop_all_nan(df)

        # Features names fix
        df.index = map(str.strip, df.index)
        df.rename(index=dc.FEATURE_NAMES_FIXES, inplace=True)

        original_english_features = df.iloc[:, 0]

        if self.dataset.language == 'en':
            features_translation = tools.get_fixed_translation(
                df.index, original_english_features, dc.FEATURE_TRANSLATION_FIXES)

        df.drop(df.columns[0], axis=1, inplace=True)

        if self.dataset.language == 'en':
            df.rename(index=features_translation, inplace=True)

        df.columns = range(df.shape[1])

        df.index.name = 'attribute'
        df.columns.name = 'respondent'

        return df

    def __clean_features_dataframe(self, df):
        df = tools.drop_all_nan(df)

        # Set right columns
        df.columns = df.iloc[1]
        df.columns = df.columns.fillna('tmp')
        new_columns = list(df.columns)
        new_columns[2] = 'freq'
        df.columns = new_columns
        df.columns = map(str.strip, df.columns)

        original_english_exemplars = df.iloc[0][3:].values

        df.drop(df.index[0], axis=0, inplace=True)
        df.drop(df.index[0], axis=0, inplace=True)

        # Set right index
        df.index = df.iloc[:, 0]
        df.index = map(str.strip, df.index)
        original_english_features = df.iloc[:, 1].values

        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        # Name columns and index
        df.index.name = 'attribute'
        df.columns.name = 'object'

        df = df.astype(int)

        # Exemplar names fix
        df.rename(columns=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        # Features names fix
        df.rename(index=dc.FEATURE_NAMES_FIXES, inplace=True)

        # Translation
        if self.dataset.language == 'en':
            exemplar_translation = tools.get_fixed_translation(
                df.columns[1:], original_english_exemplars, dc.EXEMPLAR_TRANSLATION_FIXES)
            features_translation = tools.get_fixed_translation(
                df.index, original_english_features, dc.FEATURE_TRANSLATION_FIXES)

            df.rename(columns=exemplar_translation, inplace=True)
            df.rename(index=features_translation, inplace=True)

        return df


class FeaturesDataset():
    def __init__(self, data, frequencies, name, feature_type):
        self.name = name
        self.frequencies = frequencies
        self.data = data
        self.feature_type = feature_type

    def __str__(self):
        return "DutchFeatureDataset({})".format(self.name)

    def __repr__(self):
        return "DutchFeatureDataset({})".format(self.name)

    def __len__(self):
        return len(self.data)


class FeatureImportanceDataset():
    def __init__(self, data, name, feature_type):
        self.name = name
        self.data = data
        self.feature_type = feature_type

    def __str__(self):
        return "DutchFeatureImportanceDataset({})".format(self.name)

    def __repr__(self):
        return "DutchFeatureImportanceDataset({})".format(self.name)

    def __len__(self):
        return len(self.data)
