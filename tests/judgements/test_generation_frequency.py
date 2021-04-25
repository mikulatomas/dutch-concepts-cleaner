import pytest
from dutch_concepts import DutchConcepts


def test_generation_frequency_label_content(dc_languages):
    for dc in dc_languages:
        compare_to = [
            dc.exemplar_features.category,
            dc.category_features.category,
        ]

        for data in compare_to:
            for concept_name, generation_frequency in dc.judgements.generation_frequency.items():
                assert set(data[concept_name].data.index) == set(
                    generation_frequency.data.index)
