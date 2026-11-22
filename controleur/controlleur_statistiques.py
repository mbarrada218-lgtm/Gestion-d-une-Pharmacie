from openpyxl import Workbook, load_workbook
from tkinter import messagebox
from datetime import datetime
from controleur.controlleur_medicament import _ouvrir_fichier_medicaments
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


def lire_prix_medicaments():
    prix = {}
    wb, ws = _ouvrir_fichier_medicaments()

    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[1] is None:
            continue
        nom = str(row[1]).strip().lower()
        prix[nom] = (en_nombre(row[6]), en_nombre(row[7]))

    wb.close()
    return prix


def calculer_statistiques(mois, annee):
    liste_ventes = []
    resume = {}
    ca_total = 0
    benefice_total = 0

    if not os.path.exists(FICHE_VENTES):
        messagebox.showwarning("Attention", "Le fichier VENTS.xlsx n'existe pas encore")
        return liste_ventes, resume, 0, 0, 0

    prix_medicaments = lire_prix_medicaments()
    introuvables = []

    wb_ventes = load_workbook(FICHE_VENTES)
    ws_ventes = wb_ventes["VENTS"]

    for row in ws_ventes.iter_rows(min_row=2, values_only=True):
        if row[3] is None:
            continue

        num_serie = row[1]
        date = row[2]
        nom = row[3]
        dosage = row[4]
        quantite = int(en_nombre(row[6]))

        mois_vente, annee_vente = lire_mois_annee(date)
        if mois_vente != mois or annee_vente != annee:
            continue

        cle = str(nom).strip().lower()
        if cle in prix_medicaments:
            prix_achat = prix_medicaments[cle][0]
            prix_vente = prix_medicaments[cle][1]
        else:
            prix_achat = 0
            prix_vente = 0
            if nom not in introuvables:
                introuvables.append(nom)

        ca = round(quantite * prix_vente, 2)
        benefice = round((prix_vente - prix_achat) * quantite, 2)
        id_auto = len(liste_ventes) + 1

        liste_ventes.append([id_auto, num_serie, date, nom, dosage,
                             quantite, prix_achat, prix_vente, ca, benefice])

        if nom not in resume:
            resume[nom] = [0, 0, 0]

        resume[nom][0] = resume[nom][0] + quantite
        resume[nom][1] = round(resume[nom][1] + ca, 2)
        resume[nom][2] = round(resume[nom][2] + benefice, 2)

        ca_total = ca_total + ca
        benefice_total = benefice_total + benefice

    wb_ventes.close()

    if len(introuvables) > 0:
        messagebox.showwarning(
            "Attention",
            "Ces médicaments n'existent plus dans le fichier médicaments :\n" + "\n".join(str(n) for n in introuvables))

    return liste_ventes, resume, len(liste_ventes), round(ca_total, 2), round(benefice_total, 2)


def sauvegarder_statistiques(liste_ventes, resume):
    wb = Workbook()

    ws1 = wb.active
    ws1.title = "VENTES DETAILEES"
    ws1.append(["ID", "N° SERIE", "Date", "Nom du Médicament", "Dosage (mg/ml)",
                "Quantité", "Prix d'Achat", "Prix de Vente", "CA", "Bénéfice"])
    for ligne in liste_ventes:
        ws1.append(ligne)

    ws2 = wb.create_sheet("RESUME PAR MEDICAMENT")
    ws2.append(["Nom du Médicament", "Quantité Totale", "CA Total", "Bénéfice Total"])
    for nom in resume:
        ws2.append([nom, resume[nom][0], resume[nom][1], resume[nom][2]])

    try:
        wb.save(FICHE_STATISTIQUE)
    except PermissionError:
        messagebox.showerror("Erreur", "Ferme le fichier STATISTIQUE.xlsx dans Excel puis réessaie")
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
    for item in treview_B_VENTS.get_children():
        treview_B_VENTS.delete(item)
    for item in treview_B_RESUME.get_children():
        treview_B_RESUME.delete(item)

    liste_ventes, resume, nb, ca_total, benefice_total = calculer_statistiques(mois, annee)

    for ligne in liste_ventes:
        treview_B_VENTS.insert("", "end", values=ligne)

    for nom in resume:
        treview_B_RESUME.insert("", "end", values=(nom, resume[nom][0], resume[nom][1], resume[nom][2]))

    sauvegarder_statistiques(liste_ventes, resume)

    return nb, ca_total, benefice_total