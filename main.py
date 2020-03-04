from automate import Automate

def lecture_automate():      
    err=1
    alphabet=[]
    etats=[]
    etatinit=''
    etatfin=[]
    transitions={}#dictionary
    #Lecture de l'alphabet
    while err:
        msg=input("Entrer l'alphaber , les lettre séparé par des éspaces :")
        alphabet=msg.split(' ')
        err=0
        alphabet = list(set(filter(len, alphabet)))
        for lettre in alphabet:
            if(len(lettre)>1):
                err=1
                print("La langueur des lettres doit etre inferieur a 1")
                break
            
    print(alphabet)
    #Lecture de l'état initial
    err=1
    while err:
        msg=input("Entrer l'état initial :")
        etatinit=msg.split(' ')
        err=0
        etatinit = list(filter(len, etatinit))
        if len(etatinit)>=1:
            etatinit=etatinit[0]
        else:
            err=1

    print(etatinit)
    #Lecture des états finaux   
    err=1
    while err:
        msg=input("\n\nEntrer l'ensemble des etats finaux séparer par des espaces :")
        etatfin=msg.split(' ')
        err=0
        etatfin = list(set(filter(len, etatfin)))

    print(etatfin)
    
    #Lecture des états intermediaires  
    err=1
    while err:
        msg=input("\n\nEntrer l'ensemble des états intermediaires séparer par des espaces (état initial et les états finaux exclu) :")
        etats=msg.split(' ')
        err=0
        etats = set(filter(len, etats))
        print(list(etats))
        for etat_final in etatfin:
            etats.add(etat_final)
        etats.add(etatinit)
        etats=list(etats)
    print(etats)
    
    #Lecture des transitions
    err=1
    terminer=0
    while not terminer:
        msg=input("\n\nEntrer une transition : S1 v S2 : (epsilone=#)")
        tmp=msg.split(' ')
        tmp = list(filter(len, tmp))
        if len(tmp)==3 :
            if tmp[0] not in etats or tmp[2] not in etats:
                print("Erreur états de transition entré n'éxiste pas dans l'ensemble des états")
            elif sum([True for i in tmp[1] if i not in alphabet])>0 and tmp[1]!="#":
                print("Erreur le mot de transition entré n'est pas dans l'Alphabet")                
            else:
                if (tmp[0],tmp[1]) in transitions:
                    transitions[tmp[0],tmp[1]].add(tmp[2])
                else:
                    transitions[tmp[0],tmp[1]]={tmp[2]}
        else:
            print("Erreur la lettre n'est pas dans l'Alphabet")
        msg=input("\n\nVoulez vous entrer une nouvelle transision : Y?")
        if msg!='Y' and msg!='y':
            terminer=1    

    automate = Automate(alphabet,etats,etatinit,etatfin,transitions)
    return automate

def default_automate():      
   # err=1
    alphabet=["a","b","c"]
    etats=["s0","s1","s2","sf","sF"]
    etatinit="s0"
    etatfin=["sf","sF"]
    transitions={}
    #mine
    """ 
    transitions["s0","ab"]={"sf"}
    transitions["s0","c"]={"s1"}
    transitions["s0","#"]={"s1"}
    transitions["s0","a"]={"s0","s3"}
    transitions["sf","c"]={"sf"}
    transitions["s1","#"]={"sf"}
    transitions["s1","#"]={"s0"}
   # transitions["s1","b"]={"s2"}
    transitions["s1","a"]={"sf"}
    transitions["s2","ab"]={"s1"} 
    #sarah    
    """
    transitions["s0","a"]={"s2"}
    transitions["s0","b"]={"s1"}
    transitions["s0","c"]={"s0"}
    transitions["s1","a"]={"sf"}
    transitions["s2","b"]={"s2"}
    transitions["s2","c"]={"sf"}
    transitions["sF","a"]={"s0"}
    transitions["sF","b"]={"sF"}
 
       
    #print("les transitions: \n\n",transitions,"\n\n\n")
    automate = Automate(alphabet,etats,etatinit,etatfin,transitions)
    return automate

print("Test:\n\n")

msg=input("Voulez vous utiliser l'automate par défaut? Y ")
if msg=='Y' or msg=='y':
    auto=default_automate()
else:
    auto=lecture_automate()

#ta3iiiiiii
"""
print("\n\nAffichage de toutes les transitions:\n",auto.transitions)
print("\n\nAffichage état mot a lire:\n",auto.etat_motsdetransitions)

auto.drow_automate()
auto.partiel_get_simple()
print("\n\nAffichage de toutes les transitions:\n",auto.transitions)
print("\n\nAffichage état mot a lire:\n",auto.etat_motsdetransitions)
auto.drow_automate("automatkkkk.gv")
"""
#sarahhhhhhhhhhhhhhh

#auto.drow_automate()

#la réduction de l'automate

#suppression des etats non accessibles

#auto.drow_automate()

auto.supp_nAcc()

print("\n\nAffichage des etats finaux:\n",auto.etats_finaux)
print("\n\nAffichage de toutes les transitions 2:\n",auto.transitions)
print("\n\nAffichage de tous les motsdetr 2:\n",auto.etat_motsdetransitions)
#auto.drow_automate("acc.gv")

#suppression des etats non coaccessibles
auto.supp_nCoa()
print("\n\nAffichage des etats finaux:\n",auto.etats_finaux)
print("\n\nAffichage de toutes les transitions 3:\n",auto.transitions)
print("\n\nAffichage de tous les motsdetr 3:\n",auto.etat_motsdetransitions)
#auto.drow_automate("coacc.gv")
'''
#du generalisé au par generalisé
auto.gen_parGen()
auto.drow_automate("gen.gv")
'''
'''
mot=input("entrer le mot ")
while (sum([True for i in mot if i not in auto.alphabet])>0):
    print("veuillez entrer un mot composé des lettres de l'alphabet initial")
    mot=input()
print(auto.chemin(mot))'''