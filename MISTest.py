import random

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def update_expanded_graph(H, D_H, M):

    # Set of maximal independent nodes
    m = nx.maximal_independent_set(H) ## ['1S','2e']
    # Reduce the demand of the chosen nodes (in M) by 1

    for u in m:
        if D_H[u] > 0:
            D_H[u] = D_H[u] - 1

    H.remove_nodes_from([u for u in m if D_H[u] == 0])

    M.append(m)
    return M, H, D_H


'''
nF=5
R=0.65
G = nx.Graph()
#D = {f:[0,0] for f in FAPs}
FAPs = [i for i in range(nF)]
D_H=  {f:[0] for f in FAPs}
    
G.add_nodes_from(FAPs)
    
for f1 in FAPs:
    for f2 in FAPs:
        if f2<=f1:
            continue
        if random.random()<R:
            G.add_edge(f1,f2)
for i in FAPs:
    D_H[i]=random.randint(1,3)
print("D",D_H)

while True:
    #number of FAPs
    M, H, D_H = update_expanded_graph(G, D_H)
    print("My current MIS",M)
    # Allocate resources to nodes in M based on (1) high priority and (2) low priority
    nx.draw(H)
    plt.show()
    if nx.is_empty(H):
        break

'''
