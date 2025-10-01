def count_words(text: str) -> int:
    return len(text.split())

def count_characters(text: str) -> int:
    counter: int = 0

    for word in text.split():
        counter += len(word) 

    return counter

