from tkinter import *
from tkinter import messagebox
import pandas as pd
import os

from themes import colors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FICHE_UTILISATEUR = os.path.join(BASE_DIR, "..", "UTILISATEUR.xlsx")

COLONNES_UTILISATEUR = [
    "Nom d'utilisateur",
    "Nom Complet",
    "Mot de passe",
    "Confirmer le Mot de passe",
    "Téléphone",
    "Rôle"
]

# ============================================================
# DATABASE - UTILISATEUR
# ============================================================
def bd_utilisateur():
    """Crée le fichier Excel avec un admin par défaut s'il n'existe pas."""
    if os.path.exists(FICHE_UTILISATEUR):
        return

    pd.DataFrame([{
        "Nom d'utilisateur"        : "mehdi",
        "Nom Complet"              : "mehdi",
        "Mot de passe"             : "1234",
        "Confirmer le Mot de passe": "1234",
        "Téléphone"                : "0612345678",
        "Rôle"                     : "Admin"
    }]).to_excel(FICHE_UTILISATEUR, index=False)


def enregistrer_utilisateur(ustil, nom, password, conf, tele, role):
    """Ajoute un nouvel utilisateur dans le fichier Excel."""
    if os.path.exists(FICHE_UTILISATEUR):
        df = pd.read_excel(FICHE_UTILISATEUR)
    else:
        df = pd.DataFrame(columns=COLONNES_UTILISATEUR)

    nouveau = pd.DataFrame([{
        "Nom d'utilisateur"        : ustil,
        "Nom Complet"              : nom,
        "Mot de passe"             : password,
        "Confirmer le Mot de passe": conf,
        "Téléphone"                : tele,
        "Rôle"                     : role
    }])

    df = pd.concat([df, nouveau], ignore_index=True)
    df.to_excel(FICHE_UTILISATEUR, index=False)


def verifier_login(username, password):
    """Vérifie les identifiants et retourne (True, role) ou (False, message)."""
    if not os.path.exists(FICHE_UTILISATEUR):
        return False, "Fichier introuvable"

    df = pd.read_excel(FICHE_UTILISATEUR)

    user = df[
        (df["Nom d'utilisateur"] == username) &
        (df["Mot de passe"].astype(str) == password)
    ]

    if not user.empty:
        return True, user.iloc[0]["Rôle"]

    return False, "Nom d'utilisateur ou mot de passe incorrect"


def connexion(root, ent_user, ent_password):
    from view import dashbord

    username = ent_user.get().strip()
    passw = ent_password.get().strip()

    if not username or not passw:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
        return

    succes, resultat = verifier_login(username, passw)

    if succes:
        dashbord.open_dashboard(
            root,
            resultat,      # role
            username,      # username
            colors.BG_MAIN,
            colors.COLOR_ENTRY,
            colors.COLOR_TEXT,
            colors.COLOR_BTN,
            colors.ECRITURE,
            colors.FONT_TITLE,
            colors.on_enter,
            colors.on_leave
        )
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")


# Crée le fichier utilisateur par défaut au chargement du module
bd_utilisateur()
