# intrinsicgenediversity

The purpose is to quantify the intrinsic gene diversity (using various metrics) and understand everything that this information can bring to us.

## Summary

- [Summary](#summary)
- [Requirement](#requirement)
- [Organization of the repo](#organization-of-the-repo)
- [Metrics](#metrics)
    - [Metrics computed in all isoform](#metrics-computed-in-all-isoform)
    - [Metrics computed for each pair of isoform](#metrics-computed-for-each-pair-of-isoform)
- [Run the code](#run-the-code)
    - [Evaluate isoforms diversity for each gene](#evaluate-isoforms-diversity-for-each-gene)
        -[Exploring the results interactively with a Dash app](#exploring-the-results-interactively-with-a-dash-app)
    - [Compute Jaccard Index between isoforms for each gene](#compute-jaccard-index-between-isoforms-for-each-gene)
- [Notebook used to produce graph](#notebook-used-to-produce-graph)
- [Experimental analysis](#experimental-analysis)
    - [Comparing diversity between orthologues genes](#comparing-diversity-between-orthologues-genes)
    - [Explore functional convergeance of gene](#explore-functional-convergeance-of-gene)


## Requirement


If you want to get input data by yourselves :

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
- [`res`](res) : output files

## Metrics

Different metrics were selected to represent the diversity / similarity of isoforms.


### Metrics computed in all isoform :

Some metrics are computed at all isoform at once. To compute them, let's first define some concept.

Let $G$, the gene, be a set of $n$ isoform defined as :
$$ G = \{ I_1, I_2, \ldots, I_n \} $$
where each $I_i$ is a set of $m_i$ GO terms defined as :
$$ I_i = \{ T_{i1}, T_{i2}, \ldots, T_{im_i} \} $$


***Number of isoform : number of isoform***
$$n_{isoform} = n = |G|$$

***Standard deviation of the number of GO term***
$$\sigma_{m} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}{(m_i-\bar{m} )^2}}$$

***Redundancy metric***\
This metrics was designed to have an idea of the number of times a GO term appear in the genes.
For each unique GO term, his number of reoccurence is count ($0$ if it appear only in $1$ isoform, and $n-1$ if it appear in all isoform). Then, the mean of this counting is done to have the mean count of reoccurence. Finally, this count is divided by the $n-1$.
If $r$ is close to $1$, that's means that all GO terms are present in all isoforms, and if $r$ is close to $0$, each isoform is different.

If there is 1 isoform, the redudancy metric is set to $1$.

Let $O$ be the set of all $n_o$ unique GO terms defined as :
$$O = \bigcup_{i=1}^n I_i = \{ T_{1}, T_{2}, \ldots, T_{n_o} \}$$
Let $count(T_i)$ the number of isoform where $T_i$ is present.

$$rdd(T_i) = \frac{1}{n-1} (count(T_i)-1)$$

We then return the mean $\overline{rdd_T}$.

Else, the formula can be simplify as :
$$rdd(G) = \overline{rdd_T} =  \frac{1}{n_o(n-1)} \sum_{i=1}^ {n_o}(count(T_i)-1)$$

 <br/> 

### Metrics computed for each pair of isoform :
Some metrics were calculated for each pair of isoforms before all the values were averaged.

***Jaccard index***\
The Jaccard index is measure of similarity.\
If $I_1 \cup I_2  = \emptyset$, $J(I_1, I_2) = 1$, else

$$J(I_1, I_2) = \frac{|I_1 \cap I_2|}{|I_1 \cup I_2|}$$

***Dice coefficient***\
The Sørensen–Dice coefficient is measure of similarity.\
If $I_1 \cup I_2  = \emptyset$, $D(I_1, I_2) = 1$, else

$$D(I_1, I_2) = \frac{2|I_1 \cap I_2|}{|I_1| + |I_2|}$$

***Overlap coefficient***\
If $min(|I_1|,|I_2|) = 0$, then $overlap(I_1, I_2) = 1$, else

$$overlap(I_1, I_2) = \frac{|I_1 \cap I_2|}{min(|I_1|,|I_2|)}$$

***BP, CC and MF GOGO similarity***\
Semantic similarity computed between GO terms of each isoform.
More information in the paper :
`Zhao, C. and Wang, Z. (2018) GOGO: An improved algorithm to measure the semantic similarity between gene ontology terms. Scientific Reports, 8, 15107; doi:10.1038/s41598-018-33219-y.`


## Run the code


### Evaluate isoforms diversity for each gene

To evaluate isoforms diversity for each gene with different metrics, you should run :

```sh
python3 src/intragene_isoform_diversity.py -i data/human_input.tsv -g ~/Software/GOGO/ -o res/human.intragene_isoform_diversity
```

- `-i` : path of the input file (from a multiple-isoform annotation) \[MANDATORY\]
- `-g` : path of GOGO directory \[MANDATORY\]
- `-o` : name of the output file \[MANDATORY\]

Input should have 3 columns :
- Gene ID
- Transcript ID
- List of GO term ID separated by ';'

Two files are generated :
- `output.data.tsv` : measurement for each gene
- `output.summary.tsv` : descriptive statistics for each measurement


#### Exploring the results interactively with a Dash app

You can explore the table with interactivity (filter table, remove column, export to csv and sort) with a Dash app if you run :

```sh
python3 src/intragene_isoform_diversity_interactive.py -d res/human.intragene_isoform_diversity
```

- `-d` : prefix path to the data produced by the scripts `intragene_isoform_diversity` (do not write the `.data.tsv` and `.summary.tsv`) \[MANDATORY\]

This app use the implemented filter features for datatable. To filter a `int` column, you can use `<` or `>` before a number of get all row where the value in inferior/superior to your threshold in the current columns. 

### Compute Jaccard Index between isoforms for each gene

To compute Jaccard Index between isoforms for each gene, run :

```sh
python3 src/gene_intrinsic_jaccard_index.py -i data/mouse_input.tsv -o res/mouse.gene_intrinsic_jaccard_index
```

- `-i` : path of the input file (from a multiple-isoform annotation) \[MANDATORY\]
- `-o` : name of the output file \[MANDATORY\]

Input should have 3 columns :
- Gene ID
- Transcript ID
- List of GO term ID separated by ';'

The output will have 2 columns :
- Gene ID
- Jaccard Index (1 if the gene has 1 isoform)

## Notebook used to produce graph

Some notebook was used to produce graph and can be useful as support. There were push in this repository.

You can find :

- [`src/correlation_matrix_igd.ipynb`](src/correlation_matrix_igd.ipynb) to produce a correlation matrix between all diversity metrics tested and produce graph to compare them all with a parametrable function.
- [`src/correlation_matrix_igd_no_empty_transcript.ipynb`](src/correlation_matrix_igd_no_empty_transcript.ipynb) : same as before but with the data produced after the deletion of empty transcripts (transcripts without GO term predicted)

## Experimental analysis

To understand this diversity, some preliminary results have been made.

### Comparing diversity between orthologues genes

You can observed the conservation of diversity between orthologues genes in [`src/orthologue_analysis.ipynb`](src/orthologue_analysis.ipynb) and [`src/orthologue_analysis_no_empty_transcript.ipynb`](src/orthologue_analysis_no_empty_transcript.ipynb).

### Additional graph

Comparisons of the diversity VS the number of exons or the protein length. Visualization of the repartition of the diversity.
Available in [`src/additional_graph.ipynb`](src/additional_graph.ipynb).

### Explore functional convergeance of gene

This is a really experimental part. We want to see if annotating new isoforms for a gene will brings new function (GO term) or if we already explore everything. This analysis was abandonned (result not relevant).

You can explore our gene convergeance attempt with a notebook in [`src/convergence_graph.ipynb`](src/convergence_graph.ipynb).

You can explore our gene convergeance data with a dash app.

```sh
python3 src/dash_convergence_graph.py -d data/human_input.tsv
```