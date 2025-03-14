import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from base import Database
from main import Main

class TestMain(unittest.TestCase):
    def setUp(self):
        self.mock_root = MagicMock()
        self.mock_db = MagicMock()
        self.app = Main(self.mock_root)
        self.app.base = self.mock_db


        self.app.login_entry = MagicMock()
        self.app.has_entry = MagicMock()

    @patch("tkinter.messagebox.showerror")
    def test_logowanie_poprawne(self, mock_messagebox):
        self.app.login_entry.get.return_value = "test_user"
        self.app.has_entry.get.return_value = "password"

        self.mock_db.sprawdzanie.return_value = (1, "test_user", "hashed_password")

        with patch.object(self.app, "otwieranie_notatki") as mock_otwieranie:
            self.app.log()
            mock_otwieranie.assert_called_once_with("test_user")
            mock_messagebox.assert_not_called()

    @patch("tkinter.messagebox.showerror")
    def test_logowanie_niepoprawne(self, mock_messagebox):
        self.app.login_entry.get.return_value = "test_user"
        self.app.has_entry.get.return_value = "wrong_password"

        self.mock_db.sprawdzanie.return_value = None

        self.app.log()
        mock_messagebox.assert_called_once_with(title="Error", message="Błędny login lub hasło")

    @patch("tkinter.messagebox.showerror")
    def test_rejestracja_nowy_uzytkownik(self, mock_messagebox):
        self.app.login_entry.get.return_value = "new_user"
        self.app.has_entry.get.return_value = "password"

        self.mock_db.sprawdzanie.return_value = None

        with patch.object(self.app, "otwieranie_notatki") as mock_otwieranie:
            self.app.rejestracja()
            self.mock_db.wpisz_uzytkownika.assert_called_once_with("new_user", "password")
            mock_otwieranie.assert_called_once_with("new_user")
            mock_messagebox.assert_not_called()

    @patch("tkinter.messagebox.showerror")
    def test_rejestracja_istniejacy_uzytkownik(self, mock_messagebox):
        self.app.login_entry.get.return_value = "existing_user"
        self.app.has_entry.get.return_value = "password"

        self.mock_db.sprawdzanie.return_value = (1, "existing_user", "hashed_password")

        self.app.rejestracja()
        self.mock_db.wpisz_uzytkownika.assert_not_called()
        mock_messagebox.assert_called_once_with(title="Error", message="Użytkownik już istnieje")

    def test_wylogowywanie(self):
        mock_frame = MagicMock()

        with patch.object(self.app, "okno_logowania") as mock_logowanie:
            self.app.wylogowywanie(mock_frame)

            mock_frame.destroy.assert_called_once()

            mock_logowanie.assert_called_once()

        print("Udane wylogowanie")

    def test_dodawanie_notatki(self):
        self.app.login_entry.get.return_value = "test_user"

        self.mock_db.get_uzytkownik_id.return_value = 1
        self.mock_db.wpisz_notatka = MagicMock()

        notatka_entry = MagicMock()
        notatka_entry.get.return_value = "Nowa notatka"

        notatki_listbox = MagicMock()

        self.app.dodawanie_notatki(notatka_entry, "test_user", notatki_listbox)

        self.mock_db.wpisz_notatka.assert_called_once_with("Nowa notatka", 1)
        notatka_entry.delete.assert_called_once_with("1.0", tk.END)

    def test_usuwanie_notatki(self):
        self.app.login_entry.get.return_value = "test_user"

        self.mock_db.get_uzytkownik_id.return_value = 1
        self.mock_db.wypisz_notatki_uzytkownika.return_value = [(1, "Stara notatka")]

        self.mock_db.usun_notatka = MagicMock()

        notatka_entry = MagicMock()
        notatki_listbox = MagicMock()
        notatki_listbox.curselection.return_value = [0]

        self.app.usuwanie_notatki(notatki_listbox, notatka_entry, "test_user")

        self.mock_db.usun_notatka.assert_called_once_with(1)
        notatka_entry.delete.assert_called_once_with("1.0", tk.END)

    def test_wyswietlanie_notatek(self):
        self.app.login_entry.get.return_value = "test_user"

        self.mock_db.get_uzytkownik_id.return_value = 1
        self.mock_db.wypisz_notatki_uzytkownika.return_value = [(1, "Notatka1"), (2, "Notatka2")]

        notatki_listbox = MagicMock()

        self.app.wyswietlanie(notatki_listbox, "test_user")

        notatki_listbox.delete.assert_called_once_with(0, tk.END)
        notatki_listbox.insert.assert_any_call(tk.END, "Notatka1")
        notatki_listbox.insert.assert_any_call(tk.END, "Notatka2")


if __name__ == "__main__":
    unittest.main()
