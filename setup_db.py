import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_user(name, email, password):
    conn = sqlite3.connect('data/db.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    query = f"INSERT INTO user (name, email, password) VALUES('{name}', '{email}','{password}')"
    c.execute(query)
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect('data/db.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    query = f"SELECT id,name,password FROM user WHERE email = '{email}'"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result

def get_user_by_email_and_password(email,password):
    conn = sqlite3.connect('data/db.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    query = f"SELECT id,name,password FROM user WHERE email = '{email}' and password = '{password}'"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result

def get_user_by_id(id):
    conn = sqlite3.connect('data/db.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    query = f"SELECT id,name,email,password,gender,birthday,genre,avatar FROM user WHERE id = '{id}'"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result
