import requests
import json
import os

def make_semantic_scholar_api_call(paper_ids, api_key, field):
    url = 'https://api.semanticscholar.org/graph/v1/paper/batch'
    params = {'fields': field, 'apiKey': api_key}
    payload = {"ids": paper_ids}
    
    print("starting the API call to retrieve data...")
    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None

# Read paper IDs from the JSON file
def filter_paper_ids(filename):
    print("filtering paper ids...")
    with open(filename, 'r') as json_file:
        papers = json.load(json_file)
    return [paper['paperId'] for paper in papers]

# Save papers to a JSON file
def save_to_json(papers, filename):
    print("saving data to a json file...")
    with open(filename, 'w') as json_file:
        json.dump(papers, json_file, indent=2)

# defining paths
root_path= 'D:/BDMA/UPC/SDM/LAB/LAB1'
json_path= os.path.join(root_path, 'semantic_scholar_data science_papers.json')

# API key
api_key = 'NTWZI8h2eS87Rqgr7E05k3TAp28pBbR48WicDcNj'

# Paper IDs
paper_ids = filter_paper_ids(json_path)
print(paper_ids)

# fields required
field= "paperId,url,title,abstract,venue,publicationVenue,year,citationCount,referenceCount,isOpenAccess,influentialCitationCount,fieldsOfStudy,publicationTypes,publicationDate,journal,authors,citations,references,tldr"

# Make API call
result = make_semantic_scholar_api_call(paper_ids, api_key, field)

# saving to a json file
save_to_json(result, f'dataset.json')
