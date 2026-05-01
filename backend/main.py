from fastapi import FastAPI
import sqlite3
import os

app = FastAPI()

# chemin vers la base (même logique que tout à l'heure)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "db.sqlite")

def get_db():
    return sqlite3.connect(DB_PATH)

# route test
@app.get("/")
def home():
    return {"message": "API Job Tracker OK ✔️"}
from pydantic import BaseModel

class Candidature(BaseModel):
    entreprise: str
    poste: str
    date: str
    statut: str
    commentaire: str

@app.post("/candidatures")
def add_candidature(c: Candidature):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidatures (entreprise, poste, date, statut, commentaire)
    VALUES (?, ?, ?, ?, ?)
    """, (c.entreprise, c.poste, c.date, c.statut, c.commentaire))

    conn.commit()
    conn.close()

    return {"message": "Candidature ajoutée ✔️"}
@app.get("/candidatures")
def get_candidatures():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidatures")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "entreprise": r[1],
            "poste": r[2],
            "date": r[3],
            "statut": r[4],
            "commentaire": r[5]
        }
        for r in rows
    ]