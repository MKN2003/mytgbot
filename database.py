import sqlite3

conn = sqlite3.connect("database.db")
sql = conn.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, user_name TEXT, phone_number TEXT);")
sql.execute("CREATE TABLE IF NOT EXISTS products(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT, "
            "pr_price REAL, pr_des TEXT, pr_photo TEXT);")
sql.execute("CREATE TABLE IF NOT EXISTS cart(user_id INTEGER, pr_id INTEGER, pr_name TEXT, "
            "pr_count INTEGER total_price REAL);")
conn.commit()


def register_user(user_id, user_name, phone_number):
    conn = sqlite3.connect("database.db")
    sql = conn.cursor()

    sql.execute("INSERT INTO users(user_id, user_name, phone_number) VALUES(?,?,?)",
                (user_id, user_name, phone_number))
    conn.commit()


def check_user(user_id):
    conn = sqlite3.connect("database.db")
    sql = conn.cursor()

    checker = sql.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,)).fetchone()

    if checker:
        return True
    return False


def add_product(pr_name, pr_price, pr_des, pr_photo):
    conn = sqlite3.connect("database.db")
    sql = conn.cursor()

    sql.execute("INSERT INTO products(pr_name, pr_price, pr_des, pr_photo) VALUES(?,?,?,?)",
                (pr_name, pr_price, pr_des, pr_photo))
    conn.commit()


def add_to_cart(user_id, pr_id, pr_name, pr_count, pr_price):
    conn = sqlite3.connect("database.db")
    sql = conn.cursor()

    total_price = pr_count * pr_price

    sql.execute("INSERT INTO cart(user_id, pr_id, pr_name, pr_count, total_price) VALUES(?,?,?,?,?)",
                (user_id, pr_id, pr_name, pr_count, total_price))
    conn.commit()


def get_pr_id():
    conn = sqlite3.connect("database.db")
    sql = conn.cursor()

    all_products = sql.execute("SELECT pr_id, pr_name FROM PRODUCTS").fetchall()
    actual_products = [(i[0], i[1]) for i in all_products]

    return actual_products


def get_all_id():
    conn = sqlite3.connect("database.db")
    sql = conn.cursor()

    all_id = sql.execute("SELECT pr_id FROM products;").fetchall()
    actual_id = [i[0] for i in all_id]

    return actual_id


def delete_exact_pr_from_cart(user_id, pr_id):
    conn = sqlite3.connect("database.db")
    sql = conn.cursor()

    sql.execute("DELETE FROM cart WHERE user_id=? AND pr_id=?;",
                (user_id, pr_id))
    conn.commit()


def delete_user_cart(user_id):
    conn = sqlite3.connect("database.db")
    sql = conn.cursor()

    sql.execute("DELETE FROM cart WHERE user_id=?;", (user_id,))
    conn.commit()


def delete_product():
    conn = sqlite3.connect("database.db")
    sql = conn.cursor()

    sql.execute("DELETE FROM products")
    conn.commit()


sql.close()
