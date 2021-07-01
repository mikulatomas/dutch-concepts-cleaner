import re
import os

from glob import glob
import pandas as pd
import numpy as np

import dutch_concepts as dc
import dutch_concepts.tools as tools
from dutch_concepts.experiment_data import ExperimentData


class WordFrequncyLoader:
    def __init__(self, experiment_set):
        self.experiment_set = experiment_set

    def load(self):
        dir_name = "exemplarWFAoAPercKnownRatings"

        ratings = {}

        for csv_f in glob(
            os.path.join(self.experiment_set.sub_dataset_dir, dir_name, "*.CSV")
        ):
            result = re.search(f"^{dir_name}-(.*).CSV$", os.path.basename(csv_f))
            category_name = result.group(1)

            if category_name == "amphibians":
                continue

            df = pd.read_csv(
                csv_f,
                encoding=dc.DutchConcepts.ENCODING,
                dtype="unicode",
                usecols=range(6),
            )

            df = self.__clean_dataframe(df)

            category_enum = dc.Category.from_str(category_name)
            ratings[category_enum] = WordFrequncyData(df, category_enum)

        return ratings

    def __clean_dataframe(self, df):
        df = tools.drop_all_nan(df)

        df.index = df.iloc[:, 0]
        df.index = df.index.fillna("tmp")
        df.index = map(str.strip, df.index)

        if "tmp" in df.index:
            df.drop("tmp", axis=0, inplace=True)

        # Exemplar names fix
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        if self.experiment_set.dataset.language == "en":
            exemplar_translation = tools.get_fixed_translation(
                df.index, df.iloc[:, 1], dc.EXEMPLAR_TRANSLATION_FIXES
            )
            df.rename(index=exemplar_translation, inplace=True)

        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        df.index.name = "exemplar"

        df = df.replace("??", np.nan)
        df = df.astype(float)

        df = tools.sort_index_and_columns(df)

        df.drop(["% known", "age of acquisition"], axis=1, inplace=True)

        return df


class WordFrequncyData(ExperimentData):
    def __init__(self, data, name):
        super().__init__(data, name)
