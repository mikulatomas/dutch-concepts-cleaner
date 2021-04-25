import re
import os

from glob import glob
import pandas as pd
import numpy as np

import dutch_concepts as dc
import dutch_concepts.tools as tools
from dutch_concepts.experiment_data import ExperimentData


class GenerationFrequencyAndAssociativeLoader():
    def __init__(self, experiment_set):
        self.experiment_set = experiment_set

    def load(self):
        dir_name = 'exemplarGenerationFreqAssociationsFreq'

        generation_freq = {}
        association_freq = {}

        for csv_f in glob(os.path.join(self.experiment_set.sub_dataset_dir, dir_name, '*.CSV')):
            result = re.search(
                f'^{dir_name}-(.*).CSV$', os.path.basename(csv_f))
            concept_name = result.group(1)

            if concept_name == 'amphibians' or concept_name == 'animals':
                continue

            df = pd.read_csv(
                csv_f, encoding=dc.DutchConcepts.ENCODING, dtype='unicode', usecols=range(6))

            df = self.__clean_dataframe(df)

            df_gen_freq = df.drop(
                ['exemplar strength', 'category strength'], axis=1)
            df_assoc_freq = df.drop(
                ['generation frequency', 'mean rank position'], axis=1)

            generation_freq[concept_name] = GenerationFrequencyData(
                df_gen_freq, concept_name)
            association_freq[concept_name] = AssociativeStrengthData(
                df_assoc_freq, concept_name)

        return generation_freq, association_freq

    def __clean_dataframe(self, df):
        df = tools.drop_all_nan(df)

        df.index = df.iloc[:, 0]
        df.index = df.index.fillna('tmp')
        df.index = map(str.strip, df.index)

        # Exemplar names fix
        df.rename(index=dc.EXEMPLAR_NAMES_FIXES, inplace=True)

        if self.experiment_set.dataset.language == 'en':
            exemplar_translation = tools.get_fixed_translation(
                df.index, df.iloc[:, 1], dc.EXEMPLAR_TRANSLATION_FIXES)
            df.rename(index=exemplar_translation, inplace=True)

        df.drop(df.columns[0], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        df.index.name = 'object'

        df = df.astype(float)

        df = tools.sort_index_and_columns(df)

        return df


class GenerationFrequencyData(ExperimentData):
    pass


class AssociativeStrengthData(ExperimentData):
    pass
