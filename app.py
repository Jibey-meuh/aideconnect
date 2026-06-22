import streamlit as st
from groq import Groq

# ── Config ──────────────────────────────────────────────
st.set_page_config(page_title="AideConnect", page_icon="🇫🇷", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_BASE = """Tu es un assistant expert en droit social français, aides sociales, 
France Travail (ex-Pôle emploi), CAF, et entrepreneuriat. 
Tu réponds en français, de façon claire, simple et structurée.
Tu cites les lois et textes officiels quand c'est pertinent.
Tu ne donnes jamais de conseil médical ou fiscal personnel."""

def ask_groq(prompt, system=SYSTEM_BASE):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=2000,
    )
    return response.choices[0].message.content

# ── Navigation ───────────────────────────────────────────
st.title("🇫🇷 AideConnect — Vos droits, simplement")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💰 Mes Aides",
    "🏢 SASU & ACRE",
    "📊 Budget",
    "🏠 Logement",
    "💬 Question juridique"
])

# ══════════════════════════════════════════════════════════
# ONGLET 1 — MES AIDES
# ══════════════════════════════════════════════════════════
with tab1:
    st.header("💰 Trouvez toutes vos aides")
    st.caption("Remplissez votre profil pour obtenir une liste personnalisée.")

    with st.form("profil_form"):
        col1, col2 = st.columns(2)
        with col1:
            genre = st.selectbox("Genre", ["Homme", "Femme", "Non-binaire"])
            age = st.number_input("Âge", 18, 99, 30)
            situation = st.selectbox("Situation familiale", [
                "Célibataire", "En couple", "Marié(e)", "Divorcé(e)",
                "Veuf/veuve", "Parent isolé"
            ])
            enfants = st.number_input("Nombre d'enfants à charge", 0, 15, 0)
        with col2:
            emploi = st.selectbox("Situation professionnelle", [
                "Salarié(e)", "Demandeur d'emploi avec ARE",
                "Demandeur d'emploi sans ARE", "Auto-entrepreneur",
                "Sans emploi sans droits", "Étudiant(e)", "En formation"
            ])
            revenu = st.number_input("Revenu mensuel net (€)", 0, 20000, 0)
            logement = st.selectbox("Logement", [
                "Locataire", "Propriétaire", "Hébergé(e) gratuitement",
                "Sans domicile fixe"
            ])
            handicap = st.checkbox("Situation de handicap (RQTH ou AAH)")

        submitted = st.form_submit_button("🔍 Chercher mes aides", use_container_width=True)

    if submitted:
        prompt = f"""
Voici le profil d'une personne :
- Genre : {genre}, {age} ans
- Situation familiale : {situation}, {enfants} enfant(s)
- Emploi : {emploi}
- Revenu mensuel : {revenu}€
- Logement : {logement}
- Handicap : {'Oui' if handicap else 'Non'}

Liste TOUTES les aides auxquelles cette personne peut prétendre en France :
- Aides France Travail / Pôle emploi
- Aides CAF (APL, RSA, allocation familiale, etc.)
- Aides locales / régionales
- Aides au logement
- Aides handicap si applicable
- Aides à la création d'entreprise si applicable

Pour chaque aide : nom officiel, montant approximatif, lien ou organisme à contacter, conditions clés.
Format : liste structurée avec des sections claires.
"""
        with st.spinner("Analyse en cours..."):
            result = ask_groq(prompt)
        st.success("Aides trouvées !")
        st.markdown(result)
        st.info("⚠️ Ces informations sont indicatives. Vérifiez sur [mesaides.gouv.fr](https://www.mesaides.gouv.fr)")

