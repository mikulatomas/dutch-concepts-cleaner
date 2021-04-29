import pytest
from dutch_concepts import DutchConcepts


def test_goodnes_rank_order_label_content(dc_languages):
    for dc in dc_languages:
        compare_to = [
            dc.exemplar_features.category,
            dc.category_features.category,
        ]

        for data in compare_to:
            for category_name, goodness_rank_order in dc.judgements.goodness_rank_order.items():
                assert set(data[category_name].data.index) == set(
                    goodness_rank_order.data.index)
