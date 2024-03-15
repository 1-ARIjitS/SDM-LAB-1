
from faker import Faker
import pandas as pd
import json
import os
import random
from faker import Faker
from faker.providers import address, internet, lorem, sbn
from faker_education import SchoolProvider
from random import choice, randint, uniform
import pandas as pd
import numpy as np
import uuid


fake = Faker()
fake.add_provider(internet)
fake.add_provider(sbn)
fake.add_provider(address)
fake.add_provider(lorem)

import os
import pandas as pd
import json
import ast
import spacy
import nltk
from spacy.lang.en import English

departments = [
    "Computer Science",
    "Computer Engineering",
    "Information Technology",
    "Software Engineering",
    "Data Science",
    "Artificial Intelligence",
    "Machine Learning",
    "Human-Computer Interaction",
    "Cybersecurity",
    "Network Engineering",
    "Digital Media",
    "Game Development",
    "Virtual Reality",
    "Augmented Reality",
    "Cloud Computing",
    "Systems Architecture",
    "Bioinformatics",
    "Quantum Computing",
    "Robotics",
    "Blockchain Technology",
    "Big Data Analytics",
    "Internet of Things",
    "Computational Biology",
    "Graphics and Visualization",
    "Information Systems"
]

universities = [
    "Universitat Polytecnica De Catanlunya",
    "Universitat Libre De Brussels",
    "University of Oxford",
    "Harvard University",
    "Stanford University",
    "Massachusetts Institute of Technology",
    "University of Cambridge",
    "California Institute of Technology",
    "Princeton University",
    "University of California, Berkeley",
    "Yale University",
    "University of Chicago",
    "Columbia University",
    "University of Tokyo",
    "University of Michigan",
    "Cornell University",
    "University of Pennsylvania",
    "Tsinghua University",
    "ETH Zurich",
    "University of Toronto",
    "University College London",
    "Imperial College London",
    "National University of Singapore",
    "University of California, Los Angeles",
    "New York University",
    "Duke University",
    "University of Edinburgh",
    "Peking University",
    "University of Illinois at Urbana-Champaign",
    "University of Washington",
    "Johns Hopkins University",
    "University of California, San Diego",
    "London School of Economics and Political Science",
    "University of British Columbia",
    "University of Hong Kong",
    "King's College London",
    "University of Texas at Austin",
    "McGill University",
    "University of California, San Francisco",
    "Northwestern University",
    "Kyoto University",
    "Seoul National University",
    "University of Wisconsin-Madison",
    "University of Melbourne",
    "Georgia Institute of Technology",
    "University of Sydney",
    "Ecole Polytechnique Fédérale de Lausanne",
    "University of Queensland",
    "University of Amsterdam",
    "Sorbonne University",
    "University of Manchester",
    "Australian National University",
    "University of Southern California",
    "University of Chicago",
    "University of Munich",
    "University of Zurich",
    "University of Copenhagen",
    "Technical University of Munich",
    "Ludwig Maximilian University of Munich",
    "Monash University",
    "KU Leuven",
    "University of New South Wales",
    "University of São Paulo",
    "Heidelberg University",
    "Delft University of Technology",
    "University of California, Davis",
    "University of Maryland, College Park",
    "University of Helsinki",
    "University of Auckland",
    "University of Western Australia",
    "Karolinska Institute",
    "Purdue University",
    "University of Zurich",
    "University of Glasgow",
    "University of Alberta",
    "University of Oslo",
    "University of Sheffield",
    "University of Geneva",
    "Leiden University",
    "University of Groningen",
    "Utrecht University",
    "Erasmus University Rotterdam",
    "Wageningen University & Research",
    "VU Amsterdam",
    "University of Warwick",
    "Durham University",
    "University of Southampton",
    "Lancaster University",
    "University of York",
    "University of Bath",
    "University of Exeter",
    "University of Leicester",
    "University of Sussex",
    "University of Surrey",
    "University of Reading",
    "Cardiff University",
    "Queen Mary University of London",
    "City, University of London",
    "Brunel University London",
    "Birkbeck, University of London",
    "University of East Anglia",
    "University of Essex",
    "University of Kent",
    "Royal Holloway, University of London",
]



# Download necessary NLTK data and load spaCy's 'en_core_web_sm' model
nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")

def load_json(json_filepath):
    """Load JSON data from a file."""
    with open(json_filepath, 'r') as json_file:
        return json.load(json_file)


