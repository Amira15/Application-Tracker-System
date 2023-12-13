import streamlit as st
import spacy
from spacy.matcher import PhraseMatcher
import fitz  # Importer PyMuPDF (MuPDF)
import json

# Charger le modèle SpaCy
nlp = spacy.load('fr_core_news_sm')

# Fonction pour calculer le pourcentage de correspondance avec des mots-clés
def calculate_matching_percentage(text, keywords):
    doc = nlp(text.lower())
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp(keyword.lower()) for keyword in keywords]
    matcher.add("Keywords", None, *patterns)
    matches = matcher(doc)
    total_keywords = len(keywords)
    matching_keywords = len(matches)
    percentage = (matching_keywords / total_keywords) * 100
    return percentage

# Fonction pour extraire le texte d'un fichier PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with fitz.open(pdf_file) as doc:
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
    except Exception as e:
        st.error(f"Erreur lors de l'extraction du texte du PDF : {e}")

    return text

# Streamlit app
def main():
    st.title("CV Matching App")

    # Fichier PDF à traiter
    pdf_path = st.file_uploader("Upload CV (PDF)", type=["pdf"])

    if pdf_path:
        # Extraire le texte du CV PDF
        cv_text = extract_text_from_pdf(pdf_path).lower()

        # Fichier TXT contenant les mots-clés
        keywords_file_path = st.file_uploader("Upload Keywords (TXT)", type=["txt"])

        if keywords_file_path:
            # Charger les mots-clés depuis le fichier TXT
            with keywords_file_path as keywords_file:
                keywords = keywords_file.read().decode('utf-8').strip().lower().split('\n')

            # Calculer le pourcentage de correspondance
            matching_percentage = calculate_matching_percentage(cv_text, keywords)

            # Afficher le texte extrait et le pourcentage sur l'interface Streamlit
            st.write(f"Texte du CV PDF :\n\n{cv_text}")
            st.write(f"\n\nPourcentage de correspondance : {matching_percentage}%")

            # Sauvegarder le texte extrait dans un fichier JSON
            output_json = {"cv_text": cv_text, "matching_percentage": matching_percentage}
            json_path = "output.json"  # Choisissez le nom et le chemin du fichier JSON
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(output_json, json_file)

            st.success(f"Texte extrait sauvegardé dans {json_path}")

# Exécuter l'application Streamlit
if __name__ == "__main__":
    main()
