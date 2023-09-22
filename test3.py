import nltk

# Download the NLTK sentence tokenizer data if not already downloaded
nltk.download("punkt")

# Import the NLTK sentence tokenizer
from nltk.tokenize import sent_tokenize

# Sample text
text = "This is the first sentence. This is the second sentence. And this is the third sentence."

# Tokenize the text into sentences
sentences = sent_tokenize(text)

# Get the first sentence
if sentences:
    first_sentence = sentences[0]
    print("First Sentence:", first_sentence)
else:
    print("No sentences found in the text.")
