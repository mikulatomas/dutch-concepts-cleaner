import os

import dutch_concepts as dc
import dutch_concepts.judgements as ej


class Judgements():
    def __init__(self, dataset):
        self.dataset = dataset
        self.sub_dataset_dir = os.path.join(
            self.dataset.dataset_dir, dc.DutchConcepts.CSV_DIR, 'exemplar judgments')

        self.typicality_ratings = ej.TypicalityRatingsLoader(
            self).load()

        self.similarities = ej.SimilarityJudgementsLoader(
            self).load()
