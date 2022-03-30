# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 13:49:10 2022

@author: email
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:35:53 2022

@author: email
"""

import sys # Library for INT_MAX

import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import distance
import time 
start_time = time.time()

def prepareGraph(attrs):
    
    #Add nodes
    G = nx.Graph() #Create a graph object called G
    for node in attrs.keys():
        G.add_node(node)
        nx.set_node_attributes(G, attrs)
    a=0.1 #weight
    key_list=list(attrs.keys())
    for i in key_list:
        for j in key_list:
            #calculate distance between nodes to account for it when
            #calculating weight
            dst=distance.euclidean(G.nodes[i]["coordinates"], G.nodes[j]["coordinates"])
            if i!=j:
                if G.nodes[i]["obj_type"]=='House' and G.nodes[j]["obj_type"]=='House'\
                    or G.nodes[i]["obj_type"]=='House' and G.nodes[j]["obj_type"]=='Mall'\
                    or G.nodes[j]["obj_type"]=='House' and G.nodes[i]["obj_type"]=='Mall':
                    G.add_edge(key_list[i],key_list[j],weight=(1-a)*dst, distance=dst, road_type='Local', color='black')
                    
                elif G.nodes[i]["obj_type"]=='Mall' and G.nodes[j]["obj_type"]=='Center'\
                    or G.nodes[j]["obj_type"]=='Mall' and G.nodes[i]["obj_type"]=='Center':
                    G.add_edge(key_list[i],key_list[j],weight=a*dst, distance=dst, road_type='Express', color='r')
    print(G.edges)
    return nx.adjacency_matrix(G).todense(), G



class Graph(): 
    def __init__(self, vertices, attrs):
        self.V = vertices
        self.graph, self.graphNX =prepareGraph(attrs)
        #self.graph is a matrix representation
        #self.graphNX contains all the info on edges and nodes
    

    #A function to print the constructed MST stored in parent[]
    def printMST(self, parent):
        MSTedges=[]
        MSTweights=[]
        loc_len=0
        exp_len=0
        print ("Edge \tWeight \t\t\t\tRoad Type")
        for i in range(1, self.V):
            print (parent[i], "-", i, "\t", \
                   self.graph.tolist()[i][parent[i]],
                   self.graphNX[parent[i]][i]['road_type'])
            MSTedges.append((parent[i],i))
            MSTweights.append(self.graph.tolist()[i][parent[i]])
            if self.graphNX[parent[i]][i]['road_type']=='Local':
                loc_len+=self.graphNX[parent[i]][i]['distance']
            else:
                exp_len+=self.graphNX[parent[i]][i]['distance']
            
        print('Total lenght of Local and Express roads is {} and {}, \
              respectively'.format(loc_len, exp_len))
        return MSTedges, MSTweights
    
            
    def plotMST(self, parent):
        #plot nodes
        MSTedges, MSTweights=self.printMST(parent)
        pos = nx.kamada_kawai_layout(self.graphNX )
        #pos = nx.spring_layout(self.graphNX)
        #pos=nx.circular_layout(self.graphNX) 
        nx.draw_networkx_nodes(self.graphNX,pos,node_color='#BBE3DF',\
                               node_size=500)
     
        #3.add labels to the nodes
        labels = {}
        for node_name in range(self.V):
                labels[(node_name)]\
                    =str(self.graphNX.nodes[node_name]["obj_type"])\
                        +str(node_name)       
        nx.draw_networkx_labels(self.graphNX,pos,labels,font_size=10)
     
     
        #Plot the edges  one by one
       
        
        for edge in MSTedges:
      
            width = self.graphNX[edge[0]][edge[1]]['weight']*3

            nx.draw_networkx_edges(self.graphNX,pos,\
                                   edgelist=[edge],width=width,\
                                       edge_color=\
                                    self.graphNX[edge[0]][edge[1]]['color'])
            
     
        #Plot the graph
        plt.axis('off')
        plt.title('Town Plan')
        plt.savefig("town_plan.png") 
        plt.show() 
      

    #find the vertex with
    #minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minKey(self, key, mstSet):

        # Initialize min value
        min = sys.maxsize
        
        for v in range(self.V):
            print('Within minkey: key[v], min, mstSet[v]',  key[v], min, mstSet[v])

            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v
                #print('mi',min_index)
        return min_index

    # Function to construct and print MST for a graph
    # represented using adjacency matrix representation
    def primMST(self):

        # Key values used to pick minimum weight edge in cut
        key = [sys.maxsize] * self.V
        parent = [None] * self.V # Array to store constructed MST
        # Make key 0 so that this vertex is picked as first vertex
        key[0] = 0
        mstSet = [False] * self.V

        parent[0] = -1 # First node is always the root of

        for count in range(self.V):

            #u is the minimum distance vertex from
            #the set of vertices not yet processed.
            u = self.minKey(key, mstSet)
            

            #put the minimum distance vertex in
            #the shortest path tree
            mstSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                # graph[u][v] is non zero only for adjacent vertices of v
                # mstSet[v] is false for vertices not yet included in MST
                # Update the key only if graph[u][v] is smaller than key[v]
                if self.graph.tolist()[u][v] > 0 and mstSet[v] == False and key[v] > self.graph.tolist()[u][v]:
                       key[v] = self.graph.tolist()[u][v]
                       parent[v] = u
        self.printMST(parent)
        self.plotMST(parent)
        return  time.time() - start_time
    


#----------DRIVER-------------

attrs = {0: {"obj_type": 'House', "coordinates": (1,2)},
        1: {"obj_type": 'Mall', "coordinates": (2,3)},
        2: {"obj_type": 'House', "coordinates": (1,3)},
        3: {"obj_type": 'House', "coordinates": (1,4)},
        4: {"obj_type": 'Mall', "coordinates": (3,3)},
        5: {"obj_type": 'House', "coordinates": (2,4)},
        6: {"obj_type": 'Center', "coordinates": (3,5)},
        7: {"obj_type": 'House', "coordinates": (1,2)},
        8: {"obj_type": 'Mall', "coordinates": (5,3)},
        9: {"obj_type": 'House', "coordinates": (3,7)},
        10: {"obj_type": 'House', "coordinates": (1,1)},
        11: {"obj_type": 'Mall', "coordinates": (1,5)},
        12: {"obj_type": 'House', "coordinates": (2,2)},
        13: {"obj_type": 'House', "coordinates": (4,4)}}

g = Graph(len(attrs), attrs).primMST();
print("--- %s seconds ---" % (time.time() - start_time))

#--------------TIME-------------
#generate datasets of various times and measure how well your model scales.

# dataset generator
# orders=[5,10,20,50,100,150,200, 300] #500,1000,2000,5000,10000,50000,100000,1000000
# orders_and_times=list() #list of tupples w number of orders and times of execution
# for i in orders:
#     print('Currently obtaining time for the graph with number of nodes',i)
#     dic=dict()
#     dic[0]={"obj_type": 'Center', "coordinates": (random.randint(0, 15),random.randint(0, 15))}
#     for j in range(1,i):
#         dic[j]={'obj_type':random.choice(['House', 'Mall']),  "coordinates": (random.randint(0, 15),random.randint(0, 15))}
#     t=Graph(len(dic),dic).primMST()
#     orders_and_times.append((i,t))
# plt.plot(*zip(*orders_and_times))
# plt.show()



