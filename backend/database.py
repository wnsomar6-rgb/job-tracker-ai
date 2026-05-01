import sqlite3
import os

# Crée le dossier database s’il n’existe pas
os.makedirs("database", exist_ok=True)

def init_db():
    conn = sqlite3.connect("database/db.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entreprise TEXT,
        poste TEXT,
        date TEXT,
        statut TEXT,
        commentaire TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Base de données créée ✔️")

if __name__ == "__main__":
    init_db()