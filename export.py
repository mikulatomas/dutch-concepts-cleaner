## Export clean version of dataset

import os, errno
import shutil
import zipfile

from dutch_concepts_cleaner import DutchConceptsCleaner, Domain


def safe_string(str):
    return str.replace(" ", "_")


def export_similarities(similarities_folder):
    for category, data in dataset.judgements.pairwise_similarity.items():
        category_name = safe_string(category.value)

        folder = os.path.join(similarities_folder, category_name)
        os.makedirs(folder)

        # mean values
        data.data.to_csv(
            os.path.join(folder, f"{category_name}_{SIMILARITIES_FOLDER}_mean.csv")
        )

        # respondents
        respondents_folder = os.path.join(folder, RESPONDENTS_FOLDER)
        os.makedirs(respondents_folder)

        for respondent, data in data.respondents.items():
            data.to_csv(
                os.path.join(
                    respondents_folder,
                    f"{category_name}_{SIMILARITIES_FOLDER}_{safe_string(respondent)}.csv",
                )
            )


def export_judgment(data, judgments_folder, folder, suffix=None):
    specific_judgements_folder = os.path.join(judgments_folder, folder)

    os.makedirs(specific_judgements_folder)

    for category, data in data.items():
        category_name = safe_string(category.value)

        if suffix:
            filename = f"{category_name}_{folder}_{suffix}.csv"

        filename = f"{category_name}_{folder}.csv"

        data.data.to_csv(os.path.join(specific_judgements_folder, filename))


def export_feature_categories(data, feature_folder, folder, name, suffix="sum"):
    specific_features_folder = os.path.join(feature_folder, folder)

    for category, data in data.items():
        category_name = safe_string(category.value)

        sub_folder = os.path.join(specific_features_folder, category_name)
        os.makedirs(sub_folder)

        filename = f"{category_name}_{name}"

        data.data.to_csv(os.path.join(sub_folder, f"{filename}_{suffix}.csv"))

        # respondents
        respondents_folder = os.path.join(sub_folder, RESPONDENTS_FOLDER)
        os.makedirs(respondents_folder)

        for respondent, data in data.respondents.items():
            data.to_csv(
                os.path.join(
                    respondents_folder,
                    f"{filename}_{safe_string(respondent)}.csv",
                )
            )


def export_feature_domains(data, feature_folder, folder, name, suffix="sum"):
    specific_domain_folder = os.path.join(feature_folder, DOMAIN_FOLDER, folder)
    os.makedirs(specific_domain_folder)

    filename = f"{folder}_{name}"

    data.data.to_csv(os.path.join(specific_domain_folder, f"{filename}_{suffix}.csv"))

    # respondents
    respondents_folder = os.path.join(specific_domain_folder, RESPONDENTS_FOLDER)
    os.makedirs(respondents_folder)

    for respondent, data in data.respondents.items():
        data.to_csv(
            os.path.join(
                respondents_folder,
                f"{filename}_{safe_string(respondent)}.csv",
            )
        )


def export_feature_freq_domains(data, main_folder, folder, suffix):
    specific_domain_folder = main_folder

    filename = f"{folder}_{suffix}_feature_frequency"

    data.frequencies.to_csv(os.path.join(specific_domain_folder, f"{filename}.csv"))


def export_feature_freq_categories(data, main_folder, folder, suffix):
    specific_features_folder = os.path.join(main_folder, folder)
    os.makedirs(specific_features_folder)

    for category, data in data.items():
        category_name = safe_string(category.value)

        filename = f"{category_name}_{suffix}_feature_frequency"

        data.frequencies.to_csv(
            os.path.join(specific_features_folder, f"{filename}.csv")
        )


EXPORT_ROOT = "export"
DATA_ROOT = "dutch_data"

RESPONDENTS_FOLDER = "respondents"

SIMILARITIES_FOLDER = "pairwise_similarities"

TYPICALITY_FOLDER = "typicality_ratings"

FAMILIARITY_FOLDER = "familiarity_ratings"

