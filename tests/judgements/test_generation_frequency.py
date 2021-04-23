import pytest
from dutch_concepts import DutchConcepts


dc_en = DutchConcepts(root='tests', download=True, language='en')
dc_nl = DutchConcepts(root='tests', download=True, language='nl')


@pytest.mark.parametrize(
    'dc', [dc_en, dc_nl])
def test_generation_frequency_label_content(dc):
    compare_to = [
        dc.exemplar_features.category,
        dc.category_features.category,
    ]

    for data in compare_to:
        for concept_name, generation_frequency in dc.judgements.generation_frequency.items():
            assert set(data[concept_name].data.index) == set(
                generation_frequency.data.index)
