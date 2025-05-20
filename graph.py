import os
import sys
import subprocess
import matplotlib.pyplot as plt

# Überprüfen und Installieren der erforderlichen Bibliotheken
try:
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
    import numpy as np

# Definition der Graph-Klasse
class Graph:
    def __init__(self):
        self.nodes = {}  # {node_id: (x, y)}
        self.edges = []  # [(node_id1, node_id2)]

    def add_node(self, node_id, x, y):
        self.nodes[node_id] = (x, y)

    def add_edge(self, node1, node2):
        self.edges.append((node1, node2))

# Funktion zum Plotten des Graphen und Speichern als Bild
def plot_graph(graph, output_dir, filename="graph.jpg"):
    # Falls der Ausgabeordner nicht existiert, erstellen
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    fig, ax = plt.subplots()
    node_radius = 15

    # Zeichnen der Kanten
    for node1, node2 in graph.edges:
        x1, y1 = graph.nodes[node1]
        x2, y2 = graph.nodes[node2]
        ax.plot([x1, x2], [y1, y2], 'k-', zorder=1)  # Schwarze Linie für Kanten

    # Zeichnen der Knoten
    for node_id, (x, y) in graph.nodes.items():
        circle = plt.Circle((x, y), node_radius, color='black', zorder=2)
        ax.add_artist(circle)
        ax.text(x, y, str(node_id), color='white', fontsize=10, ha='center', va='center', zorder=3)
    
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    plt.title("Graph Visualisierung")
    
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight') # Graph speichern
    plt.close()
    print(f"Graph gespeichert unter: {output_path}")
