import re
import spacy
from langdetect import detect

# Charger les modèles spaCy complets
nlp_fr = spacy.load("fr_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")

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
