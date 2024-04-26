import gene_transcript_go_api as gtga
import pandas as pd
import argparse
from os.path import basename


parser = argparse.ArgumentParser(
                    prog='gene_intrinsic_jaccard_index',
                    description='Compute Jaccard Index for each gene',
                    epilog='For more information, contact pierre.gerenton@crg.eu')


parser.add_argument(
    '-i', '--input',
    type=str, required=True,
    help='Correctly formatted input'
)

parser.add_argument(
    '-o', '--output-name',
    type=str, default='number_genes_with_different_go_term_between_files',
    help='Name of the output file'
)


args = parser.parse_args()



def main():

    print('Reading input ...')

    annotation : gtga.Annotation = gtga.parse_input(args.input)

    print('Done\n')

    print('Computing Jaccard index for given data ...')

    data = pd.DataFrame()
    data['Gene'] = annotation.genes.keys()
    data['Jaccard Index'] = data['Gene'].apply(annotation.get_gene).apply(gtga.Gene.diversity_by_pair, similarity_function=gtga.jaccard_index)

    print('Done\n')

    print('Writing output ...')


    data.to_csv(args.output_name + '.tsv', sep='\t', index=False)

    print('Done')


if __name__=="__main__":
    main()


