# intrinsicgenediversity

The purpose is to quantify the intrinsic gene diversity (using various metrics) and understand everything that this information can bring to us.

## Summary

- [Summary](#summary)
- [Requirement](#requirement)
- [Organization of the repo](#organization-of-the-repo)
- [Run the code](#run-the-code)


## Requirement


If you want to get input data by yourselves :

- [samtools](https://github.com/samtools/samtools)
- [AGAT](https://github.com/NBISweden/AGAT)

To compute GO semantic similarity :

- [GOGO](https://github.com/zwang-bioinformatics/GOGO) : to run this software, your current working directory needs to be the installation GOGO directory

You'll also need [python3](https://www.python.org/downloads/) and some packages written in [`requirement.txt`](requirement.txt).

You can install all with :

```sh
pip install -r requierement.txt 
```

## Organization of the repo

- [`data`](data) : data location with [`data/get_data.md`](./data/get_data.md) with information to retreive them
- [`src`](src) : scripts (cf below)

## Run the code
