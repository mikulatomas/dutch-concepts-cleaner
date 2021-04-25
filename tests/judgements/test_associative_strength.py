import pytest
from dutch_concepts import DutchConcepts


def test_associative_strength_label_content(dc_languages):
    for dc in dc_languages:
        compare_to = [
            dc.exemplar_features.category,
            dc.category_features.category,
        ]

        for data in compare_to:
            for concept_name, associative_strength in dc.judgements.associative_strength.items():
                assert set(data[concept_name].data.index) == set(
                    associative_strength.data.index)
