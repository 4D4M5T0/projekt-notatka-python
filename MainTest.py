import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from main import Main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.mock_root = MagicMock()
        self.mock_db = MagicMock()
        self.app = Main(self.mock_root)
        self.app.base = self.mock_db

        self.app.login_entry = MagicMock()
        self.app.has_entry = MagicMock()

    def tearDown(self):
        self.mock_root = None
        self.mock_db = None
        self.app = None

    @patch("tkinter.messagebox.showerror")
    def test_logowanie(self, mock_messagebox):
        # Ustawienie poprawnych danych logowania
        self.app.login_entry.get.return_value = "test_user"
        self.app.has_entry.get.return_value = "password"

        self.mock_db.sprawdzanie.return_value = (1, "test_user", "hashed_password")

        with patch.object(self.app, "otwieranie_notatki") as mock_otwieranie:
            self.app.log()  # Wywołanie logowania
            mock_otwieranie.assert_called_once_with("test_user")
            mock_messagebox.assert_not_called()

    @patch("tkinter.messagebox.showerror")
    def test_rejestracja(self, mock_messagebox):
        self.app.login_entry.get.return_value = "new_user"
        self.app.has_entry.get.return_value = "password"

        self.mock_db.sprawdzanie.return_value = None

        with patch.object(self.app, "otwieranie_notatki") as mock_otwieranie:
            self.app.rejestracja()
            self.mock_db.wpisz_uzytkownika.assert_called_once_with("new_user", "password")
            mock_otwieranie.assert_called_once_with("new_user")
            mock_messagebox.assert_not_called()

    def test_wylogowywanie(self):
        mock_frame = MagicMock()
        with patch.object(self.app, "okno_logowania") as mock_logowanie:
            self.app.wylogowywanie(mock_frame)
            mock_frame.destroy.assert_called_once()
            mock_logowanie.assert_called_once()

if __name__ == "__main__":
    unittest.main()
