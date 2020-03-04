from automate import Automate

def default_automate():      
    alphabet=["a","b","c"]
    etats=["s0","s1","s2","s3","sf","s4"]
    etatinit="s0"
    etatfin=["sf"]
    transitions={}
    transitions["s0","a"]={"s1","s2"}
    transitions["s1","a"]={"s1","s3"}
    transitions["s2","b"]={"s2"}
    transitions["s2","c"]={"s3","s4"}
    transitions["s3","a"]={"sf"}
    transitions["s4","b"]={"s3","sf"}
    automate = Automate(alphabet,etats,etatinit,etatfin,transitions)
    return automate

def default_automate2():  
    #exo2 TD      
    alphabet=["0","1"]
    etats=["s0","s01","s1","s11","s2"]
    etatinit="s0"
    etatfin=["s1"]
    transitions={}
    transitions["s0","0"]={"s1","s01"}
    transitions["s01","1"]={"s0"}
    transitions["s1","1"]={"s1"}
    transitions["s1","0"]={"s11"}
    transitions["s11","0"]={"s2"}
    transitions["s2","1"]={"s1"}
    automate = Automate(alphabet,etats,etatinit,etatfin,transitions)
    return automate

def default_automate3(): 
    #exo2 TD     
    alphabet=["0","1"]
    etats=["s0","s1","s2"]
    etatinit="s0"
    etatfin=["s2"]
    transitions={}
    transitions["s0","01"]={"s0"}
    transitions["s0","0"]={"s1"}
    transitions["s1","00"]={"s2"}
    transitions["s1","#"]={"s2"}
    transitions["s2","1"]={"s1"}
    automate = Automate(alphabet,etats,etatinit,etatfin,transitions)
    return automate

def default_automate4():    
    #exo2 EMD  
    alphabet=["a","b","c"]
    etats=["s0","s1","s2","s3","s4","s5"]
    etatinit="s0"
    etatfin=["s4","s0"]
    transitions={}
    transitions["s0","aa"]={"s0"}
    transitions["s0","#"]={"s1"}
    transitions["s1","#"]={"s2"}
    transitions["s1","c"]={"s0"}
    transitions["s2","bba"]={"s2"}
    transitions["s2","a"]={"s1"}
    transitions["s2","aab"]={"s5"}
    transitions["s2","#"]={"s5"}
    transitions["s2","#"]={"s3"}
    transitions["s3","b"]={"s2"}
    transitions["s4","bab"]={"s4"}
    transitions["s4","a"]={"s0"}
    automate = Automate(alphabet,etats,etatinit,etatfin,transitions)
    return automate

print("Test:\n\n")

auto=default_automate4()
auto.drow_automate("1")
auto.supp_nAcc()
auto.supp_nCoa()
auto.drow_automate("2")

auto.gen_parGen()
auto.drow_automate("3")

auto.partiel_get_simple()
auto.drow_automate("4")

auto2=auto.deterministe()
auto2.drow_automate("5")

#auto2.supp_nAcc()
#auto2.supp_nCoa()
#auto2.drow_automate("4")
