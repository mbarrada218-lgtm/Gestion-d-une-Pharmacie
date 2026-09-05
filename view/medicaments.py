import sys
import os

# Ajoute le dossier racine du projet (parent de "view") au sys.path,
# pour que "controleur" soit trouvable meme quand ce fichier est lance directement.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from controleur.controlleur_medicament import (medicament_controlleur,
                                                enregistrer_medicament,
                                                charger_medicaments_expires,
                                                charger_stock_faible)

Font_texte = ("Bookman Old Style", 9, "bold")

def medicament(content_frame, BG_MAIN, COLOR_TEXT, COLOR_ENTRY,ECRITURE, COLOR_BTN
                     ,clear_content ,on_enter,on_leave):
    clear_content()

    ent_midecament  = None
    ent_dosage      = None
    ent_date_ex     = None
    ent_quantite    = None
    combo_categorie = None
    ent_fourni      = None
    ent_prix_achat  = None
    ent_prix_vente  = None
    wb = None
    ws = None

    sub_widgets = []

    def clear_sub_widgets():
        for w in sub_widgets:
            try:
                w.destroy()
            except Exception:
                pass
        sub_widgets.clear()


    F1 = Frame(content_frame, bd=3, relief="groove" , bg=BG_MAIN)
    F1.place(y=10 , width=970, height=630)

    title = Label(F1, text=" ➜  GESTION DES MEDICAMENTS ", font=("Bookman old style", 18, "bold"), width=110
                   , height=3,bg=COLOR_TEXT, fg=BG_MAIN)
    title.pack()

    #=========================================================================================================
    #                                       AJOUTER LES MEDICAMENTS
    #=========================================================================================================
    def ajouter_medicamant(values=None):

        nonlocal ent_midecament, ent_dosage, ent_date_ex
        nonlocal ent_quantite, combo_categorie, ent_fourni
        nonlocal ent_prix_achat, ent_prix_vente, wb, ws

        selected_row = [None]

        clear_sub_widgets()
        F2.place_forget()   # <-- khabbi tableau_general mli kandkhlo l'formulaire

        # =============================== FICHE DES MEDICAMENT ====================
        F3 = Frame(F1, bd=1, relief="flat", bg=BG_MAIN)
        F3.place(x=20, y=150, width=890, height=450)
        sub_widgets.append(F3)

        # ========================= NOM DU MEDICAMENT ============================
        nom_midecament = Label(F3, text=" Nom du Médicament : ", font=Font_texte, bg=BG_MAIN, fg=COLOR_TEXT)
        nom_midecament.grid(row=0, pady=10, sticky="w")

        ent_midecament = Entry(F3, font=("Bookman old style", 11), width=40,
                            relief="groove", bd=2, bg=COLOR_ENTRY, fg=ECRITURE)
        ent_midecament.grid(row=1, ipady=7, padx=5)

        # ========================= DOSAGE ============================
        dosage = Label(F3, text=" Dosage (mg/ml) : ", font=Font_texte, bg=BG_MAIN, fg=COLOR_TEXT)
        dosage.grid(row=2, pady=10, sticky="w")

        ent_dosage = Entry(F3, font=("Bookman old style", 11), width=40,
                        relief="groove", bd=2, bg=COLOR_ENTRY, fg=ECRITURE)
        ent_dosage.grid(row=3, ipady=7, padx=5)

        # ========================= QUANTITE EN STOCK ==========================
        quantite = Label(F3, text=" Quantité en stock :", font=Font_texte, bg=BG_MAIN, fg=COLOR_TEXT)
        quantite.grid(row=4, pady=10, sticky="w")

        ent_quantite = Entry(F3, font=("Bookman old style", 11), width=40,
                            relief="groove", bd=2, bg=COLOR_ENTRY, fg=ECRITURE)
        ent_quantite.grid(row=5, ipady=7, padx=5)

        # ========================= DATE EXPIRATION ==========================
        date_ex = Label(F3, text=" Date d'Expiration :  ", font=Font_texte, bg=BG_MAIN, fg=COLOR_TEXT)
        date_ex.grid(row=6, pady=10, sticky="w")

        ent_date_ex = Entry(F3, font=("Bookman old style", 11), width=40,
                            relief="groove", bd=2, bg=COLOR_ENTRY, fg=ECRITURE)
        ent_date_ex.grid(row=7, ipady=7, padx=5)

        # ==================== CATEGORIE ============================
        categorie = Label(F3, text=" Catégorie : ", font=Font_texte, bg=BG_MAIN, fg=COLOR_TEXT)
        categorie.grid(row=0, column=1, padx=100, pady=10, sticky="w")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", font=("Bookman old style", 11),
                        background=COLOR_ENTRY, foreground=ECRITURE, arrowcolor=ECRITURE,
                        relief="groove", borderwidth=2)
        style.map("TCombobox",
                fieldbackground=[("readonly", COLOR_ENTRY)],
                foreground=[("readonly", ECRITURE)])

        categories_medicaments = ["Analgésiques", "Anti-inflammatoires", "Antibiotiques",
                                "Antiviraux", "Antifongiques", "Antipyrétiques",
                                "Antihistaminiques", "Médicaments cardiovasculaires",
                                "Médicaments digestifs", "Psychotropes", "Vaccins"]

        combo_categorie = ttk.Combobox(F3, values=categories_medicaments,
                                    font=("Bookman old style", 11), state="readonly", width=38)
        combo_categorie.grid(row=1, column=1, ipady=7, padx=100)
        combo_categorie.option_add("*TCombobox*Listbox.font",("Bookman old style", 11))
        combo_categorie.option_add("*TCombobox*Listbox.background",      COLOR_ENTRY)
        combo_categorie.option_add("*TCombobox*Listbox.foreground",      ECRITURE)
        combo_categorie.option_add("*TCombobox*Listbox.selectBackground", ECRITURE)
        combo_categorie.option_add("*TCombobox*Listbox.selectForeground", COLOR_ENTRY)
        combo_categorie.current(0)

        # ========================= PRIX D'ACHAT ===========================

        prix_achat = Label(F3, text=" Prix d'Achat : ", font=Font_texte, bg=BG_MAIN, fg=COLOR_TEXT)
        prix_achat.grid(row=2, column=1, padx=100, pady=10, sticky="w")

        ent_prix_achat = Entry(F3, font=("Bookman old style", 11), width=40,
                        relief="groove", bd=2, bg=COLOR_ENTRY, fg=ECRITURE)
        ent_prix_achat.grid(row=3, column=1, ipady=7, padx=100)

        # ========================= PRIX DE VENTE ===========================

        prix_vente = Label(F3, text=" Prix de Vente : ", font=Font_texte, bg=BG_MAIN, fg=COLOR_TEXT)
        prix_vente.grid(row=4, column=1, padx=100, pady=10, sticky="w")

        ent_prix_vente = Entry(F3, font=("Bookman old style", 11), width=40,
                        relief="groove", bd=2, bg=COLOR_ENTRY, fg=ECRITURE)
        ent_prix_vente.grid(row=5, column=1, ipady=7, padx=100)


        # ========================= FOURNISSEUR ===========================
        fournisseur = Label(F3, text=" Fournisseur : ", font=Font_texte, bg=BG_MAIN, fg=COLOR_TEXT)
        fournisseur.grid(row=6, column=1, padx=100, pady=10, sticky="w")

        ent_fourni = Entry(F3, font=("Bookman old style", 11), width=40,
                        relief="groove", bd=2, bg=COLOR_ENTRY, fg=ECRITURE)
        ent_fourni.grid(row=7, column=1, ipady=7, padx=100)

        # ============================ LES BUTTONS ======================
        def enregistrer_medicament_ui():
            # Récupérer les valeurs
            nom       = ent_midecament.get()
            dosage    = ent_dosage.get()
            quantite  = ent_quantite.get()
            date_ex   = ent_date_ex.get()
            categorie = combo_categorie.get()
            p_achat   = ent_prix_achat.get()
            p_vente   = ent_prix_vente.get()
            fourni    = ent_fourni.get()

            # La validation + l'enregistrement (Excel + tableau) se font dans le controlleur
            ok, message = enregistrer_medicament(wb, ws, tableau_general, nom, dosage,
                                                  quantite, date_ex, categorie,
                                                  p_achat, p_vente, fourni)
            if not ok:
                messagebox.showinfo("Attention", message)
                return

            # Vider les champs
            ent_midecament.delete(0, END)
            ent_dosage.delete(0, END)
            ent_quantite.delete(0, END)
            ent_date_ex.delete(0, END)
            ent_prix_achat.delete(0, END)
            ent_prix_vente.delete(0, END)
            ent_fourni.delete(0, END)

            # Réinitialiser la catégorie
            combo_categorie.set("")

        save = Button(F3, text="╰┈➤ Enregistre",
                    font=("Bookman Old Style", 10, "bold"),
                    fg=BG_MAIN, bg=COLOR_BTN, width=15, relief="raised", height=2,
                    command=enregistrer_medicament_ui)
        save.place(x=680, y=380)
        save.bind("<Enter>", on_enter)
        save.bind("<Leave>", on_leave)

        retour = Button(F3, text="⬅️ RETOUR",
                        font=("Bookman Old Style", 10, "bold"),
                        fg=BG_MAIN, bg=COLOR_BTN, width=15, relief="raised", height=2,
                        command=lambda: medicament(content_frame, BG_MAIN, COLOR_TEXT,
                                                COLOR_ENTRY, ECRITURE, COLOR_BTN,
                                                clear_content, on_enter, on_leave))
        retour.place(x=510, y=380)
        retour.bind("<Enter>", on_enter)
        retour.bind("<Leave>", on_leave)

    btn_ajout = Button(F1, text="✚ AJOUTER LES MEDICAMENTS",
                    fg=BG_MAIN, bg=COLOR_BTN, font=Font_texte,
                    width=30, height=2, command=lambda: ajouter_medicamant())
    
    btn_ajout.place(x=5, y=95)
    btn_ajout.bind("<Enter>", on_enter)
    btn_ajout.bind("<Leave>", on_leave)

    
    #=========================================================================================================
    #=========================================================================================================
    #                                            GESTION DES ALERTES
    #=========================================================================================================
    #=========================================================================================================
    def alertes_medicament ():
            
            clear_sub_widgets()
            F2.place_forget()   # <-- khabbi tableau_general mli kandkhlo les alertes

                #===================================================
                #                     MEDICAMENT EXPIRE
                #===================================================
            def medicament_expiré ():
                F4 = Frame(F1, bd=3, relief="flat" , bg=BG_MAIN)
                F4.place(x=1, y=150, width=950, height=200)
                sub_widgets.append(F4)

                titre_med = Label(F4, text=" ▶ Médicament Expirés : ", font=Font_texte,bg=BG_MAIN, fg=COLOR_TEXT)
                titre_med.place(x=5 , y=5)

                style = ttk.Style()
                style.theme_use("clam")
                style.configure("Treeview.Heading",
                                        font=("Bookman Old Style", 8, "bold"),
                                        background=BG_MAIN)

                style.configure("Treeview",
                                        font=("Bookman old style", 8),
                                        background=BG_MAIN )

                tableau_medicament = ttk.Treeview(F4 , columns=(1,2,3,4,5,6,7,8,9) , height=6, 
                                    show="headings", style="Treeview")


                sc = ttk.Scrollbar(F4, orient="vertical" , command=tableau_medicament.yview)
                sc.place( x= 930 , y= 40 , height=148)
                tableau_medicament.config(yscrollcommand=sc.set)
                
                tableau_medicament.heading(1, text="N°")
                tableau_medicament.heading(2, text="Nom du Médicament")
                tableau_medicament.heading(3, text=" Dosage (mg/ml)")
                tableau_medicament.heading(4, text=" Catégorie")
                tableau_medicament.heading(5, text="Quantité en stock")
                tableau_medicament.heading(6, text="Date d'Expiration")
                tableau_medicament.heading(7, text="Prix d'Achat")
                tableau_medicament.heading(8, text="Prix de Vente")
                tableau_medicament.heading(9, text="Fournisseur")

                tableau_medicament.column(1, width=25)
                tableau_medicament.column(2, width=120)
                tableau_medicament.column(3, width=110)
                tableau_medicament.column(4, width=110)
                tableau_medicament.column(5, width=110)
                tableau_medicament.column(6, width=110)
                tableau_medicament.column(7, width=110)
                tableau_medicament.column(8, width=110)
                tableau_medicament.column(9, width=110)
                
                tableau_medicament.place(x=10, y=40)

                # Remplir le tableau avec les medicaments dont la date est depassee
                charger_medicaments_expires(ws, tableau_medicament)

            medicament_expiré ()
                #===================================================
                #                     STOCK DES MEDICAMENT 
                #===================================================
            def stock_medicament():
                F5 = Frame(F1, bd=3, relief="flat" , bg=BG_MAIN)
                F5.place(x=1, y=350, width=950, height=200)
                sub_widgets.append(F5)
                
                titre_med_exp = Label(F5, text=" ▶ Stock Faible (<=10) : ", font=Font_texte,bg=BG_MAIN, fg=COLOR_TEXT)
                titre_med_exp.place(x=5 , y=5)

                style = ttk.Style()
                style.theme_use("clam")
                style.configure("Treeview.Heading",
                                        font=("Bookman Old Style", 8, "bold"),
                                        background=BG_MAIN)
                
                style.configure("Treeview",
                                        font=("Bookman old style", 8),
                                        background=BG_MAIN )
                
                tableau_stock = ttk.Treeview(F5 , columns=(1,2,3,4,5,6,7,8,9) , height=6, 
                                    show="headings", style="Treeview")
                
                
                sc = ttk.Scrollbar(F5, orient="vertical" , command=tableau_stock.yview)
                sc.place( x= 930 , y= 40 , height=148)
                tableau_stock.config(yscrollcommand=sc.set)
                
                tableau_stock.heading(1, text="N°")
                tableau_stock.heading(2, text="Nom du Médicament")
                tableau_stock.heading(3, text=" Dosage (mg/ml)")
                tableau_stock.heading(4, text=" Catégorie")
                tableau_stock.heading(5, text="Quantité en stock")
                tableau_stock.heading(6, text="Date d'Expiration")
                tableau_stock.heading(7, text="Prix d'Achat")
                tableau_stock.heading(8, text="Prix de Vente")
                tableau_stock.heading(9, text="Fournisseur")
                
                tableau_stock.column(1, width=25)
                tableau_stock.column(2, width=120)
                tableau_stock.column(3, width=110)
                tableau_stock.column(4, width=110)
                tableau_stock.column(5, width=110)
                tableau_stock.column(6, width=110)
                tableau_stock.column(7, width=110)
                tableau_stock.column(8, width=110)
                tableau_stock.column(9, width=110)
                
                tableau_stock.place(x=10, y=40)

                # Remplir le tableau avec les medicaments dont la quantite est <= 10
                charger_stock_faible(ws, tableau_stock)

            stock_medicament()

            retour = Button(F1, text="⬅️ RETOUR",
                        font=("Bookman Old Style", 10, "bold"),
                        fg=BG_MAIN, bg=COLOR_BTN, width=15, relief="raised", height=2,
                        command=lambda: medicament(content_frame, BG_MAIN, COLOR_TEXT,
                                                COLOR_ENTRY, ECRITURE, COLOR_BTN,
                                                clear_content, on_enter, on_leave))
            retour.place(x=570, y=550)
            retour.bind("<Enter>", on_enter)
            retour.bind("<Leave>", on_leave)
            sub_widgets.append(retour)

        #=========================================================================================================
        #=========================================================================================================
  
    btn_gestin = Button(F1 , text="🔔 GESTION DES ALERTES", fg=BG_MAIN , bg=COLOR_BTN 
                           ,font=Font_texte , width= 30 , height=2 , command=lambda:alertes_medicament() )
    btn_gestin.place(x=260, y=95)
    btn_gestin.bind("<Enter>", on_enter)
    btn_gestin.bind("<Leave>", on_leave)
    #=========================================================================================================
    #=========================================================================================================
    #                                            TABLEAU DES MEDICAMENT 
    #=========================================================================================================
    #=========================================================================================================

    #================= TABLEAU DES MEDICAMENT ======================
    F2 = Frame(F1, bd=3, relief="flat" , bg=BG_MAIN)
    F2.place(x=1, y=150, width=950, height=390)
 
        #=============== CREATION DE TABLEAU =====================
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading",
                            font=("Bookman Old Style", 8, "bold"),
                            background=BG_MAIN)

    style.configure("Treeview",
                            font=("Bookman old style", 8),
                            background=BG_MAIN )
    
    tableau_general = ttk.Treeview(F2 , columns=(1,2,3,4,5,6,7,8,9) , height=14, 
                           show="headings", style="Treeview")
    
          
    sc = ttk.Scrollbar(F2, orient="vertical" , command=tableau_general.yview)
    sc.place( x= 915 , y= 10 , height=307)
    tableau_general.config(yscrollcommand=sc.set)

    tableau_general.heading(1, text="N°")
    tableau_general.heading(2, text="Nom du Médicament")
    tableau_general.heading(3, text=" Dosage (mg/ml)")
    tableau_general.heading(4, text=" Catégorie")
    tableau_general.heading(5, text="Quantité en stock")
    tableau_general.heading(6, text="Date d'Expiration")
    tableau_general.heading(7, text="Prix d'Achat")
    tableau_general.heading(8, text="Prix de Vente")
    tableau_general.heading(9, text="Fournisseur")
    

    tableau_general.column(1, width=25)
    tableau_general.column(2, width=115)
    tableau_general.column(3, width=110)
    tableau_general.column(4, width=110)
    tableau_general.column(5, width=110)
    tableau_general.column(6, width=110)
    tableau_general.column(7, width=110)
    tableau_general.column(8, width=110)
    tableau_general.column(9, width=110)

    tableau_general.place(x=1, y=10)

    wb, ws = medicament_controlleur(tableau_general)