# ══════════════════════════════════════════════════════════
# ONGLET 2 — SASU & ACRE
# ══════════════════════════════════════════════════════════
with tab2:
    st.header("🏢 Créer sa SASU avec l'ARE et l'ACRE")
    st.caption("Guide étape par étape pour les demandeurs d'emploi qui veulent entreprendre.")

    st.info("""
**Ce que vous pouvez cumuler :**
- 🟢 **ARE** (Allocation Retour Emploi) → vous continuez à la percevoir en partie
- 🟢 **ACRE** → exonération de charges sociales la 1ère année
- 🟢 **ARCE** → recevoir 60% de vos droits ARE en capital (au lieu de mensuel)
    """)

    steps = {
        "1️⃣ Vérifier vos droits ARE": """
**Condition :** Vous devez être inscrit à France Travail et percevoir l'ARE.

**Ce que vous gardez :**
- Si vous créez une SASU et vous versez un salaire → ARE réduite proportionnellement
- Si vous ne vous versez pas de salaire → ARE maintenue à 100%
- [Simulateur ARE → ARCE](https://www.unedic.org/indemnisation/vos-droits-avant-tout/quelle-indemnisation-en-cas-de-creation-ou-reprise-dentreprise)
        """,
        "2️⃣ Choisir entre ARE mensuelle ou ARCE (capital)": """
**ARCE = 60% de vos droits restants en 2 versements**

| Option | Avantage | Inconvénient |
|--------|----------|--------------|
| ARE mensuelle | Sécurité, revenus réguliers | Moins de capital dispo |
| ARCE (capital) | Trésorerie pour démarrer | Tout perdu si échec |

👉 Demandez l'ARCE à France Travail **après** immatriculation.
        """,
        "3️⃣ Créer votre SASU sur le guichet unique": """
**Site officiel :** [formalites.entreprises.gouv.fr](https://formalites.entreprises.gouv.fr)

Étapes :
1. Choisir "Créer une société" → SASU
2. Remplir : dénomination, adresse, objet social, capital (1€ minimum)
3. Déposer le capital en banque → obtenir attestation
4. Publier une annonce légale (~150€ sur un journal habilité)
5. Soumettre le dossier → obtenir le Kbis (3-5 jours)
        """,
        "4️⃣ Demander l'ACRE": """
**ACRE = Aide à la Création ou Reprise d'Entreprise**

- Exonération partielle de charges sociales la 1ère année
- Automatique pour les demandeurs d'emploi depuis 2019

**Démarche :**
1. Lors de la création sur le guichet unique → cocher "demande d'ACRE"
2. Ou envoyer le formulaire [Cerfa 13584*02](https://www.service-public.fr/professionnels-entreprises/vosdroits/R17122) à l'URSSAF sous 45 jours

**Montant :** Exonération de 50% des cotisations la 1ère année.
        """,
        "5️⃣ Prévenir France Travail": """
**Obligatoire sous 72h après création**

1. Connectez-vous sur [pole-emploi.fr](https://www.francetravail.fr)
2. Déclarez la création d'entreprise dans "Mes démarches"
3. Envoyez votre Kbis
4. Choisissez ARE mensuelle ou ARCE

**Documents à préparer :**
- Extrait Kbis
- Attestation de dépôt de capital
- RIB professionnel
        """,
        "6️⃣ Liens utiles": """
| Ressource | Lien |
|-----------|------|
| Guichet unique création | [formalites.entreprises.gouv.fr](https://formalites.entreprises.gouv.fr) |
| ACRE / URSSAF | [urssaf.fr](https://www.urssaf.fr) |
| Simulateur ARE | [unedic.org](https://www.unedic.org) |
| France Travail | [francetravail.fr](https://www.francetravail.fr) |
| Annonces légales | [journal-officiel.gouv.fr](https://www.journal-officiel.gouv.fr) |
| BPI France (financement) | [bpifrance.fr](https://www.bpifrance.fr) |
        """
    }

    for title, content in steps.items():
        with st.expander(title):
            st.markdown(content)

    st.divider()
    st.subheader("🤖 Posez une question sur votre cas")
    q_sasu = st.text_input("Ex: Je touche 1200€ d'ARE, que se passe-t-il si je me verse 800€ de salaire ?")
    if st.button("Répondre", key="sasu_btn") and q_sasu:
        with st.spinner("..."):
            r = ask_groq(f"Question sur SASU/ACRE/ARE en France : {q_sasu}")
        st.markdown(r)

