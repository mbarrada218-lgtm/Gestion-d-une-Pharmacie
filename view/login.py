from tkinter import *


#================= APPLICATION  =========
def login(BG_MAIN, COLOR_ENTRY, COLOR_TEXT, COLOR_BTN, ECRITURE, FONT_TITLE, on_enter, on_leave):
    from controleur import controlleur_login

    root = Tk()
    root.title("PROJET S1-DEV - MIAGE")
    root.geometry("1100x700+70+10")
    root.resizable(FALSE, FALSE)
    root.config(bg=BG_MAIN)

    # =================== TITRE ===================
    Label(root, text=" ✚ GESTION D'UNE PHARMACIE",
          font=("Bookman Old Style", 22, "bold"),
          height=4, fg=COLOR_TEXT, bg=BG_MAIN).pack()

    separator = Frame(root, height=2, width=200, bg=COLOR_TEXT)
    separator.pack(pady=1)

    Label(root, text="╰┈➤ BIENVENUE SUR VOTRE APPLICATION",
          font=("Bookman Old Style", 9, "bold"),
          fg=COLOR_TEXT, bg=BG_MAIN).pack(pady=20)

    # =================== LOGIN UI ===================
    fram = Frame(root, bg=BG_MAIN, width=400, height=390, relief="raised", bd=2)
    fram.pack()
    fram.pack_propagate(False)

    Label(fram, text=" 👥  Nom d'utilisateur", font=("Bookman Old Style", 12, "bold"),
          bg=BG_MAIN, fg=COLOR_TEXT).pack(pady=20)

    ent_user = Entry(fram, font=("Bookman old style", 11), width=25,
                      relief="raised", bd=2, bg=COLOR_ENTRY, fg=ECRITURE, state="normal")
    ent_user.pack(ipady=7)

    Label(fram, text=" 🔒  Mot de passe", font=("Bookman Old Style", 12, "bold"),
          bg=BG_MAIN, fg=COLOR_TEXT).pack(pady=20)

    ent_password = Entry(fram, font=("Bookman old style", 11), width=25,
                          relief="raised", bd=2, bg=COLOR_ENTRY, fg=ECRITURE, show="*", state="normal")
    ent_password.pack(ipady=7)

    B0 = Button(fram, text="SE CONNECTER ➜]", font=("Bookman Old Style", 10, "bold"),
                bg=COLOR_TEXT, fg=BG_MAIN, relief="raised", height=2,
                command=lambda: controlleur_login.connexion(root, ent_user, ent_password))
    B0.pack(pady=40)
    B0.bind("<Enter>", on_enter)
    B0.bind("<Leave>", on_leave)

    Frame(fram, height=2, width=100, bg=COLOR_TEXT).pack(pady=5)

    y = -300
    def slide():
        nonlocal y
        if y < 220:
            y += 10
            fram.place(x=350, y=y)
            root.after(5, slide)

    slide()
    root.mainloop()
