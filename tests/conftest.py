import pytest
from dutch_concepts import DutchConcepts


@pytest.fixture(scope='session', autouse=True)
def dc_languages(request):
    return [
        DutchConcepts(root='tests', download=True, language='en'), DutchConcepts(root='tests', download=True, language='nl')]