def flatten_data(json_data):
    """Flatten JSON data excluding authors."""
    flattened_data = []
    for paper in json_data:
        # Ensure publicationTypes is an iterable (list)
        publication_types = paper.get("publicationTypes", [])
        if not isinstance(publication_types, list):
            publication_types = [publication_types] if publication_types else []
        publication_types_str = ', '.join(publication_types)

        # Ensure fieldsOfStudy is an iterable (list)
        fields_of_study = paper.get("fieldsOfStudy", [])
        if not isinstance(fields_of_study, list):
            fields_of_study = [fields_of_study] if fields_of_study else []
        fields_of_study_str = ', '.join(fields_of_study)

        flattened_paper = {
            "paperId": paper.get("paperId", ""),
            "title": paper.get("title", ""),
            "abstract": paper.get("abstract", ""),
            "venue": paper.get("venue", ""),
            "year": paper.get("year", ""),
            "citationCount": paper.get("citationCount", ""),
            "referenceCount": paper.get("referenceCount", ""),
            "fieldsOfStudy": fields_of_study_str,
            "publicationTypes": publication_types_str,
        }
        flattened_data.append(flattened_paper)
    return flattened_data


def extract_and_save_authors(json_data, csv_folder_path):
    authors = []
    author_writes = []

    for paper in json_data:
        paper_id = paper.get("paperId", "")
        is_corresponding = True  # Assuming the first author is the corresponding author

        for author in paper.get("authors", []):
            author_id = author.get("authorId", "")
            name = author.get("name", "")
            email = fake.email()
            department = random.choice(departments) 
            institution = random.choice(universities)

            authors.append({
                "authorId": author_id,
                "name": name,
                "email": email,
                "institution": institution,
                "department": department,
                "paperId": paper_id 
            })

            author_writes.append({
                "start_id": author_id,
                "end_id": paper_id,
                "corresponding_author": is_corresponding
            })

            is_corresponding = False  # Only the first author is marked as corresponding

    # Convert lists to DataFrames
    authors_df = pd.DataFrame(authors)
    author_writes_df = pd.DataFrame(author_writes)

    # Save to CSV
    authors_df.to_csv(os.path.join(csv_folder_path, "authors.csv"), index=False)
    author_writes_df.to_csv(os.path.join(csv_folder_path, "author_writes.csv"), index=False)

    print("Authors and author_writes data saved.")
    
    

# Load the authors data from CSV
authors_df = pd.read_csv("/home/pce/Pictures/data/authors.csv")

# Assuming we have a DataFrame papers_df for papers from your JSON data
# For demonstration, let's create a mock papers_df
papers_df = pd.DataFrame({
    "paperId": authors_df["paperId"].unique()  # Extract unique paper IDs from authors data
})

def assign_reviewers(authors_df, papers_df):
    reviewer_assignments = pd.DataFrame(columns=['paperId', 'reviewerId'])
    reviews = []  # Use a list to collect data
    
    # Iterate over each paper
    for paper_id in papers_df['paperId']:
        # Exclude authors of the current paper from potential reviewers
        paper_authors_ids = authors_df[authors_df['paperId'] == paper_id]['authorId'].unique()
        potential_reviewers = authors_df[~authors_df['authorId'].isin(paper_authors_ids)]
        
        if len(potential_reviewers) >= 3:
            # Randomly select 3 reviewers
            selected_reviewers = potential_reviewers.sample(3)['authorId']
            for reviewer_id in selected_reviewers:
                reviews.append({'paperId': paper_id, 'reviewerId': reviewer_id})
        else:
            print(f"Not enough unique reviewers for paper {paper_id}")

    return pd.DataFrame(reviews)


# Assuming papers_df is already defined or loaded
reviewer_assignments_df = assign_reviewers(authors_df, papers_df)
reviewer_assignments_df.to_csv('/home/pce/Pictures/data/author_review_papers.csv', index=False)
print("Authors review paper data saved.")


    
def extract_keywords(abstract):
    if not abstract:
        return []
    doc = nlp(abstract)
    return [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]

def add_reviewers(df, authors_df):
    authors_list = authors_df[['authorId', 'name']].drop_duplicates().to_dict('records')
    random.seed(42)  # For reproducibility
    df['reviewers'] = df['paperId'].apply(lambda x: random.sample(authors_list, 3))
    return df

def add_keywords(df):
    df['keywords'] = df['abstract'].apply(extract_keywords)
    return df

