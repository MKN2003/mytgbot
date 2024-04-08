import sqlite3

conn = sqlite3.connect("users.db")
sql = conn.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, user_name TEXT, phone_number TEXT);")
conn.commit()


def register_user(user_id, user_name, phone_number):
    conn = sqlite3.connect("users.db")
    sql = conn.cursor()

    sql.execute("INSERT INTO users(user_id, user_name, phone_number) VALUES(?,?,?)",
                (user_id, user_name, phone_number))
    conn.commit()


sql.close()
