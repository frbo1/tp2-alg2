import networkx as nx

def twice_around_the_tree(grafo):
    T = nx.minimum_spanning_tree(grafo, algorithm="prim")
    H = nx.dfs_preorder_nodes(T)

    return list(H)

def algoritmo_de_christofides(grafo):
    T = nx.minimum_spanning_tree(grafo)
    grafo_induzido = nx.subgraph(grafo, [v for v, deg in T.degree if deg % 2 == 1])
    M = list(nx.min_weight_matching(grafo_induzido))
    G = nx.MultiGraph()
    G.add_nodes_from(grafo.nodes)
    G.add_weighted_edges_from(grafo_induzido.edges(M, data=True))
    G.add_weighted_edges_from(T.edges(data=True))
    circ = list(nx.dfs_preorder_nodes(G))

    return circ
