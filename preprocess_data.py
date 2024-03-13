import os
import pandas as pd
import json
import csv
import ast
import random
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy
import argparse

# def load_json
def load_json(json_filepath):
    print("loading the json file...")
    with open(json_filepath, "r") as json_file:
        data = json.load(json_file)
    return data

# Covert JSON to CSV with basic fields
def convert_json_to_csv(json, headers, csv_folder_path):
    # Normalize the JSON data
    df = pd.json_normalize(json, max_level=0)
    df= df[headers]
    raw_data_path= os.path.join(csv_folder_path,'ml_raw_data.csv') 
    df.to_csv(raw_data_path, index=False)

# Extract keywords from an abstract using spaCy
def extract_keywords(abstract):
    # Load English language model for spacy
    nlp = spacy.load("en_core_web_sm")
    updated_keywords=[]
    try:
        # Extracting tokens that are nouns or adjectives (you can modify this based on your requirements)
        doc = nlp(abstract)
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]
        print(keywords)
        updated_keywords= random.sample(keywords, 5)
    except:
        pass
    return updated_keywords

# add reviewers
def add_reviewers(df):
    print("adding reviewers for each paper...")
    # extracting all the authors
    author_pool=[]
    for author_list in df['authors']:
        author_pool.extend(ast.literal_eval(author_list))

    df['reviewers']=0
    for i, author_list in enumerate(df['authors']):
        authors= ast.literal_eval(author_list)
        not_reviewer_list= []
        valid_reviewer_list=[]
        for dict in authors:
            for key, value in dict.items():
                if key=='author_id':
                    not_reviewer_list.append(value)
        for dict in author_pool:
            if dict['authorId'] not in not_reviewer_list:
                valid_reviewer_list.append(dict)
        reviewers= list(random.sample(valid_reviewer_list, 3))
        print(reviewers)
        df.at[i, 'reviewers']= reviewers

    return df

# add keywords to the dataframe
def add_keywords(df):
    print("adding keywords for each paper...")
    # Apply the function to each row in the DataFrame
    df['keywords'] = df['abstract'].apply(extract_keywords)
    return df

def add_publication_type(df):
    print("adding publication type of each paper to the dataframe...")
    df['publicationType']=0
    for index, row in df.iterrows():
        try:
            publication_dict= ast.literal_eval(row['publicationVenue'])
            publication_type= str(publication_dict['type'])
            # Add the modified entry to the DataFrame
            df.at[index, 'publicationType'] = publication_type
        except:
            df.at[index, 'publicationType'] = 'journal'
    return df

# remove duplicate papers
def remove_duplicate_papers(df):
    print("removing duplicate papers...")
    df.drop_duplicates(subset='paperId', keep='first', inplace=True)
    return df

# saving it to new csv file
def save_updated_csv(df):
    print("saving the upadted csv file...")
    updated_csv_filepath= os.path.join(csv_folder_path, "ml_updated_data.csv")
    df.to_csv(updated_csv_filepath, index=False)

# adding flags 
parser = argparse.ArgumentParser(description="Script to preprocess the raw JSON obtained from the semantic scholar API call")
parser.add_argument('-rp', '--root_path', type=str, help='Root path for the files')
parser.add_argument('-jp', '--json_path', type=str, help='Path to the JSON file')

args = parser.parse_args()

# Accessing the values of the flags
root_path = args.root_path
json_file_path = args.json_path
json_folder_path= os.path.join(root_path, 'JSON_files')
csv_folder_path= os.path.join(root_path, 'CSV_files')
csv_file_path= os.path.join(csv_folder_path, "ml_raw_data.csv")

# loading the json file
json_data= load_json(json_filepath= json_file_path)

# Define headers for CSV file
headers = ["paperId", "publicationVenue", "title", "abstract", "venue", "year", "citationCount", "referenceCount", "fieldsOfStudy", "publicationTypes", "journal", "authors", "citations", "references"]

# convert json to csv
convert_json_to_csv(json_data, headers, csv_folder_path)

# read the csv file and include reviewers
print("reading the raw csv file...")
df= pd.read_csv(csv_file_path, delimiter=',')
df_w_reviewers= add_reviewers(df)

# change the csv file to include keywords as well
df_w_reviwers_n_keywords= add_keywords(df_w_reviewers)

# adding the type of paper like journal, review or workshop
df_w_type= add_publication_type(df_w_reviwers_n_keywords)

# remove rows with same paperId
updated_df= remove_duplicate_papers(df_w_type)

# saving the csv file
save_updated_csv(updated_df)