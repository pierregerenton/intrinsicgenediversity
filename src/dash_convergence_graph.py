import sys
sys.path.append("..")
import gene_transcript_go_api as gtga
from random import sample
from statistics import mean
import scipy.optimize
import numpy as np
import argparse
from dash import Dash, html, dcc, Input, Output, callback
import dash_daq as daq
import plotly.graph_objects as go

__author__ = "Gérenton Pierre"
__credits__ = ["Gérenton Pierre", "Fabio Zanarello", "Roderic Guigó i Serra"]
__license__ = "CC0 1.0 Universal"

parser = argparse.ArgumentParser(
                    prog='convergence',
                    description='App to easily test convergence for random gene',
                    epilog='For more information, contact fabio.zanarello@crg.eu')


parser.add_argument(
    '-d', '--data',
    type=str, required=True,
    help='Path of the output of the "intragene_isoform_diversity" script'
)


args = parser.parse_args()

def logistic(x, K, r, m):
    a = ( K  /  ( K - m) ) - 1
    offset =  - (K / (1 + a))
    return (K)/(1+ a*np.exp(-r*x)) + offset

def logistic_offset(K, r, m):
    a = ( K  /  ( K - m) ) - 1
    offset = - (K / (1 + a))
    return offset

def asymptote(param):
    return param[2]

def nGO(gene : gtga.Gene) -> int:
    return len(gene.get_go_term_id())

def plot_fit_nGO(nminiso : int, genen : int) -> None:
    gene : gtga.Gene = [data[gene] for gene in data if data[gene].number_of_isoforms() >= nminiso][genen] # 953 et 85 et 45
    n_max : int = gene.number_of_isoforms()
    nGOs : list[int] = []
    ni : list[int] = []
    for i in range(0, n_max+1):
        transcript_list : list[gtga.Transcript] = list(gene.transcripts.values())
        iterresult : list[int]= []
        for _ in range(5000):
            sub_transcript_list : list[gtga.Transcript] = sample(transcript_list, i)
            tmp_gene : gtga.Gene = gtga.Gene('unk','unk')
            tmp_gene.add_transcripts(sub_transcript_list)
            iterresult.append(nGO(tmp_gene))
        nGOs.append(mean(iterresult))
        ni.append(i)
    fig = go.Figure()
    fig.add_scatter(x=ni, y=nGOs)
    fig.update_layout(xaxis_title="Number of isoforms", yaxis_title="Number of GO terms", title="Number of GO terms as a function of the number of isoforms",
                      width=1400, height=800, showlegend = False)



    opt_coef, pcov = scipy.optimize.curve_fit(logistic, ni, nGOs,p0=[2*np.max(nGOs), 0.5, np.max(nGOs)], bounds=([np.max(nGOs),0,np.max(nGOs)],[np.inf, np.inf, np.inf]),maxfev = 50000)
    curve_x = np.arange(0,gene.number_of_isoforms()+5, 0.2)
    curve_y = logistic(np.array(curve_x), *opt_coef)
    fig.add_hline(asymptote(opt_coef), line_color = 'red')
    fig.add_scatter(x=curve_x, y=curve_y, mode='lines', marker={'color' : "green"})
    
    residuals = np.array(nGOs) - logistic(np.array(ni), *opt_coef)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((nGOs - np.mean(nGOs))**2)
    return fig, 1 - (ss_res / ss_tot), opt_coef


data = gtga.parse_input(args.data, 'main_data')

fig, _, _ = plot_fit_nGO(3, 85)

max_nb_isoform = max([data[gene].number_of_isoforms() for gene in data])

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive convergence graph"),
    html.Div([
        dcc.Graph(id="graph", figure=fig),
        html.Div([
            daq.NumericInput(id='n_iso_min', label='Minimum number of isoforms', min=1, max=max_nb_isoform, value=3),
            daq.NumericInput(id='genenb', label="Gene n.", max=10, value=0)
        ], style={'float': 'right', 'margin-left': '20px', 'margin-top': '20px'})
    ], style={'display': 'flex'})
])

@callback(
    Output('genenb', 'max'),
    Input('n_iso_min', 'value')
)
def set_genen_max(value_iso_min):
    return len([data[gene] for gene in data if data[gene].number_of_isoforms() >= value_iso_min]) - 1

@callback(
    Output('graph', 'figure'),
    Input('n_iso_min','value'),
    Input('genenb', 'value')
)
def update_graph(n_iso_min,genenb):
    return plot_fit_nGO(n_iso_min, genenb)[0]


if __name__=="__main__":
    app.run(debug=True)

