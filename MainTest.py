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

    @patch("builtins.print")
    def test_logowanie(self, mock_print):
        self.app.login_entry.get.return_value = "test_user"
        self.app.has_entry.get.return_value = "password"

        self.mock_db.sprawdzanie.return_value = (1, "test_user", "hashed_password")

        with patch.object(self.app, "otwieranie_notatki") as mock_otwieranie:
            self.app.log()
            mock_otwieranie.assert_called_once_with("test_user")
            mock_print.assert_called_once_with("Zalogowano jako test_user")

    @patch("builtins.print")
    def test_rejestracja(self, mock_print):
        self.app.login_entry.get.return_value = "new_user"
        self.app.has_entry.get.return_value = "password"

        self.mock_db.sprawdzanie.return_value = None

        with patch.object(self.app, "otwieranie_notatki") as mock_otwieranie:
            self.app.rejestracja()
            self.mock_db.wpisz_uzytkownika.assert_called_once_with("new_user", "password")
            mock_otwieranie.assert_called_once_with("new_user")
            mock_print.assert_called_once_with("Rejestracja użytkownika: new_user")

    @patch("builtins.print")
    def test_wylogowywanie(self, mock_print):
        mock_frame = MagicMock()
        with patch.object(self.app, "okno_logowania") as mock_logowanie:
            self.app.wylogowywanie(mock_frame)
            mock_frame.destroy.assert_called_once()
            mock_logowanie.assert_called_once()
            mock_print.assert_called_once_with("Udane wylogowanie")


if __name__ == "__main__":
    unittest.main()
