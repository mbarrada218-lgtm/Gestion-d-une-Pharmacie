import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import *
from tkinter import ttk
from controleur.controlleur_vents import (validation_donnees , vents_controlleur)


Font_texte = ("Bookman Old Style", 9, "bold")

def vents(content_frame, BG_MAIN, COLOR_TEXT, COLOR_ENTRY,ECRITURE, COLOR_BTN
                     ,clear_content ,on_enter,on_leave):
    clear_content()

    
    F1 = Frame(content_frame, bd=3, relief="groove" , bg=BG_MAIN)
    F1.place(y=10 , width=970, height=630)

    title = Label(F1, text=" ➜  GESTION DES VENTES ", font=("Bookman old style", 18, "bold"), width=110
                   , height=3,bg=COLOR_TEXT, fg=BG_MAIN)
    title.pack()


    # ================================================================
    # FUNCTION POUR CHANGER ENTRE LES DEUX MODES
    # ================================================================
    def basculer_mode():
        if type_vente.get() == "simple":
            # Afficher Vente Simple
            F2.place(x=10,y=130,width=300,height=200)
            # Cacher Vente sur ordonnance
            F3.place_forget()

        elif type_vente.get() == "ordonnance":
            # Cacher Vente Simple
            F2.place_forget()
            # Afficher Vente sur ordonnance
            F3.place(x=10,y=130,width=300,height=200)


    Label(F1 , text="CHOISISSEZ LE TYPE DE VENTE :" , font=("Bookman old style" , 10 , "bold ")).place(x=5 , y=100)
    
 
    #====================================================================
    #                           VENTE SIMPLE
    #=====================================================================

    
    F2 = Frame(F1 , bd=3, relief="groove" )
    F2.place(x= 10, y=130 , width=300, height=240)

    Label(F2 , text="RECHERCHER :" , font= Font_texte).place(x = 5 , y=10)
    RECH = Entry(F2 , font=("Bookman old style" , 9 , "bold " ), highlightbackground="#5B9E96" , highlightthickness=2)
    RECH.place(x= 120 , y=10)

    Label(F2 , text="NOM MED       :" , font= Font_texte).place(x = 5 , y=40)
    NOM = Entry(F2 , font=("Bookman old style" , 9 , "bold " ), highlightbackground="#5B9E96" , highlightthickness=2)
    NOM.place(x= 120 , y=40)

    Label(F2 , text="DOSAGE         :" , font= Font_texte).place(x = 5 , y=70)
    DOSAGE = Entry(F2 , font=("Bookman old style" , 9 , "bold " ), highlightbackground="#5B9E96" , highlightthickness=2)
    DOSAGE.place(x= 120 , y=70)

    Label(F2 , text="STOCK            :" , font= Font_texte).place(x = 5 , y=100)
    STOCK = Entry(F2 , font=("Bookman old style" , 9 , "bold " ), highlightbackground="#5B9E96" , highlightthickness=2)
    STOCK.place(x= 120 , y=100)

    Label(F2 , text="PRIX DE VENTE :" , font= ("Bookman old style" , 8 , "bold ")).place(x = 5 , y=130)
    PR_VENT = Entry(F2 , font=("Bookman old style" , 9 , "bold " ), highlightbackground="#5B9E96" , highlightthickness=2)
    PR_VENT.place(x= 120 , y=130)

    Label(F2 , text="QUANTITE :" , font= ("Bookman old style" , 8 , "bold ")).place(x = 5 , y=160)
    QUAN = Spinbox(F2, from_=1, to=100, width=5, bg=COLOR_ENTRY, 
                      font=("Bookman old style", 11))
    QUAN.place(x= 120 , y=160)

    #====================================================================
    #                           VENTE SUR ORDONANACE 
    #=====================================================================

    F3 = Frame(F1 , bd=3, relief="groove" )
    F3.place(x= 10, y=130 , width=300, height=130)
    F3.place_forget()
    Label(F3, text=" ➜ INFORMATION ORDONNANCE " , font=Font_texte).place(y=5)

    Label(F3 , text="NOM DU CLIENT :" , font= ("Bookman old style" , 8 , "bold ")).place(x = 5 , y=30)
    NOM_CLIENT = Entry(F3 , font=("Bookman old style" , 9 , "bold " ), highlightbackground="#5B9E96" , highlightthickness=2)
    NOM_CLIENT.place(x= 120 , y=30)

    Label(F3 , text="MEDECIN           :" , font= ("Bookman old style" , 8 , "bold ")).place(x = 5 , y=60)
    MEDECIN = Entry(F3 , font=("Bookman old style" , 9 , "bold " ), highlightbackground="#5B9E96" , highlightthickness=2)
    MEDECIN.place(x= 120 , y=60)

    Label(F3 , text="N° ORDONNANCE :" , font= ("Bookman old style" , 8 , "bold ")).place(x = 5 , y=90)
    N_ORD = Entry(F3 , font=("Bookman old style" , 9 , "bold " ), highlightbackground="#5B9E96" , highlightthickness=2)
    N_ORD.place(x= 120 , y=90)


    def basculer_mode():
        if type_vente.get() == "simple":
            # Cacher Vente sur ordonnance
            F3.place_forget()
            # Afficher Vente Simple
            F2.place(x=10,y=130,width=300,height=240)

        elif type_vente.get() == "ordonnance":
            # Afficher Vente sur ordonnance
            F3.place(x=10,y=130,width=300,height=130)
            # Cacher Vente Simple
            F2.place(x=10,y=260,width=300,height=240)
    type_vente = StringVar(value="simple")

    Radiobutton(F1, text=" ➜ Vente Simple",
                variable=type_vente, value="simple",
                font=("Bookman old style" , 10 , "bold "), bg="whitesmoke", fg="darkblue",
                command=basculer_mode).place(x=250 , y=100)

    Radiobutton(F1, text=" ➜ Sur Ordonnance",
                variable=type_vente, value="ordonnance",
                font=("Bookman old style" , 10 , "bold "), bg="whitesmoke", fg="darkblue",
                command=basculer_mode).place(x=400 , y=100)
    basculer_mode()

    #====================================================================
    #                           TABLEAU DE PANIER
    #=====================================================================

    F4 = Frame(F1 , bd=3, relief="groove" )
    F4.place(x= 310, y=130 , width=650, height=480)

    Label(F4, text=" ➜ PANIER DE VENTE " , font=Font_texte).place(y=3)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=("Bookman Old Style", 8, "bold"), background=BG_MAIN)

    style.configure("Treeview",font=("Bookman old style", 8),background=BG_MAIN )

    tableau_panier = ttk.Treeview(F4 , columns=(1,2,3,4,5) , height=5, 
        show="headings", style="Treeview")


    sc = ttk.Scrollbar(F4, orient="vertical" , command=tableau_panier.yview)
    sc.place( x= 595 , y= 30 , height=127)
    tableau_panier.config(yscrollcommand=sc.set)

    tableau_panier.heading(1, text="N° SERIE")
    tableau_panier.heading(2, text="Nom du Médicament")
    tableau_panier.heading(3, text=" Dosage (mg/ml)")
    tableau_panier.heading(4, text="Quantité")
    tableau_panier.heading(5, text="Prix de Vente")


    tableau_panier.column(1, width=100)
    tableau_panier.column(2, width=120)
    tableau_panier.column(3, width=120)
    tableau_panier.column(4, width=120)
    tableau_panier.column(5, width=120)

    tableau_panier.place(x=10, y=30)

    Label(F4, text=" ➜ TOTALE : " , font=Font_texte , bg="#86B7B1" , width=67).place(x=41 , y=159)

    VALIDE = Button(F4, text="VALIDE ➜]", font=("Bookman Old Style", 10, "bold"),
                bg=COLOR_TEXT, fg=BG_MAIN, relief="raised", height=2 , width=15, 
                command=lambda:validation_donnees(RECH,NOM,DOSAGE,STOCK,PR_VENT,QUAN,NOM_CLIENT,MEDECIN,
                       N_ORD,wb,ws,tableau_historique))
    VALIDE.place(x= 40 , y=180)
    VALIDE.bind("<Enter>", on_enter)
    VALIDE.bind("<Leave>", on_leave)


    ANNULEE = Button(F4, text="ANNULEE", font=("Bookman Old Style", 10, "bold"),
                bg=COLOR_TEXT, fg=BG_MAIN, relief="raised", height=2 , width=15)
    ANNULEE.place(x= 438 , y=180)
    ANNULEE.bind("<Enter>", on_enter)
    ANNULEE.bind("<Leave>", on_leave)

    
    Label(F4, text=" ➜ HISTORIQUE DES VENTES " , font=Font_texte).place( y=250)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=("Bookman Old Style", 8, "bold"), background=BG_MAIN)

    style.configure("Treeview",font=("Bookman old style", 8),background=BG_MAIN )

    tableau_historique = ttk.Treeview(F4 , columns=(1,2,3,4,5,6,7,8,9,10) , height=7, 
        show="headings", style="Treeview")

    scV = ttk.Scrollbar(F4, orient="vertical" , command=tableau_historique.yview)
    scV.place( x= 631 , y= 280 , height=165)

    scH = ttk.Scrollbar(F4, orient="horizontal" , command=tableau_historique.xview)
    scH.place(y= 448 , width=643)


    tableau_historique.config(yscrollcommand=scV.set , xscrollcommand=scH.set)

    tableau_historique.heading(1, text="ID")
    tableau_historique.heading(2, text="N° SERIE")
    tableau_historique.heading(3, text="Date")
    tableau_historique.heading(4, text="Nom du Médicament")
    tableau_historique.heading(5, text="Dosage (mg/ml)")
    tableau_historique.heading(6, text="Prix")
    tableau_historique.heading(7, text="Quantité")
    tableau_historique.heading(8, text="Médecin")
    tableau_historique.heading(9, text="N°Ordonnance")
    tableau_historique.heading(10, text="Nom du Client")


    tableau_historique.column(1, width=25)
    tableau_historique.column(2, width=90)
    tableau_historique.column(3, width=100)
    tableau_historique.column(4, width=140)
    tableau_historique.column(5, width=110)
    tableau_historique.column(6, width=80)
    tableau_historique.column(7, width=80)
    tableau_historique.column(8, width=100)
    tableau_historique.column(9, width=100)
    tableau_historique.column(10, width=100)

    tableau_historique.place(x=0,y=280,width=630,height=165)
    wb, ws = vents_controlleur(tableau_historique)

    AJOUTER = Button(F2, text="➜ AJOUTER AU PANIER", font=("Bookman Old Style", 8, "bold"),
                      bg=COLOR_TEXT, fg=BG_MAIN, relief="raised" )
    AJOUTER.place(x=70, y=200)
    AJOUTER.bind("<Enter>", on_enter)
    AJOUTER.bind("<Leave>", on_leave)






































































if __name__ == "__main__":
    root = Tk()
    root.title("Test - Gestion des Médicaments")
    root.geometry("1000x600+100+20")
    

    BG_MAIN = "#F1F9F3"
    COLOR_ENTRY = "#E8EDEC"
    COLOR_TEXT = "#3B7E76"
    COLOR_BTN = "#5B9E96"
    ECRITURE = "#1B1E1D"

    content_frame = Frame(root, bg=BG_MAIN)
    content_frame.pack(fill=BOTH, expand=True)
   
    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    def on_enter(event):
        event.widget.config(bg="#5a5a80")

    def on_leave(event):
        event.widget.config(bg=COLOR_BTN)

    vents(content_frame, BG_MAIN, COLOR_TEXT, COLOR_ENTRY,
               ECRITURE, COLOR_BTN, clear_content, on_enter, on_leave)

    root.mainloop()