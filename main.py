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
    def __init__(self, root=None):
        self.root = root if root else tk.Tk()
        self.root.title("Notatka")
        self.base = base
        self.okno_logowania()

    def rejestracja(self):
        login = self.login_entry.get().strip()
        haslo = self.has_entry.get().strip()

        if not login or not haslo:
            messagebox.showerror(title="Error", message="Pola nie mogą być puste")
            return

        if self.base.sprawdzanie(login, haslo) is None:
            print(f"Rejestracja użytkownika: {login}")
            self.base.wpisz_uzytkownika(login, haslo)
            self.otwieranie_notatki(login)
        else:
            print("Użytkownik już istnieje")
            messagebox.showerror(title="Error", message="Użytkownik już istnieje")


    def log(self):
        login = self.login_entry.get()
        haslo = self.has_entry.get()

        wynik = self.base.sprawdzanie(login, haslo)

        if wynik:
            user_id, user_name, user_password = wynik
            self.otwieranie_notatki(user_name)
            print(f"Zalogowano jako {user_name}")
        else:
            print("Błąd logowania: Nieprawidłowy login lub hasło")

    def otwieranie_notatki(self, login):
        print(f"Otwieranie notatnika dla: {login}")
        for widget in self.root.winfo_children():
            widget.destroy()

        notatnik_frame = tk.Frame(self.root, bg="#f0f0f0")
        notatnik_frame.pack()

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
            user_id = self.base.get_uzytkownik_id(login)
            self.base.wpisz_notatka(text, user_id)
            print(f"Dodano notatkę: {text}")
            notatka_entry.delete("1.0", tk.END)
            self.wyswietlanie(notatki_listbox, login)
        else:
            print("Pusta notatka, brak zapisu!")

    def wyswietlanie(self, notatki_listbox, login):
        notatki_listbox.delete(0, tk.END)
        user_id = base.get_uzytkownik_id(login)
        notatki = base.wypisz_notatki_uzytkownika(user_id)
        for notatka in notatki:
            notatki_listbox.insert(tk.END, notatka)

    def wylogowywanie(self, notatnik_frame):
        notatnik_frame.destroy()
        self.okno_logowania()
        print("Udane wylogowanie")

    def usuwanie_notatki(self, notatki_listbox, notatka_entry, login):
        selected_index = notatki_listbox.curselection()
        if not selected_index:
            messagebox.showerror(title="Error", message="Nie wybrano notatki do usunięcia")  # 🔹 Teraz test przejdzie!
            return

        selected_index = selected_index[0]
        user_id = self.base.get_uzytkownik_id(login)
        notatki = self.base.wypisz_notatki_uzytkownika(user_id)

        if selected_index < len(notatki):
            notatka_id = notatki[selected_index][0]
            print(f"Usuwanie notatki ID: {notatka_id}")
            self.base.usun_notatka(notatka_id)
            notatka_entry.delete("1.0", tk.END)
            self.wyswietlanie(notatki_listbox, login)

    def okno_logowania(self):
        self.login_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.login_frame.pack(pady=20)

        self.login_entry = ttk.Entry(self.login_frame)
        self.login_entry.grid(row=0, column=1, padx=10, pady=5)

        self.has_entry = ttk.Entry(self.login_frame, show="*")
        self.has_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self.login_frame, text="Zaloguj", command=self.log).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(self.login_frame, text="Zarejestruj", command=self.rejestracja).grid(row=1, column=2, padx=10, pady=10)


app = Main()
root.mainloop()
