import requests
import json
import time

def make_semantic_scholar_api_call(api_key, query, limit):
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    params = {'query': query, 'limit': limit}
    papers = []
    total_papers = 0

    try:
        while total_papers < limit:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            result = response.json()
            papers.extend(result['data'])
            total_papers += len(result['data'])
            params['offset'] = total_papers  # Update offset for the next page
            # time.sleep(0.5)  # Add a short delay to avoid hitting rate limits
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")

    return papers[:limit]  # Return at most limit papers

# Save papers to a JSON file
def save_to_json(papers, filename):
    with open(filename, 'w') as json_file:
        json.dump(papers, json_file, indent=2)

# API key
api_key = 'NTWZI8h2eS87Rqgr7E05k3TAp28pBbR48WicDcNj'

# Query for data science related papers
query = 'data science'

# adding limit
limit=100

# Retrieve 1000 papers relevant to data science
papers = make_semantic_scholar_api_call(api_key, query, limit)

# saving to a json file
save_to_json(papers, f'semantic_scholar_{query}_papers.json')