import random
import networkx as nx
import matplotlib.pyplot as plt

from scipy.spatial.distance import euclidean
def position_nodes(FAPs, Xlim, Ylim):

    C = {}
    for f in FAPs:
        C[f] = (random.randint(0,Xlim), random.randint(0,Ylim))

    return C
    
def create_network(FAPs,priority_fap,R, Xlim, Ylim, range_dist):
    
    # priority_fap: Dictionary of format IoT --> (Priority, Fap, IoT_Demand)

    G = nx.Graph()
    D = {f:[0,0] for f in FAPs}
    G.add_nodes_from(FAPs)

    # Decide coordinates for fog nodes 
    C = position_nodes(FAPs, Xlim, Ylim)

    for f1 in FAPs:
        for f2 in FAPs:
            if f2 <= f1:
                continue
            
            #toss = random.choice([False, True])
            #if toss:
            #r = random.random()
            #print ('why me',r,R)
            
            ## R is the graph density we want to set, called from main
            # if  random.random() < R:
                # G.add_edge(f1, f2)

            #Assign links between distance between nodes
            if euclidean(C[f1], C[f2]) <= range_dist:
                G.add_edge(f1, f2)
            
    # Assign the demand for FAPs based on priority of each IoT within it
    for i in priority_fap:

        priority = priority_fap[i][0]
        owner_fap = priority_fap[i][1]
        demand = priority_fap[i][2]

        if priority == 1:
            #D-> [Dmin,Dmax]            # Dmin , #Dmax
            D[owner_fap][0] += demand #Dmin
            D[owner_fap][1] += demand #Dmax
            
        else:
            D[owner_fap][1] += demand
    
    #nx.draw(G)
    #lt.show()
    
    return G, D

def create_network_new(FAPs,priority_fap,G):
    
    # priority_fap: Dictionary of format IoT --> (Priority, Fap, IoT_Demand)
    '''
    G = nx.Graph()
    D = {f:[0,0] for f in FAPs}
    G.add_nodes_from(FAPs)

    # Decide coordinates for fog nodes 
    C = position_nodes(FAPs, Xlim, Ylim)

    for f1 in FAPs:
        for f2 in FAPs:
            if f2 <= f1:
                continue
            
            #toss = random.choice([False, True])
            #if toss:
            #r = random.random()
            #print ('why me',r,R)
            
            ## R is the graph density we want to set, called from main
            # if  random.random() < R:
                # G.add_edge(f1, f2)

            #Assign links between distance between nodes
            if euclidean(C[f1], C[f2]) <= range_dist:
                G.add_edge(f1, f2)
    '''       
    # Assign the demand for FAPs based on priority of each IoT within it
    D = {f:[0,0] for f in FAPs}
    print ("My len", len(FAPs))
    for i in priority_fap:

        priority = priority_fap[i][0]
        owner_fap = priority_fap[i][1]
        demand = priority_fap[i][2]

        if priority == 1:
            #D-> [Dmin,Dmax]            # Dmin , #Dmax
            D[owner_fap][0] += demand #Dmin
            D[owner_fap][1] += demand #Dmax
            
        else:
            D[owner_fap][1] += demand
    
    #nx.draw(G)
    #lt.show()
    
    return G, D

