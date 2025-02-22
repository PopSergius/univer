import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from flask import Flask, render_template, request, jsonify
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Ініціалізація Flask-додатку
server = Flask(__name__)


#
class PetriNet:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.tokens = {}

    def add_subnet(self, subnet_id, tokens=0):
        self.graph.add_node(subnet_id, type="subnet", tokens=tokens)
        self.tokens[subnet_id] = tokens

    def add_port(self, port_id):
        self.graph.add_node(port_id, type="port")
        self.tokens[port_id] = 0

    def add_edge(self, src, dst):
        if src in self.graph.nodes and dst in self.graph.nodes:
            self.graph.add_edge(src, dst)

    def can_fire(self, node):
        if self.graph.nodes[node]["type"] == "subnet":
            return self.tokens.get(node, 0) > 0
        return False

    def step(self):
        new_tokens = self.tokens.copy()
        fired = False

        for node in self.graph.nodes():
            if self.graph.nodes[node]["type"] == "subnet" and self.can_fire(node):
                successors = list(self.graph.successors(node))

                if not successors:
                    continue

                for port in successors:
                    if self.graph.nodes[port]["type"] == "port":
                        port_successors = list(self.graph.successors(port))

                        for final_node in port_successors:
                            if self.graph.nodes[final_node]["type"] == "subnet":
                                if new_tokens[node] > 0:
                                    # Віднімаємо токен з початкової вершини
                                    new_tokens[node] -= 1
                                    # Порт тимчасово отримує токен
                                    new_tokens[port] = 0
                                    # Додаємо токен до існуючих токенів у кінцевій вершині
                                    new_tokens[final_node] = (
                                        new_tokens.get(final_node, 0) + 1
                                    )
                                    fired = True

        if fired:
            self.tokens = new_tokens

        return fired

    def get_plotly_figure(self):
        pos = nx.spring_layout(self.graph)
        edge_x = []
        edge_y = []
        annotations = []

        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            annotations.append(
                dict(
                    ax=x0,
                    ay=y0,
                    axref="x",
                    ayref="y",
                    x=x1,
                    y=y1,
                    xref="x",
                    yref="y",
                    text="",
                    showarrow=True,
                    arrowhead=3,
                    arrowsize=2,
                    arrowwidth=1,
                )
            )

        node_shapes = []
        for node in self.graph.nodes():
            x, y = pos[node]
            is_subnet = self.graph.nodes[node]["type"] == "subnet"

            shape = dict(
                type="circle" if is_subnet else "rect",
                xref="x",
                yref="y",
                x0=x - 0.05,
                y0=y - 0.05,
                x1=x + 0.05,
                y1=y + 0.05,
                line=dict(color="black"),
                fillcolor="white" if is_subnet else "lightgray",
            )

            token_count = self.tokens.get(node, 0)
            if token_count > 0 or is_subnet:
                annotations.append(
                    dict(
                        x=x,
                        y=y,
                        xref="x",
                        yref="y",
                        text=str(token_count),
                        showarrow=False,
                        font=dict(size=14, color="black"),
                        align="center",
                    )
                )

            node_shapes.append(shape)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=edge_x,
                y=edge_y,
                line=dict(width=1, color="gray"),
                hoverinfo="none",
                mode="lines",
            )
        )

        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            annotations=annotations,
            shapes=node_shapes,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )

        return fig


petri_net = PetriNet()

# Ініціалізація Dash-додатку
dash_app = dash.Dash(__name__, server=server, url_base_pathname="/dashboard/")

dash_app.layout = html.Div(
    [
        html.H1("Редактор мережі Петрі"),
        dcc.Input(id="node-id", type="text", placeholder="ID вершини"),
        dcc.Dropdown(
            id="node-type",
            options=[
                {"label": "Змістовна вершина", "value": "subnet"},
                {"label": "Порт", "value": "port"},
            ],
            placeholder="Тип вершини",
        ),
        dcc.Input(
            id="token-count", type="number", placeholder="Кількість токенів", min=0
        ),
        html.Button("Додати вершину", id="add-node-btn", n_clicks=0),
        html.Button("Видалити вершину", id="remove-node-btn", n_clicks=0),
        dcc.Input(id="edge-src", type="text", placeholder="Звідки дуга"),
        dcc.Input(id="edge-dst", type="text", placeholder="Куди дуга"),
        html.Button("Додати дугу", id="add-edge-btn", n_clicks=0),
        html.Button("Видалити дугу", id="remove-edge-btn", n_clicks=0),
        dcc.Graph(id="network-graph"),
        html.Button("Почати", id="start-btn", n_clicks=0),
    ]
)


@dash_app.callback(
    Output("network-graph", "figure"),
    [
        Input("add-node-btn", "n_clicks"),
        Input("remove-node-btn", "n_clicks"),
        Input("add-edge-btn", "n_clicks"),
        Input("remove-edge-btn", "n_clicks"),
        Input("start-btn", "n_clicks"),
    ],
    [
        State("node-id", "value"),
        State("node-type", "value"),
        State("token-count", "value"),
        State("edge-src", "value"),
        State("edge-dst", "value"),
    ],
)
def update_graph(
    add_node_clicks,
    remove_node_clicks,
    add_edge_clicks,
    remove_edge_clicks,
    start_btn,
    node_id,
    node_type,
    token_count,
    edge_src,
    edge_dst,
):
    ctx = dash.callback_context
    if not ctx.triggered:
        return petri_net.get_plotly_figure()

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "add-node-btn" and node_id and node_type:
        if node_type == "subnet":
            petri_net.add_subnet(node_id, token_count or 0)
        elif node_type == "port":
            petri_net.add_port(node_id)

    elif button_id == "remove-node-btn" and node_id:
        petri_net.remove_node(node_id)

    elif button_id == "add-edge-btn" and edge_src and edge_dst:
        petri_net.add_edge(edge_src, edge_dst)

    elif button_id == "remove-edge-btn" and edge_src and edge_dst:
        petri_net.remove_edge(edge_src, edge_dst)

    elif button_id == "start-btn":
        petri_net.step()

    return petri_net.get_plotly_figure()


if __name__ == "__main__":
    server.run(debug=True)
