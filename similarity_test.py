from sentence_transformers import SentenceTransformer 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
import json

# define the model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2') 

# load abbreviations json file
with open("fin_abbreviations.json") as file:
    abv = json.load(file)

def replace_abbreviations(sentence, abbreviation_dict):
    # need to change dtype
    sentence = str(sentence)
    words = sentence.split()
    updated_sentence = []

    for word in words:
        # Remove punctuation from the word
        cleaned_word = word.strip(',!?()[]{}:;"\'')
        
        # Check if the cleaned word is an abbreviation in the dictionary
        if cleaned_word in abbreviation_dict:
            updated_sentence.append(abbreviation_dict[cleaned_word])
        else:
            updated_sentence.append(word)

    return ' '.join(updated_sentence)

def compare(input_1,input_2):
    input_1=replace_abbreviations(sentence=input_1,abbreviation_dict=abv)
    input_2=replace_abbreviations(sentence=input_2,abbreviation_dict=abv)

    sentences = [input_1,input_2]
    embeddings = model.encode(sentences)
    type(embeddings)

    # calculate cosine similarity
    embed_1 = np.array(embeddings[0])
    embed_2 = np.array(embeddings[1])

    embed_1 = embed_1.reshape(1,-1)
    embed_2 = embed_2.reshape(1,-1)

    similarity = cosine_similarity(embed_1,embed_2)[0][0]
    return similarity


# s1 = "profit before tax"
# s2 = "PBT"

# print(compare(s1,s2))
