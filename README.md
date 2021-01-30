# py-dutch-normative-data
Python script for download Dutch normative data for semantic concepts dataset and clean the original `.csv`.

## Changes
* Removed columns/rows: Dutch names, empty values.
* Unified filenames ('Feature' vs 'Features')
* Translated into english (avoid duplicates in english translation, more in `translation/`).

## Translation diff
```
% > diff translation_objects_original.json translation_objects.json
60,61c60,61
<     "bromfiets": "scooter",
<     "brommer": "motorbike",
---
>     "bromfiets": "moped",
>     "brommer": "scooter",
64c64
<     "camion": "truck",
---
>     "camion": "camion",
96a97
>     "engelsesleutel": "adjustable spanner",
178c179
<     "koevoet": "crowbar",
---
>     "koevoet": "jimmy bar",
198a200
>     "libel (langpootmug)": "dragonfly",
199a202
>     "lieveheerbeestje": "ladybug",
219a223
>     "mitrailleur": "machine gun",
```

```
% > diff translation_attributes_original.json translation_attributes.json
114c114
<     "bestaat in verschillende groottes": "exists in several sizes",
---
>     "bestaat in verschillende groottes": "exists in different sizes (groottes)",
116c116
<     "bestaat in verschillende kleuren": "comes in different colours",
---
>     "bestaat in verschillende kleuren": "exists in different colors",
119c119
<     "bestaat in verschillende maten": "exists in different sizes",
---
>     "bestaat in verschillende maten": "exists in different sizes (maten)",
122c122
<     "bestaat in verschillende soorten": "exists in several kinds",
---
>     "bestaat in verschillende soorten": "exists in different kinds",
473c473
<     "er zijn verschillende soorten van": "exists in different kinds",
---
>     "er zijn verschillende soorten van": "there are different kinds",
540c540
<     "gebruikt bij volksmuziek": "used in folk music",
---
>     "gebruikt bij volksmuziek": "used in folk music (in dutch: volksmuziek)",
747c747
<     "heeft bandjes": "has ribbons",
---
>     "heeft bandjes": "has straps",
749c749
<     "heeft benen": "has legs",
---
>     "heeft benen": "has legs (2)",
834c834
<     "heeft een kap": "has a cap",
---
>     "heeft een kap": "has a cap/hood",
842c842
<     "heeft een klep": "has a lid",
---
>     "heeft een klep": "has a valve",
852c852
<     "heeft een kroontje": "has a little crown",
---
>     "heeft een kroontje": "has a crown",
907c907
<     "heeft een snoer": "has a wire",
---
>     "heeft een snoer": "has a cord",
947c947
<     "heeft felle kleuren": "has bright colours",
---
>     "heeft felle kleuren": "has bright colors",
1049c1049
<     "heeft scherpe nagels": "has sharp claws",
---
>     "heeft scherpe nagels": "has sharp claws (nagels)",
1058c1058
<     "heeft spaghettibandjes": "has straps",
---
>     "heeft spaghettibandjes": "has spaghetti straps",
1074c1074
<     "heeft toetsen": "has buttons",
---
>     "heeft toetsen": "has (piano) keys",
1107c1107
<     "heeft verschillende motiefjes": "has different patterns",
---
>     "heeft verschillende motiefjes": "has different motifs",
1264c1264
<     "is dik": "is big",
---
>     "is dik": "is thik",
1274c1274
<     "is een apparaat": "is a machine",
---
>     "is een apparaat": "is a device",
1307c1307
<     "is een fluitinstrument": "is a wind instrument",
---
>     "is een fluitinstrument": "is a flute instrument",
1359c1359
<     "is een mens": "is a human being",
---
>     "is een mens": "is a human",
1428c1428
<     "is een wagen": "is a car",
---
>     "is een wagen": "is a car (in dutch: wagen)",
1493c1493
<     "is gezellig": "is pleasant",
---
>     "is gezellig": "is cozy",
1497,1498c1497,1498
<     "is glad": "is smooth",
<     "is glibberig": "is slippery",
---
>     "is glad": "is slippery",
>     "is glibberig": "is slithery",
1502c1502
<     "is goed voor de ogen": "is good for the eyes",
---
>     "is goed voor de ogen": "is good for your eyes",
1541c1541
<     "is klein": "is small",
---
>     "is klein": "is little",
1644c1644
<     "is populair": "is popular",
---
>     "is populair": "is popular  ",
1646c1646
<     "is populair in Amerika": "is popular in America",
---
>     "is populair in Amerika": "is popular in the United States",
1665c1665
<     "is sappig": "is juicy",
---
>     "is sappig": "is sappy",
1744c1744
<     "is voedzaam": "is nutritious",
---
>     "is voedzaam": "is nutricious",
1760c1760
<     "is vrouwelijk": "is female",
---
>     "is vrouwelijk": "is feminine",
2018c2018
<     "kan stuk gaan": "can break",
---
>     "kan stuk gaan": "can break to pieces",
2338c2338
<     "maakt een ronkend geluid": "makes a humming sound",
---
>     "maakt een ronkend geluid": "makes a roaring sound",
2350c2350
<     "maakt lawaai": "makes a lot of noise",
---
>     "maakt lawaai": "produces noise",
2388c2388
<     "mekkert": "bleats",
---
>     "mekkert": "bleats (2)",
2545c2545
<     "ruikt lekker": "smells good",
---
>     "ruikt lekker": "smells well",
2561c2561
<     "scheldnaam": "term of abuse (in dutch)",
---
>     "scheldnaam": "term of abuse",
2678c2678
<     "tsjilpt": "chirps",
---
>     "tsjilpt": "chirps (2)",
3066c3066
<     "wordt gebruikt door de schrijnwerker": "used by carpenters",
---
>     "wordt gebruikt door de schrijnwerker": "used by joiner",
3408c3408
<     "zit gemakkelijk": "is comfortable",
---
>     "zit gemakkelijk": "sits comfortably",
3459c3459
<     "zweeft": "floats",
---
>     "zweeft": "glides",
```

## Requirements
`pandas`

## How to use
```
pip install -r requirements.txt
chmod +x run_all.sh
./run_all.sh
```

Or run each python scripts one by one. Cleaned csv files will appear in `clean_csv` folder.

## Original paper
> De Deyne, Simon, et al. "Exemplar by feature applicability matrices and other Dutch normative data for semantic concepts." Behavior research methods 40.4 (2008): 1030-1048.

## Original data
https://link.springer.com/article/10.3758/BRM.40.4.1030