def add_publication_type(df):
    # This is a placeholder. Adjust the logic based on your JSON structure
    df['publicationType'] = 'Journal'
    return df

def remove_duplicate_papers(df):
    df.drop_duplicates(subset='paperId', keep='first', inplace=True)
    return df




def extract_and_process_paper_keyword_data(json_data, papers_csv_path, keywords_csv_path, paper_keyword_csv_path):
    papers = []
    keywords_data = {"ID": [], "name": [], "domain": [], "keyword_abstract": []}
    paper_has_keywords = {"START_ID": [], "END_ID": []}
    keywords_dict = {}

    for paper in json_data:
        paper_id = paper.get("paperId")
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        doi = paper.get("externalIds", {}).get("DOI", "")
        link = paper.get("url", "")
        citation_count = paper.get("citationCount", 0)
        reference_count = paper.get("referenceCount", 0)
        year = paper.get("year", "")

        journal_info = paper.get("journal")
        pages = journal_info.get("pages") if journal_info and "pages" in journal_info else f"{random.randint(1, 100)}-{random.randint(101, 200)}"

        papers.append({
            "paperId": paper_id,
            "title": title,
            "abstract": abstract,
            "pages": pages,
            "DOI": doi,
            "link": link,
            "citationCount": citation_count,
            "referenceCount": reference_count,
            "year": year,
        })

        if paper.get("fieldsOfStudy") is None or len(paper.get("fieldsOfStudy", [])) == 0:
            paper_has_keywords["START_ID"].append(paper.get("paperId"))
            paper_has_keywords["END_ID"].append(choice(list(keywords_dict.values())))
        else:
            for fs in paper.get("fieldsOfStudy"):
                fs_id = str(uuid.uuid4())
                if fs not in keywords_dict:
                    keywords_data["ID"].append(fs_id)
                    keywords_data["name"].append(fs)
                    keywords_data["domain"].append(paper.get("fieldsOfStudy")[0])
                    keywords_data["keyword_abstract"].append(extract_keywords(abstract))

                k_id = keywords_dict.setdefault(fs, fs_id)

                paper_has_keywords["START_ID"].append(paper.get("paperId"))
                paper_has_keywords["END_ID"].append(k_id)


    pd.DataFrame(papers).to_csv(papers_csv_path, index=False)
    pd.DataFrame(keywords_data).to_csv(keywords_csv_path, index=False)
    pd.DataFrame(paper_has_keywords).to_csv(paper_keyword_csv_path, index=False)

    print(f"Papers data saved to {papers_csv_path}")
    print(f"Keywords data saved to {keywords_csv_path}")
    print(f"Paper-Keyword relationships saved to {paper_keyword_csv_path}")
    
    

def extract_citations_and_save(json_data, papers_csv_path, citations_csv_path):
    # Load papers data
    papers_df = pd.read_csv(papers_csv_path)

    # Initialize list for paper citations
    paper_citations = []

    for paper in json_data:
        paper_id = paper.get("paperId")
        citations = paper.get("citations", [])
        
        for citation in citations:
            cited_paper_id = citation.get("paperId")
            cited_paper_title = citation.get("title")
            
            # Ensure the citation is not self-referencing
            if paper_id != cited_paper_id:
                paper_citations.append({
                    "paper_id": paper_id,
                    "cited_paper_id": cited_paper_id,
                    "title": cited_paper_title
                })
    
    # Convert list to DataFrame
    paper_citations_df = pd.DataFrame(paper_citations)

    # Merge with papers_df to ensure cited_paper_id exists in the dataset and get the title
    paper_citations_df = paper_citations_df.merge(papers_df[['paperId', 'title']], how='left', left_on='cited_paper_id', right_on='paperId')
    paper_citations_df.drop(['paperId'], axis=1, inplace=True)
    paper_citations_df.rename(columns={'title_y': 'cited_paper_title'}, inplace=True)

    # Save to CSV
    paper_citations_df.to_csv(citations_csv_path, index=False)
    print(f"Citations data saved to {citations_csv_path}")


