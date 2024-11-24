import sqlite3

def create_user(name, email, password):
    conn = sqlite3.connect('data/db.db')
    c = conn.cursor()
    query = f'''"INSERT INTO user (name, email, password)
                 ('{name}'{email}','{password}')"'''
    c.execute(query)
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect('data/db.db')
    c = conn.cursor()
    query = f"SELECT id,name,password  WHERE email = {email}"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result

def get_user_by_email_and_password(email,password):
    conn = sqlite3.connect('data/db.db')
    c = conn.cursor()
    query = f"SELECT id,name,password  WHERE email = {email} and password = {password}"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result

def get_user_by_id(id):
    conn = sqlite3.connect('data/db.db')
    c = conn.cursor()
    query = f"SELECT id,name,password,gender,birthday,gendre,avatar WHERE id = {id}"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result
