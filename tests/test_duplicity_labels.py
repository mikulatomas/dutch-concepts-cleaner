import pytest

from dutch_concepts_cleaner import DutchConceptsCleaner


def test_duplicity_index(dc_languages):
    for dc in dc_languages:
        data = [dc.judgements.typicality,
                dc.category_features.importance,
                dc.exemplar_features.importance]

        for sub_data in data:
            for _, data in sub_data.items():
                assert data.data.index.duplicated().any() == False


def test_duplicity_both(dc_languages):
    for dc in dc_languages:
        data = [dc.category_features.domain,
                dc.category_features.category,
                dc.exemplar_features.domain,
                dc.exemplar_features.category,
                dc.judgements.pairwise_similarity]

        for sub_data in data:
            for _, data in sub_data.items():
                assert data.data.index.duplicated().any() == False
                assert data.data.columns.duplicated().any() == False
