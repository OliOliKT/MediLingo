from docx import Document
import os
import re
import spacy as sp
from nltk.stem.snowball import DanishStemmer
import lemmy

# Read .docx file and return the text in list format
def read_docx(file_path):
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return ' '.join(text)

current_directory = os.path.dirname(__file__)
file_name = "merged_transcriptions.docx"
file_path = os.path.join(current_directory, file_name)
text = read_docx(file_path)

# To lower case
lower_cased = text.lower()

# Remove punctuation
pattern = r'[^\w\s]'
text = re.sub(pattern, '', lower_cased)

# Remove stopwords
nlp = sp.load("da_core_news_sm")
doc = nlp(text)
filtered_tokens = [token.text for token in doc if not token.is_stop]

# Remove specific words
names = ["oliver", "sonja", "arthur", "charlotte"]
tokens_without_names = list(filter(lambda x: x not in names, filtered_tokens))

# Normalize text with stemming
stemmer = DanishStemmer()
stemmed_tokens = [stemmer.stem(token) for token in tokens_without_names]

# Normalize text with lemmatization
lemmatizer = lemmy.load("da")
lemmatized_tokens = [lemmatizer.lemmatize("", token) for token in stemmed_tokens]

# Print results
print(len(lemmatized_tokens))
print(lemmatized_tokens)