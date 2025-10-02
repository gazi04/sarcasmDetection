import re
import string

def text_preprocessing(text: str) -> str:
    text.lower()
    text = _remove_urls(text)
    text = _remove_punctuations(text)
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
    tokens = text.split()
    
    basic_stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at'}
    tokens = [token for token in tokens if token not in basic_stop_words]
    
    return ' '.join(tokens)
