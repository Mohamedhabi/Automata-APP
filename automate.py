#(alphabet, état initial, états finaux et l’ensemble des transitions)
class Automate:        
    # init method or constructor  
        
    def __init__(self, alphabet,etats,etat_initial,etats_finaux,transitions):    
        
        self.alphabet = alphabet
        self.etats = etats
        self.etat_initial = etat_initial
        self.etats_finaux = etats_finaux  
        self.transitions = transitions
        self.reduit=False
        self.etat_motsdetransitions={}#dictionaire exemple:{"s0":{"a","b","ab"}} pour savoir les mot qu'on peut lire apartir d'un état
        self.atomate_type=self.__get_type() #"G","PG","SND","SD"
        for transition in transitions:
            if transition[0] in self.etat_motsdetransitions:
                self.etat_motsdetransitions[transition[0]].add(transition[1])
            else:
                self.etat_motsdetransitions[transition[0]]={transition[1]}            
    
    def __get_type(self):
        type_="SD"
        for transition in self.transitions:
            if len(transition[1])>1:
                    type_="G"
                    break
            elif transition[1]=="#":
                type_="PG"
            elif type_!="PG" and  len(self.transitions[transition])>1:
                type_="SND"
        return type_
          
    def drow_automate(self,filename='automate'):
        
        err=0
        try:             
            from graphviz import Digraph
        except Exception:
            print("vous devez installer la bibliothèque python 'graphviz'")
            err=1
        if not err:
            f = Digraph(filename, filename,format='png')
            f.attr(rankdir='LR', size='8,5')
            #shape de l'etat initiale
            if type(self.etat_initial) == str:
                if self.etat_initial in self.etats_finaux:
                    f.attr('node', shape='doubleoctagon')
                else:
                    f.attr('node', shape='octagon')
                f.node(self.etat_initial)
            else:
                for node in self.etat_initial:
                    if node in self.etats_finaux:
                        f.attr('node', shape='doubleoctagon')
                    else:
                        f.attr('node', shape='octagon')
                    f.node(node)
                    
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
            
            g=f.render(filename=filename)


          
    #ajouter l'elsemble (set_) a l'element dictio[key]
    def __add_set_to_dict(self,dictio,key,set_):
        if key in dictio:
            dictio[key]=dictio[key].union(set_)
        else:
            dictio[key]=set_
    
    #elimination des epsilone dans l'automate
    def __partiel_gen_simple(self):
        for s in self.etat_motsdetransitions:
            if "#" in self.etat_motsdetransitions[s]:
                for tr in self.transitions[s,"#"]:
                    succeurs=self.get_sucesseur(s,tr)
                    self.etat_motsdetransitions[s].remove("#")
                    for sx in succeurs:
                        self.etat_motsdetransitions[s].add(sx[1])
                        self.__add_set_to_dict(self.transitions,sx,succeurs[sx])     
                del self.transitions[s,"#"]
        self.atomate_type="SND"
  
    #trouver tout les successeur d'un etat (fermeture epsilone) et retourner toutes les transitions
    def get_sucesseur(self,s0,s):
        if s in self.etats_finaux:
            self.etats_finaux.append(s0)
        succes={}
        if s in self.etat_motsdetransitions:
            for mot in (self.etat_motsdetransitions[s]):
                if mot!="#":
                    self.__add_set_to_dict(succes,(s0,mot),self.transitions[s,mot])                  
                else:
                    for etat in self.transitions[s,mot]:
                        #si on pas de boucle d'epsilones
                        if(etat!=s0):
                            succ=self.get_sucesseur(s0,etat)
                            for sx in succ:
                                self.__add_set_to_dict(succes,sx,succ[sx])       
        return succes
    
    
    def __liste_Acc(self,S0,acc):
        if S0 in self.etat_motsdetransitions:
            for x in self.etat_motsdetransitions[S0]:
                for succ in self.transitions[S0,x]:
                    if(succ not in acc):
                        acc.add(succ)
                        self.__liste_Acc(succ,acc)

    def __supp_nAcc(self):
        trans=self.transitions.copy()
        #acc={self.etat_initial}
        acc= set(self.etat_initial)
        for etat in self.etat_initial:
            self.__liste_Acc(etat,acc)
        for S in self.etats:
            if S not in acc:
                if S in self.etat_motsdetransitions:
                    for x in self.etat_motsdetransitions[S]:
                        del trans[S,x]
                    del self.etat_motsdetransitions[S]
                if (S in self.etats_finaux):
                    self.etats_finaux.remove(S)
        self.transitions=trans.copy()
        self.etats=list(acc.copy())
        #s'il n ya plus d'etats finaux
        if (not self.etats_finaux):
            print("l'automate n'a plus d'etats finaux")
            
            
    #suppression des etats non coaccessibles (qui sont deja accessibles)
    def __predecesseur(self,S0): #methode pour lobtention des predecesseurs d'un sommet
        Pred={}
        for [S,x] in self.transitions:
            if (S0 in self.transitions[S,x]):
                if (S in Pred):
                    Pred[S].add(x)
                else:
                    Pred[S]={x}
        return Pred

    #obtention de la liste des etats coaccessibles
    
    def __liste_Coacc(self,sf,coacc):
        pre=self.__predecesseur(sf)
        for P in pre:
            if (P not in coacc):
                coacc.add(P)
                coacc=coacc.union(self.__liste_Coacc(P,coacc))
        return coacc

    #suppression des etats non coaccessibles
    def __supp_nCoa(self):
        trans=self.transitions.copy()
        etat_MDT=self.etat_motsdetransitions.copy()
        coacc=set()
        for sf in self.etats_finaux: #obtention de tous les etats coacc
            coacc=coacc.union(self.__liste_Coacc(sf,{sf}))
        for [S,x] in self.transitions:
            succ= list(self.transitions[S,x])
            for P in succ:
                if (P not in coacc):
                    trans[S,x].remove(P)
                    if (not trans[S,x]):
                        del trans[S,x]
                        etat_MDT[S].remove(x)
                        if (not etat_MDT[S]):
                            del etat_MDT[S]
        self.etats=list(coacc.copy())
        self.transitions=trans.copy()
        self.etat_motsdetransitions=etat_MDT.copy()
        #supprimer les etats initiaux non coacc
        for S in self.etat_initial:
            if S not in coacc:
                self.etat_initial.remove(S)
        if( not set(self.etat_initial).intersection(coacc)):
            print("l'automate n'a plus d'etat initial")

        
    def __complet(self):
        #si l'automate est simple deterministe
        sp="sp"
        while sp in self.etats:
            sp+="p"
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
     
    def __complement(self):
        self.etats_finaux=list(set(self.etats)-set(self.etats_finaux))
    
    
    def __miroir(self):
        #simple deterministe
        fin=self.etat_initial
        self.etat_initial=self.etats_finaux
        new_transitions={}
        for transition in self.transitions:
            self.__add_set_to_dict(new_transitions,(list(self.transitions[transition])[0],transition[1]),{transition[0]})
        self.transitions=new_transitions
        #self.__add_set_to_dict(self.transitions,(self.etat_initial,"#"),set(self.etats_finaux))
        self.etats_finaux=fin
            

    #de l'automate généralisé a l'automate partiellement généralisé

    #ajouter des etats supplementaires 
    def __ajouter_etat(self,P,x,Nom,i): 
        trans=self.transitions[P,x].copy()
        #Nom est le 'nom' de l'etat initial, par ex si P='S3' le premier etat a rajouter s'appelle S31, le deuxieme, S32..
        for succ in trans:
            y=x[0]
            z=x[1:]
            S=Nom+str(i)
            while(S in self.etats):
                i+=1
                S=Nom+str(i)
            self.etats.append(S)
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
            if ((P,y) not in self.transitions):
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
                self.__ajouter_etat(S,z,Nom,i)


    #le passage du généraliser au partiellement généralisé
    def __gen_parGen(self):
        for [S,x] in self.transitions.copy():
            if (len(x)>1):
                Nom=S
                self.__ajouter_etat(S,x,Nom,1)
        self.atomate_type="PG"

    #Fonction récursive pour generer un automate deterministe
    def __nondet_det(self,automate,etats,nometat):
        if nometat not in automate.etats:
            automate.etats.append(nometat)
            if set(self.etat_initial).intersection(etats):
                automate.etat_initial.append(nometat)
            if  (set(self.etats_finaux)).intersection(etats):
                automate.etats_finaux.append(nometat)
            for lettre in self.alphabet:
                trans=set()
                for etat in etats:
                    if etat in self.etat_motsdetransitions and lettre in self.etat_motsdetransitions[etat]:
                        trans=trans.union(self.transitions[etat,lettre])                
                if trans:
                    nometat2=""
                    lsort=list(trans)
                    lsort.sort()
                    for etat in lsort:
                        nometat2+=etat+"/"
                    automate.transitions[nometat,lettre]={nometat2}
                    self.__add_set_to_dict(automate.etat_motsdetransitions,nometat,{lettre})
                    self.__nondet_det(automate,trans,nometat2)
                            
    def copy(self):    
        tran={}
        for (S,x) in self.transitions:
            tran[S,x]=self.transitions[S,x].copy()
        return Automate(self.alphabet.copy(),self.etats.copy(), self.etat_initial.copy(),self.etats_finaux.copy(),tran)        

    def __reduire(self):
        if not self.reduit:
            self.__supp_nAcc()
            self.__supp_nCoa()
            self.reduit=True
