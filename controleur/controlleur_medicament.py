from openpyxl import load_workbook, Workbook
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FICHIER_MEDICAMENTS = os.path.join(BASE_DIR, "..", "MEDICAMENTS.xlsx")
NOM_FEUILLE_MEDICAMENTS = "Medicaments"
SEUIL_STOCK_FAIBLE = 10


def _ouvrir_fichier_medicaments():
    if os.path.exists(FICHIER_MEDICAMENTS):
        wb = load_workbook(FICHIER_MEDICAMENTS)
        if NOM_FEUILLE_MEDICAMENTS in wb.sheetnames:
            ws = wb[NOM_FEUILLE_MEDICAMENTS]
        else:
            ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = NOM_FEUILLE_MEDICAMENTS
        ws["A1"] = "N°"
        ws["B1"] = "Nom du medicament"
        ws["C1"] = "Dossage (ml/mg)"
        ws["D1"] = "Categorie"
        ws["E1"] = "Quantite en stock"
        ws["F1"] = "Date expiration"
        ws["G1"] = "Prix d'achat"
        ws["H1"] = "Prix de vente"
        ws["I1"] = "Fournisseur"
        wb.save(FICHIER_MEDICAMENTS)

    return wb, ws


def lire_date(valeur):
    if isinstance(valeur, datetime):
        return valeur.date()
    try:
        return datetime.strptime(str(valeur), "%d/%m/%Y").date()
    except ValueError:
        return None


def medicament_controlleur(tableau_general):
    wb, ws = _ouvrir_fichier_medicaments()

    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        tableau_general.insert("", "end", values=row)

    return wb, ws


def validation_des_donnees(nom, dosage, quantite, date_ex, categorie, p_achat, p_vente, fourni):
    if (nom.strip() == "" or dosage.strip() == "" or quantite.strip() == "" or date_ex.strip() == ""
            or categorie == "" or p_achat.strip() == "" or p_vente.strip() == "" or fourni.strip() == ""):
        return False, "Remplis tous les champs !"

    try:
        quantite = int(quantite)
        p_achat = float(p_achat.replace(",", "."))
        p_vente = float(p_vente.replace(",", "."))
    except ValueError:
        return False, "La quantité et les prix doivent être des nombres !"

    if quantite < 0 or p_achat < 0 or p_vente < 0:
        return False, "La quantité et les prix ne peuvent pas être négatifs !"

    try:
        datetime.strptime(date_ex.strip(), "%d/%m/%Y")
    except ValueError:
        return False, "La date d'expiration doit être au format JJ/MM/AAAA !"

    valeurs = {
        "nom": nom.strip(),
        "dosage": dosage.strip(),
        "quantite": quantite,
        "date_ex": date_ex.strip(),
        "categorie": categorie,
        "p_achat": p_achat,
        "p_vente": p_vente,
        "fourni": fourni.strip(),
    }
    return True, valeurs


def enregistrer_medicament(wb, ws, tableau_general, nom, dosage, quantite,
                           date_ex, categorie, p_achat, p_vente, fourni):
    ok, resultat = validation_des_donnees(nom, dosage, quantite, date_ex,
                                          categorie, p_achat, p_vente, fourni)
    if not ok:
        return False, resultat

    v = resultat
    numero = len(tableau_general.get_children()) + 1
    valeurs = (numero, v["nom"], v["dosage"], v["categorie"], v["quantite"],
               v["date_ex"], v["p_achat"], v["p_vente"], v["fourni"])

    ws.append(valeurs)
    try:
        wb.save(FICHIER_MEDICAMENTS)
    except PermissionError:
        ws.delete_rows(ws.max_row)
        return False, "Ferme le fichier MEDICAMENTS.xlsx dans Excel puis réessaie"

    tableau_general.insert("", "end", values=valeurs)
    return True, None


def charger_medicaments_expires(ws, tableau_medicament):
    for item in tableau_medicament.get_children():
        tableau_medicament.delete(item)

    aujourdhui = datetime.now().date()

    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        date_expiration = lire_date(row[5])
        if date_expiration is not None and date_expiration < aujourdhui:
            tableau_medicament.insert("", "end", values=row)


def charger_stock_faible(ws, tableau_stock, seuil=SEUIL_STOCK_FAIBLE):
    for item in tableau_stock.get_children():
        tableau_stock.delete(item)

    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        try:
            quantite = int(row[4])
        except (ValueError, TypeError):
            continue
        if quantite <= seuil:
            tableau_stock.insert("", "end", values=row)