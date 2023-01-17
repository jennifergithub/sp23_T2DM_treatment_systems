import json

import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import csv
import networkx as nx

app = dash.Dash(__name__)

edge_list = []
# create separate edge list for NetworkX object
nx_edge_list = []
node_list = []
# read in the drug combinations CSV
with open('drug_combinations.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(row)
        source = row['source']
        target = row['target']
        label = int(row['weight'])
        # print(type(label)) should be int
        if source not in node_list:
            node_list.append(source)
        if target not in node_list:
            node_list.append(target)
        source_target_label = tuple(
            (source, target, label))
        edge_for_nx = [source, target]
        nx_edge_list.append(edge_for_nx)
        edge_list.append(source_target_label)

# create NetworkX object
G = nx.Graph()
G.add_nodes_from(node_list)
G.add_edges_from(nx_edge_list)
neighbors_dict = {}
for node in G.nodes:
    neighbors_dict[node] = [n for n in G.neighbors(node)]
# print(G.nodes)
neighbors_list = list(neighbors_dict.values())
new_list = []
for neighbor in neighbors_list:
    new_list.append(','.join(neighbor))
# print(new_list)
# p = nx.shortest_path(G, source='metformin', target='glyburide')
# print(p)


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# print(node_list)
# for node in node_list:
#     print([n for n in G.predecessors(node)])
# print(edge_list)

nodes = [
    {
        'data': {'id': label, 'label': str(label), 'neighbor': neighbor}
    }
    for label in (
        node_list
    )
    for neighbor in (
        new_list
    )
]

# print(nodes)

edges = [
    {'data': {'id': source+'--'+target+'--'+str(label), 'source': source,
              'target': target, 'label': label}}
    for source, target, label in (
        edge_list
    )
]

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'width': '2px',
            # 'label': 'data(label)',
            'font-size': '10px',
            'font-opacity': 1,
            # 'target-arrow-color': 'black',
            # 'target-arrow-shape': 'triangle',
            'line-color': 'green'
        }
    },
    {
        'selector': ':selected',
        'style': {
            'border-color': 'black',
            'border-opacity': '1',
            'border-width': '0.075px',
            'label': 'data(label)'
        }
    },
    {
        'selector': '[label > 1000]',
        'style': {
            'line-color': 'red'
        }
    }
]

cyto.load_extra_layouts()

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-event-callbacks-2',
        layout={'name': 'cola', 'nodeSpacing': 70},
        elements=edges+nodes,
        stylesheet=default_stylesheet,
        style={'width': '100%', 'height': '450px'}
    ),
    # html.P(id='cytoscape-tapNodeData-output'),
    # html.P(id='cytoscape-tapEdgeData-output'),
    html.P(id='cytoscape-mouseoverNodeData-output'),
    html.P(id='cytoscape-mouseoverEdgeData-output')
])


# @app.callback(Output('cytoscape-tapNodeData-output', 'children'),
#               Input('cytoscape-event-callbacks-2', 'tapNodeData'))
# def displayTapNodeData(data):
#     if data:
#         return "You recently clicked/tapped the node: " + data['label']


# @app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
#               Input('cytoscape-event-callbacks-2', 'tapEdgeData'))
# def displayTapEdgeData(data):
#     if data:
#         return "Use " + data['label'] + " to get from " + \
#                data['source'].upper() + " to " + data['target'].upper()


@app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
              Input('cytoscape-event-callbacks-2', 'mouseoverNodeData'))
def displayTapNodeData(data):
    if data:
        return "Taken with: " + str(neighbors_dict[data['label']])


@app.callback(Output('cytoscape-mouseoverEdgeData-output', 'children'),
              Input('cytoscape-event-callbacks-2', 'mouseoverEdgeData'))
def displayTapEdgeData(data):
    if data:
        return str(data['label']) + " patients have taken " + \
            data['source'].upper() + " with " + data['target'].upper()


if __name__ == '__main__':
    app.run_server(debug=True)
