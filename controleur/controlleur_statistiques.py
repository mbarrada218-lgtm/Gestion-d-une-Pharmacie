from openpyxl import Workbook, load_workbook
from tkinter import messagebox
from datetime import datetime
from controleur.controlleur_medicament import FICHIER_MEDICAMENTS
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FICHE_STATISTIQUE = os.path.join(BASE_DIR, "..", "STATISTIQUE.xlsx")
FICHE_VENTES = os.path.join(BASE_DIR, "..", "VENTS.xlsx")


def en_nombre(valeur):
    if valeur is None:
        return 0
    try:
        return float(str(valeur).replace(",", ".").strip())
    except ValueError:
        return 0

def lire_mois_annee(date):
    if isinstance(date, datetime):
        return date.month, date.year

    for format_date in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            d = datetime.strptime(str(date)[:10], format_date)
            return d.month, d.year
        except ValueError:
            pass
    return None, None

def trouver_colonne(entetes, mot):
    for i in range(len(entetes)):
        if mot in entetes[i]:
            return i
    return None

def lire_prix_medicaments():
    prix = {}

    if not os.path.exists(FICHIER_MEDICAMENTS):
        messagebox.showwarning("Attention", "Fichier médicaments makaynch")
        return prix

    wb = load_workbook(FICHIER_MEDICAMENTS, data_only=True)
    ws = wb.active

    # Ligne 1 = les titres dyal colonnes
    entetes = []
    for row in ws.iter_rows(min_row=1, max_row=1, values_only=True):
        entetes = [str(c).lower() if c else "" for c in row]

    col_nom = trouver_colonne(entetes, "nom")
    col_achat = trouver_colonne(entetes, "achat")
    col_vente = trouver_colonne(entetes, "vente")

    if col_nom is None or col_achat is None or col_vente is None:
        messagebox.showerror("Erreur", "Fichier médicaments: ma l9itch colonnes Nom / Prix d'Achat / Prix de Vente")
        wb.close()
        return prix

    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[col_nom] is None:
            continue
        nom = str(row[col_nom]).strip().lower()
        prix[nom] = (en_nombre(row[col_achat]), en_nombre(row[col_vente]))

    wb.close()
    return prix


def calculer_statistiques(mois, annee):

    liste_ventes = []   # tableau 1 : ventes détaillées
    resume = {}         # tableau 2 : résumé par médicament
    ca_total = 0
    benefice_total = 0

    if not os.path.exists(FICHE_VENTES):
        messagebox.showwarning("Attention", "Fichier VENTS.xlsx makaynch")
        return liste_ventes, resume, 0, 0, 0

    # Les prix mn fichier médicaments
    prix_medicaments = lire_prix_medicaments()
    introuvables = []   # médicaments li ma tlqawch f fichier médicaments

    wb_ventes = load_workbook(FICHE_VENTES)
    ws_ventes = wb_ventes["VENTS"]

    for row in ws_ventes.iter_rows(min_row=2, values_only=True):

        # Ila ligne khawya (ma fihach smiya dyal médicament) nskipiwha
        if row[3] is None:
            continue

        num_serie = row[1]
        date = row[2]
        nom = row[3]
        dosage = row[4]
        quantite = int(en_nombre(row[6]))

        # Nchoufou wach had vente f chhar w l3am li khtar l'utilisateur
        mois_vente, annee_vente = lire_mois_annee(date)
        if mois_vente != mois or annee_vente != annee:
            continue

        # Njibou prix d'achat w prix de vente mn fichier médicaments
        cle = str(nom).strip().lower()
        if cle in prix_medicaments:
            prix_achat = prix_medicaments[cle][0]
            prix_vente = prix_medicaments[cle][1]
        else:
            prix_achat = 0
            prix_vente = 0
            if nom not in introuvables:
                introuvables.append(nom)

        # Nhsbo CA w Bénéfice
        ca = round(quantite * prix_vente, 2)
        benefice = round((prix_vente - prix_achat) * quantite, 2)

        # ID automatique: 1, 2, 3 ... 7sab 3dad les lignes li f tableau
        id_auto = len(liste_ventes) + 1

        liste_ventes.append([
            id_auto, num_serie, date, nom, dosage,
            quantite, prix_achat, prix_vente, ca, benefice
        ])

        # Résumé (kol médicament lih totaux dyalo)
        if nom not in resume:
            resume[nom] = [0, 0, 0]   # [quantité, CA, bénéfice]

        resume[nom][0] = resume[nom][0] + quantite
        resume[nom][1] = round(resume[nom][1] + ca, 2)
        resume[nom][2] = round(resume[nom][2] + benefice, 2)

        ca_total = ca_total + ca
        benefice_total = benefice_total + benefice

    wb_ventes.close()

    if len(introuvables) > 0:
        messagebox.showwarning(
            "Attention",
            "Had les médicaments ma tlqawch f fichier médicaments:\n" + "\n".join(str(n) for n in introuvables))

    return liste_ventes, resume, len(liste_ventes), round(ca_total, 2), round(benefice_total, 2)


def sauvegarder_statistiques(liste_ventes, resume):
    """Katsauvegardi les 2 sheets f STATISTIQUE.xlsx"""
    wb = Workbook()

    # Sheet 1
    ws1 = wb.active
    ws1.title = "VENTES DETAILEES"
    ws1.append([
        "ID", "N° SERIE", "Date", "Nom du Médicament",
        "Dosage (mg/ml)", "Quantité", "Prix d'Achat",
        "Prix de Vente", "CA", "Bénéfice"
    ])
    for ligne in liste_ventes:
        ws1.append(ligne)

    # Sheet 2
    ws2 = wb.create_sheet("RESUME PAR MEDICAMENT")
    ws2.append(["Nom du Médicament", "Quantité Totale", "CA Total", "Bénéfice Total"])
    for nom in resume:
        ws2.append([nom, resume[nom][0], resume[nom][1], resume[nom][2]])

    try:
        wb.save(FICHE_STATISTIQUE)
    except PermissionError:
        messagebox.showerror("Erreur", "Sedd fichier STATISTIQUE.xlsx f Excel w 3awed jereb")
    wb.close()


def mettre_a_jour_statistiques(mois=None, annee=None):

    if mois is None:
        mois = datetime.now().month
    if annee is None:
        annee = datetime.now().year

    liste_ventes, resume, nb, ca_total, benefice_total = calculer_statistiques(mois, annee)
    sauvegarder_statistiques(liste_ventes, resume)
    return nb, ca_total, benefice_total


def statistique_controlleur(treview_B_VENTS, treview_B_RESUME, mois, annee):

    # Nms7o l'ancien contenu
    for item in treview_B_VENTS.get_children():
        treview_B_VENTS.delete(item)
    for item in treview_B_RESUME.get_children():
        treview_B_RESUME.delete(item)

    liste_ventes, resume, nb, ca_total, benefice_total = calculer_statistiques(mois, annee)

    # Treeview 1
    for ligne in liste_ventes:
        treview_B_VENTS.insert("", "end", values=ligne)

    # Treeview 2
    for nom in resume:
        treview_B_RESUME.insert("", "end", values=(nom, resume[nom][0], resume[nom][1], resume[nom][2]))

    sauvegarder_statistiques(liste_ventes, resume)

    return nb, ca_total, benefice_total