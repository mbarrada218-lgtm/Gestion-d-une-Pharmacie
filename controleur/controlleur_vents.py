from openpyxl import load_workbook, Workbook
from datetime import datetime
from tkinter import messagebox
import os

from controleur.controlleur_medicament import ( _ouvrir_fichier_medicaments,FICHIER_MEDICAMENTS)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FICHE_VENTES = os.path.join(BASE_DIR, "..", "VENTS.xlsx")
# ============================================================
#                    NUMERO DE SERIE
# ============================================================

numero = 1
def generer_serie(ws):
    global numero
    if numero == 1:
        for row in ws.iter_rows(min_row=2,min_col=2,max_col=2,values_only=True):
            serie = row[0]
            if serie:
                numero = int(serie[3:]) + 1
    return f"MED{numero:05d}"

# ============================================================
#                    CREATION FICHIER EXCEL
# ============================================================

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
        tableau_historique.insert( "", "end", values=row)
    return wb, ws
# ============================================================
#                    RECHERCHER MEDICAMENT
# ============================================================

def rechercher_medicament(RECH, NOM, DOSAGE, STOCK, PR_VENT):
    terme = RECH.get().strip()
    if terme == "":
        messagebox.showinfo("Attention","Veuillez saiser le Nom du Médicament")
        return

    if terme.isdigit():
        messagebox.showinfo("Attention","Le Nom de Médicament ne doit pas contenir uniquement des Chiffres")
        return
    symboles = "@.,&<>*/\\!?#$%"

    if any(caractere in symboles for caractere in terme):
        messagebox.showinfo("Attention","Le Nom du Médicament Contient des caractères non autorisés")
        return
    try:
        wb_med, ws_med = _ouvrir_fichier_medicaments()
    except Exception as e:
        messagebox.showerror("Erreur",f"Impossible de lire MEDICAMENTS.xlsx : {e}")
        return

    terme_lower = terme.lower()
    for row in ws_med.iter_rows(min_row=2, values_only=True):
        nom_medicament = row[1]
        if (nom_medicament is not None and terme_lower in str(nom_medicament).lower()):

            NOM.config(state="normal")
            NOM.delete(0, "end")
            NOM.insert(0, row[1])

            DOSAGE.config(state="normal")
            DOSAGE.delete(0, "end")
            DOSAGE.insert(0, row[2])

            STOCK.config(state="normal")
            STOCK.delete(0, "end")
            STOCK.insert(0, row[4])

            PR_VENT.config(state="normal")
            PR_VENT.delete(0, "end")
            PR_VENT.insert(0, row[7])

            return

    messagebox.showinfo("Attention","Le produit n'existe pas")
# ============================================================
#                    TOTAL GENERALE
# ============================================================
def change_totale (tableau_panier , total_var):
    total_general = 0
    for item in tableau_panier.get_children():
        value = tableau_panier.item(item, "values")
        prix_vents = float(value [4])
        quantite = int(value[3])
        total = prix_vents * quantite
        total_general = total_general + total

    total_var.set(f"{total_general:.2f}")
# ============================================================
#                    AJOUTER AU PANIER
# ============================================================

def ajouter_au_panier(RECH,NOM,DOSAGE,STOCK,PR_VENT,QUAN,ws,tableau_panier , total_var):
    if STOCK.get() == "":
        messagebox.showinfo("Attention" , "Remplis les champs")
        return

    stock = int(STOCK.get())
    quantite = QUAN.get()
    
    if RECH == "" :
        messagebox.showinfo("Attention " , "Remplis les champs")
        return
    
    if not quantite.isdigit():
        messagebox.showinfo("Attention","La Quantité ne doit pas contenir uniquement des Chiffres")
        return

    if stock < int(quantite):

        messagebox.showinfo("Attention","Attention la Quantite grand")
        return

    numero_serie = generer_serie(ws)
    tableau_panier.insert("","end",values=(numero_serie,NOM.get(),DOSAGE.get(),quantite,PR_VENT.get()))
    change_totale (tableau_panier , total_var)
    RECH.delete(0, "end")
    NOM.delete(0, "end")
    DOSAGE.delete(0, "end")
    STOCK.delete(0, "end")
    PR_VENT.delete(0, "end")
    QUAN.delete(0, "end")

# ============================================================
#                    ORDONNANCE
# ============================================================

