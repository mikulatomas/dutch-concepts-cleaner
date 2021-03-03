import pytest

from dutch_concepts import DutchConcepts

artifact_domain = [
    'clothing',
    'kitchen utensils',
    'musical instruments',
    'tools',
    'vehicles'
]

animal_domain = [
    'birds',
    'fish',
    'insects',
    'mammals'
]

dataset = DutchConcepts(root='tests', download=True)


@pytest.mark.parametrize(
    'domain, categories', [
        (dataset.features.domain_category_based['artifact'], artifact_domain),
        (dataset.features.domain_category_based['animal'], animal_domain),
        (dataset.features.domain_exemplar_based['artifact'], artifact_domain),
        (dataset.features.domain_exemplar_based['animal'], animal_domain)])
@pytest.mark.parametrize(
    'judgement', [
        dataset.judgements.typicality_ratings,
        dataset.judgements.similarities])
def test_object_labels_domain(domain, categories, judgement):
    for category in categories:
        objects = judgement[category].data.index

        for obj in objects:
            assert obj in domain.data.index


@pytest.mark.parametrize(
    'features', [
        dataset.features.semantic_category_based,
        dataset.features.semantic_exemplar_based,
    ]
)
@pytest.mark.parametrize(
    'judgement', [
        dataset.judgements.typicality_ratings,
        dataset.judgements.similarities])
def test_object_labels(features, judgement):
    for category, category_features in features.items():
        objects = judgement[category].data.index

        assert len(category_features.data.index) == len(objects)
        assert set(category_features.data.index) == set(objects)
