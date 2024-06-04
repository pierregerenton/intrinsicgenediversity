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

## Fly (*Drosophila melanogaster*) genome and annotation

Drosophila have also been chosen for orthologs analysis. Data are available [here](https://www.ensembl.org/Drosophila_melanogaster/Info/Index) :

- Ensembl release 111 :
    - [Genome](https://ftp.ensembl.org/pub/release-112/fasta/drosophila_melanogaster/dna/Drosophila_melanogaster.BDGP6.46.dna.toplevel.fa.gz)
    - [Gene annotation](https://ftp.ensembl.org/pub/release-112/gff3/drosophila_melanogaster/Drosophila_melanogaster.BDGP6.46.111.gff3.gz)

## Keeping protein-coding features, no readthrough gene and no redundant transcript

To remove non protein-coding features, readthrough gene and redundant transcript ( transcript with the same CDS coordinates), you can run this script

```sh
./src/python3 src/extract_protein_coding_features_from_gff.py -i data/[human/mouse].gff3 -o data/[human/mouse].protein_coding.no_readthrough.no_redundant_transcript.gff3 
```

As *Drosophila melanogaster* is not formatted like Gencode annotation, we propose `./src/extract_features_for_drosophila.ipynb` as an alternative.

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


## Alternative input

### Remove transcript without GO annotation

If you think that you GO predictor isn't perfect and predict 0 GO annotation to transcript that have some, you can try to compute the diversity without those transcript.

```sh
cat human_input.tsv | awk '($3!="")' > human_input.no_empty_transcript.tsv
```

### Use expressed transcript

Using a synthetic model of cell differenciation in human, the expression of each transcript was quantified at different time point. We cannot make the original data available but we keep transcript with a CPM > 1 at the first (start) and last t(end) timepoint, then filter the output to keep only transcript prediction for these genes.  These data can be use to explore new thing. There are in file `human_input.[start/end]_expressed.tsv`.


## Get orthologs from Ensembl

To compare genes between taxa, being able to get a list of orthologs is crucial. [Ensembl Biomart](https://www.ensembl.org/biomart/martview/c98efc21018805f8bab9d1633e6ab300) is a tool that let us download Ensembl database data with multiple filter. It is possible to download orthologs. Here is a small tutorial to explain how to get human-mouse orthologs. You should adapt this to your species.

- `-CHOOSE DATABASE-` -> select `Ensembl Genes 112` (the current last release of ensembl is 112)
- `-CHOOSE DATASET-` -> select `Human genes (GRCh38.p14)` (again, it depends of the version of the assembly)

On the left, a menu should appear.

- Click `Filters`
- Expend `MULTI SPECIES COMPARISONS`
- Check `Homologues filters`
- In the drop-down menu choose `Orthologous Mouse Genes` (let the radio buttons on `Only`)

Then, go to `Attributes` (in the left menu). We will select useful attributes.

- Choose `Homologues (Max select 6 orthologues)` for the RadioButtons widget
- Expend `GENE` and check all informations you want about the human gene (advice : check `Gene stable ID`)
- Expend `ORTHOLOGUES [K-O]` (we are looking at **M**ouse orthologues, so we expend the corresponding categories. Please note that the classification is by common name and not scientific case (except exception). If you do not find the species you are looking form, try to look to the other name.)
- Find `Mouse Orthologues` and check what you want. (advice : `Mouse gene stable ID` and `Mouse homology type`. We need the last one to extract only one-to-one orthologs.)

Now, we should sudmit our request. Click on `Results` above the left menu. You should be able to download your results now.

<br/>
----------------------------

Toronen P, Medlar A, Holm L (2018) PANNZER2: A rapid functional annotation webserver. Nucl. Acids Res. 46, W84-W88

Sayers, E. W., Bolton, E. E., Brister, J. R., Canese, K., Chan, J., Comeau, D. C., Connor, R., Funk, K., Kelly, C., Kim, S., Madej, T., Marchler-Bauer, A., Lanczycki, C., Lathrop, S., Lu, Z., Thibaud-Nissen, F., Murphy, T., Phan, L., Skripchenko, Y., Tse, T., … Sherry, S. T. (2022). Database resources of the national center for biotechnology information. Nucleic acids research, 50(D1), D20–D26. https://doi.org/10.1093/nar/gkab1112

