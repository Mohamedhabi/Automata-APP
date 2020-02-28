#(alphabet, état initial, états finaux et l’ensemble des transitions)
class Automate:        
    # init method or constructor  
    Automate_type= "Généralisé non déterministe" 
    def __init__(self, alphabet,etats,etat_initial,etats_finaux,transitions):  
        self.alphabet = alphabet
        self.etats = etats
        self.etat_initial = etat_initial
        self.etats_finaux = etats_finaux  
        self.transitions = transitions
          
    def drow_automate(self): 
        from graphviz import Digraph
        f = Digraph('finite_state_machine', filename='automate.gv')
        f.attr(rankdir='LR', size='8,5')
        #shape de l'etat initiale
        if self.etat_initial in self.etats_finaux:
            f.attr('node', shape='doubleoctagon')
        else:
            f.attr('node', shape='octagon')
        f.node(self.etat_initial)
        #shape des l'etats finaux
        f.attr('node', shape='doublecircle')
        for node in self.etats_finaux:
            f.node(node)
        #shape des autres états
        f.attr('node', shape='circle')
        for node in self.etats:
            f.node(node)
        #les transitions    
        for transition in self.transitions:
            for destination in self.transitions[transition]:
                f.edge(transition[0], destination, label=transition[1])
        f.view()
    
 

'''
from networkx.drawing.nx_agraph import write_dot
        import networkx as nx
        import pylab
        import pygraphviz
        import matplotlib as mpl
        import matplotlib.pyplot as plt

        
        G = nx.DiGraph(directed=True)

        for transition in self.transitions:
            G.add_edge(transition[0], self.transitions[transition], label=transition[1])
        print(G.edges)
        #write_dot(G,'graph.dot')

        #edge_labels=dict([((u,v,),d['label'])for u,v,d in G.edges(data=True)])
        pos=nx.spring_layout(G)
        values =list(map(self.color_node,G.nodes()))
        sizes =list(map(self.shape_node,G.nodes()))
        #nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
        nx.draw(G,pos, with_labels=True, node_color = values ,node_size=sizes)
        #pylab.show() 
        plt.show() 
        
           def color_node(self,node):
        if node in self.etats_finaux:
            return "red"
        else:
            return "g"
        
    def shape_node(self,node):
        if node == self.etat_initial:
            return 2500
        else:
            return 1000
'''