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

    def __semantic_concepts_features_loader(self):
        features = {}

        for csv_f in glob(os.path.join(self._features_dir, '*', '*', f'*{self.feature_type.value}*-sum.CSV')):
            result = re.search(
                f'^({self.feature_type.value})(Label)*(.*)Diagonal(.*).CSV$', os.path.basename(csv_f))

            concept_name = tools.format_concept_name(result.group(3))

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, header=None, skipinitialspace=True, dtype='unicode')

            df = self.__clean_dataframe(df)
            frequencies = df['freq']
            df.drop('freq', axis=1, inplace=True)
            df = df.transpose()

            # Exemplar names fix
            df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

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

            df = self.__clean_dataframe(df)
            frequencies = df['freq']
            df.drop('freq', axis=1, inplace=True)
            df = df.transpose()

            features[concept_name] = FeaturesDataset(
                df,
                frequencies,
                concept_name,
                self.feature_type)

        return features

    def __clean_dataframe(self, df):
        df = df.dropna(how='all', axis=0)
        df = df.dropna(how='all', axis=1)

        df.columns = df.iloc[1]

        # Exemplar names fix
        df.rename(columns=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        if self.dataset.language == 'en':
            exemplar_translation = dict(
                zip(df.columns[3:], map(str.strip, df.iloc[0][3:])))

            # Apply translation fixes
            for original, english in dc.EXEMPLAR_NAMES_TRANSLATION_FIXES.items():
                if exemplar_translation.get(original):
                    exemplar_translation[original] = english

            features_translation = dict(
                zip(df.iloc[:, 0], df.iloc[:, 1]))

            # Apply translation fixes
            for original, english in dc.FEATURE_NAMES_TRANSLATION_FIXES.items():
                if features_translation.get(original):
                    features_translation[original] = english

        # Set the right column
        df.drop(df.index[0], axis=0, inplace=True)
        df.drop(df.index[0], axis=0, inplace=True)

        # Set the right index
        df.index = df.iloc[:, 0]
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

        if self.dataset.language == 'en':
            # Exemplar translation
            df.rename(columns=exemplar_translation, inplace=True)
            df.rename(index=features_translation, inplace=True)

        import collections
        duplicity = [(item, count) for item, count in collections.Counter(
            df.index).items() if count > 1]

        if duplicity:
            raise ValueError(duplicity)

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

    def __getitem__(self, index):
        return self.data.iloc[index].to_numpy(dtype=np.single), self.data.index[index]
