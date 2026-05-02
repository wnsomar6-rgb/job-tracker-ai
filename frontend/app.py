import streamlit as st
import requests
import matplotlib.pyplot as plt

# -----------------------
# ⚙️ CONFIG
# -----------------------
st.set_page_config(
    page_title="Job Tracker AI",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/candidatures"


# -----------------------
# 🧠 SCORE IA
# -----------------------
def score_candidature(poste, statut):
    score = 50

    poste = poste.lower()

    if "data" in poste:
        score += 10
    if "engineer" in poste or "dev" in poste or "developer" in poste:
        score += 10
    if "ai" in poste or "machine" in poste:
        score += 15

    if statut == "entretien":
        score += 20
    elif statut == "refus":
        score -= 20
    elif statut == "accepté":
        score += 30

    return min(100, max(0, score))


# -----------------------
# 📡 API DATA (SAFE)
# -----------------------
try:
    response = requests.get(API_URL)
    data = response.json()
except:
    st.error("❌ Backend non accessible (uvicorn non lancé)")
    data = []


# -----------------------
# 🚀 HEADER
# -----------------------
st.title("🚀 Job Tracker AI")
st.caption("Ton assistant intelligent pour suivre et analyser tes candidatures")


# -----------------------
# ➕ AJOUT CANDIDATURE
# -----------------------
st.subheader("➕ Ajouter une candidature")

with st.form("add_form"):
    col1, col2 = st.columns(2)

    with col1:
        entreprise = st.text_input("Entreprise")
        poste = st.text_input("Poste")

    with col2:
        date = st.text_input("Date (YYYY-MM-DD)")
        statut = st.selectbox(
            "Statut",
            ["envoyé", "entretien", "refus", "accepté"]
        )

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

        res = requests.post(API_URL, json=payload)

        if res.status_code == 200:
            st.success("✔️ Candidature ajoutée")
            st.rerun()
        else:
            st.error("❌ Erreur lors de l'ajout")


# -----------------------
# 🔎 FILTRE + SEARCH
# -----------------------
st.subheader("🔎 Recherche & filtre")

col1, col2 = st.columns(2)

with col1:
    filtre = st.selectbox(
        "Filtrer par statut",
        ["Tous", "envoyé", "entretien", "refus", "accepté"]
    )

with col2:
    search = st.text_input("Rechercher (entreprise / poste)")

# filtre statut
if filtre != "Tous":
    data = [d for d in data if d["statut"] == filtre]

# search
if search:
    search = search.lower()
    data = [
        d for d in data
        if search in d["entreprise"].lower()
        or search in d["poste"].lower()
    ]


# -----------------------
# 📄 LISTE CANDIDATURES
# -----------------------
st.subheader("📄 Candidatures")

if len(data) == 0:
    st.warning("Aucune candidature trouvée")
else:
    for d in data:
        entreprise = d["entreprise"]
        poste = d["poste"]
        statut = d["statut"]

        score = score_candidature(poste, statut)

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"### 🏢 {entreprise}")
            st.write(f"💼 {poste}")
            st.write(f"📌 Statut : {statut}")

        with col2:
            st.metric("Score IA", f"{score}/100")

        st.divider()


# -----------------------
# 📊 STATS
# -----------------------
st.subheader("📊 Analytics")

total = len(data)
entretien = len([d for d in data if d["statut"] == "entretien"])
accepte = len([d for d in data if d["statut"] == "accepté"])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📄 Total", total)

with col2:
    st.metric("🎯 Entretiens", entretien)

with col3:
    st.metric("✅ Acceptés", accepte)

if total > 0:
    taux = (entretien / total) * 100
    st.info(f"📈 Taux de réponse : {taux:.1f}%")


# -----------------------
# 📊 GRAPHIQUE
# -----------------------
st.subheader("📊 Répartition des statuts")

statuts = {}

for d in data:
    s = d["statut"]
    statuts[s] = statuts.get(s, 0) + 1

fig, ax = plt.subplots()
ax.bar(statuts.keys(), statuts.values())

st.pyplot(fig)


# -----------------------
# 💌 MAIL RELANCE
# -----------------------
st.subheader("💌 Générateur de mail")

entreprise_mail = st.text_input("Entreprise")
poste_mail = st.text_input("Poste")

def generer_mail(entreprise, poste):
    return f"""
Bonjour,

Je me permets de vous recontacter concernant ma candidature pour le poste de {poste} chez {entreprise}.

Je reste très motivé par cette opportunité.

Bien cordialement,
"""

if st.button("Générer mail"):
    st.text_area("Mail", generer_mail(entreprise_mail, poste_mail), height=200)