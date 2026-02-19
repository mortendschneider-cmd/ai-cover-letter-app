import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- Funktion: PDF Text extrahieren ---
def get_pdf_text(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Fehler beim Lesen des PDFs: {e}")
    return text

# --- Funktion: Gemini fragen ---
def generate_cover_letter(api_key, job_text, cv_text, user_name):
    # Gemini Konfiguration
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Der Prompt (Die Anweisung an die KI)
    prompt = f"""
    Du bist ein professioneller Karriere-Coach. Verfasse ein überzeugendes Anschreiben auf Deutsch für {user_name}.
    
    1. LEBENSLAUF DATEN:
    {cv_text}
    
    2. STELLENAUSSCHREIBUNG:
    {job_text}
    
    Anweisungen:
    - Analysiere die Keywords der Stelle und matche sie mit den Stärken im Lebenslauf.
    - Schreibe selbstbewusst, höflich und motiviert.
    - Halte dich an die übliche Form eines deutschen Anschreibens (Einleitung, Hauptteil, Schluss).
    - Nutze [Platzhalter] für Adressdaten, die du nicht kennst.
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- Layout der Web App ---
st.set_page_config(page_title="KI Bewerbungs-Schreiber", page_icon="📝", layout="wide")

st.title("🚀 Dein KI-Anschreiben Generator")
st.markdown("Lade deinen Lebenslauf hoch, kopiere die Stellenanzeige und erhalte in Sekunden einen Entwurf.")

# Sidebar für API Key
with st.sidebar:
    st.header("🔑 Einstellungen")
    api_key = st.text_input("Google API Key eingeben", type="password")
    st.markdown("[Hier kostenlosen Key holen](https://aistudio.google.com/app/apikey)")
    st.info("Der Key wird nicht gespeichert und nur für diese Sitzung genutzt.")

col1, col2 = st.columns(2)
cv_text = ""

with col1:
    st.subheader("1. Über dich")
    user_name = st.text_input("Dein Name", "Max Mustermann")
    uploaded_file = st.file_uploader("Dein Lebenslauf (PDF)", type="pdf")
    
    if uploaded_file:
        cv_text = get_pdf_text(uploaded_file)
        st.success("PDF geladen! ✅")

with col2:
    st.subheader("2. Die Stelle")
    job_description = st.text_area("Stellenbeschreibung hier einfügen", height=300)

st.divider()

if st.button("Anschreiben generieren ✨", type="primary"):
    if not api_key:
        st.error("Bitte gib links deinen Google API Key ein.")
    elif not cv_text:
        st.warning("Bitte lade deinen Lebenslauf hoch.")
    elif not job_description:
        st.warning("Bitte füge eine Stellenbeschreibung ein.")
    else:
        with st.spinner("Die KI analysiert deine Chancen..."):
            try:
                result = generate_cover_letter(api_key, job_description, cv_text, user_name)
                st.subheader("Dein Entwurf:")
                st.text_area("Ergebnis (kopierbar)", value=result, height=600)
                st.balloons()
            except Exception as e:
                st.error(f"Fehler: {e}")
