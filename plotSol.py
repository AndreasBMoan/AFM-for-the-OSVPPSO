# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:52:35 2019

@author: andrebmo
"""

import plotly.graph_objects as go
from plotly.offline import plot
import networkx as nx
import data

Vessels = data.Vessels
Insts = data.Insts
Times = data.Times


def draw_routes(x_vars,fuel_cost):
    G = nx.Graph()

    InstTimes = [[[] for i in Insts] for v in Vessels]
    for v in Vessels:
        for i in Insts:
            for t in Times:
                count = 0
                for j in Insts:
                    for tau in Times:
                        if fuel_cost[v][j][tau][i][t] != 0 or fuel_cost[v][i][t][j][tau] != 0:
                            count += 1
                if count != 0:
                    InstTimes[v][i].append(t)

    for v in Vessels:
        for i in Insts:
            for t in InstTimes[v][i]:
                G.add_node(t*30 + i, pos=(t,i))

    for v in Vessels:
        for i in Insts:
            for t in Times:
                for j in Insts:
                    for tau in Times:
                        if x_vars[v][i][t][j][tau]!= 0:
                            G.add_edge(t*30 + i, tau*30 + j, weight=0)
                        
    
    edge_x = []
    edge_y = []
    
    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#BBB'),
        hoverinfo='none',
        mode='lines')
    
    node_x = []
    node_y = []
    
    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_x.append(x)
        node_y.append(y)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
#            ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
#             'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
#             'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
#             'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
#             'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
#             'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
#             'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
#             'orrd', 'oryel', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg',
#             'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor',
#             'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy',
#             'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral',
#             'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose',
#             'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'twilight',
#             'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd']
            colorscale='bluyl',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=10,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))    
    
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))
    
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='<br>Network graph made with Python',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="The Arc-Flow Model",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=True, zeroline=False, showticklabels=True),
                    yaxis=dict(showgrid=True, zeroline=False, showticklabels=True))
                    )
    plot(fig, auto_open=True)