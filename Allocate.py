# This function check if the resource 'c' has been used by a neighbor
'''
def isUsed(Z,L,c):

    for u in Z:
        if c in L[u]:
            return True

    return False

# This function generates the sum of resources assigned to all the FAPs so far
def check_assigned(L,S):
    return sum([len(L[u]) for u in S])

# This function assigns resources to FAPs; mode = 0 for high priority and mode = 1 for low priority
def assign(H, D_H, RC, L, M, NL, mode):

    # List of nodes to be scanned during resource allocation
    if mode == 0:
        S = sorted([u for u in H.nodes() if 'S' in u])
    else:
        S = sorted([u for u in H.nodes() if 'e' in u])

    ##print (S)

    # Total Demand of the FAP network, total demand for high or low prioority nodes
    TD = sum([D_H[u] for u in S])

    while check_assigned(L, S) < TD: ## checking whether total demand for HP/LP is met or not

        # Assign resources first to nodes belonging to MIS
        if sum([D_H[v] - len(L[v]) for v in S if v in M]) > 0:

            try:
                current_resource = RC.pop(0)
            except:
                #print ('Too few colors!')
                return L

            for u in [v for v in S if v in M]:
                if len(L[u]) < D_H[u]: ## allocate if demand for u not met
                    L[u].append(current_resource)

        # Assign resources to other nodes
        for u in [u for u in S if u not in M]:
            if len(L[u]) < D_H[u]:

                while True:
                    try:
                        current_resource = RC.pop(0)
                    except:
                        #print('Too few colors!')
                        return L

                        # Check if resource has been used by a neighbor node in the past
                    if not isUsed(NL[u],L,current_resource):
                        break

                L[u].append(current_resource)

    return L
'''

def assign_high(H, M, Rc, L):


    MD = {}
    for m in M:
        MD[tuple(m)] = []
        
    for m in M: ## ['1S','2e']--> red,[],

        subset = [u for u in list(m) if 'S' in u] ## ['1S']
        
        if len(subset) == 0:
            continue

        # Pop one color from resource list
        try:
            c = Rc.pop(0)
        except:
            #print ('Too few colors for high priority')
            return MD,L,Rc,0
            
        for u in subset:
            L[u].append(c) ## L is the list of colors assigned to each FAP

        MD[tuple(m)].append(c)

        #print ('m:',m)
        #print ('subset:',subset)
        #print ('MD:',MD)
        #print ('L:',L)
        #print
        #input ('')
        
    return MD,L,Rc,1

def assign_low(MD, L, Rc, M): ## M is the list of MIS

    for m in M:

        subset_e = [u for u in list(m) if 'e' in u]
        subset_S = [u for u in list(m) if 'S' in u]

        if len(subset_e) == 0:
            continue
        
        ##print ("my current subset is:",list(m),subset_e)
        # If all the elements are 'elaborated' (e), pop a new color from 'Rc'
        if len(subset_S) == 0: ##['1e,'2e','2e']
            #print ('Remaining color list from if:',Rc)
            # Pop one color from resource list
            try:
                c = Rc.pop(0)
                #print ('Color popped',c)
            except:
                #print ('Too few colors for low priority')
                return MD,L,Rc,0

            for u in subset_e:
                MD[tuple(m)].append(c)
                ##print("color to given subset IF",c)
                L[u].append(c)

        elif len(MD[tuple(m)]) == 0:
            #print ('Remaining color list from elif:',Rc)
            return MD, L, Rc, 1

        # If some of the elements are 'steady' (s), reuse assigned color.
        else:
            #print("my MD is",MD, m,MD[tuple(m)])
            #print ('Remaining color list from else:',Rc)
            c = MD[tuple(m)][0]
            #print("Color assigned in else", c)
            #print ("MD tuple's color",m,",",MD[tuple(m)])
            for u in subset_e:
                MD[tuple(m)].append(c)
                ##print("color to given subset",c)

                L[u].append(c)

            
        #print ('m:',m)
        #print ('MD:',MD)
        #print ('L:',L)
        #print
        #input ('')

    return MD, L, Rc, 1

#    return  None
# This function assigns resources to IoTs
def assign_to_IoTs(IoT_color,L,priority_fap):
    #print ("inside IoT assignment")
    # priority_fap: Dictionary of format IoT --> (Priority, Fap, IoT_Demand)
    ## L  is the list of colors allocated to Steady and Elaborated FAPs
    for i in priority_fap.keys():

        priority = priority_fap[i][0]
        owner_fap = priority_fap[i][1]
        demand = priority_fap[i][2]

        if priority == 1:
            logical_fap = str(owner_fap) + 'S'
        else:
            logical_fap = str(owner_fap) + 'e'

        if len(L[logical_fap]) > 0:
            choose_colors = L[logical_fap][:demand]
            ## updating L list with the colors already used
            L[logical_fap] = [v for v in L[logical_fap] if v not in choose_colors]

            IoT_color[i].extend(choose_colors)
    
    return IoT_color