#Public methods
    def get_automtereduit(self):
        auto=self.copy()
        auto.__reduire()
        return auto 
    
    def get_parc_gen(self):
        automate=self.copy()
        automate.__reduire()
        if automate.atomate_type=="G":
            automate.__gen_parGen()    
        return automate  
    
    def get_simple(self):
        automate=self.copy()
        automate.__reduire()
        if automate.atomate_type=="G":
            automate.__gen_parGen()
        if automate.atomate_type=="PG":
            automate.__partiel_gen_simple()    
        return automate
    
    def get_deterministe(self):
        automate=self.copy()
        automate.__reduire()
        if automate.atomate_type=="G":
            automate.__gen_parGen()
        if automate.atomate_type=="PG":
            automate.__partiel_gen_simple()
        if automate.atomate_type=="SND":
            automate2=Automate(automate.alphabet.copy(),[],[],[],{})
            for etat in automate.etat_initial:
                automate.__nondet_det(automate2,{etat},etat+"/")
            return automate2
        return automate
    
    def get_complet(self):
        auto_comp=self.get_deterministe()
        auto_comp.__complet()    
        return auto_comp   
    
    def get_complement(self):
        auto_comp=self.get_complet()   
        auto_comp.__complement()  
        return auto_comp  
     
    def get_miroir(self):
        auto_mir=self.get_deterministe()
        auto_mir.__miroir()    
        return auto_mir     
    
    def chemin(self,mot):
        if self.atomate_type != "SD":
            auto=self.get_deterministe()
        else: 
            auto=self
        for S in auto.etat_initial :
            continu=True
            w=mot
            while ((len(w)>0) and continu):
                x=w[0]
                if (S in auto.etat_motsdetransitions):
                    if (x in auto.etat_motsdetransitions[S]):
                        w=w[1:]
                        S=list(auto.transitions[S,x])[0]
                    else:
                        continu=False 
                else:
                    continu=False
            if ((S in auto.etats_finaux) and len(w)==0) :
                return True #or print("le mot "+mot+" est reconnu")
        return False