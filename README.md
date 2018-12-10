# Deutsch-Boerse Stock Data Extractor (2018)

## Introduction

This script is about the trading data (Xetra) from [Deutsche-Boerse](https://github.com/Deutsche-Boerse/dbg-pds) 
that is stored in public Amazon S3 Buckets in EU Central (Frankfurt).
The script awaits a so called
[ISIN-Code](https://en.wikipedia.org/wiki/International_Securities_Identification_Number)
as an input and will return a CSV file for that ISIN and per date (starting 2018-01-01 until today):
* opening price
* closing price
* daily traded volume
* percentage change to previous closing price

## Getting Started

Just
1. Download this repository
2. Install the virtual environment with requirements
3. Activate the virtual environment
4. Run the extract.py script
5. You will be asked to put in a valid ISIN
(examples: DE0005772206, AT00BUWOG001, CH0303692047)
6. After that if you want to download or synchronize the data. Answer with yes/y or no/n.
If no refresh needed it will just skip to the data processing part.
7. Wait a few minutes and get the aggregated CSV file in the result folder.