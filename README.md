# dutch-concepts
Python wrapper for easier manipulation with Dutch normative data for semantic concepts dataset.

Names of the exemplars and attributes are heavily corrected. All corrections are described in `exemplar_names.py` and `features_names.py`.

## Requirements
`pandas`

## Usage

```python
from dutch_concepts import DutchConcepts, Domain

# Download original dataset into root folder and use english translation.
dataset = DutchConcepts(root='', download=True, language='en')

# Experiment data related to category based features for animal domain
animal_domain = dataset.category_features.domain[Domain.ANIMAL]

# Raw data (pandas.DataFrame)
animal_domain.data

# Frequencies related to data
animal_domain.frequencies
```

## What is avaliable

```python
from dutch_concepts import DutchConcepts

dataset = DutchConcepts(root='', download=True, language='en')

# All category and domain category-based features
dataset.category_features.category
dataset.category_features.domain

# All category and domain exemplar-based features
dataset.exemplar_features.category
dataset.exemplar_features.domain

# Importance ratings for all category/exemplar-based features
dataset.category_features.importance
dataset.exemplar_features.importance

# Typicality ratings for all exemplars from all categories
dataset.judgements.typicality

# Pairwise_similarity ratings for all exemplars
dataset.judgements.pairwise_similarity

# Goodness ratings for all exemplars from all categories
dataset.judgements.goodness

# Goodness rank order for all exemplars from all categories
dataset.judgements.goodness_rank_order

# Familiarity rating for all exemplars from all categories
dataset.judgements.familiarity

# Age of acquisition for all exemplars from all categories
dataset.judgements.age_of_acquisition

# Generation frequency for all exemplars from all categories
dataset.judgements.generation_frequency

# Associative strength for all exemplars from all categories
dataset.judgements.associative_strength

# Imageability strength for all exemplars from all categories
dataset.judgements.imageability


```


## Original paper
> De Deyne, Simon, et al. "Exemplar by feature applicability matrices and other Dutch normative data for semantic concepts." Behavior research methods 40.4 (2008): 1030-1048.

## Original data
https://link.springer.com/article/10.3758/BRM.40.4.1030
