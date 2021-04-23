import pytest
from dutch_concepts import DutchConcepts


@pytest.mark.parametrize(
    'lang', ['en', 'nl'])
def test_goodnes_rank_order_label_content(lang):
    dc = DutchConcepts(root='tests', download=True, language=lang)

    compare_to = [
        dc.exemplar_features.category,
        dc.category_features.category,
    ]

    for data in compare_to:
        for concept_name, goodness_rank_order in dc.judgements.goodness_rank_order.items():
            assert set(data[concept_name].data.index) == set(
                goodness_rank_order.data.index)
