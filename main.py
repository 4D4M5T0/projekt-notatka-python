import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from base import Database

base = Database(host="localhost", user="root", password="", database="notatnik")
base.create_tables()


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

    haslo_label = ttk.Label(login_frame, text="Hasło:", font=("Arial", 12), background="#f0f0f0", foreground="#333")
    haslo_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    global haslo_entry
    haslo_entry = ttk.Entry(login_frame, show="*", font=("Arial", 12))
    haslo_entry.grid(row=1, column=1, padx=10, pady=5)

    log_btn = ttk.Button(login_frame, text="Zaloguj", style="TButton")
    log_btn.grid(row=0, column=2, padx=10, pady=10)

    rejestracja_btn = ttk.Button(login_frame, text="Zarejestruj", style="TButton")
    rejestracja_btn.grid(row=1, column=2, padx=10, pady=10)

    style.configure("TButton", font=("Arial", 12), padding=6, background="#5bc0de", foreground="white")
    style.map("TButton", background=[("active", "#0275d8")], foreground=[("active", "white")])


root = tk.Tk()
root.title("Notatnik")
root.geometry("415x500")
ikona = PhotoImage(file="ikona.png")
root.iconphoto(False, ikona)

okno_logowania()

root.mainloop()
