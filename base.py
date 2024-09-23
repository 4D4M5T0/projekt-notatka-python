import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self, host, user, password, database, port):
        try:
            connect = mysql.connector.connect(host=host, user=user, password=password, port=port)
            self.conn = connect
            self.cursor = self.conn.cursor()

            self.cursor.execute(f"create database if not exists {database}")
            self.conn.commit()

            self.conn.database = database

            self.create_tables()

        except Error as e:
            print(f"Błąd przy utworzeniu bazy lub połączeniu: {e}")
            self.conn = None

    def create_tables(self):
        try:
            self.cursor.execute("""
                create table if not exists uzytkownik (
                    id int auto_increment primary key,
                    login varchar(255) unique not null,
                    pass varchar(255) not null
                )
            """)

            self.cursor.execute("""
                create table if not exists notatka (
                    id int auto_increment primary key,
                    zawartosc text not null,
                    user_id int,
                    foreign key (user_id) references uzytkownik(id) on delete cascade,
                    time timestamp not null default current_timestamp
                )
            """)

            self.conn.commit()

        except Error as e:
            print(f"Błąd przy utworzeniu tabel: {e}")
            self.conn = None

    def sprawdzanie(self, login, password):
        query = "select * from uzytkownik where login = %s and password = %s"
        self.cursor.execute(query, (login, password))
        user = self.cursor.fetchone()
        return user

    def wpisz_uzytkownika(self, login, password):
        try:
            query = "insert into uzytkownik (login, password) values (%s, %s)"
            self.cursor.execute(query, (login, password))
            self.conn.commit()
        except mysql.connector.IntegrityError:
            return False
        return True

    def get_uzytkownik_id(self, login):
        query = "select id from uzytkownik where login = %s"
        self.cursor.execute(query, (login,))
        user_id = self.cursor.fetchone()
        return user_id[0] if user_id else None

    def wypisz_notatki_uzytkownika(self, user_id):
        query = "select * from notatka where user_id = %s"
        self.cursor.execute(query, (user_id,))
        notatki = self.cursor.fetchall()
        return notatki

    def wpisz_notatka(self, tresc, user_id):
        query = "insert into notatka (tresc, user_id) values (%s, %s)"
        self.cursor.execute(query, (tresc, user_id))
        self.conn.commit()

    def usun_notatka(self, notatka_id):
        query = "delete from notatka where id = %s"
        self.cursor.execute(query, (notatka_id,))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
