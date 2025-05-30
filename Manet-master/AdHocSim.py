import math
import sys

import networkx as nx
import matplotlib.pyplot as plt





commands = open("commands", "r")
"""ps = input(sys.argv[1])"""  #because i didn't finish this
nodes=[]

print('********************************')
print('AD-HOC NETWORK SIMULATOR - BEGIN')
print('********************************')
print('SIMULATION TIME: '+ str().zfill(2) + ':' + str().zfill(2) + ':' + str().zfill(2))

neigDict={}

def route(dict,x,y,routes=None):
    if routes is None:
        routes = [x]
    if x == y:
        c=0
        for a in range(1,len(routes),1):
            distxx=(Dict[routes[a-1]])[0]
            distyx=(Dict[routes[a-1]])[1]
            distxnext=(Dict[routes[a]])[0]
            distynext=(Dict[routes[a]])[1]
            dist = math.sqrt(((float(distxnext)-float(distxx))**2)+((float(distynext)-float(distyx))**2))
            cost=dist/float(Batt[routes[a]])
            c=c+cost
        Costs.append(c)
        yield routes
    for next in dict[x] - set(routes):
        yield from route(dict,next,y,routes+[next])


def send():
    neighborinfo=[]
    for i in nodes:         #for readable neighborhood information
        A= []
        x1 = int(i[1][0])+int(i[2][0])
        x2 = int(i[1][0])-int(i[2][1])
        y1 = int(i[1][1])+int(i[2][2])
        y2 = int(i[1][1])-int(i[2][3])
        A.append(i[0])
        A.append(x1)
        A.append(x2)
        A.append(y1)
        A.append(y2)
        neighborinfo.append(A)
    D=[]
    for i in range(len(neighborinfo)):
        A=[]
        A.append(neighborinfo[i][0])
        for j in range(len(neighborinfo)):
            if j==i:
                continue
            if int(nodes[j][1][0])<=neighborinfo[i][1] and int(nodes[j][1][0])>=neighborinfo[i][2] and int(nodes[j][1][1])<=neighborinfo[i][3] and int(nodes[j][1][1])>=neighborinfo[i][4]:
                A.append(nodes[j][0])
        D.append(A)
    for i in D:
        neigDict[i[0]]=i[1:]
    for i in neigDict.keys():
        neigDict[i]=set(neigDict[i])
    print('\tNODES & THEIR NEIGHBORS:', end= " ")
    for i in neigDict.keys():
        g=""
        for a in neigDict[i]:
            g=g+a+", "
        print(i,"->",g.rstrip(", "),"|", end= " ")
    print(" ")

def repeat():
    send()
    length = len(sorted(list(route(neigDict,firstnode,secondnode))))
    R =list(route(neigDict,firstnode,secondnode))
    c=0
    selectednumb=0
    selectedpath=[]
    if len(R)==0:
        print('\tNO ROUTE FROM ' + str(firstnode)+ ' TO ' + str(secondnode) + ' FOUND.')
        return None
    print("\t"+ str(length) +' ROUTE(S) FOUND:')

    for i in R:
        c+=1
        print('\tROUTE ',c,': ' + " -> ".join(i) , "\t COST: {0:.4f}".format(Costs[c-1]))
        if Costs[c-1] == min(Costs):
            selectednumb=str(c)
            selectedpath.append(i)

    print("\tSELECTED ROUTE (ROUTE " + str(selectednumb) + "): " + " -> ".join(min(selectedpath)))
    """print("\tPACKET " + + " HAS BEEN SENT")"""

def crnode():
    L=[]
    L.append(spltd[2])
    L.append(spltd[3].split(";"))
    L.append(spltd[4].split(";"))
    nodes.append(L)
    print("\tCOMMAND *CRNODE*: New node " + spltd[2] + " is created")
    Dict[L[0]]=[L[1][0],L[1][1]]
    Batt[L[0]]=spltd[5].rstrip("\n")

Batt={}
Dict={}
x=0
for aline in commands.readlines():
    spltd = aline.split("\t")

    if spltd[1] == "CRNODE"and x==0:
        crnode()
    elif spltd[1] == "CRNODE"and x!=0:
        crnode()
        Costs=[]
        repeat()
    elif spltd[1]=="SEND":
        """ds=float(spltd[4].rstrip("\n"))
        np=(float(ds)//float(ps))+1"""
        print("\tCOMMAND *SEND*: Data is ready to send from " + spltd[2] + " to " + spltd[3] )
        firstnode = spltd[2]
        secondnode = spltd[3]
        x=1
        Costs=[]
        repeat()
    elif spltd[1]== "CHBTTRY":
        Batt[spltd[2]]=spltd[3]
        print("\tCOMMAND *CHBTTRY*: Battery level of node " + str(spltd[2]) + " is changed to " + str(spltd[3].rstrip("\n")) )
        x=1
        Costs=[]
        repeat()
    elif spltd[1]=="MOVE":
        for i in nodes:
            if spltd[2] in i:
                i[1]=(spltd[3].rstrip("\n")).split(";")
        Dict[spltd[2]]=(spltd[3].rstrip("\n")).split(";")

        print("\tCOMMAND *MOVE*: The location of node " + spltd[2].rstrip("\n") + " is changed")
        x=1
        Costs=[]
        repeat()
    elif spltd[1]=="RMNODE":
        print("\tCOMMAND *RMNODE*: Node " + spltd[2].rstrip("\n") + " is removed")
        x=1
        for i in nodes:
            if (spltd[2].rstrip("\n")) in i:
                nodes.remove(i)
        del Dict[spltd[2].rstrip("\n")]
        del neigDict[spltd[2].rstrip("\n")]

        Costs=[]
        repeat()
    else:
        break




# ... (your existing code)

# Add these lines at the end of your code

# Create a graph
G = nx.Graph()

# Add nodes to the graph with location and battery level attributes
for node in nodes:
    node_id = node[0]
    location = (int(node[1][0]), int(node[1][1]))
    battery_level = float(Batt[node_id])

    # Add node to the graph with attributes
    G.add_node(node_id, pos=location, battery=battery_level)

# Add edges based on the communication dictionary (neigDict)
for source, targets in neigDict.items():
    for target in targets:
        G.add_edge(source, target)

# Extract node positions, battery levels, and labels for plotting
node_positions = nx.get_node_attributes(G, 'pos')
node_batteries = nx.get_node_attributes(G, 'battery')
node_labels = {node: f"{node}\nBattery: {battery:.2f}\nPosition: {pos}" for node, pos, battery in zip(node_batteries.keys(), node_positions.values(), node_batteries.values())}

# Plot the graph with nodes colored by battery level
node_colors = [battery / max(node_batteries.values()) for battery in node_batteries.values()]

# You can customize the node size based on other factors if needed
node_sizes = [500 * battery / max(node_batteries.values()) for battery in node_batteries.values()]

# Draw the graph with labels
nx.draw(G, pos=node_positions, with_labels=False, font_weight='bold', node_size=node_sizes,
        node_color=node_colors, cmap=plt.cm.Blues, font_size=8, edge_color='gray', width=0.5)

# Add node labels
nx.draw_networkx_labels(G, pos=node_positions, labels=node_labels, font_color='black', font_size=8, verticalalignment='bottom')

# Save the plot as a PNG file
plt.savefig('network_graph.png')

# Show the plot (optional)
plt.show()

print('******************************')
print('AD-HOC NETWORK SIMULATOR - END')
print('******************************')
