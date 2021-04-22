import pytest
from dutch_concepts import DutchConcepts

dc_en = DutchConcepts(root='tests', download=True, language='en')
dc_nl = DutchConcepts(root='tests', download=True, language='nl')


@pytest.mark.parametrize(
    'dc, to', [
        (dc_en.exemplar_features.importance, dc_en.exemplar_features.category),
        (dc_nl.exemplar_features.importance, dc_nl.exemplar_features.category),
        (dc_en.category_features.importance, dc_en.category_features.category),
        (dc_nl.category_features.importance, dc_nl.category_features.category)
    ])
def test_feature_importance_label_content(dc, to):
    for concept_name, data in dc.items():
        assert set(data.data.index) == set(to[concept_name].data.columns)
