# https://stackoverflow.com/questions/30650474/python-rename-duplicates-in-list-with-progressive-numbers-without-sorting-list
import re

from collections import Counter
from itertools import tee, count


def uniquify(seq):
    """Make all the items unique by adding a suffix (1, 2, etc).

    `seq` is mutable sequence of strings.
    `suffs` is an optional alternative suffix iterable.
    """
    suffs = count(1)
    not_unique = [k for k, v in Counter(
        seq).items() if v > 1]  # so we have: ['name', 'zip']
    # suffix generator dict - e.g., {'name': <my_gen>, 'zip': <my_gen>}
    suff_gens = dict(zip(not_unique, tee(suffs, len(not_unique))))
    for idx, s in enumerate(seq):
        try:
            suffix = str(next(suff_gens[s]))
        except KeyError:
            # s was unique
            continue
        else:
            seq[idx] += f" ({suffix})"


def format_concept_name(concept_name):
    return ' '.join(re.findall(
        '[A-Z][^A-Z]*', concept_name)).lower()
