import sys
import time
import tracemalloc
import signal
import copy

import pandas as pd
import networkx as nx

import bnb
import aprox


def carregar_info(lista_bases):
    RAIZ = "http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/"

    urls = [RAIZ + base + ".tsp.gz" for base in lista_bases]

    data = []
    i = 1
    for url in urls:
        print("> Baixando base de dados {} ...".format(i))
        raw_data = pd.read_csv(url, delim_whitespace=True, skiprows=6, names=["no", "x", "y"])[:-1]
        print("> Base de dados {} foi salva com sucesso!".format(i))
        raw_data["no"] = pd.to_numeric(raw_data["no"])

        G = nx.complete_graph(raw_data["no"])

        raw_data.set_index("no", drop=True, inplace=True)
        nx.set_node_attributes(G, raw_data.to_dict("index"))

        # Calculando as distâncias para cada nó (ponto do mapa)
        for u, v in G.edges:
            G[u][v]["weight"] = ((G.nodes[u]['x'] - G.nodes[v]['x']) ** 2 + (G.nodes[u]['y'] - G.nodes[v]['y']) ** 2) ** 1/2

        data.append(G)
        i += 1

    return data

def calcular_custo(solucao, grafo):
    custo = 0
    i = 0
    while i < len(solucao) - 1:
        custo += grafo[i][i + 1]
        i += 1

    # Acrescenta o custo de voltar ao início.
    return custo + grafo[i][0]

def handler(signum, frame):
    print("> Tempo esgotado para a tarefa!")
    raise TimeoutError("Tempo esgotado.")


ALGORITMOS_AVALIADOS = ["bnb", "Twice-around-the-tree", "Christofides"]
TEMPO_MAX_EXECUCAO = 30  # Em minutos
INDEX = "tp2_datasets.txt"

lista_bases = pd.read_csv(INDEX, sep='\t')

if sys.argv[1] != '':
    num_bases_p_ler = int(sys.argv[1])
else:
    num_bases_p_ler = len(lista_bases.index)

instancias = carregar_info(lista_bases["Dataset"].iloc[:num_bases_p_ler])

custo = {"bnb": [],
         "Christofides": [],
         "Twice-around-the-tree": []}

espaco = copy.deepcopy(custo)
t = copy.deepcopy(custo)

signal.signal(signal.SIGALRM, handler)

i = 0
for instancia in instancias:
    adj_matriz = nx.adjacency_matrix(instancia).todense()

    for algoritmo in ALGORITMOS_AVALIADOS:
        signal.alarm(60 * TEMPO_MAX_EXECUCAO)
        t0 = time.time()
        tracemalloc.start()

        print("> Processando base de dados {} usando {}...".format(i + 1, algoritmo))
        try:
            if algoritmo == "bnb":
                solucao = bnb.tsp(adj_matriz, instancia.number_of_nodes())
            elif algoritmo == "Christofides":
                solucao = aprox.algoritmo_de_christofides(instancia)
            else:
                solucao = aprox.twice_around_the_tree(instancia)

            custo[algoritmo].append(calcular_custo(solucao, adj_matriz))

        except TimeoutError:
            custo[algoritmo].append("NA")
            signal.alarm(0)

        print("> Finalizado computação para a base de dados {} usando {}!".format(i + 1, algoritmo))

        t[algoritmo].append(time.time() - t0)
        espaco[algoritmo].append(tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()
        signal.alarm(0)

    i += 1

tempos = pd.DataFrame(t)
espacos = pd.DataFrame(espaco)
custos = pd.DataFrame(custo)

custos.to_csv("custos.csv")
espacos.to_csv("espaco.csv")
tempos.to_csv("tempos.csv")
