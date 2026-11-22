from openpyxl import load_workbook, Workbook
from datetime import datetime
from tkinter import messagebox
import os

from controleur.controlleur_medicament import _ouvrir_fichier_medicaments, FICHIER_MEDICAMENTS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FICHE_VENTES = os.path.join(BASE_DIR, "..", "VENTS.xlsx")
SYMBOLES = "@.,&<>*/\\!?#$%"


def generer_serie(ws):
    dernier = 0
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2, values_only=True):
        if row[0]:
            dernier = max(dernier, int(str(row[0])[3:]))
    return f"MED{dernier + 1:05d}"


def remplir_champ(champ, valeur):
    champ.config(state="normal")
    champ.delete(0, "end")
    champ.insert(0, valeur)
    champ.config(state="readonly")


def vider_champ(champ):
    champ.config(state="normal")
    champ.delete(0, "end")
    champ.config(state="readonly")


def remettre_quantite(QUAN):
    QUAN.delete(0, "end")
    QUAN.insert(0, "1")


def creation_fiche_excel(tableau_historique):
    if os.path.exists(FICHE_VENTES):
        wb = load_workbook(FICHE_VENTES)
        ws = wb["VENTS"]
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = "VENTS"
        ws["A1"] = "ID"
        ws["B1"] = "N° SERIE"
        ws["C1"] = "Date"
        ws["D1"] = "Nom du Médicament"
        ws["E1"] = "Dosage (mg/ml)"
        ws["F1"] = "Prix"
        ws["G1"] = "Quantité"
        ws["H1"] = "Médecin"
        ws["I1"] = "N° Ordonnance"
        ws["J1"] = "Nom du Client"
        wb.save(FICHE_VENTES)

    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        tableau_historique.insert("", "end", values=row)
    return wb, ws


def rechercher_medicament(RECH, NOM, DOSAGE, STOCK, PR_VENT):
    terme = RECH.get().strip()

    if terme == "":
        messagebox.showinfo("Attention", "Veuillez saisir le nom du médicament")
        return

    if terme.isdigit():
        messagebox.showinfo("Attention", "Le nom du médicament ne doit pas contenir uniquement des chiffres")
        return

    if any(caractere in SYMBOLES for caractere in terme):
        messagebox.showinfo("Attention", "Le nom du médicament contient des caractères non autorisés")
        return

    try:
        wb_med, ws_med = _ouvrir_fichier_medicaments()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire MEDICAMENTS.xlsx : {e}")
        return

    terme_minuscule = terme.lower()
    for row in ws_med.iter_rows(min_row=2, values_only=True):
        nom_medicament = row[1]
        if nom_medicament is not None and terme_minuscule in str(nom_medicament).lower():
            remplir_champ(NOM, row[1])
            remplir_champ(DOSAGE, row[2])
            remplir_champ(STOCK, row[4])
            remplir_champ(PR_VENT, row[7])
            return

    messagebox.showinfo("Attention", "Le produit n'existe pas")


def change_totale(tableau_panier, total_var):
    total_general = 0
    for item in tableau_panier.get_children():
        valeurs = tableau_panier.item(item, "values")
        quantite = int(valeurs[3])
        prix = float(str(valeurs[4]).replace(",", "."))
        total_general = total_general + prix * quantite

    total_var.set(f"{total_general:.2f}")


def ajouter_au_panier(RECH, NOM, DOSAGE, STOCK, PR_VENT, QUAN, ws, tableau_panier, total_var):
    if STOCK.get() == "":
        messagebox.showinfo("Attention", "Cherche d'abord un médicament (écris son nom puis appuie sur Entrée)")
        return

    quantite = QUAN.get().strip()
    if not quantite.isdigit() or int(quantite) == 0:
        messagebox.showinfo("Attention", "La quantité doit être un nombre entier supérieur à 0")
        return

    quantite = int(quantite)
    stock = int(float(STOCK.get()))

    deja_dans_panier = 0
    for item in tableau_panier.get_children():
        valeurs = tableau_panier.item(item, "values")
        if str(valeurs[1]) == NOM.get():
            deja_dans_panier = deja_dans_panier + int(valeurs[3])

    if quantite + deja_dans_panier > stock:
        messagebox.showinfo("Attention", f"Stock insuffisant (stock disponible : {stock})")
        return

    numero_serie = generer_serie(ws)
    tableau_panier.insert("", "end", values=(numero_serie, NOM.get(), DOSAGE.get(), quantite, PR_VENT.get()))
    change_totale(tableau_panier, total_var)

    RECH.delete(0, "end")
    vider_champ(NOM)
    vider_champ(DOSAGE)
    vider_champ(STOCK)
    vider_champ(PR_VENT)
    remettre_quantite(QUAN)