def process_journal_data(json_data, csv_folder_path):
    print("Creating journal node...")
    journals = []
    paper_published_in_journal = []

    for paper in json_data:
        paper_id = paper.get("paperId", "")
        publication_venue = paper.get("publicationVenue")
        journal_info = paper.get("journal", {})
        venue = paper.get("venue", "")
        year = paper.get("year", "")

        # Skip if publicationVenue is None
        if publication_venue is None:
            continue

        publication_id = publication_venue.get("id", "")
        publication_type = publication_venue.get("type", "")
        
        # Initialize name, issn, url, and volume with default values or values from journal_info if available
        name = ""
        issn = ""
        url = ""
        volume = "1"  # Default to '1' if not available
        
        if journal_info:  # Check if journal_info is not None
            name = journal_info.get("name", "")
            volume = journal_info.get("volume", "1")
        
        # Retrieve issn and url from publication_venue if available
        issn = publication_venue.get("issn", "")
        url = publication_venue.get("url", "")

        # Only consider journals
        if publication_type.lower() == 'journal':
            journals.append({
                "publicationId": publication_id,
                "publicationType": publication_type,
                "name": name,
                "venue": venue,
                "year": year,
                "issn": issn,
                "url": url,
                "volume": volume,
            })

            paper_published_in_journal.append({
                "START_ID": paper_id,
                "END_ID": publication_id
            })

    # Save journals data to CSV
    pd.DataFrame(journals).to_csv(os.path.join(csv_folder_path, "journal.csv"), index=False)
    # Save paper published in journal data to CSV
    pd.DataFrame(paper_published_in_journal).to_csv(os.path.join(csv_folder_path, "paper_published_in_journal.csv"), index=False)

    print("Journal data and paper_published_in_journal data saved.")

  
def extract_and_save_conferences(json_data, csv_folder_path):
    print("Creating conference node...")
    conferences = []
    paper_presented_in_conference = []

    for paper in json_data:
        paper_id = paper.get("paperId", "")
        publication_venue = paper.get("publicationVenue", {}) if paper.get("publicationVenue") is not None else {}
        publication_type = publication_venue.get("type", "").lower() if publication_venue else ""
        venue = paper.get("venue", "")
        
        if publication_type == "conference":
            publication_id = publication_venue.get("id", "")
            name = publication_venue.get("name", "")
            year = paper.get("year", "")
            issn = publication_venue.get("issn", "") if "issn" in publication_venue else ""
            url = publication_venue.get("url", "") if "url" in publication_venue else ""
            edition = random.randint(1, 30)  # Randomly assign an edition number

            conferences.append({
                "publicationId": publication_id,
                "publicationType": publication_type,
                "name": name,
                "year": year,
                "venue": venue,
                "issn": issn,
                "url": url,
                "edition": edition
            })

            paper_presented_in_conference.append({
                "START_ID": paper_id,
                "END_ID": publication_id
            })

    # Convert to DataFrame and save to CSV
    df_conferences = pd.DataFrame(conferences)
    df_conferences.to_csv(os.path.join(csv_folder_path, "conferences.csv"), index=False)

    df_paper_presented_in_conference = pd.DataFrame(paper_presented_in_conference)
    df_paper_presented_in_conference.to_csv(os.path.join(csv_folder_path, "paper_presented_in_conference.csv"), index=False)

    print("Conferences and paper_presented_in_conference data saved.")

   
def extract_and_save_workshop(json_data, csv_folder_path):
    print("Creating workshop node...")
    conferences = []
    paper_presented_in_conference = []

    for paper in json_data:
        paper_id = paper.get("paperId", "")
        publication_venue = paper.get("publicationVenue", {}) if paper.get("publicationVenue") is not None else {}
        publication_type = publication_venue.get("type", "").lower() if publication_venue else ""
        venue = paper.get("venue", "")
        
        
        if publication_type == "workshop":
            publication_id = publication_venue.get("id", "")
            name = publication_venue.get("name", "")
            year = paper.get("year", "")
            issn = publication_venue.get("issn", "") if "issn" in publication_venue else ""
            url = publication_venue.get("url", "") if "url" in publication_venue else ""
            edition = random.randint(1, 20)  # Randomly assign an edition number

            conferences.append({
                "publicationId": publication_id,
                "publicationType": publication_type,
                "name": name,
                "year": year,
                "venue": venue,
                "issn": issn,
                "url": url,
                "edition": edition
            })

            paper_presented_in_conference.append({
                "START_ID": paper_id,
                "END_ID": publication_id
            })

    # Convert to DataFrame and save to CSV
    df_conferences = pd.DataFrame(conferences)
    df_conferences.to_csv(os.path.join(csv_folder_path, "workshop.csv"), index=False)

    df_paper_presented_in_conference = pd.DataFrame(paper_presented_in_conference)
    df_paper_presented_in_conference.to_csv(os.path.join(csv_folder_path, "paper_presented_in_workshop.csv"), index=False)

    print("Workshop and paper_presented_in_workshop data saved.")

   
