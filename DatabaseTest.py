import unittest
from unittest.mock import MagicMock, patch
from base import Database


class TestDatabase(unittest.TestCase):

    @patch('mysql.connector.connect')
    def setUp(self, mock_connect):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor

        self.db = Database(host="localhost", user="root", password="", database="test_db")

    def test_sprawdzanie(self):
        self.mock_cursor.fetchone.return_value = (1, "test_user", "hashed_password")

        result = self.db.sprawdzanie("test_user", "password")
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM uzytkownik WHERE login = %s AND pass = md5(%s)", ("test_user", "password"))
        self.assertEqual(result, (1, "test_user", "hashed_password"))

    def test_wpisz_uzytkownika(self):
        self.mock_cursor.execute.return_value = None
        self.mock_conn.commit.return_value = None

        result = self.db.wpisz_uzytkownika("new_user", "password")
        self.mock_cursor.execute.assert_called_once_with("INSERT INTO uzytkownik (login, pass) VALUES (%s, md5(%s))", ("new_user", "password"))
        self.assertTrue(result)

    def test_get_uzytkownik_id(self):
        self.mock_cursor.fetchone.return_value = (42,)

        user_id = self.db.get_uzytkownik_id("test_user")
        self.mock_cursor.execute.assert_called_once_with("SELECT id FROM uzytkownik WHERE login = %s", ("test_user",))
        self.assertEqual(user_id, 42)

    def test_wypisz_notatki_uzytkownika(self):
        self.mock_cursor.fetchall.return_value = [(1, "Notatka 1", 42), (2, "Notatka 2", 42)]

        notatki = self.db.wypisz_notatki_uzytkownika(42)
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM notatka WHERE user_id = %s", (42,))
        self.assertEqual(notatki, [(1, "Notatka 1", 42), (2, "Notatka 2", 42)])

    def test_wpisz_notatka(self):
        self.mock_cursor.execute.return_value = None
        self.mock_conn.commit.return_value = None

        self.db.wpisz_notatka("Nowa notatka", 42)
        self.mock_cursor.execute.assert_called_once_with("INSERT INTO notatka (text, user_id) VALUES (%s, %s)", ("Nowa notatka", 42))

    def test_usun_notatka(self):
        self.mock_cursor.execute.return_value = None
        self.mock_conn.commit.return_value = None

        self.db.usun_notatka(10)
        self.mock_cursor.execute.assert_called_once_with("DELETE FROM notatka WHERE id = %s", (10,))

    def tearDown(self):
        self.db.close()


if __name__ == '__main__':
    unittest.main()