def sur_ordonanace(type_vente, NOM_CLIENT, MEDECIN, N_ORD):
    nom_client = NOM_CLIENT.get().strip()
    medecin = MEDECIN.get().strip()
    n_ord = N_ORD.get().strip()

    if nom_client == "" or medecin == "" or n_ord == "":
        messagebox.showinfo("Attention", "Veuillez remplir les informations de l'ordonnance")
        return False

    for terme in [nom_client, medecin, n_ord]:
        if any(caractere in SYMBOLES for caractere in terme):
            messagebox.showinfo("Attention", "Les informations de l'ordonnance contiennent des caractères non autorisés")
            return False

    if nom_client.isdigit() or medecin.isdigit() or not n_ord.isdigit():
        messagebox.showinfo("Attention", "Veuillez vérifier les données de l'ordonnance")
        return False

    return True


def decrement_stock(tableau_panier):
    try:
        wb_med, ws_med = _ouvrir_fichier_medicaments()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire MEDICAMENTS.xlsx : {e}")
        return False

    for item in tableau_panier.get_children():
        valeurs = tableau_panier.item(item, "values")
        nom_panier = str(valeurs[1])
        quantite_panier = int(valeurs[3])

        for row in ws_med.iter_rows(min_row=2):
            if str(row[1].value) == nom_panier:
                row[4].value = int(row[4].value) - quantite_panier
                break

    try:
        wb_med.save(FICHIER_MEDICAMENTS)
    except PermissionError:
        messagebox.showerror("Erreur", "Ferme le fichier MEDICAMENTS.xlsx dans Excel puis réessaie")
        return False

    return True


def validation_de_historique(tableau_panier, type_vente, tableau_historique, NOM_CLIENT, MEDECIN, N_ORD, ws, wb, total_var):
    if len(tableau_panier.get_children()) == 0:
        messagebox.showinfo("Attention", "Le panier est vide")
        return

    medecin = "-"
    n_ord = "-"
    nom_client = "-"

    if type_vente.get() == "ordonnance":
        if not sur_ordonanace(type_vente, NOM_CLIENT, MEDECIN, N_ORD):
            return
        nom_client = NOM_CLIENT.get().strip()
        medecin = MEDECIN.get().strip()
        n_ord = N_ORD.get().strip()

    if not decrement_stock(tableau_panier):
        return

    ID = len(tableau_historique.get_children()) + 1
    date_vente = datetime.now().strftime("%d/%m/%Y %H:%M")

    for ligne in tableau_panier.get_children():
        valeurs = tableau_panier.item(ligne, "values")
        nouvelle_ligne = [ID, valeurs[0], date_vente, valeurs[1], valeurs[2],
                          valeurs[4], valeurs[3], medecin, n_ord, nom_client]
        tableau_historique.insert("", "end", values=nouvelle_ligne)
        ws.append(nouvelle_ligne)
        ID = ID + 1

    for item in tableau_panier.get_children():
        tableau_panier.delete(item)

    NOM_CLIENT.delete(0, "end")
    MEDECIN.delete(0, "end")
    N_ORD.delete(0, "end")
    change_totale(tableau_panier, total_var)

    try:
        wb.save(FICHE_VENTES)
    except PermissionError:
        messagebox.showerror("Erreur", "Ferme le fichier VENTS.xlsx dans Excel puis réessaie")


def annuler(tableau_panier, RECH, NOM, DOSAGE, STOCK, PR_VENT, QUAN, NOM_CLIENT, MEDECIN, N_ORD, total_var):
    for item in tableau_panier.get_children():
        tableau_panier.delete(item)

    RECH.delete(0, "end")
    vider_champ(NOM)
    vider_champ(DOSAGE)
    vider_champ(STOCK)
    vider_champ(PR_VENT)
    remettre_quantite(QUAN)
    NOM_CLIENT.delete(0, "end")
    MEDECIN.delete(0, "end")
    N_ORD.delete(0, "end")
    change_totale(tableau_panier, total_var)