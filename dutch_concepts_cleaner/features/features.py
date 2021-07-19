import os
import re

import numpy as np
import pandas as pd
from glob import glob

import dutch_concepts_cleaner as dc
import dutch_concepts_cleaner.tools as tools
from dutch_concepts_cleaner.experiment_data import ExperimentData

LABEL_HOTFIX = ["feature/ exemplar ENGLISH", "", "a synonym is 'schuiftrompet'", "accompagnies (other) music", "is played by a drummer", "is played by an organist", "is played with a plectrum", "is played during concerts", "is played while standing", "has been existing for a long time", "exists in different measurements", "exists in different sizes", "exists in different colors", "exists in different kinds", "exists in pairs", "consists of different parts", "shines", "creates a good atmosphere", "is used to beat on", "also used as a toy", "een example is the piccolo", "has a skin", "you play chords on it", "you play musical notes on it", "you play rhythms on it", "exists in different tube lengths", "associated with kilt", "used in folk dance", "used in folk music", "used in the Middle Ages", "used in the Mass", "used to announce something", "produces only one sound", "gives a nasty sound", "indicates the rhythm", "made of wood", "made of metal", "checkered", "hangs from a rope", "you need much breath for this", "requires much practise", "has Belgian inventor", "has little bells all round", "has a complex shape", "has a deep sound", "has a dull sound", "has a neck", "has a grip", "has a sound bell", "has a sound box ", "has a keyboard", "has a lid", "has a bag of air", "has a mouthpiece", "makes a nice sound/noise", "requires a belt for wearing it", "has a straw", "has a shrill sound", "has a warm sound", "has a soft sound", "has holes", "has pedals", "has (trousers)legs", "has snares", "has tuning forks", "has buttons", "has drums", "has two keyboards", "has many buttons", "has wings", "has black and white keys", "has white keys", "has black keys", "has a clear sound", "does not weigh much", "can be played upon", "is brown", "is cylindrical", "is triangular", "is expensive", "is a wind instrument", "is part of a drumset", "is part of percussion", "is related to the violin", "is a wind instrument", "is a woodwinds", "is an instrument of the Greek god Pan", "classical instrument", "is a brass player", "is a difficult instrument", "is a musical instrument", "is an old instrument", "is a popular instrument", "is a percussion instrument", "is a string instrument", "is a sort of piano", "is a sort of violin", "is a string instrument with a bow", "is always part of a band", "predecessor of a piano", "is easy to play", "is related to a guitar", "is made of bamboo", "is slippery", "is cheap", "is golden", "is big", "is handy to transport", "is hard", "is hollow", "is small", "is long", "is elongated", "is unwieldy", "is loud", "is melodious", "is Mexican", "is beautiful", "is relaxing", "is rectangular", "is round", "is gracefull", "for sale in a music shop", "is made of iron", "is made of copper", "is for sturdy guys", "is fairly unknown", "is black and white", "is rare", "is silver-coloured", "is southern", "is heavy", "is black", "you can play songs on it", "you can play different notes whit it", "you can learn it in a school of music", "you have to be able to read notes for it", "you have to blow on it", "you have to have good lungs", "you have to read music-scores", "Jo with the banjo", "can be acoustic", "can have cymbals", "can be electronic", "you can pull it (open) and push it", "can be played on", "can be plunked upon", "can sound out of tune", "can be connected to an amplifier", "can mimic different instruments", "can produce different tones at once", "classical music", "sounds fiercely", "sounds low", "sounds nasally", "originates from Scotland", "featured in a brass band", "occurs in a choir", "featured in an orchestra", "occurs in indian culture", "occurs in many (music)bands", "ressembles a piano", "featured in a Luc Steeno song", "makes a bass noise", "makes a special noise", "makes a piercing noise", "produces sound", "produces high pitched sound", "produces noise", "produces music", "makes peacefull music", "produces different sounds", "has to be tuned", "you have to place it to your lips", "you have to hold it diagonally", "one has to learn how to play", "needs to be supported", "hangs around the neck/shoulders", "smells neutral", "has a spike at its base", "played by Toots Tielemans", "its vibrations produce sounds", "invented by Adolphe Sax", "played by Mozart", "works with a shove system", "works with air", "is played while sitting", "played by a musician", "played in a brass band", "played with the mouth", "played with a bow", "played with a stick (sticks)", "played with the fingers", "played by a single person", "used for rock music", "used in folk music", "used in traditional music", "used at parties", "used in jazz music", "used in pop music", "is used in combination with other instruments", "played by gipsies", "is stored in a box", "used in many different musical styles", "played by men", "played with the hands", "played with two hands", "used by referees", "used solo", "sometimes used to accompany voice", "often played in a church", "often used at camp sites", "often used in blues music", "often used by street musicians", "primarily played by girls", "especially played by older people", "played seldomly", "sometimes played on the street", "both large and small", "both hands and feet are used", "", "", "", "", "", ""]


class Features:
    def __init__(self, dataset, feature_type):
        self.feature_type = feature_type
        self.dataset = dataset

        self._features_dir = os.path.join(
            self.dataset.dataset_dir,
            dc.DutchConceptsCleaner.CSV_DIR,
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
                encoding=dc.DutchConceptsCleaner.ENCODING,
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
                    encoding=dc.DutchConceptsCleaner.ENCODING,
                    header=None,
                    skipinitialspace=True,
                    dtype="unicode",
                )

                if 'exemplarMusicalInstrumentsDiagonalMatrices-participant 4' in csv_f_participant:
                    # Handle missing colum in one original file
                    df.insert(loc=1, column=666, value=LABEL_HOTFIX)
                    df.columns = range(df.shape[1])
                    df.dropna(axis=0, inplace=True)
                
                df = self.__clean_features_dataframe(df)
                frequencies = df["freq"]
                df.drop("freq", axis=1, inplace=True)
                df = df.transpose()

                respondents[f"respondent {csv_f_participant[-5]}"] = df

            df = pd.read_csv(
                csv_f,
                encoding=dc.DutchConceptsCleaner.ENCODING,
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
                print(csv_f_participant)
                df = pd.read_csv(csv_f_participant, encoding=dc.DutchConceptsCleaner.ENCODING, header=None)

                df = self.__clean_features_dataframe(df)
                frequencies = df["freq"]
                df.drop("freq", axis=1, inplace=True)
                df = df.transpose()

                respondents[f"respondent {csv_f_participant[-5]}"] = df

            df = pd.read_csv(csv_f, encoding=dc.DutchConceptsCleaner.ENCODING, header=None)

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

        df = df.fillna(0)
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
