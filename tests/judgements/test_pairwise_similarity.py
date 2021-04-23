import pytest
from dutch_concepts import DutchConcepts


dc_en = DutchConcepts(root='tests', download=True, language='en')
dc_nl = DutchConcepts(root='tests', download=True, language='nl')


@pytest.mark.parametrize(
    'dc', [dc_en, dc_nl])
def test_pairwise_similarity_same_labels(dc):
    for _, data in dc.judgements.pairwise_similarity.items():
        assert set(data.data.index.values) == set(data.data.columns.values)


@pytest.mark.parametrize(
    'dc', [dc_en, dc_nl])
def test_pairwise_similarity_label_content(dc):
    compare_to = [
        dc.exemplar_features.category,
        dc.category_features.category,
    ]

    for data in compare_to:
        for concept_name, similarity in dc.judgements.pairwise_similarity.items():
            assert set(data[concept_name].data.index) == set(
                similarity.data.index)