# ══════════════════════════════════════════════════════════
# ONGLET 3 — SIMULATEUR BUDGET
# ══════════════════════════════════════════════════════════
with tab3:
    st.header("📊 Simulateur de budget")
    st.caption("Estimez votre reste à vivre après aides.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenus")
        salaire = st.number_input("Salaire / ARE (€/mois)", 0, 10000, 0)
        rsa = st.number_input("RSA estimé (€/mois)", 0, 1000, 0)
        apl = st.number_input("APL estimée (€/mois)", 0, 600, 0)
        autres = st.number_input("Autres aides (€/mois)", 0, 2000, 0)

    with col2:
        st.subheader("Dépenses")
        loyer = st.number_input("Loyer charges comprises (€)", 0, 3000, 0)
        alimentation = st.number_input("Alimentation (€)", 0, 1000, 200)
        transport = st.number_input("Transport (€)", 0, 500, 80)
        autres_dep = st.number_input("Autres dépenses (€)", 0, 2000, 0)

    total_revenus = salaire + rsa + apl + autres
    total_depenses = loyer + alimentation + transport + autres_dep
    reste = total_revenus - total_depenses

    st.divider()
    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.metric("Total revenus", f"{total_revenus} €")
    col_r2.metric("Total dépenses", f"{total_depenses} €")
    
    if reste >= 0:
        col_r3.metric("✅ Reste à vivre", f"{reste} €")
    else:
        col_r3.metric("⚠️ Déficit", f"{reste} €", delta=f"{reste} €")
        st.error("Votre budget est déficitaire. Consultez un conseiller France Travail ou une assistante sociale.")

    if st.button("💡 Conseils pour optimiser mon budget"):
        prompt = f"""
Mon budget mensuel :
- Revenus : {total_revenus}€ (salaire/ARE: {salaire}€, RSA: {rsa}€, APL: {apl}€)
- Dépenses : {total_depenses}€ (loyer: {loyer}€, alimentation: {alimentation}€, transport: {transport}€)
- Reste à vivre : {reste}€

Donne-moi 5 conseils concrets pour optimiser ce budget et les aides supplémentaires que je pourrais demander.
"""
        with st.spinner("..."):
            r = ask_groq(prompt)
        st.markdown(r)

# ══════════════════════════════════════════════════════════
# ONGLET 4 — LOGEMENT
# ══════════════════════════════════════════════════════════
with tab4:
    st.header("🏠 Aides au logement")

    situation_log = st.selectbox("Votre situation", [
        "Locataire avec loyer", "Cherche un logement social (HLM)",
        "Risque d'expulsion", "Sans domicile fixe", "Hébergé(e) chez quelqu'un"
    ])
    revenu_log = st.number_input("Revenu mensuel net (€)", 0, 10000, 0, key="rev_log")
    nb_personnes = st.number_input("Personnes dans le foyer", 1, 15, 1)

    if st.button("🔍 Voir mes droits au logement"):
        prompt = f"""
Situation logement en France :
- Situation : {situation_log}
- Revenu : {revenu_log}€/mois
- Foyer : {nb_personnes} personne(s)

Liste toutes les aides logement disponibles :
- APL / ALS / ALF (CAF)
- FSL (Fonds de Solidarité Logement)
- Action Logement
- DALO (Droit au logement opposable) si applicable
- Hébergement d'urgence (115)
- Aides locales

Pour chaque aide : conditions, montant, comment faire la demande, délais.
"""
        with st.spinner("..."):
            r = ask_groq(prompt)
        st.markdown(r)
    
    st.divider()
    st.subheader("🚨 Urgence logement")
    st.error("**115** → SAMU Social (24h/24) | **0 800 306 306** → Numéro national prévention expulsions")

# ══════════════════════════════════════════════════════════
# ONGLET 5 — CHATBOT JURIDIQUE
# ══════════════════════════════════════════════════════════
with tab5:
    st.header("💬 Question juridique")
    st.caption("Posez une question sur le droit social, du travail ou familial français.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ex: Mon employeur peut-il me licencier pendant un arrêt maladie ?")
    
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        
        with st.chat_message("assistant"):
            with st.spinner("..."):
                response = ask_groq(question)
            st.markdown(response)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    if st.button("🗑️ Effacer la conversation"):
        st.session_state.chat_history = []
        st.rerun()

# ── Footer ───────────────────────────────────────────────
st.divider()
st.caption("⚠️ AideConnect fournit des informations générales. Pour un conseil personnalisé, consultez un professionnel ou [service-public.fr](https://www.service-public.fr)")
