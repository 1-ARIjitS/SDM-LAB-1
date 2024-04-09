import os
import requests
import json

def search_api_call(api_key, query, fields, limit):
    """Perform an API call to search for papers based on a query."""
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    params = {'api_key': api_key, 'query': query, 'limit': limit, 'fields': fields}
    try:
        print(f"Making Search API call for: {query}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        return result['data']
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return []

def batch_api_call(paper_ids, api_key, fields):
    """Fetch details for a batch of paper IDs."""
    url = 'https://api.semanticscholar.org/graph/v1/paper/batch'
    # headers = {'x-api-key': api_key}
    # payload = {'ids': paper_ids, 'fields': fields}
    params = {'fields': fields, 'apiKey': api_key}
    payload = {"ids": paper_ids}
    try:
        print("Making Batch API call...")
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return []

def make_folder(folder_path):
    """Create a folder if it does not exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def save_to_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def main():
    root_path = "D:/BDMA/UPC/SDM/LAB/LAB1/project"
    json_folder_path = os.path.join(root_path, "JSON_files")
    make_folder(json_folder_path)

    api_key = 'NTWZI8h2eS87Rqgr7E05k3TAp28pBbR48WicDcNj'  # Replace with your actual API key
    search_fields = 'paperId'  # Fields used in the search call
    batch_fields=  "paperId,url,title,abstract,venue,publicationVenue,year,citationCount,referenceCount,isOpenAccess,influentialCitationCount,fieldsOfStudy,publicationTypes,publicationDate,journal,authors,citationStyles,citations,references,tldr,externalIds"
    limit = 100

    queries = ['data science', 'data warehouse', 'machine learning', 'semantic data', 'database']
    all_search_results = []
    all_paper_ids = []

    for query in queries:
        search_papers = search_api_call(api_key, query, search_fields, limit)
        all_search_results.extend(search_papers)
        all_paper_ids.extend([paper['paperId'] for paper in search_papers])

    # Save the aggregated search results to a JSON file
    aggregated_json_filepath = os.path.join(json_folder_path, 'aggregated_search_results.json')
    save_to_json(all_search_results, aggregated_json_filepath)

    # Fetch and save detailed information for each paper
    detailed_papers = batch_api_call(all_paper_ids, api_key, batch_fields)
    detailed_json_filepath = os.path.join(json_folder_path, 'detailed_paper_info.json')
    save_to_json(detailed_papers, detailed_json_filepath)

    print(f"All search results have been saved to: {aggregated_json_filepath}")
    print(f"Detailed paper information has been saved to: {detailed_json_filepath}")

if __name__ == "__main__":
    main()
