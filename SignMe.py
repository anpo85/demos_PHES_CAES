import streamlit as st
from streamlit_autorefresh import st_autorefresh
import datetime

# Configuration de la page
st.set_page_config(page_title="PDF Sync Demo", layout="wide")

# Simulation d'une base de données partagée en mémoire
if 'shared_db' not in st.session_state:
    st.session_state['shared_db'] = {
        "page_actuelle": 1,
        "signature_statut": "En attente",
        "last_update": datetime.datetime.now()
    }

# Rafraîchissement automatique toutes les secondes pour simuler le "temps réel"
st_autorefresh(interval=1000, key="datarefresh")

st.title("🚀 PDF Sync: PC ↔ Mobile")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Lecteur PDF (Simulation)")
    # Simulation d'un PDF
    page = st.session_state['shared_db']["page_actuelle"]
    st.info(f"📄 Affichage du document : Page {page} / 10")

    # Zone de visualisation "synchrone"
    st.markdown(f"""
    <div style="height:300px; border:2px dashed #ccc; display:flex; align-items:center; justify-content:center; background-color:#f9f9f9">
        <h2 style="color:#333;">{"✍️ Signature apposée !" if st.session_state['shared_db']["signature_statut"] == "Signé" else "Zone de Signature"}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.header("Contrôles")

    # Action 1 : Changer de page (Simule une action sur PC ou Mobile)
    new_page = st.number_input("Aller à la page", min_value=1, max_value=10, value=page)
    if new_page != page:
        st.session_state['shared_db']["page_actuelle"] = new_page
        st.session_state['shared_db']["last_update"] = datetime.datetime.now()

    st.divider()

    # Action 2 : Signer (Simule l'outil mobile)
    st.subheader("Outil de Signature")
    if st.button("🖊️ Signer le document", use_container_width=True):
        st.session_state['shared_db']["signature_statut"] = "Signé"
        st.session_state['shared_db']["last_update"] = datetime.datetime.now()
        st.success("Synchronisation effectuée !")

    if st.button("🗑️ Réinitialiser", use_container_width=True):
        st.session_state['shared_db']["signature_statut"] = "En attente"
        st.session_state['shared_db']["page_actuelle"] = 1

st.sidebar.write("### Statut de Synchro")
st.sidebar.write(f"Dernière modif : {st.session_state['shared_db']['last_update'].strftime('%H:%M:%S')}")
st.sidebar.write(f"Mode : **Bidirectionnel (Wi-Fi)**")