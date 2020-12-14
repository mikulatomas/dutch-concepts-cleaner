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
98c98
<     "bestaat in verschillende groottes": "exists in different sizes",
---
>     "bestaat in verschillende groottes": "exists in different sizes (groottes)",
103c103
<     "bestaat in verschillende maten": "exists in different sizes",
---
>     "bestaat in verschillende maten": "exists in different sizes (maten)",
520c520
<     "gebruikt bij volksmuziek": "used in folk music",
---
>     "gebruikt bij volksmuziek": "used in folk music (in dutch: volksmuziek)",
722c722
<     "heeft bandjes": "has ribbons",
---
>     "heeft bandjes": "has straps",
724c724
<     "heeft benen": "has legs",
---
>     "heeft benen": "has legs (2)",
807c807
<     "heeft een kap": "has a cap",
---
>     "heeft een kap": "has a cap/hood",
815c815
<     "heeft een klep": "has a lid",
---
>     "heeft een klep": "has a valve",
880c880
<     "heeft een snoer": "has a wire",
---
>     "heeft een snoer": "has a cord",
961c961
<     "heeft knopen": "has buttons",
---
>     "heeft knopen": "has buttons (2)",
1014c1014
<     "heeft scherpe nagels": "has sharp claws",
---
>     "heeft scherpe nagels": "has sharp claws (nagels)",
1023c1023
<     "heeft spaghettibandjes": "has straps",
---
>     "heeft spaghettibandjes": "has spaghetti straps",
1072c1072
<     "heeft verschillende motiefjes": "has different patterns",
---
>     "heeft verschillende motiefjes": "has different motifs",
1231c1231
<     "is een apparaat": "is a machine",
---
>     "is een apparaat": "is a device",
1261c1261
<     "is een fluitinstrument": "is a wind instrument",
---
>     "is een fluitinstrument": "is a flute instrument",
1375c1375
<     "is een wagen": "is a car",
---
>     "is een wagen": "is a car (in dutch: wagen)",
1433c1433
<     "is gezellig": "is pleasant",
---
>     "is gezellig": "is cozy",
1438c1438
<     "is glibberig": "is slippery",
---
>     "is glibberig": "is slithery",
1711c1711
<     "is zwaar": "is hard",
---
>     "is zwaar": "is heavy",
1944c1944
<     "kan stuk gaan": "can break",
---
>     "kan stuk gaan": "can break to pieces",
2261c2261
<     "maakt een ronkend geluid": "makes a humming sound",
---
>     "maakt een ronkend geluid": "makes a roaring sound",
2310c2310
<     "mekkert": "bleats",
---
>     "mekkert": "bleats (2)",
2475c2475
<     "scheldnaam": "term of abuse (in dutch)",
---
>     "scheldnaam": "term of abuse",
2590c2590
<     "tsjilpt": "chirps",
---
>     "tsjilpt": "chirps (2)",
2970c2970
<     "wordt gebruikt door de schrijnwerker": "used by carpenters",
---
>     "wordt gebruikt door de schrijnwerker": "used by joiner",
3295c3295
<     "zit gemakkelijk": "is comfortable",
---
>     "zit gemakkelijk": "sits comfortably",
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
