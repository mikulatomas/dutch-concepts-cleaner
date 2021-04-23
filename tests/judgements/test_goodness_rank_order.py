import pytest
from dutch_concepts import DutchConcepts


dc_en = DutchConcepts(root='tests', download=True, language='en')
dc_nl = DutchConcepts(root='tests', download=True, language='nl')


@pytest.mark.parametrize(
    'dc', [dc_en, dc_nl])
def test_goodnes_rank_order_label_content(dc):
    compare_to = [
        dc.exemplar_features.category,
        dc.category_features.category,
    ]

    for data in compare_to:
        for concept_name, goodness_rank_order in dc.judgements.goodness_rank_order.items():
            assert set(data[concept_name].data.index) == set(
                goodness_rank_order.data.index)
