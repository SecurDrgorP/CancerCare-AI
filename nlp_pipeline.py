import re
import spacy
import subprocess
import sys
from langdetect import detect

def download_spacy_model(model_name):
    """Download spaCy model if not available"""
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
        print(f"Successfully downloaded {model_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to download {model_name}")
        raise

def load_spacy_model(model_name):
    """Load spaCy model, download if not available"""
    try:
        return spacy.load(model_name)
    except OSError:
        print(f"spaCy model '{model_name}' not found. Downloading...")
        download_spacy_model(model_name)
        return spacy.load(model_name)

# Charger les modèles spaCy complets avec téléchargement automatique
nlp_fr = load_spacy_model("fr_core_news_sm")
nlp_en = load_spacy_model("en_core_web_sm")

def nettoyage_normalisation(text, lang):
    text = text.lower()
    text = text.replace("’", "'")
    if lang == "fr":
        text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ0-9'\s]", " ", text)
    else:
        text = re.sub(r"[^a-z0-9'\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenisation_lemmatisation_stopwords(text, lang):
    nlp = nlp_fr if lang == "fr" else nlp_en
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return tokens

def ner_medical(text, lang):
    nlp = nlp_fr if lang == "fr" else nlp_en
    doc = nlp(text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    return entities

def pipeline_pretraitement_requete(text):
    try:
        lang = detect(text)
    except:
        lang = "en"
    if lang not in ("fr", "en"):
        lang = "en"

    nettoye = nettoyage_normalisation(text, lang)
    tokens = tokenisation_lemmatisation_stopwords(nettoye, lang)
    entites = ner_medical(nettoye, lang)

    return {
        "langue_detectee": lang,
        "texte_original": text,
        "texte_nettoye": nettoye,
        "tokens": tokens,
        "entites": entites
    }

# Pour tester directement
if __name__ == "__main__":
    texte = "Quels sont les effets secondaires de la chimiothérapie ?"
    resultat = pipeline_pretraitement_requete(texte)
    print(resultat)
