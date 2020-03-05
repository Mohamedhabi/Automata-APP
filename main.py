from automate import Automate

def lecture_automate():      
    err=1
    alphabet=[]
    etats=[]
    etatinit=''
    etatfin=[]
    lettre=''
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
    etats=["s0","s1","s2","s3","sf","s4","s5","s6","s7"]
    etatinit=["s0"]
    etatfin=["sf"]
    transitions={}
    '''
    transitions["s0","bc"]={"s3","s7"}
    transitions["s1","b"]={"s2"}
    transitions["s1","a"]={"s0"}
    transitions["s2","ba"]={"s5"}
    transitions["s3","aac"]={"s5","s4"}
    transitions["s5","bac"]={"s6"}
    transitions["s4","cca"]={"sf"}
    transitions["s4","cb"]={"s7"}
    transitions["s7","bc"]={"sf"}'''
    
    transitions["s0","b"]={"s3"}
    transitions["s1","b"]={"s2"}
    transitions["s1","a"]={"s0"}
    transitions["s2","b"]={"s5"}
    transitions["s3","a"]={"s5"}
    transitions["s3","b"]={"s3"}
    transitions["s5","c"]={"s6"}
    transitions["s4","b"]={"sf"}
    transitions["s4","c"]={"s7"}
    transitions["s6","c"]={"sf"}
 
 
       
    #print("les transitions: \n\n",transitions,"\n\n\n")
    automate = Automate(alphabet,etats,etatinit,etatfin,transitions)
    return automate

print("Test:\n\n")

msg=input("Voulez vous utiliser l'automate par défaut? Y ")
if msg=='Y' or msg=='y':
    auto=default_automate()
else:
    auto=lecture_automate()

auto.drow_automate("Automate.gv")
#menu
finished=False
while (not finished):
    choix=input("Veuillez introduire votre choix :\n 1- Réduction de l'automate \n 2- le passage du non det au det \n 3- le complement \n 4- le mirroir \n 5- la reconnaissance des mots \n")
    if (choix=='1'):
        auto.get_automtereduit().drow_automate("reduit.gv")
    elif (choix=='2'):
        auto.get_deterministe().drow_automate("deterministe.gv")
    elif (choix=='3'):
        auto.get_complement().drow_automate("complement.gv")
    elif (choix=='4'):
        auto.get_miroir().drow_automate("mirroir.gv")
    elif (choix=='5'):
        mot=input("entrer le mot ")
        while (sum([True for i in mot if i not in auto.alphabet])>0):
            print("veuillez entrer un mot composé des lettres de l'alphabet initial")
            mot=input()
        if (auto.chemin(mot)):
            print("le mot ",mot," est reconnu par cet automate")
        else:
            print("le mot ",mot," n'est pas reconnu par cet automate")
    
    inp=input("voulez vous faire une autre opération? Y/N ")
    if (inp != 'y' and inp != 'Y'):
        finished=True
        
    
    


    
