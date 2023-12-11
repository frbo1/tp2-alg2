import networkx as nx
from bnb import tsp
from aprox import twice_around_the_tree, algoritmo_de_christofides

def test_bnb_tsp():
    # Grafo tem 4 nós e os pesos são os primeiros 6 números naturais distribuídos em sentido anti-horário.
    edgelist = [(0, 1, 1), (0, 2, 5), (0, 3, 4),
                (1, 0, 1), (1, 2, 2), (1, 3, 6),
                (2, 0, 5), (2, 1, 2), (2, 3, 3),
                (3, 0, 4), (3, 1, 6), (3, 2, 3)]

    G = nx.Graph()
    G.add_weighted_edges_from(edgelist)

    matriz_adj = nx.adjacency_matrix(G).todense()

    assert tsp(matriz_adj, G.number_of_nodes()) == [0, 1, 2, 3, 0]

def test_twice_around_the_tree_tsp():
    edgelist = [(0, 1, 1), (0, 2, 5), (0, 3, 4),
                (1, 0, 1), (1, 2, 2), (1, 3, 6),
                (2, 0, 5), (2, 1, 2), (2, 3, 3),
                (3, 0, 4), (3, 1, 6), (3, 2, 3)]

    G = nx.Graph()
    G.add_weighted_edges_from(edgelist)

    assert twice_around_the_tree(G)

def test_algoritmo_de_christofides_tsp():
    edgelist = [(0, 1, 1), (0, 2, 5), (0, 3, 4),
                (1, 0, 1), (1, 2, 2), (1, 3, 6),
                (2, 0, 5), (2, 1, 2), (2, 3, 3),
                (3, 0, 4), (3, 1, 6), (3, 2, 3)]

    G = nx.Graph()
    G.add_weighted_edges_from(edgelist)

    assert algoritmo_de_christofides(G)
