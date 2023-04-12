import pytest
from dutch_concepts_cleaner import DutchConceptsCleaner, Domain, Category

dc_en = DutchConceptsCleaner(root="tests", download=True, language="en")
dc_nl = DutchConceptsCleaner(root="tests", download=True, language="nl")


@pytest.mark.parametrize(
    "data",
    [
        dc_en.category_features,
        dc_nl.category_features,
        dc_en.exemplar_features,
        dc_nl.exemplar_features,
    ],
)
@pytest.mark.parametrize("domain", [Domain.ANIMAL, Domain.ARTIFACT])
def test_feature_domain_labels(data, domain):
    df_compare_to = data.domain[domain].data

    for idx, df in data.domain[domain].respondents.items():
        assert not set(df_compare_to.index).symmetric_difference(set(df.index))
        assert not set(df_compare_to.columns).symmetric_difference(set(df.columns))



@pytest.mark.parametrize(
    "data",
    [
        dc_en.category_features,
        dc_nl.category_features,
        dc_en.exemplar_features,
        dc_nl.exemplar_features,
    ],
)
@pytest.mark.parametrize("category", Category)
def test_feature_category_labels(data, category):
    df_compare_to = data.category[category].data

    for idx, df in data.category[category].respondents.items():
        assert not set(df_compare_to.index).symmetric_difference(set(df.index))
        assert not set(df_compare_to.columns).symmetric_difference(set(df.columns))


@pytest.mark.parametrize(
    "data",
    [
        dc_en.category_features,
        dc_nl.category_features,
        dc_en.exemplar_features,
        dc_nl.exemplar_features,
    ],
)
@pytest.mark.parametrize("domain", [Domain.ANIMAL, Domain.ARTIFACT])
def test_feature_domain_sum(data, domain):
    dfs = list(data.domain[domain].respondents.values())

    df_sum = sum(dfs)
    df_compare_to = data.domain[domain].data

    assert df_compare_to.equals(df_sum)


@pytest.mark.parametrize(
    "data",
    [
        dc_en.category_features,
        dc_nl.category_features,
        dc_en.exemplar_features,
        dc_nl.exemplar_features,
    ],
)
@pytest.mark.parametrize("category", Category)
def test_feature_category_sum(data, category):
    dfs = list(data.category[category].respondents.values())

    df_sum = sum(dfs)
    df_compare_to = data.category[category].data

    assert df_compare_to.equals(df_sum)
