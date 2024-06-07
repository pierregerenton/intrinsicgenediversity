import argparse

__author__ = "Gérenton Pierre"
__credits__ = ["Gérenton Pierre", "Fabio Zanarello", "Roderic Guigó i Serra"]
__license__ = "CC0 1.0 Universal"

parser = argparse.ArgumentParser(
                    prog='convert_pannzer_output_to_input',
                    description='Convert pannzer output to acceptable input',
                    epilog='For more information, contact fabio.zanarello@crg.eu')

parser.add_argument(
    '-p', '--pannzer',
    type=str, required=True,
    help='Pannzer output path'
)

parser.add_argument(
    '-o', '--output',
    type=str, required=True,
    help='Path of the output'
)

args = parser.parse_args()

def main():
    first_line = True
    with open(args.pannzer) as file:
        with open(args.output, 'w') as output:

            for line in file:
                line = line.strip().split('\t')
                match line[1]:  # line[1] is type of line
                    case "original_DE":
                        if not first_line:
                            output.write(f'{gene_id}\t{transcript_id}\t{";".join(gos)}\n')
                        first_line=False
                        sequence_description = line[5].split(' ')
                        gene_id = sequence_description[0].split('=')[1].split('.')[0]
                        transcript_id = line[0]
                        gos = []
                    case "BP_ARGOT":
                        id = 'GO:' + line[-2]
                        gos.append(id)
                    case "CC_ARGOT":
                        id = 'GO:' + line[-2]
                        gos.append(id)
                    case "MF_ARGOT":
                        id = 'GO:' + line[-2]
                        gos.append(id)
                    case _:
                        pass
            output.write(f'{gene_id}\t{transcript_id}\t{";".join(gos)}\n')


if __name__=="__main__":
    main()

