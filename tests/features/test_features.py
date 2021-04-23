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

    for name, data in dc.exemplar_features.category.items():
        assert set(dc.category_features.category[name].data.index) == set(
            data.data.index)


@pytest.mark.parametrize(
    'dc', [dc_en, dc_nl])
def test_domains_label_content(dc):
    domains = {
        'artifacts': ['clothing', 'kitchen utensils', 'musical instruments', 'tools', 'vehicles', 'weapons'],
        'animal': ['birds', 'fish', 'insects', 'mammals', 'reptiles']
    }

    for dataset in [dc.exemplar_features, dc.category_features]:
        for name, domain_data in dataset.domain.items():
            labels = set(domain_data.data.index)

            compare_to = set()
            for concept_name in domains[name]:
                compare_to.update(dataset.category[concept_name].data.index)

            assert labels == compare_to
