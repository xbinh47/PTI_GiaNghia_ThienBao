import sqlite3
from model.user import * 

def remove_vietnamese_signs(text: str) -> str:
    # Replace Vietnamese characters with their non-accented equivalents
    replacements = {
        'àáạảãâầấậẩẫăằắặẳẵ': 'a',
        'ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ': 'A', 
        'èéẹẻẽêềếệểễ': 'e',
        'ÈÉẸẺẼÊỀẾỆỂỄ': 'E',
        'òóọỏõôồốộổỗơờớợởỡ': 'o', 
        'ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ': 'O',
        'ìíịỉĩ': 'i',
        'ÌÍỊỈĨ': 'I',
        'ùúụủũưừứựửữ': 'u',
        'ƯỪỨỰỬỮÙÚỤỦŨ': 'U',
        'ỳýỵỷỹ': 'y',
        'ỲÝỴỶỸ': 'Y',
        'đ': 'd',
        'Đ': 'D'
    }
    
    for vietnamese, latin in replacements.items():
        for char in vietnamese:
            text = text.replace(char, latin)
    return text

def build_alias(name: str) -> str:
    # Remove Vietnamese characters
    name = remove_vietnamese_signs(name)
    # Replace hyphens with spaces
    name = name.replace('-', ' ')
    # Convert to lowercase
    name = name.lower()
    # Trim spaces
    name = name.strip()
    # Replace spaces with hyphens
    name = name.replace(' ', '-')
    # Remove any characters that aren't a-z, 0-9, or hyphen
    name = ''.join(c for c in name if c.isalnum() or c == '-')
    # Replace multiple hyphens with single hyphen
    while '--' in name:
        name = name.replace('--', '-')
    return name

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
    query = f"SELECT id,name,email,password,gender,fav_music,avatar FROM user WHERE id = '{id}'"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    return result

def update_user(id, user: User):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    query = f"UPDATE user SET name = '{user.name}', email = '{user.email}', fav_music = '{user.fav_music}', gender = '{user.gender}', avatar = '{user.avatar}' WHERE id = '{id}'"
    c.execute(query)
    conn.commit()
    conn.close()
    
def get_songs_by_name(name):
    conn = sqlite3.connect('data/spotify.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    alias = build_alias(name)
    query = f"SELECT id,name,album_name,playcount,artist_names FROM songs WHERE name LIKE '%{name}%' OR alias LIKE '%{alias}%'"
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result

def get_first_15_songs_ordered_by_playcount():
    conn = sqlite3.connect('data/spotify.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    query = f"SELECT id,name,album_name,playcount,artist_names FROM songs ORDER BY playcount DESC LIMIT 15"
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result