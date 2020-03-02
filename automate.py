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
        self.etat_motsdetransitions={}#dictionaire exemple:{"s0":{"a","b","ab"}} pour savoir les mot qu'on peut lire apartir d'un état
        for transition in transitions:
            if transition[0] in self.etat_motsdetransitions:
                self.etat_motsdetransitions[transition[0]].add(transition[1])
            else:
                self.etat_motsdetransitions[transition[0]]={transition[1]}            
          
    def drow_automate(self,filename='automate.gv'):
        err=0
        try:             
            from graphviz import Digraph
        except Exception:
            print("vous devez installer la bibliothèque python 'graphviz'")
            err=1
        if not err:
            f = Digraph(filename, filename)
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

          
    #ajouter l'elsemble (set_) a l'element dictio[key]
    def add_set_to_dict(self,dictio,key,set_):
        if key in dictio:
            dictio[key]=dictio[key].union(set_)
        else:
            dictio[key]=set_
    
    #elimination des epsilone dans l'automate
    def partiel_get_simple(self):
        for s in self.etat_motsdetransitions:
            if "#" in self.etat_motsdetransitions[s]:
                print(s)
                for tr in self.transitions[s,"#"]:
                    succeurs=self.get_sucesseur(s,tr)
                    print(succeurs)
                    self.etat_motsdetransitions[s].remove("#")
                    for sx in succeurs:
                        self.etat_motsdetransitions[s].add(sx[1])
                        self.add_set_to_dict(self.transitions,sx,succeurs[sx])     
                del self.transitions[s,"#"]
  
    #trouver tout les successeur d'un etat (fermeture epsilone) et retourner toutes les transitions
    def get_sucesseur(self,s0,s):
        succes={}
        for mot in (self.etat_motsdetransitions[s]):
            if mot!="#":
                self.add_set_to_dict(succes,(s0,mot),self.transitions[s,mot])                  
            else:
                for etat in self.transitions[s,mot]:
                    #si on pas de boucle d'epsilones
                    if(etat!=s0):
                        succ=self.get_sucesseur(s0,etat)
                        for sx in succ:
                            self.add_set_to_dict(succes,sx,succ[sx])       
        return succes
    
    
    def liste_Acc(self,S0,acc):
        for [S0,x] in self.transitions:
            for succ in self.transitions[S0,x]:
                if(not (succ in acc)):
                    acc.add(succ)
                    acc=acc.union(self.liste_Acc(succ,acc))
        return acc

    def supp_nAcc(self):
        trans=self.transitions.copy()
        acc=self.liste_Acc(self.etat_initial,{self.etat_initial})
        for S in self.etats:
            if S not in acc:
                if S in self.etat_motsdetransitions:
                    for x in self.etat_motsdetransitions[S]:
                        del trans[S,x]
                    del self.etat_motsdetransitions[S]
                if (S in self.etats_finaux):
                    self.etats_finaux.remove(S)
        self.transitions=trans.copy()
        self.etats=acc.copy()
        self.Coacc=self.etats_finaux.copy()
        #s'il n ya plus d'etats finaux
        if (not self.etats_finaux):
            print("l'automate n'a plus d'etats finaux")
            
            
    #suppression des etats non coaccessibles (qui sont deja accessibles)
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
    
    def liste_Coacc(self,sf,coacc):
        pre=self.predecesseur(sf)
        for P in pre:
            if (P not in coacc):
                coacc.add(P)
                coacc=coacc.union(self.liste_Coacc(P,coacc))
        return coacc

    #suppression des etats non coaccessibles
    def supp_nCoa(self):
        trans=self.transitions.copy()
        etat_MDT=self.etat_motsdetransitions.copy()
        coacc=set()
        for sf in self.etats_finaux: #obtention de tous les etats coacc
            coacc=coacc.union(self.liste_Coacc(sf,{sf}))
        for [S,x] in self.transitions:
            for P in self.transitions[S,x]:
                if (P not in coacc):
                    del trans[S,x]
                    etat_MDT[S].remove(x)
                    if (not etat_MDT[S]):
                        del etat_MDT[S]
        self.etats=coacc.copy()
        self.transitions=trans.copy()
        self.etat_motsdetransitions=etat_MDT.copy()
        if( not (self.etat_initial in coacc)):
            print("l'automate n'a plus d'etat initial")
        
    def complet(self):
        #si l'automate est simple diterministe
        sp="sp"
        added=0
        for etat in self.etat_motsdetransitions:
            if len(self.etat_motsdetransitions[etat])<len(self.alphabet):
                added=1
                puis=set(self.alphabet)-self.etat_motsdetransitions[etat]
                self.etat_motsdetransitions[etat].union(puis)
                for pui in puis:
                    self.transitions[etat,pui]={sp}
        for etat_isole in self.etats:
            if etat_isole not in self.etat_motsdetransitions:
                added=1
                for pui in self.alphabet:
                        self.transitions[etat_isole,pui]={sp}
        if added:
            self.etats.append(sp)
            self.etat_motsdetransitions[sp]=(self.alphabet).copy()
            for alpha in self.alphabet:
                self.transitions[sp,alpha]={sp}
                
    def complement(self):
        self.complet()
        self.etats_finaux=list(set(self.etats)-set(self.etats_finaux))
    
    #simple diterministe
    def miroir(self):
        fin=self.etat_initial
        self.etat_initial=self.etat_initial+"0"
        new_transitions={}
        for transition in self.transitions:
            self.add_set_to_dict(new_transitions,(list(self.transitions[transition])[0],transition[1]),{transition[0]})
        self.transitions=new_transitions
        self.add_set_to_dict(self.transitions,(self.etat_initial,"#"),set(self.etats_finaux))
        self.etats_finaux={fin}
            

#de l'automate généralisé a l'automate partiellement généralisé

#ajouter des etats supplementaires 
    def ajouter_etat(self,P,x,Nom,i): 
        trans=self.transitions.copy()
#Nom est le 'nom' de l'etat initial, par ex si P='S3' le premier etat a rajouter s'appelle S31, le deuxieme, S32..
        for succ in trans[P,x]:
            y=x[0]
            z=x[1:]
            S=Nom+str(i)
            while(S in self.etats):
                i+=1
                S=Nom+str(i)
            #ajouter la liason entre S et succ
            self.transitions[S,z]={succ}
            self.etat_motsdetransitions[S]={z}
            #supprimer la liaison entre P et succ
            self.transitions[P,x].remove(succ)
            if (not self.transitions[P,x]):
                del self.transitions[P,x]
                self.etat_motsdetransitions[P].remove(x)
                if (not self.etat_motsdetransitions[P]):
                    del self.etat_motsdetransitions[P]
            #ajouter la liason entre P et S
            if ([P,y] not in self.transitions):
                self.transitions[P,y]={S}
                if (P not in self.etat_motsdetransitions):
                    self.etat_motsdetransitions[P]={y}
                else:
                    self.etat_motsdetransitions[P].add(y)
            else:
                self.transitions[P,y].add(S)
            #reitérer si z est encore lent
            if(len(z)>1):
                i+=1
                self.ajouter_etat(S,z,Nom,i)


#le passage du généraliser au partiellement généralisé
    def gen_parGen(self):
        for [S,x] in self.transitions:
            if (len(x)>1):
                Nom=S
                self.ajouter_etat(S,x,Nom,1)


            

