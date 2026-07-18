# National Churches Trust (NCT) 360Giving Data Integration Pipeline

## This repository contains a Python based data engineering pipeline that consolidates historical grant spreadsheets from the National Churches Trust (NCT) spanning from 2016 to 2024. The data is consolidated into a parquet file for seamless analysis.

------
### Overview: ###

This data enginerring pipeline automates the consolidation, normalisation and formatting of historical National Churches Trust (NCT) grant datasets spanning from 2016 to 2024.

The source data is orginally published in an Excel format complaint with 360Giving open data standard. This pipeline acts as an ingestion layer by cleaning text anomalies, resolving layout variations and unifying types into a high performance Apache Parquet datast optimised for analytics and BI tools.

------
### Built With: ###

- ![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)
- ![pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
- <a href="https://apache/org"><img src="https://arrow.apache.org/img/arrow-logo_horizontal_black-txt_white-bg.png" alt="pyarrow" height="25"></a>


------
### Disclaimer: ###

The data is licensed under the Creative Commons Attribution 4.0 International License.
