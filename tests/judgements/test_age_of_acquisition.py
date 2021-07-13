import pytest
from dutch_concepts_cleaner import DutchConceptsCleaner


def test_age_of_acquisition_label_content(dc_languages):

    for dc in dc_languages:
        compare_to = [
            dc.exemplar_features.category,
            dc.category_features.category,
        ]

        for data in compare_to:
            for category_name, age_of_acquisition in dc.judgements.age_of_acquisition.items():
                assert set(data[category_name].data.index) == set(
                    age_of_acquisition.data.index)
