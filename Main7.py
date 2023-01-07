# -*- coding: utf-8 -*-
import networkx as nx
import random
import random
import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from copy import deepcopy
from Expand import *
from Allocate import *
from FAP_network import *
from min_color import *
from mistest import update_expanded_graph
import networkx as nx
from math import sin, cos, sqrt, atan2,radians
import pandas as pd
import matplotlib



def dist_new(p_1, p_2):

    # taken from
    # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    R = 6373.0

    lat1 = radians(p_1[0])
    lon1 = radians(p_1[1])
    lat2 = radians(p_2[0])
    lon2 = radians(p_2[1])
   


    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    # Convert from kilometer to meter
    return distance *1000
def find_iot_location(fog_location, x_min, y_min, x_max, y_max, R):

    while True:
        iot_x = random.uniform(x_min, x_max)
        iot_y = random.uniform(y_min, y_max)

        if dist_new(fog_location, (iot_x, iot_y)) <= R:
            return iot_x, iot_y
def area(fname):
    server = pd.read_excel(open(fname, 'rb'))
    server = server.values
    s = np.shape(server)

    x_min, x_max, y_min, y_max = None, None, None, None

    for i in range(s[0]):
        if x_min is None or server[i, 0] < x_min:
            x_min = server[i, 0]

        elif x_max is None or server[i, 0] > x_max:
            x_max = server[i, 0]

        if y_min is None or server[i, 1] < y_min:
            y_min = server[i, 1]

        elif y_max is None or server[i, 1] > y_max:
            y_max = server[i, 1]

    return x_min, y_min, x_max, y_max
# This function executes the main steps
def main_func(PRB,iD_max):
    ## Read data for server
    server=pd.read_excel(open('mydataserver.xlsx', 'rb'))


    server=server.values
    #print (server)
    ## Read data for IoT devices
    iotdata=pd.read_excel(open('mydata.xlsx', 'rb'))

    iotdata=iotdata.values
    #print("valuesssss", iotdata)
    #print (iotdata)


# Communication range (in meters, just an example)
    cR = 250

# Create dictionary of locations and nodes in fog network
    Dloc = {}
    i = 0
    G = nx.Graph()


    s = server.shape
    nF=s[0]
    ##print("mynf are",nF)
    for i in range(s[0]):
        Dloc[i]= (server[i,0],server[i,1])
        G.add_node(i)
       

