#================= LES COULEURS ===============
BG_MAIN = "#F1F9F3"
COLOR_ENTRY = "#E8EDEC"
COLOR_TEXT = "#3B7E76"
COLOR_BTN = "#5B9E96"
ECRITURE = "#1B1E1D"

#================= LA POLICE ===================
FONT_TITLE = ("Bookman old style", 20, "bold")

#================= EFFETS HOVER SUR LES BOUTONS =========
def on_enter(e):
    e.widget.config(bg="white", fg=COLOR_TEXT)

def on_leave(e):
    e.widget.config(bg=COLOR_BTN, fg=BG_MAIN)
