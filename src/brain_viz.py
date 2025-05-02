import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

def decode_gene(gene, n_sensory, n_internal, n_action):
    bin_gene = format(int(gene, 16), "032b")
    source_type = int(bin_gene[0], 2)
    source_id = int(bin_gene[1:8], 2)
    sink_type = int(bin_gene[8], 2)
    sink_id = int(bin_gene[9:16], 2)
    weight = (int(bin_gene[16:], 2) - 32768) / 8192

    if source_type == 0:
        source = f"S{source_id % n_sensory}"
    else:
        source = f"H{source_id % n_internal}"
        
    if sink_type == 0:
        sink = f"H{sink_id % n_internal}"
    else:
        sink = f"A{sink_id % n_action}"

    return source, sink, weight

def visualize_brain(genome, n_sensory=8, n_internal=4, n_action=5):
    G = nx.DiGraph()

    # Layout positions for layers
    pos = {}
    for i in range(n_sensory):
        node = f"S{i}"
        G.add_node(node)
        pos[node] = (-2, -i)

    for i in range(n_internal):
        node = f"H{i}"
        G.add_node(node)
        pos[node] = (0, -i)

    for i in range(n_action):
        node = f"A{i}"
        G.add_node(node)
        pos[node] = (2, -i)

    # Decode and draw edges
    for gene in genome:
        src, dst, w = decode_gene(gene, n_sensory, n_internal, n_action)
        G.add_edge(src, dst, weight=w)

    edge_colors = ['red' if G[u][v]['weight'] < 0 else 'blue' for u, v in G.edges()]
    edge_widths = [abs(G[u][v]['weight']) for u, v in G.edges()]

    nx.draw(G, pos, with_labels=True, node_color='lightgray', 
            edge_color=edge_colors, width=edge_widths, arrows=True)
   
    red_patch = mpatches.Patch(color='red', label='Inhibitory (weight < 0)')
    blue_patch = mpatches.Patch(color='blue', label='Excitatory (weight > 0)')
    plt.legend(handles=[blue_patch, red_patch], loc='upper right')


    plt.title("Neural Network Structure")
    plt.axis("off")
    plt.show()

