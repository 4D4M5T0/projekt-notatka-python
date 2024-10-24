import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from base import Database

base = Database(host="localhost", user="root", password="", database="notatnik")
base.create_tables()


root = tk.Tk()
root.title("Notatnik")
root.geometry("415x500")
ikona = PhotoImage(file="ikona.png")
root.iconphoto(False, ikona)



def rejestracja():
    login = login_entry.get().strip()
    password = has_entry.get().strip()

    if login and password:
        if base.sprawdzanie(login, password):
            messagebox.showerror(title="Error", message="Użytkownik już istnieje")
        else:
            base.wpisz_uzytkownika(login, password)
            otwieranie_notatki(login)
    else:
        messagebox.showerror(title="Error", message="Wpisz login i hasło")


def log():
    login = login_entry.get().strip()
    password = has_entry.get().strip()

    user = base.sprawdzanie(login, password)

    if user:
        otwieranie_notatki(login)
    else:
        messagebox.showerror(title="Error", message="Błędny login lub hasło")


def otwieranie_notatki(login):
    login_frame.destroy()

    style = ttk.Style()
    style.theme_use("clam")

    root.configure(bg="#f0f0f0")

    notatnik_frame = tk.Frame(root, bg="#f0f0f0")
    notatnik_frame.pack(pady=20)

    tk.Label(notatnik_frame, text=f"Witaj, {login}", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)

    notatka_entry = tk.Text(notatnik_frame, height=5, width=30, font=("Arial", 12), relief="flat", bd=1)
    notatka_entry.pack(padx=10, pady=10)
    notatka_entry.config(highlightbackground="#c3c3c3", highlightthickness=1)

    dodaj_btn = ttk.Button(notatnik_frame, text="Dodaj notatkę", style="TButton",
                           command=lambda: dodawanie_notatki(notatka_entry, login, notatki_listbox))
    dodaj_btn.pack(padx=10, pady=5)

    usun_notatke_btn = ttk.Button(notatnik_frame, text="Usuń notatkę", style="TButton",
                                  command=lambda: usuwanie_notatki(notatki_listbox, notatka_entry, login))
    usun_notatke_btn.pack(padx=10, pady=5)

    notatki_listbox = tk.Listbox(notatnik_frame, height=5, width=40, font=("Arial", 12), relief="flat", bd=1)
    notatki_listbox.pack(padx=10, pady=10)
    notatki_listbox.config(highlightbackground="#c3c3c3", highlightthickness=1)

    notatki_listbox.bind('<<ListboxSelect>>',
                         lambda event: wyswietlanie_wybranej_notatki(notatki_listbox, notatka_entry, login))

    wylogowywanie_btn = ttk.Button(notatnik_frame, text="Wyloguj", style="TButton",
                                   command=lambda: wylogowywanie(notatnik_frame))
    wylogowywanie_btn.pack(pady=10)

    wyswietlanie(notatki_listbox, login)

    style.configure("TButton", font=("Arial", 12), padding=6, background="#5bc0de", foreground="white")
    style.map("TButton", background=[("active", "#0275d8")], foreground=[("active", "white")])


def dodawanie_notatki(notatka_entry, login, notatki_listbox):
    text = notatka_entry.get("1.0", tk.END).strip()
    if text:
        user_id = base.get_uzytkownik_id(login)
        base.wpisz_notatka(text, user_id)
        notatka_entry.delete("1.0", tk.END)
        wyswietlanie(notatki_listbox, login)
    else:
        messagebox.showerror(title="Error", message="Notatka nie może być pusta")


def wyswietlanie(notatki_listbox, login):
    notatki_listbox.delete(0, tk.END)
    user_id = base.get_uzytkownik_id(login)
    notatki = base.wypisz_notatki_uzytkownika(user_id)

    if not notatki:
        notatki_listbox.insert(tk.END, "Brak notatek")
    else:
        for notatka in notatki:
            short_text = (notatka[1][:41] + '...') if len(notatka[1]) > 30 else notatka[1]
            timestamp = notatka[3].strftime('%d-%m-%Y')
            notatki_listbox.insert(tk.END, f"{short_text}  {timestamp}")


def wyswietlanie_wybranej_notatki(notatki_listbox, notatka_entry, login):
    selected_index = notatki_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        user_id = base.get_uzytkownik_id(login)
        notatki = base.wypisz_notatki_uzytkownika(user_id)
        if selected_index < len(notatki):
            notatka_entry.delete("1.0", tk.END)
            notatka_entry.insert(tk.END, notatki[selected_index][1])


def usuwanie_notatki(notatki_listbox, notatka_entry, login):
    selected_index = notatki_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        user_id = base.get_uzytkownik_id(login)
        notatki = base.wypisz_notatki_uzytkownika(user_id)
        if selected_index < len(notatki):
            notatka_id = notatki[selected_index][0]
            base.usun_notatka(notatka_id)
            notatka_entry.delete("1.0", tk.END)
            wyswietlanie(notatki_listbox, login)


def wylogowywanie(notatnik_frame):
    notatnik_frame.destroy()
    okno_logowania()


def okno_logowania():
    global login_frame

    style = ttk.Style()
    style.theme_use("clam")

    root.configure(bg="#f0f0f0")

    login_frame = tk.Frame(root, bg="#f0f0f0")
    login_frame.pack(pady=20)

    login_label = ttk.Label(login_frame, text="Login:", font=("Arial", 12), background="#f0f0f0", foreground="#333")
    login_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    global login_entry
    login_entry = ttk.Entry(login_frame, font=("Arial", 12))
    login_entry.grid(row=0, column=1, padx=10, pady=5)

    has_label = ttk.Label(login_frame, text="Hasło:", font=("Arial", 12), background="#f0f0f0", foreground="#333")
    has_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    global has_entry
    has_entry = ttk.Entry(login_frame, show="*", font=("Arial", 12))
    has_entry.grid(row=1, column=1, padx=10, pady=5)

    log_btn = ttk.Button(login_frame, text="Zaloguj", style="TButton", command=log)
    log_btn.grid(row=0, column=2, padx=10, pady=10)

    rejestracja_btn = ttk.Button(login_frame, text="Zarejestruj", style="TButton", command=rejestracja)
    rejestracja_btn.grid(row=1, column=2, padx=10, pady=10)

    style.configure("TButton", font=("Arial", 12), padding=6, background="#5bc0de", foreground="white")
    style.map("TButton", background=[("active", "#0275d8")], foreground=[("active", "white")])


okno_logowania()

root.mainloop()
