import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk



Font_texte = ("Bookman Old Style", 11, "bold")

def utilisateur(content_frame, BG_MAIN, COLOR_TEXT, COLOR_ENTRY,ECRITURE, COLOR_BTN
                     ,clear_content ,on_enter,on_leave):
    clear_content()

    F1 = Frame(content_frame, bd=3, relief="groove", bg=BG_MAIN)
    F1.place(y=10, width=970, height=630)

    title = Label(F1, text=" ➜  GESTION DES UTILISATEURS ", font=("Bookman old style", 18, "bold"),
                  width=110, height=3, bg=COLOR_TEXT, fg=BG_MAIN)
    title.pack()

    Label(F1 , text="Nom de Utilisateur " , font=Font_texte , bg=BG_MAIN ).place(x=35 , y=110)
    util_input = Entry(F1 , font=Font_texte , highlightbackground="#5B9E96" , highlightthickness=2 , )
    util_input.place(x = 240 , y=110 , height=30)

    Label(F1 , text="Mote de passe" , font=Font_texte , bg=BG_MAIN ).place(x=50 , y=165)
    password = Entry(F1 , font=Font_texte , highlightbackground="#5B9E96" , highlightthickness=2 , show="*" )
    password.place(x = 240 , y=165 , height=30)

    Label(F1 , text="Confirmer le Mote de passe " , font=Font_texte , bg=BG_MAIN ).place(x=1 , y=220)
    conf_password = Entry(F1 , font=Font_texte , highlightbackground="#5B9E96" , highlightthickness=2 , show="*"  )
    conf_password.place(x = 240 , y=220 , height=30)

    Label(F1 , text="Rôle de l'Utilisateur " , font=Font_texte , bg=BG_MAIN ).place(x=30 , y=278)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox", font=("Bookman old style", 11),
                    background=COLOR_ENTRY, foreground=ECRITURE, arrowcolor=ECRITURE,
                            relief="groove", borderwidth=2)
    style.map("TCombobox",fieldbackground=[("readonly", COLOR_ENTRY)],
                            foreground=[("readonly", ECRITURE)])
    
    les_choix = ["Admin", "Utilisateur"]
    
    les_choix = ttk.Combobox(F1, values=les_choix,font=("Bookman old style", 11),state="readonly", width=20)
    les_choix.place(x=240 , y=278 , height=30)
    les_choix.option_add("*TCombobox*Listbox.font",("Bookman old style", 11))
    les_choix.option_add("*TCombobox*Listbox.background",      COLOR_ENTRY)
    les_choix.option_add("*TCombobox*Listbox.foreground",      ECRITURE)
    les_choix.option_add("*TCombobox*Listbox.selectBackground", ECRITURE)
    les_choix.option_add("*TCombobox*Listbox.selectForeground", COLOR_ENTRY)
    les_choix.current(0)

    F2 = Frame(F1, width=450 , height=200 , relief="groove" , border=5)
    F2.place(x=480 , y=110)
    original_img = Image.open("images/img3.png")
    resize_original = original_img.resize((400, 190))
    img_final = ImageTk.PhotoImage(resize_original)
    img_label = Label(F2, image=img_final)
    img_label.image = img_final
    img_label.pack(expand=True)

    F3 = Frame(F1, width=800 , height=260 , bg=BG_MAIN )
    F3.place(x=70 , y=330)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=("Bookman Old Style", 8, "bold"),background=BG_MAIN)

    style.configure("Treeview",font=("Bookman old style", 8),background=BG_MAIN )

    treeview = ttk.Treeview(F3 , columns=(1,2,3,4,5) , height=11, show="headings", style="Treeview")

    sc = ttk.Scrollbar(F3, orient="vertical" , command=treeview.yview)
    sc.place( x= 775 , y= 5 , height=248)
    treeview.config(yscrollcommand=sc.set)
                
    treeview.heading(1, text="N°")
    treeview.heading(2, text="Nom de Utilisateur ")
    treeview.heading(3, text="Mote de passe")
    treeview.heading(4, text="Confirmer le Mote de passe")
    treeview.heading(5, text="Rôle de l'Utilisateur")

    treeview.column(1, width=50)
    treeview.column(2, width=180)
    treeview.column(3, width=180)
    treeview.column(4, width=180)
    treeview.column(5, width=180)               
    treeview.place(x=1, y=5)




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