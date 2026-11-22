from openpyxl import load_workbook, Workbook
from tkinter import messagebox
import os
import hashlib
from themes import colors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FICHE_UTILISATEUR = os.path.join(BASE_DIR, "..", "UTILISATEUR.xlsx")





def initialise_fichier():
    if os.path.exists(FICHE_UTILISATEUR):
        wb = load_workbook(FICHE_UTILISATEUR)
        return wb, wb["Utilisateurs"]

    wb = Workbook()
    ws = wb.active
    ws.title = "Utilisateurs"
    ws["A1"] = "ID"
    ws["B1"] = "Nom de Utilisateur"
    ws["C1"] = "Mot de passe"
    ws["D1"] = "Rôle de l'Utilisateur"
    ws.append([1, "admin", hashlib.sha256("admin123".encode()).hexdigest(), "Admin"])
    wb.save(FICHE_UTILISATEUR)
    return wb, ws


def creation_utilisateur(treeview):
    wb, ws = initialise_fichier()

    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        treeview.insert("", "end", values=(row[0], row[1], "*******", row[3]))
    return wb, ws


def connexion(root, ent_user, ent_password):
    nom = ent_user.get().strip()
    mdp = ent_password.get()

    if nom == "" or mdp == "":
        messagebox.showwarning("Attention", "Remplis les champs")
        return

    mdp_hash = hashlib.sha256(mdp.encode()).hexdigest()
    wb, ws = initialise_fichier()

    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        if row[1] == nom and row[2] == mdp_hash:
            from view import dashbord
            dashbord.open_dashboard(root, row[3], row[1], colors.BG_MAIN, colors.COLOR_ENTRY, colors.COLOR_TEXT,
                                    colors.COLOR_BTN, colors.ECRITURE, colors.FONT_TITLE, colors.on_enter, colors.on_leave)
            return

    messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
    ent_password.delete(0, "end")


def enregistre_les_donnees(treeview, util_input, password, conf_password, les_choix, ws, wb):
    nom = util_input.get().strip()
    mdp = password.get()

    if nom == "" or mdp == "":
        messagebox.showinfo("Attention", "Remplis les champs")
        return

    if mdp != conf_password.get():
        messagebox.showinfo("Attention", "Les mots de passe ne correspondent pas !")
        return

    selection = treeview.selection()
    item_actuel = selection[0] if selection else None

    for item in treeview.get_children():
        if item != item_actuel and treeview.item(item, "values")[1] == nom:
            messagebox.showinfo("Attention", "Ce nom d'utilisateur existe déjà")
            return

    mdp_hash = hashlib.sha256(mdp.encode()).hexdigest()

    if item_actuel is None:
        numero = len(treeview.get_children()) + 1
        treeview.insert("", "end", values=(numero, nom, "*" * len(mdp), les_choix.get()))
        ws.append([numero, nom, mdp_hash, les_choix.get()])
    else:
        values = treeview.item(item_actuel, "values")
        treeview.item(item_actuel, values=(values[0], nom, "*" * len(mdp), les_choix.get()))
        row = treeview.index(item_actuel) + 2
        ws["B" + str(row)] = nom
        ws["C" + str(row)] = mdp_hash
        ws["D" + str(row)] = les_choix.get()
        treeview.selection_remove(item_actuel)

    util_input.delete(0, "end")
    password.delete(0, "end")
    conf_password.delete(0, "end")

    wb.save(FICHE_UTILISATEUR)


def modifie_utilisateur(treeview, util_input, password, les_choix, wb):
    selection = treeview.selection()

    if not selection:
        messagebox.showwarning("Attention", "Choisir un utilisateur")
        return

    values = treeview.item(selection[0], "values")

    util_input.delete(0, "end")
    util_input.insert(0, values[1])

    password.delete(0, "end")

    les_choix.set(values[3])

    messagebox.showinfo("Modifier", "Change les informations, écris le nouveau mot de passe, puis clique sur AJOUTER")


def supprime_utilisateur(treeview, ws, wb):
    selection = treeview.selection()

    if not selection:
        messagebox.showwarning("Attention", "Choisir un utilisateur")
        return

    if not messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet utilisateur ?"):
        return

    item = selection[0]
    row = treeview.index(item) + 2

    ws.delete_rows(row)
    treeview.delete(item)

    numero = 1
    for ligne in treeview.get_children():
        valeurs = list(treeview.item(ligne, "values"))
        valeurs[0] = numero
        treeview.item(ligne, values=valeurs)
        ws.cell(row=numero + 1, column=1, value=numero)
        numero += 1

    wb.save(FICHE_UTILISATEUR)