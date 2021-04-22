import pytest
from dutch_concepts import DutchConcepts

dc_en = DutchConcepts(root='tests', download=True, language='en')
dc_nl = DutchConcepts(root='tests', download=True, language='nl')


@pytest.mark.parametrize(
    'dc', [dc_en, dc_nl])
def test_feature_label_content(dc):

    for name, data in dc.exemplar_features.domain.items():
        assert set(dc.category_features.domain[name].data.index) == set(
            data.data.index)

    # dc.exemplar_features.category
    # dc.category_features.category
