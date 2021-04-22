# https://stackoverflow.com/questions/30650474/python-rename-duplicates-in-list-with-progressive-numbers-without-sorting-list
import re


def format_concept_name(concept_name):
    if concept_name.islower():
        return concept_name
    else:
        return ' '.join(re.findall(
            '[A-Z][^A-Z]*', concept_name)).lower()


def drop_all_nan(df):
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)

    return df


def get_fixed_translation(original, english, fixes):
    assert len(original) == len(english)

    translation = dict(
        zip(original, map(str.strip, english)))

    # Apply translation fixes
    for original, english in fixes.items():
        if translation.get(original):
            translation[original] = english

    return translation
