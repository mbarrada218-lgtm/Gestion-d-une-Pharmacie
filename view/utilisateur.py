import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

Font_texte = ("Bookman Old Style", 11, "bold")

def utilisateur(content_frame, BG_MAIN, COLOR_TEXT, COLOR_ENTRY,ECRITURE, COLOR_BTN
                     ,clear_content ,on_enter,on_leave):
    clear_content()

    F1 = Frame(content_frame, bd=3, relief="groove", bg=BG_MAIN)
    F1.place(y=10, width=970, height=630)

    title = Label(F1, text=" ➜  GESTION DES UTILISATEURS ", font=("Bookman old style", 18, "bold"),
                  width=110, height=3, bg=COLOR_TEXT, fg=BG_MAIN)
    title.pack()

    Label(F1 , text="Nom de Utilisateur " , font=Font_texte , bg=BG_MAIN ).place(x=35 , y=115)
    util_input = Entry(F1 , font=Font_texte , highlightbackground="#5B9E96" , highlightthickness=2 , )
    util_input.place(x = 240 , y=110 , height=30)

    Label(F1 , text="Mote de passe" , font=Font_texte , bg=BG_MAIN ).place(x=50 , y=155)
    password = Entry(F1 , font=Font_texte , highlightbackground="#5B9E96" , highlightthickness=2 , show="*" )
    password.place(x = 240 , y=150 , height=30)

    Label(F1 , text="Confirmer le Mote de passe " , font=Font_texte , bg=BG_MAIN ).place(x=1 , y=195)
    conf_password = Entry(F1 , font=Font_texte , highlightbackground="#5B9E96" , highlightthickness=2 , show="*"  )
    conf_password.place(x = 240 , y=190 , height=30)

    Label(F1 , text="Rôle de l'Utilisateur " , font=Font_texte , bg=BG_MAIN ).place(x=30 , y=230)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox", font=("Bookman old style", 11),
                    background=COLOR_ENTRY, foreground=ECRITURE, arrowcolor=ECRITURE,
                            relief="groove", borderwidth=2)
    style.map("TCombobox",fieldbackground=[("readonly", COLOR_ENTRY)],
                            foreground=[("readonly", ECRITURE)])
    
    les_choix = ["Admin", "Utilisateur"]
    
    les_choix = ttk.Combobox(F1, values=les_choix,font=("Bookman old style", 11),state="readonly", width=20)
    les_choix.place(x=240 , y=230 , height=30)
    les_choix.option_add("*TCombobox*Listbox.font",("Bookman old style", 11))
    les_choix.option_add("*TCombobox*Listbox.background",      COLOR_ENTRY)
    les_choix.option_add("*TCombobox*Listbox.foreground",      ECRITURE)
    les_choix.option_add("*TCombobox*Listbox.selectBackground", ECRITURE)
    les_choix.option_add("*TCombobox*Listbox.selectForeground", COLOR_ENTRY)
    les_choix.current(0)



if __name__ == "__main__":
    root = Tk()
    root.title("Test - Gestion des Médicaments")
    root.geometry("1000x600+100+20")

    BG_MAIN = "#F1F9F3"
    COLOR_ENTRY = "#E8EDEC"
    COLOR_TEXT = "#3B7E76"
    COLOR_BTN = "#5B9E96"
    ECRITURE = "#1B1E1D"

    content_frame = Frame(root, bg=BG_MAIN)
    content_frame.pack(fill=BOTH, expand=True)

    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    def on_enter(event):
        event.widget.config(bg="#5a5a80")

    def on_leave(event):
        event.widget.config(bg=COLOR_BTN)

    utilisateur(content_frame, BG_MAIN, COLOR_TEXT, COLOR_ENTRY,
                     ECRITURE, COLOR_BTN, clear_content, on_enter, on_leave)

    root.mainloop()