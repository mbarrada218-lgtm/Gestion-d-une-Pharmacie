from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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


    F1 = Frame(content_frame, bd=3, relief="groove" , bg=BG_MAIN)
    F1.place(y=10 , width=970, height=630)

    title = Label(F1, text=" ➜  GESTION DES MEDICAMENTS ", font=("Bookman old style", 18, "bold"), width=110
                   , height=3,bg=COLOR_TEXT, fg=BG_MAIN)
    title.pack()

    #=========================================================================================================
    # AJOUTER LES MEDICAMENTS
    #=========================================================================================================
    def ajouter_medicamant(values=None):

        nonlocal ent_midecament, ent_dosage, ent_date_ex
        nonlocal ent_quantite, combo_categorie, ent_fourni

        selected_row = [None]

        # =============================== FICHE DES MEDICAMENT ====================
        F3 = Frame(F1, bd=3, relief="raised", bg=BG_MAIN)
        F3.place(x=1, y=150, width=890, height=390)

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
        combo_categorie.option_add("*TCombobox*Listbox.font",            ("Bookman old style", 11))
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
        label_butt = Label(F3, bg=COLOR_ENTRY, width=130, height=5)
        label_butt.place(y=330)

        save = Button(label_butt, text="╰┈➤ Enregistre",
                    font=("Bookman Old Style", 10, "bold"),
                    fg=BG_MAIN, bg=COLOR_BTN, width=15, relief="raised", height=2,)
        save.place(x=680, y=10)
        save.bind("<Enter>", on_enter)
        save.bind("<Leave>", on_leave)

        retour = Button(label_butt, text="⬅️ RETOUR",
                        font=("Bookman Old Style", 10, "bold"),
                        fg=BG_MAIN, bg=COLOR_BTN, width=15, relief="raised", height=2,
                        command=lambda: medicament(content_frame, BG_MAIN, COLOR_TEXT,
                                                COLOR_ENTRY, ECRITURE, COLOR_BTN,
                                                clear_content, on_enter, on_leave))
        retour.place(x=510, y=10)
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

    #=========================================================================================================
    #=========================================================================================================
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

    # دالة كتمسح لي ما كاين فـ content_frame (باش ماتتكارراش الواجهة)
    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    # دوال بسيطة ديال hover على الأزرار
    def on_enter(event):
        event.widget.config(bg="#5a5a80")

    def on_leave(event):
        event.widget.config(bg=COLOR_BTN)

    # هنا كنعيطو مباشرة على الدالة ديال medicament
    medicament(content_frame, BG_MAIN, COLOR_TEXT, COLOR_ENTRY,
               ECRITURE, COLOR_BTN, clear_content, on_enter, on_leave)

    root.mainloop()