def sur_ordonanace(type_vente, NOM_CLIENT, MEDECIN, N_ORD):

    nom_client = NOM_CLIENT.get()
    medecin = MEDECIN.get()
    n_ord = N_ORD.get()

    symboles = "@.,&<>*/\\!?#$%"

    for terme in [nom_client, medecin, n_ord]:

        if any(caractere in symboles for caractere in terme):
            messagebox.showinfo("Attention","Veuillez Vérifier le champs sur Ordonnance : Contient des caractères non autorisés")
            return False

    if n_ord == "":
        messagebox.showinfo("Attention","Veuillez remplir les informations de l'ordonnance")
        return False

    elif nom_client.isdigit()or medecin.isdigit()or not n_ord.isdigit():
        messagebox.showinfo("Attention","Veuillez vérifier les données")
        return False
    
    return True


def decrement_stock (tableau_panier) : 
    try : 
        wb_med , ws_med = _ouvrir_fichier_medicaments()
    except Exception as e :
        messagebox.showerror("Erreur",f"Impossible de lire MEDICAMENTS.xlsx : {e}")
        return
    for item in tableau_panier.get_children():
        value = tableau_panier.item(item , "values")
        nom_med_tb = value[1]
        quantite_tbl = value[3]

    for row in ws_med.iter_rows(min_row=2) :
        nom_medicament = row [1].value
        quantite_med = row[4].value

        if nom_med_tb == nom_medicament : 
            nouvelle_stock = int(quantite_med) - int(quantite_tbl)
            row[4].value = nouvelle_stock
            break
    wb_med.save(FICHIER_MEDICAMENTS)

# ============================================================
#                    VALIDER HISTORIQUE
# ============================================================

def validation_de_historique(tableau_panier,type_vente,tableau_historique,NOM_CLIENT,MEDECIN,N_ORD, ws,wb):
    global numero
    ID = len(tableau_historique.get_children()) + 1
    DATE_VENTE = datetime.now().strftime("%d/%m/%Y %H:%M")

    # ========================================================
    #                    VENTE SIMPLE
    # ========================================================

    if type_vente.get() == "simple":
        for ligne in tableau_panier.get_children():
            value = tableau_panier.item(ligne,"values")
            tableau_historique.insert("","end",values=(ID,value[0],DATE_VENTE,
                                                       value[1],value[2],value[4],value[3],"-","-","-"))
            ws.append([ID,value[0],DATE_VENTE,value[1],value[2],value[4],value[3],"-","-","-"])
            ID += 1
    # ========================================================
    #                    VENTE ORDONNANCE
    # ========================================================
    elif type_vente.get() == "ordonnance":

        if not sur_ordonanace(type_vente,NOM_CLIENT,MEDECIN,N_ORD):
            return

        nom_client = NOM_CLIENT.get()
        medecin = MEDECIN.get()
        n_ord = N_ORD.get()

        for ligne in tableau_panier.get_children():
            value = tableau_panier.item(ligne,"values")
            tableau_historique.insert("","end",values=(ID,value[0],DATE_VENTE,value[1],
                                                       value[2],value[4],value[3],medecin,n_ord,nom_client))
            
            ws.append([ID,value[0],DATE_VENTE,value[1],value[2],value[4],
                       value[3],medecin,n_ord,nom_client])
            ID += 1
    decrement_stock(tableau_panier)
    # ========================================================
    #                    NOUVELLE SERIE
    # ========================================================
    numero += 1
    # ========================================================
    #                    VIDER PANIER
    # ========================================================
    for item in tableau_panier.get_children():
        tableau_panier.delete(item)
    NOM_CLIENT.delete(0, "end")
    MEDECIN.delete(0, "end")
    N_ORD.delete(0, "end")

    wb.save(FICHE_VENTES)
# ============================================================
#                    ANNULER PANIER ET LES CHAMPS
# ============================================================
def annuler(tableau_panier , RECH,NOM,DOSAGE,STOCK,PR_VENT,QUAN , NOM_CLIENT , MEDECIN , N_ORD):
    for item in tableau_panier.get_children():
        tableau_panier.delete(item)
    RECH.delete(0,"end")
    NOM.delete(0,"end")
    DOSAGE.delete(0,"end")
    STOCK.delete(0,"end")
    PR_VENT.delete(0,"end")
    QUAN.delete(0,"end")
    NOM_CLIENT.delete(0,"end")
    MEDECIN.delete(0,"end")
    N_ORD.delete(0,"end")



        





    