import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import *
from tkinter import ttk
from datetime import datetime
from controleur.controlleur_statistiques import statistique_controlleur

Font_texte = ("Bookman Old Style", 9, "bold")

LISTE_MOIS = ["01 - Janvier", "02 - Février", "03 - Mars", "04 - Avril",
              "05 - Mai", "06 - Juin", "07 - Juillet", "08 - Août",
              "09 - Septembre", "10 - Octobre", "11 - Novembre", "12 - Décembre"]


def statistique_view(content_frame, BG_MAIN, COLOR_TEXT, COLOR_ENTRY, ECRITURE, COLOR_BTN,
                     clear_content, on_enter, on_leave):
    clear_content()

    F1 = Frame(content_frame, bd=3, relief="groove", bg=BG_MAIN)
    F1.place(y=10, width=970, height=630)

    title = Label(F1, text=" ➜  GESTION DES STATISTIQUES ", font=("Bookman old style", 18, "bold"),
                  width=110, height=3, bg=COLOR_TEXT, fg=BG_MAIN)
    title.pack()

    # ---------- MOIS ----------
    Label(F1, text="LE MOIS :", font=Font_texte, bg=BG_MAIN).place(x=200, y=103)

    MOIS = ttk.Combobox(F1, state="readonly", width=15, font=("Bookman old style", 10),
                        values=LISTE_MOIS)
    # Chhar d daba (month - 1 hit la liste katbda mn 0)
    MOIS.set(LISTE_MOIS[datetime.now().month - 1])
    MOIS.place(x=280, y=100)

    # ---------- ANNEE ----------
    Label(F1, text="ANNEE :", font=Font_texte, bg=BG_MAIN).place(x=450, y=103)

    annee = datetime.now().year
    ANNEE = ttk.Combobox(F1, state="readonly", font=("Bookman old style", 10), width=10,
                         values=[annee - 3, annee - 2, annee - 1, annee])
    ANNEE.set(annee)
    ANNEE.place(x=520, y=100)

    # ---------- VENTES / CA / BENEFICE ----------
    vents = StringVar(value="0")
    Label(F1, text="VENTES :", font=("Bookman old style", 10, "bold"), bg=BG_MAIN).place(x=200, y=140)
    Label(F1, textvariable=vents, font=("Bookman old style", 11, "bold"), bg=BG_MAIN,
          fg=COLOR_TEXT).place(x=280, y=140)

    ca = StringVar(value="0.00 DH")
    Label(F1, text="CA :", font=("Bookman old style", 10, "bold"), bg=BG_MAIN).place(x=340, y=140)
    Label(F1, textvariable=ca, font=("Bookman old style", 11, "bold"), bg=BG_MAIN,
          fg=COLOR_TEXT).place(x=380, y=140)

    benefice = StringVar(value="0.00 DH")
    Label(F1, text="BENIFICE :", font=("Bookman old style", 10, "bold"), bg=BG_MAIN).place(x=480, y=140)
    Label(F1, textvariable=benefice, font=("Bookman old style", 11, "bold"), bg=BG_MAIN,
          fg=COLOR_TEXT).place(x=580, y=140)

    # ---------- FRAME DYAL LES TABLEAUX ----------
    F2 = Frame(F1, width=950, height=380, relief="ridge", bd=1, bg=BG_MAIN)
    F2.place(x=5, y=240)

    # Style (mra whda safi)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Bookman Old Style", 8, "bold"), background=BG_MAIN)
    style.configure("Treeview", font=("Bookman old style", 8), background=BG_MAIN)

    # ---------- TREEVIEW 1 : VENTES DETAILEES ----------
    treview_B_VENTS = ttk.Treeview(F2, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), height=20,
                                   show="headings", style="Treeview")

    scV_ventes = ttk.Scrollbar(F2, orient="vertical", command=treview_B_VENTS.yview)
    scH_ventes = ttk.Scrollbar(F2, orient="horizontal", command=treview_B_VENTS.xview)
    treview_B_VENTS.config(yscrollcommand=scV_ventes.set, xscrollcommand=scH_ventes.set)

    titres_ventes = ["ID", "N° SERIE", "Date", "Nom du Médicament", "Dosage (mg/ml)",
                     "Quantité", "Prix d'Achat", "Prix de Vente", "CA", "Bénifice"]
    largeurs_ventes = [40, 90, 140, 140, 140, 140, 140, 140, 140, 140]

    for i in range(10):
        treview_B_VENTS.heading(i + 1, text=titres_ventes[i])
        treview_B_VENTS.column(i + 1, width=largeurs_ventes[i])

    # ---------- TREEVIEW 2 : RESUME PAR MEDICAMENT ----------
    treview_B_RESUME = ttk.Treeview(F2, columns=(1, 2, 3, 4), height=20,
                                    show="headings", style="Treeview")

    scV_resume = ttk.Scrollbar(F2, orient="vertical", command=treview_B_RESUME.yview)
    treview_B_RESUME.config(yscrollcommand=scV_resume.set)

    titres_resume = ["Nom du Médicament", "Quantité Vendue", "CA", "Bénifice"]
    for i in range(4):
        treview_B_RESUME.heading(i + 1, text=titres_resume[i])
        treview_B_RESUME.column(i + 1, width=220)

    # ---------- FONCTIONS : afficher tableau 1 wla tableau 2 ----------
    def afficher_treview_B_VENTS():
        treview_B_RESUME.place_forget()
        scV_resume.place_forget()
        scV_ventes.place(x=927, y=10, height=300)
        scH_ventes.place(x=5, y=312, width=930)
        treview_B_VENTS.place(x=5, y=10, width=920, height=300)

    def afficher_treview_B_RESUME():
        treview_B_VENTS.place_forget()
        scV_ventes.place_forget()
        scH_ventes.place_forget()
        scV_resume.place(x=927, y=10, height=300)
        treview_B_RESUME.place(x=5, y=10, width=920, height=300)

    # ---------- FONCTION : charger les données selon chhar w l3am ----------
    def charger_donnees(event=None):
        numero_mois = int(MOIS.get()[:2])      # "10 - Octobre" -> 10
        numero_annee = int(ANNEE.get())

        nb, total_ca, total_benef = statistique_controlleur(
            treview_B_VENTS, treview_B_RESUME, numero_mois, numero_annee)

        vents.set(str(nb))
        ca.set(f"{total_ca:.2f} DH")
        benefice.set(f"{total_benef:.2f} DH")

    # Mnin tbdl chhar wla l3am, kay3awd ycharger
    MOIS.bind("<<ComboboxSelected>>", charger_donnees)
    ANNEE.bind("<<ComboboxSelected>>", charger_donnees)

    afficher_treview_B_VENTS()
    charger_donnees()

    # ---------- BOUTONS ----------
    B_VENTS = Button(F1, text="➜ VENTES DETAILEES", font=Font_texte, width=25, height=2,
                     bg=COLOR_BTN, command=afficher_treview_B_VENTS)
    B_VENTS.place(x=200, y=190)
    B_VENTS.bind("<Enter>", on_enter)
    B_VENTS.bind("<Leave>", on_leave)

    B_RESUME = Button(F1, text="➜ RESUME PAR MEDICAMENT", font=Font_texte, width=25, height=2,
                      bg=COLOR_BTN, command=afficher_treview_B_RESUME)
    B_RESUME.place(x=450, y=190)
    B_RESUME.bind("<Enter>", on_enter)
    B_RESUME.bind("<Leave>", on_leave)