# Add links between fog nodes
    for u in G.nodes():
        for v in G.nodes():
            if v <= u:
                continue

        # Calculate distance between two fog nodes
           
            if dist_new(Dloc[u], Dloc[v]) < cR:
                G.add_edge(u, v)
    #print ('Number of links in undirected fog graph:', len(G.edges()))

    #nx.draw(G)
    #plt.show()
    #print ('Number of links in undirected fog graph:', len(G.edges()))
    Dloc2 = {}
    mynewlist=[]
    i = 0
    s2= iotdata.shape
    for i in range(s2[0]):
        Dloc2[i]= (iotdata[i,0],iotdata[i,1])
    nI=s2[0]
    #print("my initial IoTs",nI)
    nP=PRB
    nP2=((nF)*(nF-1))
    #print("nC2",nC2)
    # IoT and FAP list
    IoTs = [i for i in range(nI)]
    #print("Initial list of IoTs***************", IoTs)
    FAPs = [i for i in range(nF)]
    new_dic={i: None for i in range(nI)}
    sum1=0
    # priority_fap: Dictionary of format IoT --> (Priority, Fap, IoT_Demand)
    priority_fap= {}
    #graph_density=0
    # IoT_color: Dictionary of format IoT --> Color (-1 suggesting color not assigned)
    IoT_color = {}
    count=0
    
    for j in range(len(Dloc2)):
        new_dic[j]=random.randint(0, (nF-1))
    #print("new_dictionary", new_dic)
    #for kk in range(len(Dloc2)):
     #   if (new_dic[kk]==None):
      #      mynewlist.append(kk)
       
    #print("count of IoTs that fall under FAP range",count)
    #print("new list of IoTs that have NONE FAP", mynewlist)
    fname = 'mydataserver.xlsx'
    x_min, y_min, x_max, y_max = area(fname)
    myx=[]
    myy=[]
    myiotx=[]
    myioty=[]
    print("Step 1")
    labels=['FAP','IoT']
    for j in range(len(Dloc)):
        myx.append(Dloc[j][0])
        myy.append(Dloc[j][1])
    for mk in range(len(Dloc2)):
        ## find the FAP that iot belongs to first
        fap_of_iot=new_dic[mk]
        fap_lat=Dloc[fap_of_iot][0]
        fap_long=Dloc[fap_of_iot][1]
        fog_location = (fap_lat, fap_long)
        # Find location of IoT near given fog location
        x_min, y_min, x_max, y_max = area(fname)
        iot_location = find_iot_location(fog_location, x_min, y_min, x_max, y_max, 250)
        
        print("Step 2")
        myiotx.append(iot_location[0])
        myioty.append(iot_location[1])
    plt.scatter(myx, myy, c='blue',alpha=1, label='FAP')
    plt.scatter(myiotx,myioty,c='red',alpha=0.2, label='IoT')
    plt.title('FAPs and IoTs geographic distribution')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.legend()
    plt.show()  
    
   
    for i in IoTs:
        priority_fap[i] = (random.choice([0, 1]), new_dic[i], random.randint(1, iD_max))
        sum1=sum1+priority_fap[i][0]
        IoT_color[i] = []

    R = [i for i in range(PRB)]

    # Create interference network of FAP nodes
    G, D = create_network_new(FAPs, priority_fap,G)
    edges=G.size()
    
    graph_density=mydensity(edges,float(nP2))
    #print ('D:',D)

    # Generate the expanded graph (Algo. 2)
    H, D_H = algo_two(G,D)
  
    L = {u:[] for u in H.nodes()}

    # Dictionary of MIS FAP nodes and the assigned color

    M = []

    H.remove_nodes_from([u for u in H.nodes() if D_H[u] == 0])
    while True:

       
        M, H, D_H = update_expanded_graph(H, D_H, M)
       
        #print ('######D_H:',D_H,H.nodes())
        if len(H) == 0:
            break
  
    MD,L,Rc, flag = assign_high(H, M, R,L)

    

    MD,L,Rc, flag = assign_low(MD, L, Rc, M)

  
   
    #Assign resources to IoT devices
    IoT_color = assign_to_IoTs(IoT_color,deepcopy(L),priority_fap)
    ##print("IoT color****", IoT_color)
    # Minimum number of colors used
    MC = find_min_colors(IoT_color)

    #print ('D:',D)
    #print ('L:',L)
    #print ('priority fap:',priority_fap)
    #print ('IoT_color:',IoT_color)
   # print ('Minimum number of colors used:',MC)
    #Matrix Y (FAP, IoT, Color)
    Y = create_Y(priority_fap, IoT_color, nF, nI, nP)
    count=0
  
    X, eta = create_X_eta(Y, nF, nI, nP, priority_fap)
    #return D,L,priority_fap,IoT_color,MC,eta,count
    return D,L,priority_fap,IoT_color,MC,eta,graph_density,sum1
   
def create_Y(priority_fap, IoT_color, nF, nI, nP):
    Y = [[ [0 for col in range(nP)] for col in range(nF)] for row in range(nI)]
    #print("my ni 2", nI)
    for i in IoT_color.keys():
        for c in IoT_color[i]:
            Y[i][priority_fap[i][1]][c] = 1

    return Y
def create_X_eta(Y, nF, nI, nP, Priority_FAP):
    X= lst = [[0 for col in range(nF)] for row in range(nI)]
    #print (assigned_array)
    eta = 0

    for i in range(nI):
        for k in range(nF):
            flag = False
            for n in range(nP):

                if Y[i][k][n] == 1:
                    flag = True
                    break

            if flag:
                X[i][k] = 1
                eta += 1
    return X,eta

#main_func(nI,nF,nP,iD_max)
#for i in range(100):
#    main_func(200,50,500,5,0.8)


####

Xlim = 200
Ylim = 200
range_dist=50

def mydensity(edges,nP2):

   
    graph_density=((2*edges)/float(nP2))
    return graph_density


density=0.8

