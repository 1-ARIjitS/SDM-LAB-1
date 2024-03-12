import os
import pandas as pd
import numpy as np
import spacy
import ast
import requests
import json
import argparse

# extract paperIds in a particular field ex- data science, machine learning etc. (GET- search)
def search_api_call(api_key, query, fields, limit):
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    params = {'api_key': api_key, 'query': query, 'limit': limit, 'fields':fields}
    papers = []
    print("Making Search API call...")
    try:
      response = requests.get(url, params=params)

      # Raise an exception for HTTP errors
      response.raise_for_status()

      # get papers
      result = response.json()
      papers.extend(result['data'])
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")

    # Return the papers
    print("saving results of serach API call...")
    return papers 

# Read paper IDs from the JSON file
def filter_paper_ids(filename):
    print("filtering paper ids...")
    with open(filename, 'r') as json_file:
        papers = json.load(json_file)
    return [paper['paperId'] for paper in papers]

# extract the whole data for different paperIds (POST- batch)
def batch_api_call(paper_ids, api_key, fields):
    url = 'https://api.semanticscholar.org/graph/v1/paper/batch'
    params = {'fields': fields, 'apiKey': api_key}
    payload = {"ids": paper_ids}
    
    print("Making Batch API call...")
    try:
        response = requests.post(url, params=params, json=payload)

        # Raise an exception for HTTP errors
        response.raise_for_status() 
        print("saving results of Batch API call...") 
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None

# make folders
def make_folder(folder_path):
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)

# Save papers to a JSON file
def save_to_json(papers, filename):
    with open(filename, 'w') as json_file:
        json.dump(papers, json_file, indent=2)
        
# adding flags 
parser = argparse.ArgumentParser(description="Script for semantic scholar API call")
parser.add_argument('-rp', '--root_path', type=str, help='Root path for the files')

args = parser.parse_args()

# Accessing the values of the flags
root_path = args.root_path

# JSON folder path
json_folder_path= os.path.join(root_path, "JSON_files")
make_folder(json_folder_path)

# CSV folder path
csv_folder_path= os.path.join(root_path, "CSV_files")
make_folder(csv_folder_path)

# API key
api_key = 'NTWZI8h2eS87Rqgr7E05k3TAp28pBbR48WicDcNj'

# for search API call
# Query for particular field related papers
query = 'machine learning'
# adding limit
limit= 100
# search fields
search_field='paperId'
# Retrieve 100 papers relevant to data science
search_papers = search_api_call(api_key, query, search_field, limit)
# saving to a json file
json_filepath= os.path.join(json_folder_path, f'search_{query}.json')
save_to_json(search_papers, json_filepath)

# for batch API call
# filtering Paper IDs
paper_ids = filter_paper_ids(json_filepath)
print(paper_ids)
# fields required
batch_fields= "paperId,url,title,abstract,venue,publicationVenue,year,citationCount,referenceCount,isOpenAccess,influentialCitationCount,fieldsOfStudy,publicationTypes,publicationDate,journal,authors,citations,references,tldr"
# Retrieve batch info of all the 100 papers above
batch_papers = batch_api_call(paper_ids, api_key, batch_fields)
# saving to a json file
json_filepath= os.path.join(json_folder_path, f'raw_dataset.json')
save_to_json(batch_papers, json_filepath)