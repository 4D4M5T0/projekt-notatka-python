import mysql.connector
from mysql.connector import Error
import bcrypt


class Database:
    def __init__(self, host, user, password, database):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Error as e:
            print(f"Error: {e}")
            self.conn = None

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                login VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notatki (
                id INT AUTO_INCREMENT PRIMARY KEY,
                zawartosc TEXT NOT NULL,
                user_id INT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

        def rejestracja(login, password):
            cursor = self.conn.cursor()

            cursor.execute("SELECT * FROM user WHERE login = %s", (login,))
            if cursor.fetchone():
                print("Użytkownik o podanym loginie już istnieje.")
                return

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            cursor.execute("INSERT INTO user (login, password) VALUES (%s, %s)", (login, hashed_password))
            self.conn.commit()
            print("Rejestracja zakończona sukcesem.")
            self.conn.close()

        def logowanie(login, password):
            cursor = self.conn.cursor()

            cursor.execute("SELECT * FROM user WHERE login = %s", (login,))
            user = cursor.fetchone()

            if user:
                userid, _, hashed_password = user
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    print("Logowanie zakończone sukcesem.")
                    self.conn.close()
                    return userid
                else:
                    print("Błędne hasło.")
            else:
                print("Nie znaleziono użytkownika.")

            self.conn.close()
            return None

        def wyswietlanie_notatki(userid):
            cursor = self.conn.cursor()

            cursor.execute("SELECT * FROM notatki WHERE user_id = %s", (userid,))
            notes = cursor.fetchall()

            if notes:
                for note in notes:
                    print(f"ID: {note[0]}, Timestamp: {note[1]}, Text: {note[2]}")
            else:
                print("Brak notatek.")

            self.conn.close()

        def dodawanie_notatki(userid, text):
            cursor = self.conn.cursor()

            cursor.execute("INSERT INTO notatki (text, user_id) VALUES (%s, %s)", (text, userid))
            self.conn.commit()
            print("Dodano nową notatkę.")

            self.conn.close()

        def usuwanie_notatki(note_id, userid):
            cursor = self.conn.cursor()

            cursor.execute("DELETE FROM notatki WHERE id = %s AND user_id = %s", (note_id, userid))
            self.conn.commit()

            if cursor.rowcount > 0:
                print("Notatka została usunięta.")
            else:
                print("Nie znaleziono notatki do usunięcia.")

            self.conn.close()

        def edycja_notatki(note_id, userid, new_text):
            cursor = self.conn.cursor()

            cursor.execute("UPDATE notatki SET text = %s WHERE id = %s AND user_id = %s", (new_text, note_id, userid))
            self.conn.commit()

            if cursor.rowcount > 0:
                print("Notatka została zaktualizowana.")
            else:
                print("Nie znaleziono notatki do edycji.")

            self.conn.close()


if __name__ == "__main__":
    rejestracja("user1", "password123")

    # Logowanie
    user_id = logowanie("user1", "password123")

    if user_id:
        # Dodawanie notatki
        dodawanie_notatki(user_id, "Moja pierwsza notatka.")

        # Wyświetlanie notatek
        wyswietlanie_notatki(user_id)

        # Edytowanie notatki
        edycja_notatki(1, user_id, "Zaktualizowana notatka")

        # Usuwanie notatki
        usuwanie_notatki(1, user_id)
