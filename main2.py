from automate import Automate

def default_automate():      
   # err=1
    alphabet=["a","b","c"]
    etats=["s0","s1","s2","s3","sf","sF","s4"]
    etatinit="s0"
    etatfin=["sf","sF"]
    transitions={}
    #mine
    transitions["s0","a"]={"sf"}
    transitions["s0","c"]={"s1"}
    transitions["sf","b"]={"sf"}
    transitions["s1","b"]={"sf"}
    transitions["s1","c"]={"s0"}
   # transitions["s1","b"]={"s2"}
    transitions["s1","a"]={"sf"}
    transitions["s2","a"]={"s1"}    
    #print("les transitions: \n\n",transitions,"\n\n\n")
    automate = Automate(alphabet,etats,etatinit,etatfin,transitions)
    return automate

print("Test:\n\n")

msg=input("Voulez vous utiliser l'automate par défaut? Y ")
if msg=='Y' or msg=='y':
    auto=default_automate()
auto.drow_automate()
auto.complet()
print(auto.transitions)
auto.drow_automate("complet")
auto.complement()
auto.drow_automate("complement")
