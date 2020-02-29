#(alphabet, état initial, états finaux et l’ensemble des transitions)
class Automate:        
    # init method or constructor  
    Automate_type= "Généralisé non déterministe" 
    def __init__(self, alphabet,etats,etat_initial,etats_finaux,transitions):  
        self.Acc={etat_initial}
        self.Coacc=[]
        self.alphabet = alphabet
        self.etats = etats
        self.etat_initial = etat_initial
        self.etats_finaux = etats_finaux  
        self.transitions = transitions
        self.etat_motsdetransitions={}#dictionaire exemple:{"s0":{"a","b","ab"}} pour savoir les mot qu'on peut lire apartir d'un état
        for transition in transitions:
            if transition[0] in self.etat_motsdetransitions:
                self.etat_motsdetransitions[transition[0]].add(transition[1])
            else:
                self.etat_motsdetransitions[transition[0]]={transition[1]}            
          
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

        
    def liste_Acc(self,S0):
        for [S0,x] in self.transitions:
            for succ in self.transitions[S0,x]:
                if(not (succ in self.Acc)):
                    self.Acc.add(succ)
                    self.liste_Acc(succ)

    def supp_nAcc(self):
        trans=self.transitions.copy()
        for S in self.etats:
            if (not (S in self.Acc)) :
                for x in self.etat_motsdetransitions[S]:
                    del trans[S,x]
                del self.etat_motsdetransitions[S]
                if (S in self.etats_finaux):
                    self.etats_finaux.remove(S)
        self.transitions=trans.copy()
        self.etats=self.Acc.copy()
        self.Coacc=self.etats_finaux.copy()
        #s'il n ya plus d'etats finaux
        if (not self.etats_finaux):
            print("l'automate n'a plus d'etats finaux")
    


    #suppression des etats non coaccessibles (qui dont deja accessibles)
    def predecesseur(self,S0): #methode pour lobtention des predecesseurs d'un sommet
        Pred={}
        for [S,x] in self.transitions:
            if (S0 in self.transitions[S,x]):
                if (S in Pred):
                    Pred[S].add(x)
                else:
                    Pred[S]={x}
        return Pred

    #obtention de la liste des etats coaccessibles
    
    def liste_Coacc(self,sf):
        pre=self.predecesseur(sf)
        for P in pre:
            if (P not in self.Coacc):
                self.Coacc.append(P)
                self.liste_Coacc(P)

    #suppression des etats non coaccessibles
    def supp_nCoa(self):
        trans=self.transitions.copy()
        etat_MDT=self.etat_motsdetransitions.copy()
        for sf in self.etats_finaux: #obtention de tous les etats coacc
            self.liste_Coacc(sf)
        for [S,x] in self.transitions:
            for P in self.transitions[S,x]:
                if (P not in self.Coacc):
                    del trans[S,x]
                    etat_MDT[S].remove(x)
                    if (not etat_MDT[S]):
                        del etat_MDT[S]
        self.etats=self.Coacc.copy()
        self.transitions=trans.copy()
        self.etat_motsdetransitions=etat_MDT.copy()
        if( not (self.etat_initial in self.Coacc)):
            print("l'automate n'a plus d'etat initial")
        
                

