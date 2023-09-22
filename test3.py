import nltk
import imdb

ia = imdb.Cinemagoer()
# Set up SQLite caching
movies = ia.search_movie('Avengers: Endgame')

def plot():
    plot_str = ''
    for i in movies[0]["plot"]:
        plot_str += str(i)
    return plot_str



# Download the NLTK sentence tokenizer data if not already downloaded
nltk.download("punkt")

# Import the NLTK sentence tokenizer
from nltk.tokenize import sent_tokenize

# Sample text
text = plot()

# Tokenize the text into sentences
sentences = sent_tokenize(text)

# Get the first sentence
if sentences:
    first_sentence = sentences[0]
    print("First Sentence:", first_sentence)
else:
    print("No sentences found in the text.")
