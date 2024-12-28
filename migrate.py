import sqlite3
import os
def row_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# get all songs
def get_all_songs():
    conn = sqlite3.connect('data/spotify.db')
    conn.row_factory = row_factory
    c = conn.cursor()
    query = "SELECT * FROM songs"
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result

def get_all_artists():
    conn = sqlite3.connect('data/db.db')
    conn.row_factory = row_factory
    c = conn.cursor()
    query = "SELECT * FROM artists"
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result
songs = get_all_songs()
# missing_image = []
# for song in songs:
#     # check image path exist in songs_images folder
#     if song["image_path"] == "" or song["image_path"] is None:
#         missing_image.append(song["id"])
#     else:
#         # check image path exist in songs_images folder
        
#         if not os.path.exists(song["image_path"]):
#             missing_image.append(song["id"])
# for song_id in missing_image:
#     with open("data2.txt", "a") as f:
#         f.write(f"{song_id}\n")
# artists = get_all_artists()
# artist_map = {artist["id"]: artist["name"] for artist in artists}
# get all songs and artist id than add artist name to song
# for song in songs:
#     artist_names = []
#     # Check if artist_ids exists and convert from string if needed
#     if song["artist_ids"]:
#         # Remove brackets and split by comma
#         artist_id_list = song["artist_ids"].strip('[]').split(',')
#         for artist_id in artist_id_list:
#             # Remove quotes and whitespace
#             clean_id = artist_id.strip().strip('"\'')
#             artist_names.append(artist_map.get(clean_id, "Unknown Artist"))
#     song["artist_names"] = artist_names
    

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

# Update the database with artist names
conn = sqlite3.connect('data/db.db')
c = conn.cursor()
for song in songs:
    # Join artist names with comma if multiple artists
    c.execute("""
        UPDATE songs 
        SET  alias = ? 
        WHERE id = ?
    """, (build_alias(song["name"]), song["id"]))

conn.commit()
conn.close()

# update song_images
# with open("data.txt", "r") as f:
#     lines = f.readlines()
#     for line in lines:
#         song_id, image_id = line.strip().split(" - ")
#         conn = sqlite3.connect('data/spotify.db')
#         c = conn.cursor()
#         c.execute("""
#             UPDATE songs 
#             SET image_path = ? 
#             WHERE id = ?
#         """, (f"songs_images/{image_id}.jpg", song_id))
#         conn.commit()
#         conn.close()