def generate_conferences_proceedings_and_mapping(json_data, csv_folder_path):
    proceedings = {"ID": [], "name": [], 'city': []}
    conference_part_of_proceedings = {"START_ID" : [], "END_ID": []}
    proceedings_dict = {}

    for paper in json_data:
        # Ensure paper and publicationVenue exist and are not None
        if paper and paper.get("publicationVenue") and paper["publicationVenue"].get("type") == "conference":
            conference_id = paper["publicationVenue"].get("id", str(uuid.uuid4()))
            conference_name = paper["publicationVenue"].get("name", "Unknown Conference")
            city = fake.city()  # Generate a random city name for the proceeding

            # Check if we already processed this conference to avoid duplicate proceedings
            if conference_id not in proceedings_dict:
                # Proceeding data
                proc_id = str(uuid.uuid4())  # Unique ID for each proceeding
                proceedings_dict[conference_id] = proc_id
                
                proceedings["ID"].append(proc_id)
                proceedings["name"].append(conference_name)
                proceedings['city'].append(city)
                
                
                # Mapping between conference and its proceeding
                conference_part_of_proceedings["START_ID"].append(conference_id)
                conference_part_of_proceedings["END_ID"].append(proc_id)

    # Convert dictionaries to pandas DataFrames
    df_proceedings = pd.DataFrame(proceedings)
    df_conference_part_of_proceedings = pd.DataFrame(conference_part_of_proceedings)

    # Save to CSV
    proceedings_csv_path = os.path.join(csv_folder_path, "proceedings.csv")
    conference_part_of_proceedings_csv_path = os.path.join(csv_folder_path, "conference_part_of_proceedings.csv")

    df_proceedings.to_csv(proceedings_csv_path, index=False)
    df_conference_part_of_proceedings.to_csv(conference_part_of_proceedings_csv_path, index=False)

    print(f"Proceedings data saved to {proceedings_csv_path}")
    print(f"Conference-part-of-proceedings data saved to {conference_part_of_proceedings_csv_path}")


def process_data(json_data, csv_folder_path):
    # Extract and save authors to a separate CSV
    extract_and_save_authors(json_data, csv_folder_path)
    
    # Convert the main data to a DataFrame
    df = pd.DataFrame(json_data)

    # Load the authors DataFrame for reviewer assignment
    authors_df = pd.read_csv(os.path.join(csv_folder_path, "authors.csv"))
    
    # Add reviewers, keywords, and publication type
    df = add_reviewers(df, authors_df)
    df = add_keywords(df)
    df = add_publication_type(df)
    df = remove_duplicate_papers(df)

    # Save the processed data
    processed_csv_filepath = os.path.join(csv_folder_path, "processed_data.csv")
    df.to_csv(processed_csv_filepath, index=False)
    print(f"Processed data saved to {processed_csv_filepath}")


if __name__ == "__main__":
    # Hardcoded paths for demonstration purposes
    root_path = "/home/pce/Pictures/data/"
    json_path = "/home/pce/Pictures/data/JSON_files/detailed_paper_info.json"
    papers_csv_path = "/home/pce/Pictures/data/papers.csv"  # Define where to save the papers CSV
    keywords_csv_path = "/home/pce/Pictures/data/keywords.csv"  # Define where to save the keywords CSV
    paper_keyword_csv_path = "/home/pce/Pictures/data/paper_keyword.csv"
    citations_csv_path = "/home/pce/Pictures/data/paper_cite_paper.csv"
    csv_folder_path = "/home/pce/Pictures/data"


    json_data = load_json(json_path)
    flattened_data = flatten_data(json_data)
    extract_and_save_authors(json_data, root_path)
    extract_and_process_paper_keyword_data(json_data, papers_csv_path, keywords_csv_path, paper_keyword_csv_path)
    extract_citations_and_save(json_data, papers_csv_path, citations_csv_path)
    process_journal_data(json_data, csv_folder_path)
    extract_and_save_conferences(json_data, root_path)
    extract_and_save_workshop(json_data, csv_folder_path)
    generate_conferences_proceedings_and_mapping(json_data, csv_folder_path)

    process_data(json_data, root_path)
    


  


