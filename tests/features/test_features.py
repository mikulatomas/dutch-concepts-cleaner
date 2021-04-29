import pytest
from dutch_concepts import DutchConcepts, Domain


def test_feature_label_content(dc_languages):
    for dc in dc_languages:
        for name, data in dc.exemplar_features.domain.items():
            assert set(dc.category_features.domain[name].data.index) == set(
                data.data.index)

        for name, data in dc.exemplar_features.category.items():
            assert set(dc.category_features.category[name].data.index) == set(
                data.data.index)


def test_domains_label_content(dc_languages):
    # domains = {
    #     'artifacts': ['clothing', 'kitchen utensils', 'musical instruments', 'tools', 'vehicles', 'weapons'],
    #     'animal': ['birds', 'fish', 'insects', 'mammals', 'reptiles']
    # }

    for dc in dc_languages:
        for dataset in [dc.exemplar_features, dc.category_features]:
            for domain, domain_data in dataset.domain.items():
                labels = set(domain_data.data.index)

                compare_to = set()
                for category in domain.members:
                    compare_to.update(
                        dataset.category[category].data.index)

                assert labels == compare_to
