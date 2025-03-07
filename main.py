import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from base import Database

base = Database(host="localhost", user="root", password="", database="notatnik")
base.create_tables()

root = tk.Tk()
root.title("Notatnik")
root.geometry("415x500")
ikona = PhotoImage(file="ikona.png")
root.iconphoto(False, ikona)


class Main:
    def __init__(self):
        self.okno_logowania()

    def rejestracja(self):
        login = self.login_entry.get().strip()
        password = self.has_entry.get().strip()

        if login and password:
            if base.sprawdzanie(login, password):
                messagebox.showerror(title="Error", message="Użytkownik już istnieje")
            else:
                base.wpisz_uzytkownika(login, password)
                self.otwieranie_notatki(login)
        else:
            messagebox.showerror(title="Error", message="Wpisz login i hasło")

    def log(self):
        login = self.login_entry.get().strip()
        password = self.has_entry.get().strip()

        user = base.sprawdzanie(login, password)

        if user:
            self.otwieranie_notatki(login)
        else:
            messagebox.showerror(title="Error", message="Błędny login lub hasło")

    def otwieranie_notatki(self, login):
        self.login_frame.destroy()

        notatnik_frame = tk.Frame(root, bg="#f0f0f0")
        notatnik_frame.pack(pady=20)

        tk.Label(notatnik_frame, text=f"Witaj, {login}", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=10)

        notatka_entry = tk.Text(notatnik_frame, height=5, width=30, font=("Arial", 12))
        notatka_entry.pack(padx=10, pady=10)

        notatki_listbox = tk.Listbox(notatnik_frame, height=5, width=40, font=("Arial", 12))
        notatki_listbox.pack(padx=10, pady=10)

        ttk.Button(notatnik_frame, text="Dodaj notatkę",
                   command=lambda: self.dodawanie_notatki(notatka_entry, login, notatki_listbox)).pack(pady=5)

        ttk.Button(notatnik_frame, text="Usuń notatkę",
                   command=lambda: self.usuwanie_notatki(notatki_listbox, notatka_entry, login)).pack(pady=5)

        ttk.Button(notatnik_frame, text="Wyloguj",
                   command=lambda: self.wylogowywanie(notatnik_frame)).pack(pady=10)

        self.wyswietlanie(notatki_listbox, login)

    def dodawanie_notatki(self, notatka_entry, login, notatki_listbox):
        text = notatka_entry.get("1.0", tk.END).strip()
        if text:
            user_id = base.get_uzytkownik_id(login)
            base.wpisz_notatka(text, user_id)
            notatka_entry.delete("1.0", tk.END)
            self.wyswietlanie(notatki_listbox, login)

    def wyswietlanie(self, notatki_listbox, login):
        notatki_listbox.delete(0, tk.END)
        user_id = base.get_uzytkownik_id(login)
        notatki = base.wypisz_notatki_uzytkownika(user_id)
        for notatka in notatki:
            notatki_listbox.insert(tk.END, notatka[1])

    def wylogowywanie(self, notatnik_frame):
        notatnik_frame.destroy()
        self.okno_logowania()

    def usuwanie_notatki(self, notatki_listbox, notatka_entry, login):
        selected_index = notatki_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            user_id = base.get_uzytkownik_id(login)
            notatki = base.wypisz_notatki_uzytkownika(user_id)
            if selected_index < len(notatki):
                notatka_id = notatki[selected_index][0]
                base.usun_notatka(notatka_id)
                notatka_entry.delete("1.0", tk.END)
                self.wyswietlanie(notatki_listbox, login)

    def okno_logowania(self):
        self.login_frame = tk.Frame(root, bg="#f0f0f0")
        self.login_frame.pack(pady=20)

        self.login_entry = ttk.Entry(self.login_frame)
        self.login_entry.grid(row=0, column=1, padx=10, pady=5)

        self.has_entry = ttk.Entry(self.login_frame, show="*")
        self.has_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self.login_frame, text="Zaloguj", command=self.log).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(self.login_frame, text="Zarejestruj", command=self.rejestracja).grid(row=1, column=2, padx=10, pady=10)


app = Main()
root.mainloop()
