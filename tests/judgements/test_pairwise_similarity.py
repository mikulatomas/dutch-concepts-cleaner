import pytest
from dutch_concepts import DutchConcepts


@pytest.mark.parametrize(
    'lang', ['en', 'nl'])
def test_pairwise_similarity_same_labels(lang):
    dc = DutchConcepts(root='tests', download=True, language=lang)

    for _, data in dc.judgements.pairwise_similarity.items():
        assert set(data.data.index.values) == set(data.data.columns.values)


@pytest.mark.parametrize(
    'lang', ['en', 'nl'])
def test_pairwise_similarity_label_content(lang):
    dc = DutchConcepts(root='tests', download=True, language=lang)

    compare_to = [
        dc.exemplar_features.category,
        dc.category_features.category,
    ]

    for data in compare_to:
        for concept_name, similarity in dc.judgements.pairwise_similarity.items():
            assert set(data[concept_name].data.index) == set(
                similarity.data.index)
