import pytest
from dutch_concepts_cleaner import DutchConceptsCleaner


def test_pairwise_similarity_same_labels(dc_languages):
    for dc in dc_languages:
        for _, data in dc.judgements.pairwise_similarity.items():
            assert set(data.data.index.values) == set(data.data.columns.values)


def test_pairwise_similarity_label_content(dc_languages):
    for dc in dc_languages:
        compare_to = [
            dc.exemplar_features.category,
            dc.category_features.category,
        ]

        for data in compare_to:
            for category_name, similarity in dc.judgements.pairwise_similarity.items():
                assert set(data[category_name].data.index) == set(
                    similarity.data.index)
