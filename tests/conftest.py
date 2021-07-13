import pytest
from dutch_concepts_cleaner import DutchConceptsCleaner


@pytest.fixture(scope='session', autouse=True)
def dc_languages(request):
    return [
        DutchConceptsCleaner(root='tests', download=True, language='en'), DutchConceptsCleaner(root='tests', download=True, language='nl')]
