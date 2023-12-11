import numpy as np

def calcular_estimativa(grafo, n, caminho):
    custo = 0

    j = 0
    for v in range(n):
        i = list(np.argsort(grafo[v], axis=0))
        i.remove(v)

        if v in caminho and caminho != [0]:
            # Se v não estiver nem no final nem no início de *caminho*
            if len(caminho) - 1 > j > 0:
                # aresta do vértice anterior no caminho ao atual + aresta do vértice atual até o próximo
                custo += grafo[caminho[j], caminho[j - 1]] + grafo[caminho[j], caminho[j + 1]]
            else:
                if grafo[v, i[0]] == grafo[caminho[j], caminho[(j + 1) % len(caminho)]]:
                    custo += grafo[v, i[0]] + grafo[v, i[1]]
                else:
                    custo += grafo[v, i[0]] + grafo[caminho[j], caminho[(j + 1) % len(caminho)]]

            j += 1
        else:
            custo += grafo[v, i[0]] + grafo[v, i[1]]

    return np.ceil(custo / 2)


def tsp(grafo, n):
    import heapq

    # Estimativa = 0 | Nível = 1 | Custo = 2 | Solução = 3
    raiz = (calcular_estimativa(grafo, n, [0]), 0, 0, [0])

    melhores_caminhos = []
    heapq.heappush(melhores_caminhos, raiz)

    # O menor custo real de uma solução completa encontrado até o momento.
    min_custo_encontrado = np.infty
    sol = []

    while melhores_caminhos:
        no = heapq.heappop(melhores_caminhos)

        if no[1] == n:
            if min_custo_encontrado > no[2]:
                min_custo_encontrado = no[2]
                sol = no[3]

        # Vale a pena explorar esse ramo?
        elif no[0] < min_custo_encontrado:

            # Não cheguei em um nó folha?
            if no[1] < n - 1:
                for k in range(1, n):
                    estimativa = calcular_estimativa(grafo, n, no[3] + [k])

                    # O nó já foi visitado?
                    cond1 = k not in no[3]

                    # Existe uma aresta ligando os dois nós?
                    cond2 = grafo[no[3][-1]][k] != 0

                    if cond1 and cond2 and estimativa < min_custo_encontrado:
                        novo_no = (estimativa, no[1] + 1, no[2] + grafo[no[3][-1]][k], no[3] + [k])
                        heapq.heappush(melhores_caminhos, novo_no)

            # Existe aresta ligando o último nó da solução com o primeiro? + Todos os nós do grafo estão na solução encontrada?
            elif grafo[no[3][-1]][0] != 0 and calcular_estimativa(grafo, n, no[3] + [0]) < min_custo_encontrado and np.sum(no[3]) == np.sum(range(n)):
                estimativa = calcular_estimativa(grafo, n, no[3] + [0])
                novo_no = (estimativa, no[1] + 1, no[2] + grafo[no[3][-1]][0], no[3] + [0])
                heapq.heappush(melhores_caminhos, novo_no)
    return sol
