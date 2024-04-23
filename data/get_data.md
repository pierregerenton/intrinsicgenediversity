# Getting data

This file contains usefull information to regenerate input file for all scripts of this repository if you don't have them, as data are not provided.

## Human and mouse genome and annotation

Gencode assembly and annotation have been chosen. Data are available [here](https://ftp.ebi.ac.uk/pub/databases/gencode/) :

- Human  (release 45):
    - [Genome](https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_45/GRCh38.p14.genome.fa.gz)
    - [Gene annotation](https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_45/gencode.v45.annotation.gff3.gz)
- Mouse (release M34):
    - [Genome](https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M34/GRCm39.genome.fa.gz) 
    - [Gene annotation](https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M34/gencode.vM34.annotation.gff3.gz)


## Keeping protein-coding features, no readthrough gene and no redundant transcript

To remove non protein-coding features, readthrough gene and redundant transcript ( transcript with the same CDS coordinates), you can run this script

```sh
./src/python3 src/extract_protein_coding_features_from_gff.py -i data/[human/mouse].gff3 -o data/[human/mouse].protein_coding.no_readthrough.no_redundant_transcript.gff3 
```

## Extracting proteome

From each annotation, a proteome can be extract. The proteome is a multi-fasta file where each sequence is extracted from the reference genome according to the coordinates of the CDS of a coding transcript in an annotation.

With `AGAT`, you can do that by running :

```sh
agat_sp_extract_sequences.pl -g [human/mouse].[all/long/mane].gff3 -f [human/mouse].fa -t cds -p -o protein.[human/mouse].[all/long/mane].fa
```

## GO term annotation

GO term annotation was done with the PANNZER web interface at http://ekhidna2.biocenter.helsinki.fi/sanspanz/.
We suggest you to uncheck **Remove redundant filter** (cf [`../src/choice_go_set`](../src/choice_go_set)), precise the species of your dataset (if known) and let other parameters by default.

## Convert Pannzer output as accepted input

Run :

```sh
python3 src/convert_pannzer_output_to_input.py -p data/[human/mouse]_pannzer.out -o data/[human/mouse]_input.tsv
```


<br/>
----------------------------

Toronen P, Medlar A, Holm L (2018) PANNZER2: A rapid functional annotation webserver. Nucl. Acids Res. 46, W84-W88

Sayers, E. W., Bolton, E. E., Brister, J. R., Canese, K., Chan, J., Comeau, D. C., Connor, R., Funk, K., Kelly, C., Kim, S., Madej, T., Marchler-Bauer, A., Lanczycki, C., Lathrop, S., Lu, Z., Thibaud-Nissen, F., Murphy, T., Phan, L., Skripchenko, Y., Tse, T., … Sherry, S. T. (2022). Database resources of the national center for biotechnology information. Nucleic acids research, 50(D1), D20–D26. https://doi.org/10.1093/nar/gkab1112

