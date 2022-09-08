EXEMPLAR_NAMES_FIXES = {
    # duplicity: "libel", "libel (langpootmug)" -> "libel"
    "libel (langpootmug)": "libel",
    # typo: "lieveheerbeestje" -> "lieveheersbeestje"
    "lieveheerbeestje": "lieveheersbeestje",
    # typo: "engelsesleutel" -> "engelse sleutel"
    "engelsesleutel": "engelse sleutel",
    # typo/duplicity: "mitraillette" -> "mitrailleur"
    "mitraillette": "mitrailleur",
    # duplicity: "pad", "pad (dier)" -> "pad"
    "pad (dier)": "pad",
}

EXEMPLAR_TRANSLATION_FIXES = {
    # duplicity: "brommer", "moto" both translated as "motorbike"
    "brommer": "motorbike (brommer)",
    "moto": "motorbike (moto)",
    # duplicity: "camion", "vrachtwagen" are both "truck",
    "camion": "truck (camion)",
    "vrachtwagen": "truck (vrachtwagen)",
    # duplicity: "koevoet", "breekijzer" are both "crowbar"
    "koevoet": "crowbar (koevoet)",
    "breekijzer": "crowbar (breekijzer)",
    # translation error: "fluit" is sometimes translated as "flute" insteda of "recorder"
    "fluit": "recorder",
    # typo: "cabary" vs "canary"
    "kanarie": "canary",
    # translation error: "kip" is not english, "chicken" is the right translation
    "kip": "chicken",
    # unify translation: "meikever" is translated to "cockchafer" or "maybug"
    "meikever": "cockchafer",
    # unify translation: "oliespuit" is translated to "oilcan" or "oil can"
    "oliespuit": "oil can",
    # lowercase (originaly Zeppelin)
    "zeppelin": "zeppelin",
    # unify translation: "engelsesleutel" is "adjustable spanner" or "screw wrench"
    "engelse sleutel": "adjustable spanner",
    # "engelse sleutel": "screw wrench (engelse sleutel)",
    # translation error: "houtklem" is tranlated in one file as "spanner" instead of "clamp"s
    "houtklem": "clamp",
    # duplicity: "plamuurmes" is "filling-knife" and "filling knife"
    "plamuurmes": "filling knife",
    # duplicity: "camionette" is translated both as "delivery van" and "van"
    "camionette": "van",
    # duplicity: "caravan" is translated both as "caravan" and "trailer"
    "caravan": "trailer",
    # typo: "double barreled shotgun" vs "double barrelled shotgun"
    "tweeloop": "double-barreled shotgun",
    # duplicity: "mitraillette" is translated both as "machine gun" and "machinegun"
    "mitrailleur": "machine gun",
    # duplicity: "katapult" is translated both as "slingshot" and "catapult"
    "katapult": "slingshot",
    # translation error: "staalborstel" is translated as "moped" in one file
    "staalborstel": "wire brush",
    # duplicity: "step" is translated both as "kick scooter" and "scooter"
    "step": "kick scooter",
    # typo: "adder" translated as "viger"
    "adder": "viper",
    # typo: missing space in "paintbrush"
    "verfborstel": "paint brush",
    # duplicity: "lychee" is translated both as "lychee" and "litchi"
    "lychee": "lychee",
    # duplicity: "clementine" is translated both as "clementine" and "mandarine"
    "clementine": "mandarine"
    
    # duplicity: "brommer", "bromfiets" are both "scooter" because of the rule above
    # ?? check
    # "bromfiets": "scooter (bromfiets)",
    # "brommer": "scooter (brommer)",
}
