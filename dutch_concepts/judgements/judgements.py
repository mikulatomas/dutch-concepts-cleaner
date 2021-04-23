import os

import dutch_concepts as dc
import dutch_concepts.judgements as dcj


class Judgements():
    def __init__(self, dataset):
        self.dataset = dataset
        self.sub_dataset_dir = os.path.join(
            self.dataset.dataset_dir, dc.DutchConcepts.CSV_DIR, 'exemplar judgments')

        self.typicality = dcj.TypicalityLoader(
            self).load()

        self.pairwise_similarity = dcj.PairwiseSimilarityLoader(
            self).load()

        self.goodness = dcj.GoodnessLoader(
            self).load()

        self.goodness_rank_order = dcj.GoodnessRankOrderLoader(
            self).load()

        self.familiarity = dcj.FamiliarityLoader(self).load()

        self.age_of_acquisition = dcj.AgeOfAcquisitionLoader(self).load()
