import nltk
import imdb

ia = imdb.Cinemagoer()
# Set up SQLite caching
movies = ia.search_movie('Avengers: Endgame')
# Fetch additional details, including images
ia.update(movies[0])
def plotp():
    plot_str = ''
    for i in movies[0]["plot"]:
        plot_str += str(i)
    return plot_str

# Sample text
text = plotp()

print(text)

# Download the NLTK sentence tokenizer data if not already downloaded
nltk.download("punkt")

# Import the NLTK sentence tokenizer
from nltk.tokenize import sent_tokenize



# Tokenize the text into sentences
sentences = sent_tokenize(text)

# Get the first sentence
if sentences:
    first_sentence = sentences[0]
    print("First Sentence:", first_sentence)
else:
    print("No sentences found in the text.")