GENERATION_FREQ_FOLDER = "exemplar_generation_frequency"

ASSOCIATIVE_STRENGTH_FOLDER = "associative_strength"

GOODNESS_RANK_ORDER_FOLDER = "goodness_rank_order"

GOODNESS_RATINGS_FOLDER = "goodness_ratings"

IMAGEABILITY_RATINGS_FOLDER = "imageability_ratings"

AGE_OF_ACQUISITION_FOLDER = "acquisition_ratings"

WORD_FREQUENCY_FOLDER = "word_frequency"

EXEMPLAR_JUDGMENTS = "exemplar_judgments"

EXEMPLAR_FEATURE_JUDGMENTS = "exemplar_feature_judgments"

CATEGORY_FEATURES = "category_features"
EXEMPLAR_FEATURES = "exemplar_features"

CATEGORY_FEATURE_IMPORTANCE_FOLDER = "feature_importance_ratings"

EXEMPLAR_FEATURE_IMPORTANCE_FOLDER = "feature_importance_ratings"

EXEMPLAR_CATEGORY_FEATURES_FOLDER = "categories"

CATEGORY_CATEGORY_FEATURES_FOLDER = "categories"

DOMAIN_FOLDER = "domains"

EXEMPLAR_ANIMAL_DOMAIN_FEATURES_FOLDER = "animal"

EXEMPLAR_ARTIFACT_DOMAIN_FEATURES_FOLDER = "artifact"

CATEGORY_ANIMAL_DOMAIN_FEATURES_FOLDER = "animal"

CATEGORY_ARTIFACT_DOMAIN_FEATURES_FOLDER = "artifact"

FEATURE_FREQ_FOLDER = "feature_generation_frequency"


# remove previous export
shutil.rmtree(os.path.join(EXPORT_ROOT), ignore_errors=True)

LANGUAGUES = ["en", "nl"]

