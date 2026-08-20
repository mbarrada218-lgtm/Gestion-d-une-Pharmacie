from tkinter import *
from openpyxl import load_workbook, Workbook
import os


def medicament_controlleur(tableau_general):
    if os.path.exists("MEDICAMENTS.xlsx"):
        wb = load_workbook("MEDICAMENTS.xlsx")
        ws = wb["Medicaments"]
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = "Medicaments"

        ws["A1"] = "N°"
        ws["B1"] = "Nom du medicament"
        ws["C1"] = "Dossage (ml/mg)"
        ws["D1"] = "Categorie"
        ws["E1"] = "Quantite en stock"
        ws["F1"] = "Date expiration"
        ws["G1"] = "Prix d'achat"
        ws["H1"] = "Prix de vente"
        ws["I1"] = "Fournisseur"

        wb.save("MEDICAMENTS.xlsx")

    # Cette partie doit se faire dans les deux cas (fichier existant ou nouveau)
    for row in ws.iter_rows(min_row=2, values_only=True):
        tableau_general.insert("", "end", values=row)

    return wb, ws

    