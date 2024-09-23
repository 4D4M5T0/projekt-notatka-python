import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self, host, user, password, database):
        try:
            self.conn = mysql.connector.connect(host=host, user=user, password=password)
            self.cursor = self.conn.cursor()

            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            self.conn.commit()

            self.conn.database = database

            self.create_tables()

        except Error as e:
            print(f"Błąd przy utworzeniu bazy lub połączeniu: {e}")
            self.conn = None

    def create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS uzytkownik (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    login VARCHAR(255) UNIQUE NOT NULL,
                    pass VARCHAR(255) NOT NULL
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS notatka (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tresc TEXT NOT NULL,
                    user_id INT,
                    FOREIGN KEY (user_id) REFERENCES uzytkownik(id) ON DELETE CASCADE,
                    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.conn.commit()

        except Error as e:
            print(f"Błąd przy utworzeniu tabel: {e}")
            self.conn = None

    def sprawdzanie(self, login, password):
        query = "SELECT * FROM uzytkownik WHERE login = %s AND pass = %s"
        self.cursor.execute(query, (login, password))
        user = self.cursor.fetchone()
        return user

    def wpisz_uzytkownika(self, login, password):
        try:
            query = "INSERT INTO uzytkownik (login, pass) VALUES (%s, %s)"
            self.cursor.execute(query, (login, password))
            self.conn.commit()
        except mysql.connector.IntegrityError:
            return False
        return True

    def get_uzytkownik_id(self, login):
        query = "SELECT id FROM uzytkownik WHERE login = %s"
        self.cursor.execute(query, (login,))
        user_id = self.cursor.fetchone()
        return user_id[0] if user_id else None

    def wypisz_notatki_uzytkownika(self, user_id):
        query = "SELECT * FROM notatka WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        notatki = self.cursor.fetchall()
        return notatki

    def wpisz_notatka(self, zawartosc, user_id):
        query = "INSERT INTO notatka (zawartosc, user_id) VALUES (%s, %s)"
        self.cursor.execute(query, (zawartosc, user_id))
        self.conn.commit()

    def usun_notatka(self, notatka_id):
        query = "DELETE FROM notatka WHERE id = %s"
        self.cursor.execute(query, (notatka_id,))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
