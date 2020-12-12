# py-dutch-normative-data
Python script for download Dutch normative data for semantic concepts dataset and clean the original `.csv`.

## Changes
* Removed columns/rows: Dutch names, empty values.
* Unified filenames ('Feature' vs 'Features')
* Translated into english (avoid duplicates in english translation, more in `translation.json`).

## Translation diff
```
60,61c60,61
<     "bromfiets": "moped",
<     "brommer": "scooter",
---
>     "bromfiets": "scooter",
>     "brommer": "motorbike",
64c64
<     "camion": "camion",
---
>     "camion": "truck",
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
