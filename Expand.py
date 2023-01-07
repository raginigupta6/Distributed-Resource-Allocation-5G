import networkx as nx

# This function creates the expanded graph based on the demand and interference among the FAP nodes
def algo_two(G,D_G):

    # Duplicated graph H
    H = nx.Graph()
    D_H = {}

    # Create duplicate nodes along with the steady(s) and elaborated(e) node weights
    for u in G.nodes():

        # Create nodes s and e
        s = str(u) + 'S'
        e = str(u) + 'e'

        H.add_node(s)
        H.add_node(e)
        H.add_edge(s, e)

        # Add edge weights to duplicated graph
        D_H[s] = D_G[u][0]   ## Demand for steady node, Dmin
        D_H[e] = D_G[u][1] - D_G[u][0] ## Demand of elab node, Dmax-Dmin

    # Add duplicate edges
    for u in H.nodes():

        # List of neighbors for node 'u' in interference graph G
        L = G.neighbors(int(u[:-1]))

        for v in L:
            H.add_edge(str(u), str(v) + 'S')
            H.add_edge(str(u), str(v) + 'e')

    return H, D_H
