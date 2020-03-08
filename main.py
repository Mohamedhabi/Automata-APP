# main.py
from automate import Automate
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
Config.set('graphics', 'resizable', False)

alphabet=[]
etats=[]
etatinit=''
etatfin=[]
lettre=''
transitions={}
automate={}
automate_tmp={}

class ReadAutomateWindow(Screen):

    alphabetF = ObjectProperty(None)
    etat_initF= ObjectProperty(None)
    etat_finF = ObjectProperty(None)
    etatF = ObjectProperty(None)
    errmsg=ObjectProperty(None)
    
    def submit(self):
        #Alphabet
        global alphabet,etatfin,etatinit,etats
        alphabet= self.alphabetF.text.split(' ')
        err=0
        alphabet = list(set(filter(len, alphabet)))
        if len(alphabet)<1:
            err=1
            msg="Vous devez avoir une lettre"
        for lettre in alphabet:
            if(len(lettre)>1):
                err=1
                msg="La langueur des lettres doit etre inferieur a 1"
                break
        
        #etat init
        etatinit=self.etat_initF.text.split(' ')
        etatinit = list(filter(len, etatinit))
        if len(etatinit)>=1:
            etatinit=etatinit[0]
        else:
            err=1
            msg="Vous devez avoir un etat initial"

        if not err:
            #etat fin     
            etatfin=self.etat_finF.text.split(' ')
            err=0
            etatfin = list(set(filter(len, etatfin)))
            
            #etat
            global etats
            etats=self.etatF.text.split(' ')
            etats = set(filter(len, etats))
            for etat_final in etatfin:
                etats.add(etat_final)
            etats.add(etatinit)
            etats=list(etats)
        
        if err:
            self.errmsg.text=msg
        else:
            sm.current = "trans"
    
    def default(self):
        global alphabet,etatfin,etatinit,etats,automate
        alphabet=["a","b","c"]
        etats=["s0","s1","s2","s3","sf","s4","s5","s7"]
        etatinit=["s0"]
        etatfin=["sf","s7"]
        transitions={}
        
        transitions["s0","ba"]={"s3"}
        transitions["s1","b"]={"s2"}
        transitions["s1","a"]={"s0"}
        transitions["s0","c"]={"s2"}
        transitions["s2","#"]={"s3"}
        transitions["s2","b"]={"s5"}
        transitions["s3","b"]={"s5"}
        transitions["s3","bb"]={"s3"}
        transitions["s5","c"]={"s7"}
        transitions["s4","b"]={"sf"}
        transitions["s4","c"]={"s7"}
        automate = Automate(alphabet,etats,etatinit,etatfin,transitions)
        automate.drow_automate()
        mainscr=sm.get_screen("main")
        mainscr.reloadpic()
        sm.current = "main"
 



class ReadTransitionsWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    err_msg= ObjectProperty(None)
    nbtrans=ObjectProperty(None)
    nb=0
    global etats,alphabet,transitions
    def addTrans(self):
        self.err_msg.text=""
        courant = ObjectProperty(None)
        mot= ObjectProperty(None)
        suiv = ObjectProperty(None)
        if self.courant.text not in etats or self.suiv.text not in etats:
                self.err_msg.text="Erreur l'état de transition entré n'éxiste \npas dans l'ensemble des états"
        elif len(self.mot.text)<1 or sum([True for i in self.mot.text if i not in alphabet])>0 and self.mot.text!="#" :
           self.err_msg.text="Erreur le mot de transition entré \nn'est pas dans l'Alphabet"                
        else:
            self.nb+=1
            self.nbtrans.text=str(self.nb)+" Transitions"
            if (self.courant.text,self.mot.text) in transitions:
                transitions[self.courant.text,self.mot.text].add(self.suiv.text)
            else:
                transitions[self.courant.text,self.mot.text]={self.suiv.text}
        
    def submit(self):
        global automate
        automate = Automate(alphabet,etats,[etatinit],etatfin,transitions)
        print(automate.transitions,automate.etat_motsdetransitions,automate.alphabet,automate.etats)
        automate.drow_automate()
        mainscr=sm.get_screen("main")
        mainscr.reloadpic()
        sm.current = "main"


class MainWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        import os
        if os.path.exists("./automate.png"):
            os.remove("./automate.png")
        if os.path.exists("./automate2.png"):
            os.remove("./automate2.png")
        if os.path.exists("./automate"):
            os.remove("./automate")
        if os.path.exists("./automate2"):
            os.remove("./automate2")
    exists=False  
    label_op=ObjectProperty(None)
    mot=ObjectProperty(None)
    motexist=ObjectProperty(None)
    def reduire(self):
        global automate,automate_tmp
        automate_tmp=automate.get_automtereduit()
        self.reloadpic()
        self.label_op.text="Reduit:"
        
        
    def gen_simple(self):
        global automate,automate_tmp
        automate_tmp=automate.get_simple()
        self.reloadpic()
        self.label_op.text="Simple:"

    def det(self):
        global automate,automate_tmp
        automate_tmp=automate.get_deterministe()
        self.reloadpic()
        self.label_op.text="Déterministe:"

    def complement(self):
        global automate,automate_tmp
        automate_tmp=automate.get_complement()
        self.reloadpic()
        self.label_op.text="Complement:"


    def mirroir(self):
        global automate,automate_tmp
        automate_tmp=automate.get_miroir()
        self.reloadpic()
        self.label_op.text="Miroir:"


    def rec(self):
        global automate,automate_tmp
        if automate.chemin(self.mot.text):
            self.motexist.text="le mot est reconnu \n   par l'automate"
        else:
            self.motexist.text="    Le mot n'est pas \nreconnu par l'automate"


    def reloadpic(self):
        global automate_tmp
        if not self.exists:
            self.ids.image1.reload()
            self.exists=True
        else:
            automate_tmp.drow_automate("automate2")
        self.ids.image2.reload()


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("./my.kv")

sm = WindowManager()

screens =  [ReadAutomateWindow(name="lect_auto"),ReadTransitionsWindow(name="trans"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "lect_auto"



class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()