import networkx as nx
from bnb import calcular_estimativa

def test_k4_padrao():
    # Pesos são os primeiros 4 números naturais distribuídos em sentido anti-horário.
    edgelist = [(0, 1, 1), (0, 2, 5), (0, 3, 4),
                (1, 0, 1), (1, 2, 2), (1, 3, 6), 
                (2, 0, 5), (2, 1, 2), (2, 3, 3),
                (3, 0, 4), (3, 1, 6), (3, 2, 3)]

    G = nx.Graph()
    G.add_weighted_edges_from(edgelist)
    matriz_adj = nx.adjacency_matrix(G).todense()

    assert calcular_estimativa(matriz_adj, G.number_of_nodes(), [0]) == 10

def test_k4_incluindo_0_2():
    # Pesos são os primeiros 4 números naturais distribuídos em sentido anti-horário.
    edgelist = [(0, 1, 1), (0, 2, 5), (0, 3, 4),
                (1, 0, 1), (1, 2, 2), (1, 3, 6), 
                (2, 0, 5), (2, 1, 2), (2, 3, 3),
                (3, 0, 4), (3, 1, 6), (3, 2, 3)]

    G = nx.Graph()
    G.add_weighted_edges_from(edgelist)
    matriz_adj = nx.adjacency_matrix(G).todense()

    assert calcular_estimativa(matriz_adj, G.number_of_nodes(), [0, 2]) == 12 

def test_k4_incluindo_0_1_e_1_3():
    # Pesos são os primeiros 4 números naturais distribuídos em sentido anti-horário.
    edgelist = [(0, 1, 1), (0, 2, 5), (0, 3, 4),
                (1, 0, 1), (1, 2, 2), (1, 3, 6), 
                (2, 0, 5), (2, 1, 2), (2, 3, 3),
                (3, 0, 4), (3, 1, 6), (3, 2, 3)]

    G = nx.Graph()
    G.add_weighted_edges_from(edgelist)
    matriz_adj = nx.adjacency_matrix(G).todense()

    assert calcular_estimativa(matriz_adj, G.number_of_nodes(), [0, 1, 3]) == 12