for lang in LANGUAGUES:
    dataset = DutchConceptsCleaner(root="tests/", download=True, language=lang)

    lang_root = os.path.join(EXPORT_ROOT, DATA_ROOT, lang)

    # similarities
    similarities_folder = os.path.join(lang_root, SIMILARITIES_FOLDER)

    export_similarities(similarities_folder)

    # exemplar judgments
    judgments_folder = os.path.join(lang_root, EXEMPLAR_JUDGMENTS)

    export_judgment(
        dataset.judgements.typicality,
        judgments_folder,
        TYPICALITY_FOLDER,
        suffix="mean",
    )

    export_judgment(
        dataset.judgements.familiarity,
        judgments_folder,
        FAMILIARITY_FOLDER,
    )

    export_judgment(
        dataset.judgements.generation_frequency,
        judgments_folder,
        GENERATION_FREQ_FOLDER,
    )

    export_judgment(
        dataset.judgements.associative_strength,
        judgments_folder,
        ASSOCIATIVE_STRENGTH_FOLDER,
    )

    export_judgment(
        dataset.judgements.goodness_rank_order,
        judgments_folder,
        GOODNESS_RANK_ORDER_FOLDER,
    )

    export_judgment(
        dataset.judgements.goodness,
        judgments_folder,
        GOODNESS_RATINGS_FOLDER,
    )

    export_judgment(
        dataset.judgements.imageability,
        judgments_folder,
        IMAGEABILITY_RATINGS_FOLDER,
    )

    export_judgment(
        dataset.judgements.age_of_acquisition,
        judgments_folder,
        AGE_OF_ACQUISITION_FOLDER,
    )

    export_judgment(
        dataset.judgements.word_frequency,
        judgments_folder,
        WORD_FREQUENCY_FOLDER,
    )

    # exemplar feature judgments
    # category features
    feature_judgments_folder = os.path.join(
        lang_root, EXEMPLAR_FEATURE_JUDGMENTS, CATEGORY_FEATURES
    )

    export_judgment(
        dataset.category_features.importance,
        feature_judgments_folder,
        CATEGORY_FEATURE_IMPORTANCE_FOLDER,
    )

    export_feature_categories(
        dataset.category_features.category,
        feature_judgments_folder,
        CATEGORY_CATEGORY_FEATURES_FOLDER,
        "category_features",
    )

    export_feature_domains(
        dataset.category_features.domain[Domain.ANIMAL],
        feature_judgments_folder,
        CATEGORY_ANIMAL_DOMAIN_FEATURES_FOLDER,
        "category_features",
    )

    export_feature_domains(
        dataset.category_features.domain[Domain.ARTIFACT],
        feature_judgments_folder,
        CATEGORY_ARTIFACT_DOMAIN_FEATURES_FOLDER,
        "category_features",
    )

    # feature freq
    category_features_freq = os.path.join(feature_judgments_folder, FEATURE_FREQ_FOLDER)
    os.makedirs(category_features_freq)

    export_feature_freq_categories(
        dataset.category_features.category,
        category_features_freq,
        CATEGORY_CATEGORY_FEATURES_FOLDER,
        "category",
    )

    feature_freq_domains = os.path.join(category_features_freq, DOMAIN_FOLDER)
    os.makedirs(feature_freq_domains)

    export_feature_freq_domains(
        dataset.category_features.domain[Domain.ANIMAL],
        feature_freq_domains,
        CATEGORY_ANIMAL_DOMAIN_FEATURES_FOLDER,
        "category",
    )

    export_feature_freq_domains(
        dataset.category_features.domain[Domain.ARTIFACT],
        feature_freq_domains,
        CATEGORY_ARTIFACT_DOMAIN_FEATURES_FOLDER,
        "category",
    )

    # exemplar features
    feature_judgments_folder = os.path.join(
        lang_root, EXEMPLAR_FEATURE_JUDGMENTS, EXEMPLAR_FEATURES
    )

    export_judgment(
        dataset.exemplar_features.importance,
        feature_judgments_folder,
        EXEMPLAR_FEATURE_IMPORTANCE_FOLDER,
    )

    export_feature_categories(
        dataset.exemplar_features.category,
        feature_judgments_folder,
        EXEMPLAR_CATEGORY_FEATURES_FOLDER,
        "exemplar_features",
    )

    export_feature_domains(
        dataset.exemplar_features.domain[Domain.ANIMAL],
        feature_judgments_folder,
        EXEMPLAR_ANIMAL_DOMAIN_FEATURES_FOLDER,
        "exemplar_features",
    )

    export_feature_domains(
        dataset.exemplar_features.domain[Domain.ARTIFACT],
        feature_judgments_folder,
        EXEMPLAR_ARTIFACT_DOMAIN_FEATURES_FOLDER,
        "exemplar_features",
    )

    # feature freq
    exemplar_features_freq = os.path.join(feature_judgments_folder, FEATURE_FREQ_FOLDER)
    os.makedirs(exemplar_features_freq)

    export_feature_freq_categories(
        dataset.exemplar_features.category,
        exemplar_features_freq,
        EXEMPLAR_CATEGORY_FEATURES_FOLDER,
        "exemplar",
    )

    feature_freq_domains = os.path.join(exemplar_features_freq, DOMAIN_FOLDER)
    os.makedirs(feature_freq_domains)

    export_feature_freq_domains(
        dataset.exemplar_features.domain[Domain.ANIMAL],
        feature_freq_domains,
        EXEMPLAR_ANIMAL_DOMAIN_FEATURES_FOLDER,
        "exemplar",
    )

    export_feature_freq_domains(
        dataset.exemplar_features.domain[Domain.ARTIFACT],
        feature_freq_domains,
        EXEMPLAR_ARTIFACT_DOMAIN_FEATURES_FOLDER,
        "exemplar",
    )


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

zipf = zipfile.ZipFile(os.path.join(EXPORT_ROOT, 'dutch_data.zip'), 'w', zipfile.ZIP_DEFLATED)
zipdir(os.path.join(EXPORT_ROOT, DATA_ROOT), zipf)
zipf.close()