'''
#nF_range = [i for i in range(4, 30, 10)]
nF=20
#nI_range = [i for i in range(50,450, 50)]
nI=100
nP_range = [p for p in range(20,110 ,20)]
range_dist_list = [k1 for k1 in range(20,1300, 20)]
#nP=20
marker = itertools.cycle(('d', '+', 'v', 'o', '*', '^' , '|', 'X'))
#Maximum IoT demand
iD_max = 1
iterate=30
#1. IoT vs. ETA for varying PRBS
for nP in  nP_range:
    #print ('I am at', nI)
    X = []
    Y = []
    x_v = []
    y_v = []
    #markers = ["**" , "," , "o" , "v" , "^" , "<", ">", "*"]
    #colors = ['r','g','b','c','m', 'y', 'k']
    for range_dist in range_dist_list:
        #print ("np:range_dist",nP,range_dist)
        #input("ente a key")
        #ETA_LIST = []
        #MIN_COLOR_LIST = []
       
        for i in range(iterate):
            #(eta, min_colors), D = main_f(nF, nI, nP)
            #A,D,IoT_color = main_f(nF, nI, nP, 5)
            D,L,priority_fap,IoT_color,MC,eta2,graph_dens,mysum3= main_func(nI,nF,nP,iD_max,density,Xlim, Ylim, range_dist)
            #print ('iterate',i)
            x_v.append(graph_dens)
            y_v.append(eta2)
            #print ("IoT_color",IoT_color)

        X.append(np.mean(x_v))
        Y.append(np.mean(y_v))

    plt.plot(X,Y,marker=marker.next(),markersize=6,label = '#PRBs: ' + str(nP))
print (" Graph Density is", graph_dens)
plt.legend()
plt.grid()
#plt.title('Eta vs Graph Density, #FAP=20, # IoTs=100')
plt.xlim([0.08,1.0])
plt.ylim([20,102])
plt.xlabel('Graph Density')
plt.ylabel(u'η (Y)')
plt.show()
'''



#nF_range = [i for i in range(4, 30, 10)]
#FAP=20
nF=50
#nI_range = [i for i in range(100,600, 100)]
#nI=500
nP_range = [p for p in range(10,110 , 10)]
#nP=30
#nI_iterations=[i for i in range (1,11,1)]
marker = itertools.cycle(('d', '+', 'v', 'x', 'o', '^' , '|', 'X'))
#colors=itertools.cycle(('blue','green','red','cyan','magenta','yellow','black'))
lcolors=['blue','green','red','cyan','magenta','yellow','black']
#Maximum IoT demand
iD_max_range = [j for j in range(1,6,1)]
iterate=2
my_sum=0
my=0

#D,L,priority_fap,IoT_color,MC,eta2,graph_dens,my_sum= main_func(100,1)
#print ("My eta is", eta2)
#D,L,priority_fap,IoT_color,MC,eta2,graph_dens,my_sum= main_func(100,5)
#################################################################################################

#1. IoT vs. ETA for varying PRBS
for iD_max in  iD_max_range:
    #print ('I am at', nI)
    X = []
    Y = []
    Z=[]
    x_v = []
    y_v = []
    z_v=[]
    #markers = ["**" , "," , "o" , "v" , "^" , "<", ">", "*"]
    #colors = ['r','g','b','c','m', 'y', 'k']
    #print("IoT",nI)
    for nP in nP_range:
        #print ("np:ni",nP,nI)
        #input("ente a key")
        #ETA_LIST = []
        #MIN_COLOR_LIST = []
       
        for i in range(iterate):
            #(eta, min_colors), D = main_f(nF, nI, nP)
            #A,D,IoT_color = main_f(nF, nI, nP, 5)
            D,L,priority_fap,IoT_color,MC,eta2,graph_dens,my_sum= main_func(nP,iD_max)
           
            #print ('iterate',i)
            y_v.append(eta2)
            #z_v.append(my_sum)
            #print ("IoT_color",IoT_color)

        X.append(nP)
        Y.append(np.mean(y_v))
        print ('X', nP)
        print ("Y", np.mean(y_v))
       
        #Z.append(np.mean(z_v))
    m=marker.next()
    col=lcolors[my]
    plt.plot(X,Y,marker=m,color=col,markersize=6,label = '#IoT Demand: ' + str(iD_max))
    #plt.plot(X,Z,marker=m,linestyle='dashed',label = '#IoTs: ' + str(nI))
    #plt.plot(X,Z,marker=m,linestyle='dotted', color=col,dash_joinstyle='miter', label= u'η(Y) High Priority IoT:' + str(nI))
    my=my+1
##print (" Graph Density is", graph_dens)
plt.legend()
plt.legend(loc='upper left',ncol=2)
##plt.legend(loc='lower left')
#plt.title('Eta vs Number of PRBs')
plt.grid()
plt.xlabel('Number of PRBs')
plt.xlim([10,100])
plt.ylim([100,1250])
plt.ylabel(u'η (Y)')
plt.show()

