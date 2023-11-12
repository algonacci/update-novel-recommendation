import re
import string
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity

# Download stopwords
nltk.download("stopwords")

# Load and preprocess data
data = pd.read_csv("novel_data.csv")
data["text"] = data["Title"] + " " + data["Description"]
data["text"] = data["text"].str.lower()


def preprocess_text(text):
    text = re.sub(r"\d+", "", text)  # remove numbers
    text = text.translate(str.maketrans(
        "", "", string.punctuation))  # remove punctuation
    text = text.strip()  # remove whitespace leading & trailing
    # remove multiple whitespace into single whitespace
    text = re.sub('\s+', ' ', text)
    text = re.sub(r"\b[a-zA-Z]\b", "", text)  # remove single char
    return text


for col in ['text']:
    data[col] = data[col].apply(preprocess_text)

stop_words = set(stopwords.words('indonesian') + stopwords.words('english'))


def stopwords_removal(words):
    return [word for word in words if word not in stop_words]


data['text'] = data['text'].apply(lambda x: x.split()).apply(stopwords_removal)
data['text'] = data['text'].apply(lambda x: ' '.join(x))

tagged_data = [TaggedDocument(words=doc.split(), tags=[str(i)])
               for i, doc in enumerate(data['text'])]

pvdbow_model = Doc2Vec(tagged_data, vector_size=100,
                       window=3, min_count=2, workers=6, dm=0)

data['pvdbow_vector'] = data['text'].apply(
    lambda x: pvdbow_model.infer_vector(x.split()))

# Create indices for titles
titles = data['Title']
indices = pd.Series(data.index, index=data['Title']).drop_duplicates()


def identify_input_type(input_text, data):
    """
    Identify whether the input text is a title or a description.
    """
    if input_text in data['Title'].values:
        return 'title'
    else:
        return 'description'


def preprocess_and_vectorize(text):
    """
    Preprocess the input text and convert it to a vector using the trained model.
    """
    processed_text = preprocess_text(text)
    processed_text = stopwords_removal(processed_text.split())
    return pvdbow_model.infer_vector(processed_text)


def rec_pvdbow_by_text(input_text, data=data):
    input_type = identify_input_type(input_text, data)
    recommendation = pd.DataFrame(
        columns=['Title', 'Description', 'Genre', 'Author', 'Cover', 'Score', 'Detail'])

    if input_type == 'title':
        idx = indices[input_text]
        pvdbow = cosine_similarity(
            [data['pvdbow_vector'].iloc[idx]], list(data['pvdbow_vector'])).flatten()
    else:
        input_vector = preprocess_and_vectorize(input_text)
        pvdbow = cosine_similarity(
            [input_vector], list(data['pvdbow_vector'])).flatten()

    sim_scores = list(enumerate(pvdbow))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Get top 5 recommendations
    book_indices = [i[0] for i in sim_scores]

    for count, i in enumerate(book_indices):
        recommendation.at[count, 'Title'] = data['Title'].iloc[i]
        recommendation.at[count, 'Description'] = data['Description'].iloc[i]
        recommendation.at[count, 'Genre'] = data['Genre'].iloc[i]
        recommendation.at[count, 'Author'] = data['Author'].iloc[i]
        recommendation.at[count, 'Cover'] = data['Cover'].iloc[i]
        recommendation.at[count, 'Score'] = sim_scores[count][1]
        recommendation.at[count, 'Detail'] = data['Detail'].iloc[i]

    return recommendation
