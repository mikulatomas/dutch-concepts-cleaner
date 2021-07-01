import os
import re

import numpy as np
import pandas as pd
from glob import glob

import dutch_concepts as dc
import dutch_concepts.tools as tools
from dutch_concepts.experiment_data import ExperimentData


class Features:
    def __init__(self, dataset, feature_type):
        self.feature_type = feature_type
        self.dataset = dataset

        self._features_dir = os.path.join(
            self.dataset.dataset_dir,
            dc.DutchConcepts.CSV_DIR,
            "exemplar feature judgments",
        )

        self.domain = self.__domains_features_loader()
        self.category = self.__semantic_concepts_features_loader()
        self.importance = self.__features_importance_loader()

    def __features_importance_loader(self):
        categories = {}

        for csv_f in glob(
            os.path.join(self._features_dir, "*", f"{self.feature_type.value}*.CSV")
        ):

            result = re.search(
                f"^{self.feature_type.value}FeatureImportanceRatings-(.*).CSV$",
                os.path.basename(csv_f),
            )

            category_name = result.group(1)

            df = pd.read_csv(
                csv_f,
                encoding=dc.DutchConcepts.ENCODING,
                header=None,
                dtype="unicode",
                index_col=0,
            )

            df = self.__clean_importance_dataframe(df)

            std = df.std(axis=1)
            mean = df.mean(axis=1)

            df["mean"] = mean
            df["std"] = std

            category_enum = dc.Category.from_str(category_name)
            categories[category_enum] = FeatureImportanceData(
                df, category_enum, self.feature_type
            )

        return categories

    def __semantic_concepts_features_loader(self):
        features = {}

        for csv_f in glob(
            os.path.join(
                self._features_dir, "*", "*", f"*{self.feature_type.value}*-sum.CSV"
            )
        ):
            result = re.search(
                f"^({self.feature_type.value})(Label)*(.*)Diagonal(.*).CSV$",
                os.path.basename(csv_f),
            )

            category_name = tools.format_category_name(result.group(3))

            respondents = {}

            for csv_f_participant in glob(
                os.path.join(
                    self._features_dir,
                    "*",
                    "*",
                    f"*{self.feature_type.value}*{result.group(3)}*-participant *.CSV",
                )
            ):

                df = pd.read_csv(
                    csv_f_participant,
                    encoding=dc.DutchConcepts.ENCODING,
                    header=None,
                    skipinitialspace=True,
                    dtype="unicode",
                )
                df = self.__clean_features_dataframe(df)
                frequencies = df["freq"]
                df.drop("freq", axis=1, inplace=True)
                df = df.transpose()

                respondents[f"respondent {csv_f_participant[-5]}"] = df

            df = pd.read_csv(
                csv_f,
                encoding=dc.DutchConcepts.ENCODING,
                header=None,
                skipinitialspace=True,
                dtype="unicode",
            )

            df = self.__clean_features_dataframe(df)
            frequencies = df["freq"]
            df.drop("freq", axis=1, inplace=True)
            df = df.transpose()

            category_enum = dc.Category.from_str(category_name)
            features[category_enum] = FeaturesData(
                df, respondents, frequencies, category_enum, self.feature_type
            )

        return features

    def __domains_features_loader(self):
        features = {}

        for csv_f in glob(
            os.path.join(
                self._features_dir,
                "*",
                f"*{self.feature_type.value.capitalize()}*-sum.CSV",
            )
        ):
            result = re.search(
                f"^(.*)(Animal|Artifacts)({self.feature_type.value.capitalize()})(.*).CSV$",
                os.path.basename(csv_f),
            )

            domain_name = result.group(2).lower()

            respondents = {}

            for csv_f_participant in glob(
                os.path.join(
                    self._features_dir,
                    "*",
                    f"*{self.feature_type.value.capitalize()}*-participant *.CSV",
                )
            ):

                df = pd.read_csv(csv_f, encoding=dc.DutchConcepts.ENCODING, header=None)

                df = self.__clean_features_dataframe(df)
                frequencies = df["freq"]
                df.drop("freq", axis=1, inplace=True)
                df = df.transpose()

                respondents[f"respondent {csv_f_participant[-5]}"] = df

            df = pd.read_csv(csv_f, encoding=dc.DutchConcepts.ENCODING, header=None)

            df = self.__clean_features_dataframe(df)
            frequencies = df["freq"]
            df.drop("freq", axis=1, inplace=True)
            df = df.transpose()

            domain_enum = dc.Domain.from_str(domain_name)
            features[domain_enum] = FeaturesData(
                df, respondents, frequencies, domain_enum, self.feature_type
            )

        return features

    def __clean_importance_dataframe(self, df):
        df = tools.drop_all_nan(df)

        # Features names fix
        df.index = map(str.strip, df.index)
        df.rename(index=dc.FEATURE_NAMES_FIXES, inplace=True)

        original_english_features = df.iloc[:, 0]

        if self.dataset.language == "en":
            features_translation = tools.get_fixed_translation(
                df.index, original_english_features, dc.FEATURE_TRANSLATION_FIXES
            )

        df.drop(df.columns[0], axis=1, inplace=True)

        if self.dataset.language == "en":
            df.rename(index=features_translation, inplace=True)

        df.columns = [f"respondent {i}" for i in range(df.shape[1])]

        df.index.name = "feature"
        df.columns.name = None

        df = tools.sort_index_and_columns(df)
        df = df.astype(int)

        return df

    def __clean_features_dataframe(self, df):
        df = tools.drop_all_nan(df)

        # Set right columns
        df.columns = df.iloc[1]
        df.columns = df.columns.fillna("tmp")
        new_columns = list(df.columns)
        new_columns[2] = "freq"
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
        df.index.name = "feature"
        df.columns.name = "exemplar"

        df = df.astype(int)

        # Exemplar names fix
        df.rename(columns=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        # Features names fix
        df.rename(index=dc.FEATURE_NAMES_FIXES, inplace=True)

        # Translation
        if self.dataset.language == "en":
            exemplar_translation = tools.get_fixed_translation(
                df.columns[1:],
                original_english_exemplars,
                dc.EXEMPLAR_TRANSLATION_FIXES,
            )
            features_translation = tools.get_fixed_translation(
                df.index, original_english_features, dc.FEATURE_TRANSLATION_FIXES
            )

            df.rename(columns=exemplar_translation, inplace=True)
            df.rename(index=features_translation, inplace=True)

        df = tools.sort_index_and_columns(df)

        return df


class FeaturesData(ExperimentData):
    def __init__(self, data, respondents, frequencies, name, feature_type):
        super().__init__(data, name)
        self.respondents = respondents
        self.frequencies = frequencies
        self.feature_type = feature_type


class FeatureImportanceData(ExperimentData):
    def __init__(self, data, name, feature_type):
        super().__init__(data, name)
        self.feature_type = feature_type
