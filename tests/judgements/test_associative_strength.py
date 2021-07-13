import pytest
from dutch_concepts_cleaner import DutchConceptsCleaner


def test_associative_strength_label_content(dc_languages):
    for dc in dc_languages:
        compare_to = [
            dc.exemplar_features.category,
            dc.category_features.category,
        ]

        for data in compare_to:
            for category_name, associative_strength in dc.judgements.associative_strength.items():
                assert set(data[category_name].data.index) == set(
                    associative_strength.data.index)
