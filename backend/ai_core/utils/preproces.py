import re
import string
import nltk
nltk.download("stopwords")
nltk.download("punkt_tab")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def text_preprocessing(text: str) -> str:
    text.lower()
    text = _remove_urls(text)
    text = _remove_punctuations(text)
    text = _remove_stop_words(text)
    return text

def _remove_urls(text: str, replacement_text: str ="[URL REMOVED]") -> str:
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    urls = url_pattern.findall(text)

    for url in urls:
        text = text.replace(url, replacement_text)

    return text

def _remove_punctuations(text: str) -> str:
    all_punctuations = string.punctuation
    punctuations_to_remove = all_punctuations.replace("?", "").replace("!", "").replace(".", "")
    translator = str.maketrans('', '', punctuations_to_remove)
    return text.translate(translator)

def _remove_stop_words(text: str) -> str:
    
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))

    filtered_words = [word for word in words if word not in stop_words]

    return " ".join(filtered_words)
