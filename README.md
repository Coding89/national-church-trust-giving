# National Churches Trust (NCT) 360Giving Data Integration Pipeline

## This repository contains a Python based data engineering pipeline that consolidates historical grant spreadsheets from the National Churches Trust (NCT) spanning from 2016 to 2024. The data is consolidated into a parquet file for seamless analysis.

------
### Overview: ###

This data engineering pipeline automates the consolidation, normalisation and formatting of historical National Churches Trust (NCT) grant datasets spanning from 2016 to 2024.

The source data is orginally published in an Excel format complaint with 360Giving open data standard. This pipeline acts as an ingestion layer by cleaning text anomalies, resolving layout variations and unifying types into a high performance Apache Parquet datast optimised for analytics and BI tools.

------
### Built With: ###

- ![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)
- ![pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
- <a href="https://apache/org"><img src="https://arrow.apache.org/img/arrow-logo_horizontal_black-txt_white-bg.png" alt="pyarrow" height="25"></a>

------
## Setup and Execution ##

### Prerequisites ###

Please ensure that your local environment has the required data processing dependencies installed:

```
pip install pandas openpyxl pyrarrow
```

### Directory Structure ###

Before executing, please ensure that your historical files are dropped into a folder named "Datasets" in the Directory root:

```
|--- datasets/
    |---2016_national_churches_trust_360_giving_data.xlsx
    |---2017_national_churches_trust_360_giving_data.xlsx
    |---2018_national_churches_trust_360_giving_data.xlsx
    |---2019_national_churches_trust_360_giving_data.xlsx
    |---2020_national_churches_trust_360_giving_data.xlsx
    |---2021_national_churches_trust_360_giving_data.xlsx
    |---2022_national_churches_trust_360_giving_data.xlsx
    |---2023_national_churches_trust_360_giving_data.xlsx
    |---2024_national_churches_trust_360_giving_data.xlsx
|---main.py
|---README.md
```

### Running the Pipeline ###

Run the script directly via your terminal:

```
python main.py
```
------
### Disclaimer: ###

The data is licensed under the Creative Commons Attribution 4.0 International License.
