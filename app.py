import dash
import dash_cytoscape as cyto
from dash import html
import networkx as nx

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Define age groups and spending categories
age_groups = ["18-25", "26-35", "36-50", "51+"]
categories = ["Groceries", "Electronics", "Clothing", "Entertainment", "Restaurants", "Travel", "Healthcare", "Fitness"]

# Generate spending data
spending_data = {
    "18-25": {"Groceries": 8000, "Entertainment": 6000, "Clothing": 7000},
    "26-35": {"Electronics": 9000, "Restaurants": 7000},
    "36-50": {"Healthcare": 10000, "Travel": 8000},
    "51+": {"Groceries": 10000, "Healthcare": 9000, "Fitness": 5000}
}

# Create NetworkX bipartite graph
B = nx.Graph()
B.add_nodes_from(age_groups, bipartite=0)  # Age groups
B.add_nodes_from(categories, bipartite=1)  # Spending categories

edges = []
for age, spends in spending_data.items():
    for category, weight in spends.items():
        B.add_edge(age, category, weight=weight / 1000)  # Normalize weight for visualization
        edges.append({"source": age, "target": category, "weight": weight / 1000})

# Create Cytoscape Elements (Nodes + Edges)
cyto_elements = []

# Add nodes
for node in B.nodes():
    cyto_elements.append({
        "data": {"id": node, "label": node},
        "classes": "age" if node in age_groups else "category"
    })

# Add edges
for edge in edges:
    cyto_elements.append({
        "data": {"source": edge["source"], "target": edge["target"], "weight": edge["weight"]}
    })

# Layout for Dash Cytoscape
cyto_stylesheet = [
    {"selector": "node", "style": {"content": "data(label)", "text-valign": "center", "text-halign": "center"}},
    {"selector": ".age", "style": {"background-color": "lightblue", "shape": "rectangle", "width": "100px"}},
    {"selector": ".category", "style": {"background-color": "lightcoral", "shape": "ellipse"}},
    {"selector": "edge", "style": {"line-color": "gray", "width": "data(weight)"}}
]

# Dash Layout
app.layout = html.Div([
    html.H2("Bipartite Graph: Age Groups & Spending Categories"),
    cyto.Cytoscape(
        id="bipartite-graph",
        elements=cyto_elements,
        style={"width": "900px", "height": "600px", "border": "1px solid black"},
        layout={"name": "cose"},  # Force-directed layout
        stylesheet=cyto_stylesheet
    )
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
