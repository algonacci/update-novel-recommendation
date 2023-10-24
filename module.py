import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords")

data = pd.read_csv("novel_data.csv")
data["text"] = data["Title"] + " " + data["Description"]
data["text"] = data["text"].str.lower()
# data["Genre_low"] = data["Genre"].str.lower()
# data["Author_low"] = data["Author"].str.lower()


def preprocess_text(text):
    # remove numbers
    text = re.sub(r"\d+", "", text)
    # remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # remove whitespace leading & trailing
    text = text.strip()
    # remove multiple whitespace into single whitespace
    text = re.sub('\s+', ' ', text)
    # remove single char
    text = re.sub(r"\b[a-zA-Z]\b", "", text)
    return text


for col in ['text']:
    data[col] = data[col].apply(preprocess_text)

stop_words = set(stopwords.words('indonesian') + stopwords.words('english'))


def stopwords_removal(words):
    return list(set(words) - stop_words)


data['text'] = data['text'].apply(stopwords_removal)
data['text'] = data['text'].agg(lambda x: ' '.join(map(str, x)))

tagged_data = [TaggedDocument(words=doc.split(), tags=[str(i)])
               for i, doc in enumerate(data['text'])]

pvdbow_model = Doc2Vec(tagged_data, vector_size=100,
                       window=3, min_count=2, workers=6, dm=0)

data['pvdbow_vector'] = data['text'].apply(
    lambda x: pvdbow_model.infer_vector(x.split()))

pvdbow = data['pvdbow_similarity'] = data['pvdbow_vector'].apply(
    lambda x: cosine_similarity([x], list(data['pvdbow_vector'])).flatten())

data = data.reset_index()
titles = data['Title']
indices = pd.Series(data.index, index=data['Title']).drop_duplicates()


def rec_pvdbow(title, data=data):
    recommendation = pd.DataFrame(
        columns=['Title', 'Description', 'Genre', 'Author', 'Cover', 'Score', 'Detail'])
    count = 0

    idx = indices[title]
    sim_scores = list(enumerate(pvdbow[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Get top 5 recommendations
    book_indices = [i[0] for i in sim_scores]

    for i in book_indices:
        recommendation.at[count, 'Title'] = data['Title'].iloc[i]
        recommendation.at[count, 'Description'] = data['Description'].iloc[i]
        recommendation.at[count, 'Genre'] = data['Genre'].iloc[i]
        recommendation.at[count, 'Author'] = data['Author'].iloc[i]
        recommendation.at[count, 'Cover'] = data['Cover'].iloc[i]
        recommendation.at[count, 'Score'] = sim_scores[count][1]
        recommendation.at[count, 'Detail'] = data['Detail'].iloc[i]
        count += 1

    return recommendation
