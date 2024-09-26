import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt', quiet=True)

def tokenize_text(text: str) -> list:
    return sent_tokenize(text)