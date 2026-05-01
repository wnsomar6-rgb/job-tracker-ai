import streamlit as st
import requests
import matplotlib.pyplot as plt

# -----------------------
# 🧠 SCORE IA
# -----------------------
def score_candidature(poste, statut):
    score = 50

    if "data" in poste.lower():
        score += 10
    if "engineer" in poste.lower() or "dev" in poste.lower():
        score += 10

    if statut == "entretien":
        score += 20
    elif statut == "refus":
        score -= 20
    elif statut == "accepté":
        score += 30

    return min(100, max(0, score))


# -----------------------
# 📡 UNE SEULE REQUÊTE API (OPTIMISATION)
# -----------------------
response = requests.get("http://127.0.0.1:8000/candidatures")
data = response.json()


# -----------------------
# 📊 APP
# -----------------------
st.title("📊 Suivi des candidatures")

# -----------------------
# ➕ FORMULAIRE
# -----------------------
st.subheader("➕ Ajouter une candidature")

with st.form("add_form"):
    entreprise = st.text_input("Entreprise")
    poste = st.text_input("Poste")
    date = st.text_input("Date (YYYY-MM-DD)")
    statut = st.selectbox("Statut", ["envoyé", "entretien", "refus", "accepté"])
    commentaire = st.text_area("Commentaire")

    submitted = st.form_submit_button("Ajouter")

    if submitted:
        payload = {
            "entreprise": entreprise,
            "poste": poste,
            "date": date,
            "statut": statut,
            "commentaire": commentaire
        }

        res = requests.post("http://127.0.0.1:8000/candidatures", json=payload)

        if res.status_code == 200:
            st.success("Candidature ajoutée ✔️")
        else:
            st.error("Erreur lors de l'ajout")


# -----------------------
# 📄 LISTE + SCORE
# -----------------------
st.subheader("📄 Liste des candidatures + score")

for d in data:
    entreprise = d["entreprise"]
    poste = d["poste"]
    statut = d["statut"]

    score = score_candidature(poste, statut)

    st.write("----")
    st.write(f"🏢 Entreprise : {entreprise}")
    st.write(f"💼 Poste : {poste}")
    st.write(f"📌 Statut : {statut}")
    st.write(f"🧠 Score IA : {score}/100")


# -----------------------
# 📊 STATS
# -----------------------
st.subheader("📊 Statistiques")

total = len(data)

entretien = len([d for d in data if d["statut"] == "entretien"])
accepte = len([d for d in data if d["statut"] == "accepté"])

st.metric("Total candidatures", total)
st.metric("Entretiens obtenus", entretien)
st.metric("Offres acceptées", accepte)

if total > 0:
    taux = (entretien / total) * 100
    st.write(f"📈 Taux de réponse : {taux:.1f}%")


# -----------------------
# 📈 GRAPHIQUE
# -----------------------
st.subheader("📈 Graphique des statuts")

statuts = {}

for d in data:
    statut = d["statut"]
    statuts[statut] = statuts.get(statut, 0) + 1

labels = list(statuts.keys())
values = list(statuts.values())

fig, ax = plt.subplots()
ax.bar(labels, values)

st.pyplot(fig)


# -----------------------
# 💌 MAIL
# -----------------------
st.subheader("💌 Générateur de mail de relance")

entreprise_mail = st.text_input("Entreprise (relance)")
poste_mail = st.text_input("Poste (relance)")

def generer_mail(entreprise, poste):
    return f"""
Bonjour,

Je me permets de vous recontacter concernant ma candidature pour le poste de {poste} chez {entreprise}.

Je reste très motivé par cette opportunité et disponible pour un entretien.

Bien cordialement,
"""

if st.button("Générer le mail"):
    mail = generer_mail(entreprise_mail, poste_mail)
    st.text_area("Ton mail", mail, height=200)