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

dataset = DutchConcepts(root='tests', download=True, language='nl')


@pytest.mark.parametrize(
    'domain, categories', [
        (dataset.category_features.domain['artifacts'], artifact_domain),
        (dataset.category_features.domain['animal'], animal_domain),
        (dataset.exemplar_features.domain['artifacts'], artifact_domain),
        (dataset.exemplar_features.domain['animal'], animal_domain)])
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
        dataset.category_features.category,
        dataset.exemplar_features.category,
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
        set(category_features.data.index).symmetric_difference(set(objects))
        assert set(category_features.data.index) == set(objects)
