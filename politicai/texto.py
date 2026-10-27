"""Limpieza de texto y métricas sencillas para comparar programas electorales."""

import re
from collections import Counter

import numpy as np

# Palabras muy frecuentes en los programas que no aportan significado.
PALABRAS_EXCLUIDAS = ["lectura", "fácil", "maspaises", "n", "programa", "elecciones", "generales", "resumen"]


class CleanText:
    """Prepara un texto en castellano para contar palabras.

    `do_all` deja las palabras tal cual (para nubes de palabras) y
    `do_all_stem` las reduce a su raíz (para comparar temas sin que importen
    plurales ni conjugaciones).

    Necesita los recursos de NLTK ``punkt``, ``stopwords`` y ``wordnet``
    (``nltk.download(...)``).
    """

    def __init__(self, banned_words=PALABRAS_EXCLUIDAS):
        from nltk.corpus import stopwords

        self.banned_words = set(banned_words)
        self.stopwords = set(stopwords.words("spanish"))

    def tokens(self, text):
        """Devuelve las palabras de `text` en minúsculas, sin HTML, números, puntuación ni stopwords."""
        from bs4 import BeautifulSoup
        import nltk

        text = BeautifulSoup(text, "html.parser").get_text()
        text = re.sub(r"\[[^]]*\]", "", text)
        text = re.sub(r"[-+]?[0-9]+", "", text)
        words = (re.sub(r"[^\w\s]", "", w.lower()) for w in nltk.word_tokenize(text))
        return [w for w in words if w and w not in self.stopwords and w not in self.banned_words]

    def do_all(self, text):
        """Texto limpio, con las palabras separadas por espacios."""
        return " ".join(self.tokens(text))

    def do_all_stem(self, text):
        """Como `do_all`, pero con cada palabra reducida a su raíz."""
        from nltk.stem import SnowballStemmer, WordNetLemmatizer

        stemmer = SnowballStemmer("spanish")
        lemmatizer = WordNetLemmatizer()
        return " ".join(lemmatizer.lemmatize(stemmer.stem(w), pos="v") for w in self.tokens(text))


def frecuencias(texto):
    """Cuenta cuántas veces aparece cada palabra de un texto separado por espacios."""
    return dict(Counter(texto.split(" ")))


def cobertura_tema(texto, tema):
    """Porcentaje de palabras de `texto` que pertenecen al conjunto `tema`."""
    palabras = texto.split(" ")
    return np.round(100 * sum(1 for p in palabras if p in tema) / len(palabras), 2)


def cobertura_temas(texto, temas):
    """Aplica `cobertura_tema` a cada tema de un diccionario {nombre: palabras}."""
    return {nombre: cobertura_tema(texto, palabras) for nombre, palabras in temas.items()}
