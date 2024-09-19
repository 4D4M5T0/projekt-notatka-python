import mysql.connector
import bcrypt


# Funkcja do połączenia z bazą danych
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Twój użytkownik MySQL
        password="",  # Hasło do MySQL
        database="notes_app"
    )


# Rejestracja użytkownika
def register_user(login, password):
    db = connect_to_db()
    cursor = db.cursor()

    # Sprawdzanie czy login już istnieje
    cursor.execute("SELECT * FROM user WHERE login = %s", (login,))
    if cursor.fetchone():
        print("Użytkownik o podanym loginie już istnieje.")
        return

    # Haszowanie hasła
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Wstawianie nowego użytkownika do bazy danych
    cursor.execute("INSERT INTO user (login, password) VALUES (%s, %s)", (login, hashed_password))
    db.commit()
    print("Rejestracja zakończona sukcesem.")
    db.close()


# Logowanie użytkownika
def login_user(login, password):
    db = connect_to_db()
    cursor = db.cursor()

    # Pobieranie użytkownika na podstawie loginu
    cursor.execute("SELECT * FROM user WHERE login = %s", (login,))
    user = cursor.fetchone()

    if user:
        # Sprawdzanie hasła
        user_id, _, hashed_password = user
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print("Logowanie zakończone sukcesem.")
            db.close()
            return user_id
        else:
            print("Błędne hasło.")
    else:
        print("Nie znaleziono użytkownika.")

    db.close()
    return None


# Wyświetlanie notatek dla zalogowanego użytkownika
def show_notes(user_id):
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM notatka WHERE user_id = %s", (user_id,))
    notes = cursor.fetchall()

    if notes:
        for note in notes:
            print(f"ID: {note[0]}, Timestamp: {note[1]}, Text: {note[2]}")
    else:
        print("Brak notatek.")

    db.close()


# Dodawanie nowej notatki
def add_note(user_id, text):
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("INSERT INTO notatka (text, user_id) VALUES (%s, %s)", (text, user_id))
    db.commit()
    print("Dodano nową notatkę.")

    db.close()


# Usuwanie notatki
def delete_note(note_id, user_id):
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM notatka WHERE id = %s AND user_id = %s", (note_id, user_id))
    db.commit()

    if cursor.rowcount > 0:
        print("Notatka została usunięta.")
    else:
        print("Nie znaleziono notatki do usunięcia.")

    db.close()


# Edycja notatki
def edit_note(note_id, user_id, new_text):
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("UPDATE notatka SET text = %s WHERE id = %s AND user_id = %s", (new_text, note_id, user_id))
    db.commit()

    if cursor.rowcount > 0:
        print("Notatka została zaktualizowana.")
    else:
        print("Nie znaleziono notatki do edycji.")

    db.close()


# Przykład użycia:
if __name__ == "__main__":
    # Rejestracja nowego użytkownika
    register_user("user1", "password123")

    # Logowanie
    user_id = login_user("user1", "password123")

    if user_id:
        # Dodawanie notatki
        add_note(user_id, "Moja pierwsza notatka.")

        # Wyświetlanie notatek
        show_notes(user_id)

        # Edytowanie notatki
        edit_note(1, user_id, "Zaktualizowana notatka")

        # Usuwanie notatki
        delete_note(1, user_id)