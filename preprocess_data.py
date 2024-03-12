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
    with open(json_filepath) as json_file:
        data = json.load(json_file)
    return data

# Cobvert JSON to CSV with basic fields
def convert_json_to_csv(data, csv_file_path, headers):
    # Write to CSV file
    print("converting json to csv...")
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        row_data=[]
        # Iterate over each paper
        for paper in data:
            # Extract data for each row
            try:
                row_data = [
                    str(paper["paperId"]),
                    str(paper["title"]),
                    str(paper["abstract"]),
                    str(paper["venue"]),
                    dict(paper["publicationVenue"]),
                    str(paper["year"]),
                    str(paper["citationCount"]),
                    str(paper["referenceCount"]),
                    str(paper["fieldsOfStudy"]),
                    list(paper["publicationTypes"]),
                    dict(paper["journal"]),
                    list(paper["authors"]),
                    [citation["paperId"] for citation in paper["citations"]],
                    [reference["paperId"] for reference in paper["references"]]
                ]
            except:
                pass
            writer.writerow(row_data)

# Extract keywords from an abstract using spaCy
def extract_keywords(abstract):
    # Load English language model for spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(abstract)
    # Extracting tokens that are nouns or adjectives (you can modify this based on your requirements)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]
    print(keywords)
    updated_keywords=[]
    try:
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
# remove duplicate papers
def remove_duplicate_papers(df):
    print("removing dupliacte papers...")
    df.drop_duplicates(subset='paperId', keep='first', inplace=True)
    return df

# saving it to new csv file
def save_updated_csv(df):
    print("saving the upadted csv file...")
    updated_csv_filepath= os.path.join(csv_folder_path, "updated_data.csv")
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
csv_file_path= os.path.join(csv_folder_path, "raw_data.csv")

# loading the json file
json_data= load_json(json_filepath= json_file_path)

# Define headers for CSV file
headers = ["paperId", "title", "abstract", "venue", "publicationVenue", "year", "citationCount", "referenceCount", "fieldOfStudy", "publicationTypes", "journal", "authors", "citations", "references"]

# convert json to csv
convert_json_to_csv(json_data, csv_file_path, headers)

# read the csv file and include reviewers
print("reading the raw csv file...")
df= pd.read_csv(csv_file_path, delimiter=',')
df_w_reviewers= add_reviewers(df)

# change the csv file to include keywords as well
df_w_reviwers_n_keywords= add_keywords(df_w_reviewers)

# remove rows with same paperId
updated_df= remove_duplicate_papers(df_w_reviwers_n_keywords)

# saving the csv file
save_updated_csv(updated_df)