import random
import time
import networkx as nx
import matplotlib.pyplot as plt

def findParent(v, parent):
    if v != parent[v]:
        parent[v] = findParent(parent[v], parent)
    return parent[v]

def unionSets(u, v, parent, rank):
    rootU = findParent(u, parent)
    rootV = findParent(v, parent)
    if rootU != rootV:
        if rank[rootU] > rank[rootV]:
            parent[rootV] = rootU
        elif rank[rootU] < rank[rootV]:
            parent[rootU] = rootV
        else:
            parent[rootV] = rootU
            rank[rootU] += 1

def KruskalMST(edges, v):
    edges.sort(key=lambda wgt: wgt[2])  # Sort edges by weight
    parent = [i for i in range(v)]
    rank = [0] * v
    mst = []
    mstWeight = 0

    G = nx.Graph()
    G.add_weighted_edges_from(edges)

    # Plot the initial graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{w}" for u, v, w in edges})
    plt.title("Initial Graph")
    plt.show(block=False)
    plt.pause(2)

    for edge in edges:
        u, v, w = edge
        if findParent(u, parent) != findParent(v, parent):
            # Edge does not form a cycle, add it to MST
            mst.append(edge)
            mstWeight += w
            unionSets(u, v, parent, rank)

            # Highlight MST edges in red
            plt.clf()
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=10)
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{w}" for u, v, w in edges})
            nx.draw_networkx_edges(G, pos, edgelist=mst, edge_color='red', width=2)
            plt.title(f"Adding edge {u}-{v} ({w}) to the MST")
            plt.show(block=False)
            plt.pause(2)
        else:
            # Edge forms a cycle, highlight in green briefly
            plt.clf()
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=10)
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{w}" for u, v, w in edges})
            nx.draw_networkx_edges(G, pos, edgelist=mst, edge_color='red', width=2)
            nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='green', width=2, style='dashed')
            plt.title(f"Cycle detected with edge {u}-{v} ({w})")
            plt.show(block=False)
            plt.pause(2)

    # Final MST visualization
    plt.clf()
    mstGraph = nx.Graph()
    mstGraph.add_weighted_edges_from(mst)
    nx.draw(mstGraph, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=10)
    nx.draw_networkx_edge_labels(mstGraph, pos, edge_labels={(u, v): f"{w}" for u, v, w in mst})
    nx.draw_networkx_edges(mstGraph, pos, edgelist=mst, edge_color='red', width=2)
    plt.title("Final MST")
    plt.show()

    print("Edges in MST:")
    for u, v, w in mst:
        print(f'{u} - {v} : {w}')
    print(f'The total weight of MST: {mstWeight}')
    
def generate_random_edges(v, max_weight=10, additional_edges=5):
    """
    Generates a connected graph with v vertices and additional random edges.

    Args:
    v (int): Number of vertices in the graph.
    max_weight (int): Maximum weight of the edges (default is 10).
    additional_edges (int): Additional edges beyond the minimum required for connectivity (default is 5).

    Returns:
    list: A list of tuples representing the edges in the format (u, v, weight).
    """
    edges = []

    # Ensure the graph is connected by creating a spanning tree
    for i in range(1, v):
        u = random.randint(0, i - 1)
        w = random.randint(1, max_weight - 1)  # Random weight
        edges.append((u, i, w))

    # Add additional random edges
    while additional_edges > 0:
        if v < 2: 
            break
        u, v = random.sample(range(v), 2)  # Ensure no self-loops (u != v)
        w = random.randint(1, max_weight - 1)
        edge = (u, v, w)
        if edge not in edges and (v, u, w) not in edges:  # Avoid duplicates
            edges.append(edge)
            additional_edges -= 1

    return edges

def main():
    v = 6  # Number of vertices
    edges = []
    
    # edges = generate_random_edges(v)
    
    #Adding edges in graph manually
    edges.append((0, 1, 4));
    edges.append((0, 2, 4));
    edges.append((1, 2, 2));
    edges.append((1, 0, 4));
    edges.append((2, 0, 4));
    edges.append((2, 1, 2));
    edges.append((2, 3, 3));
    edges.append((2, 5, 2));
    edges.append((2, 4, 4));
    edges.append((3, 2, 3));
    edges.append((3, 4, 3));
    edges.append((4, 2, 4));
    edges.append((4, 3, 3));
    edges.append((5, 2, 2));
    edges.append((5, 4, 3));

    start_time = time.time()
    KruskalMST(edges, v)
    end_time = time.time()
    print('Time taken: %f' % (end_time - start_time))

if __name__ == "__main__":
    main()