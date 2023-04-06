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

csv_ddi = 'ddis_from_spreadsheet.csv'

with open(csv_ddi, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(row)
        source = row['source']
        if row['target'] != None:  # if target is present
            target = row['target']
            description = row['description']
            label = row['label']  # classification of risk
            if target not in node_list:
                node_list.append(target)
            source_target_label = tuple(
                (source, target, label, description))
            edge_for_nx = [source, target]
            nx_edge_list.append(edge_for_nx)
            edge_list.append(source_target_label)
        # label = int(row['weight'])
        # print(type(label)) should be int
        if source not in node_list:
            node_list.append(source)

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
    {'data': {'id': source+'--'+target+'--'+label, 'source': source,
              'target': target, 'label': label, 'description': description}}
    for source, target, label, description in (
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
    # {
    #     'selector': 'body',
    #     'style': {
    #         'background-color':'black'
    #     }
    # },
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
        'selector': '[label *= "Moderate"]',
        'style': {
            'line-color': '#ffc72b'
        }
    },
    {
        'selector': '[label *= "Severe"]',
        'style': {
            'line-color' : 'red'
        }
    },
    {
        'selector': '[label *= "Mild"]',
        'style': {
            'line-color': '#62ff3b'
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


@ app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
               Input('cytoscape-event-callbacks-2', 'mouseoverNodeData'))
def displayTapNodeData(data):
    if data:
        return "Cannot be taken with: " + str(neighbors_dict[data['label']])


@ app.callback(Output('cytoscape-mouseoverEdgeData-output', 'children'),
               Input('cytoscape-event-callbacks-2', 'mouseoverEdgeData'))
def displayTapEdgeData(data):
    if data:
        # return "The DDI between " + str(data['source'].upper()) + " and " + str(data['target'].upper()) + " is classified as " + str(data['label'])
        return "The DDI between " + str(data['source'].upper()) + " and " + str(data['target'].upper()) + " is classified as " + str(data['label']) + ", Adverse effect: " + str(data['description'])


if __name__ == '__main__':
    app.run_server(debug=True)
