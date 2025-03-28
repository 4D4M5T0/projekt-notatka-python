import unittest
from unittest.mock import MagicMock
from base import Database  # Zakładam, że masz plik database.py


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Tworzymy mock połączenia i kursora
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Tworzymy instancję Database z fałszywymi danymi
        self.db = Database(host="localhost", user="test_user", password="test_pass", database="test_db")

        # Podmieniamy prawdziwe połączenie na mock
        self.db.conn = self.mock_conn

        # Resetujemy mock przed każdym testem
        self.mock_cursor.reset_mock()

    def test_sprawdzanie(self):
        self.db.sprawdzanie("test_user", "password")
        self.mock_cursor.execute.assert_any_call(
            "SELECT * FROM uzytkownik WHERE login = %s AND pass = md5(%s)", ("test_user", "password")
        )

    def test_wpisz_uzytkownika(self):
        self.db.wpisz_uzytkownika("new_user", "password")
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO uzytkownik (login, pass) VALUES (%s, md5(%s))", ("new_user", "password")
        )

    def test_get_uzytkownik_id(self):
        self.db.get_uzytkownik_id("test_user")
        self.mock_cursor.execute.assert_any_call(
            "SELECT id FROM uzytkownik WHERE login = %s", ("test_user",)
        )

    def test_wypisz_notatki_uzytkownika(self):
        self.db.wypisz_notatki_uzytkownika(42)
        self.mock_cursor.execute.assert_any_call(
            "SELECT * FROM notatka WHERE user_id = %s", (42,)
        )

    def test_wpisz_notatka(self):
        self.db.wpisz_notatka("Nowa notatka", 42)
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO notatka (text, user_id) VALUES (%s, %s)", ("Nowa notatka", 42)
        )

    def test_usun_notatka(self):
        self.db.usun_notatka(10)
        self.mock_cursor.execute.assert_any_call(
            "DELETE FROM notatka WHERE id = %s", (10,)
        )


if __name__ == "__main__":
    unittest.main()
