
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
    organizations = []  # To store organization data including type
    organization_affiliations = []  # To store relationships between authors and organizations

    for paper in json_data:
        paper_id = paper.get("paperId", "")
        is_corresponding = True  # Assuming the first author is the corresponding author

        for author in paper.get("authors", []):
            author_id = author.get("authorId", "")
            name = author.get("name", "")
            department = random.choice(departments) 

            # Randomly decide between a university and a company, and create the organization accordingly
            if random.choice([True, False]):
                affiliation_name = random.choice(universities)
                affiliation_type = "university"
            else:
                affiliation_name = fake.company()
                affiliation_type = "company"

            # Generate email based on affiliation type and name
            email_username = name.lower().replace(' ', '.')
            if affiliation_type == "university":
                email_domain = "@" + affiliation_name.replace(' ', '').lower() + ".edu"
            else:  # affiliation_type == "company"
                email_domain = "@" + affiliation_name.replace(' ', '').lower() + ".com"
            email = email_username + email_domain
                
            # Create organization entry
            organization_id = str(uuid.uuid4())
            organizations.append({
                "OrganizationID": organization_id,
                "affiliation_name": affiliation_name,
                "affiliationType": affiliation_type
            })

            authors.append({
                "authorId": author_id,
                "name": name,
                "email": email,
                "department": department,
                 "paperId": paper_id 
            })

            author_writes.append({
                "start_id": author_id,
                "end_id": paper_id,
                "corresponding_author": is_corresponding
            })

            organization_affiliations.append({
                "start_id": author_id,
                "end_id": organization_id  
            })

            is_corresponding = False 

    # Convert lists to DataFrames
    authors_df = pd.DataFrame(authors)
    author_writes_df = pd.DataFrame(author_writes)
    organizations_df = pd.DataFrame(organizations)
    organization_affiliations_df = pd.DataFrame(organization_affiliations)

    # Save to CSV
    authors_df.to_csv(os.path.join(csv_folder_path, "authors.csv"), index=False)
    author_writes_df.to_csv(os.path.join(csv_folder_path, "author_writes.csv"), index=False)
    organizations_df.to_csv(os.path.join(csv_folder_path, "organizations.csv"), index=False)
    organization_affiliations_df.to_csv(os.path.join(csv_folder_path, "organization_affiliated_with_author.csv"), index=False)

    print("Data saved: Authors, Author Writes, Organizations, and Organization Affiliations.")

# Assign Reviewers
def load_review_policies(editor_csv, chair_csv, papers_df):
    editor_df = pd.read_csv(editor_csv)
    chair_df = pd.read_csv(chair_csv)
    
    # Combine the editor and chair data
    review_policy_df = pd.concat([editor_df, chair_df])
    
    # Merge review policies with papers
    papers_with_policies = papers_df.merge(review_policy_df, left_on='paperId', right_on='START_ID', how='left')
    
    return papers_with_policies

def assign_reviews_with_decisions(authors_df, papers_with_policies_df):
    review_data = []
    
    for _, paper_row in papers_with_policies_df.iterrows():
        paper_id = paper_row['paperId']
        review_policy = paper_row['reviewPolicy'] if not pd.isnull(paper_row['reviewPolicy']) else 3
        
        # Exclude authors of the paper from potential reviewers
        potential_reviewers = authors_df[~authors_df['authorId'].isin(authors_df[authors_df['paperId'] == paper_id]['authorId'])]
        
        if len(potential_reviewers) >= review_policy:
            selected_reviewers = potential_reviewers.sample(n=review_policy)
            
            decisions = []
            for _, reviewer_row in selected_reviewers.iterrows():
                review_content = fake.paragraph()
                decision = random.choice(['accept', 'reject'])
                decisions.append(decision)
                
                review_data.append({
                    'paperId': paper_id,
                    'reviewerId': int(reviewer_row['authorId']),
                    'reviewContent': review_content,
                    'decision': decision
                })
            
            majority_decision = 'Accepted' if decisions.count('accept') > len(decisions) / 2 else 'Rejected'
            for review in review_data:
                if review['paperId'] == paper_id:
                    review['majorityDecision'] = majority_decision
        else:
            print(f"Not enough unique reviewers for paper {paper_id}")
    
    return pd.DataFrame(review_data)



# editor_csv = 'D:/BDMA/UPC/SDM/LAB/LAB1/project/editor_assign_reviewer.csv'
# chair_csv = 'D:/BDMA/UPC/SDM/LAB/LAB1/project/chair_assign_reviewer.csv'

# papers_with_policies_df = load_review_policies(editor_csv, chair_csv, papers_df)
# reviews_df = assign_reviews_with_decisions(authors_df, papers_with_policies_df)
# reviews_df.dropna()
# reviews_df.to_csv('D:/BDMA/UPC/SDM/LAB/LAB1/project/reviews_with_decisions.csv', index=False)
# print("Review data with decisions and majority acceptance saved.")

database_keywords_set = set(['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying'])

def extract_keywords(abstract):
    if abstract is None:
        return []
    doc = nlp(abstract.lower())  
    return [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ'] and not token.is_stop]

def extract_and_process_paper_keyword_data(json_data, papers_csv_path, keywords_csv_path, paper_keyword_csv_path):
    papers = []
    keywords_data = {"ID": [], "name": [], "domain": []}
    paper_has_keywords = {"START_ID": [], "END_ID": []}
    keywords_dict = {}
    
    # Pre-populate keywords_dict with database keywords to ensure they're included
    for kw in database_keywords_set:
        kw_id = str(uuid.uuid4())  # Generate a unique ID for each keyword
        keywords_dict[kw] = kw_id
        keywords_data["ID"].append(kw_id)
        keywords_data["name"].append(kw)
        keywords_data["domain"].append("Database")  # Assign the "Database" domain
        
    for paper in json_data:     
    
        abstract = paper.get("abstract", "")
        extracted_keywords = extract_keywords(abstract)
        fields_of_study = paper.get("fieldsOfStudy", []) or []
        # default_domain = fields_of_study[0] if fields_of_study else "Unspecified"
        paper_id = paper.get("paperId")
        title = paper.get("title", "")
        doi = paper.get("externalIds", {}).get("DOI", "")
        link = paper.get("url", "")
        citation_count = paper.get("citationCount", 0)
        date = paper.get("publicationDate", "")

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
            "date": date,
                })

        all_keywords = set(fields_of_study + extracted_keywords)

        # Ensure database_keywords_set keywords are considered
        all_keywords.update(database_keywords_set)

        for keyword in all_keywords:
            if keyword not in keywords_dict:
                # For new keywords not in database_keywords_set
                keyword_id = str(uuid.uuid4())
                keywords_dict[keyword] = keyword_id
                domain = fields_of_study[0] if fields_of_study else "Unspecified"
                keywords_data["ID"].append(keyword_id)
                keywords_data["name"].append(keyword)
                keywords_data["domain"].append(domain if keyword not in database_keywords_set else "Database")

            paper_has_keywords["START_ID"].append(paper.get("paperId"))
            paper_has_keywords["END_ID"].append(keywords_dict[keyword])

        # Convert dictionaries to pandas DataFrames
    paper_df = pd.DataFrame(papers)
    paper_df['citationCount'] = paper_df['citationCount'].fillna(0).astype(int)

    keywords_df = pd.DataFrame.from_dict(keywords_data)
    paper_keyword_relationship_df = pd.DataFrame(paper_has_keywords)

    # Save DataFrames to CSV files
    paper_df.to_csv(papers_csv_path, index=False)
    keywords_df.to_csv(keywords_csv_path, index=False)
    paper_keyword_relationship_df.to_csv(paper_keyword_csv_path, index=False)

    print(f"Papers data saved to {papers_csv_path}")
    print(f"Keywords data saved to {keywords_csv_path}")
    print(f"Paper-Keyword relationships saved to {paper_keyword_csv_path}")


def extract_citations_and_save(json_data, citations_csv_path):
    
    papers_set = {paper["paperId"] for paper in json_data}

# Initialize a dictionary to hold paper citation relationships
    paper_cites_paper = {"paper_id": [], "cited_paper_id": []}

    # Generate citation relationships
    for cited_paper in papers_set:
        for _ in range(randint(0, 50)):
            # Choose a paper to cite the current cited_paper, ensuring it's not citing itself
            paper = choice(list(papers_set - {cited_paper}))

            # Append the relationship to the dictionary
            paper_cites_paper['paper_id'].append(paper)
            paper_cites_paper['cited_paper_id'].append(cited_paper)

    # Convert the dictionary to a DataFrame
    pcp_df = pd.DataFrame.from_dict(paper_cites_paper)
    pcp_df.to_csv(citations_csv_path, index=False)
    print(f"Citations data saved to {citations_csv_path}")



def process_journal_data(json_data, csv_folder_path):
    print("Creating journal and editor assignment data...")
    journals = []
    paper_published_in_journal = []
    editor_assign_reviewer = []

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
        name = journal_info.get("name", "") if journal_info else ""
        volume = journal_info.get("volume", "1") if journal_info else "1"
        issn = publication_venue.get("issn", "") if publication_venue else ""
        url = publication_venue.get("url", "") if publication_venue else ""
        journal_editor = fake.name()

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
                "JournalEditor": journal_editor
            })

            paper_published_in_journal.append({
                "START_ID": paper_id,
                "END_ID": publication_id
            })

            # Assigning an editor and review policy specifically for journal assignments
            editor_name = fake.name()  # Assign a random name as editor
            review_policy = random.randint(3, 5)  # Randomly assign review policy between 3 and 5

            # Selecting reviewer IDs from authors_df randomly based on the review policy
            selected_reviewers = authors_df.sample(n=review_policy)['authorId'].tolist()
            for reviewer_id in selected_reviewers:
                editor_assign_reviewer.append({
                    "START_ID": publication_id,
                    "END_ID": reviewer_id,
                    "editorName": editor_name,  
                    "reviewPolicy": review_policy  
                })

    # Convert to DataFrame and save to CSV
    pd.DataFrame(journals).to_csv(os.path.join(csv_folder_path, "journal.csv"), index=False)
    pd.DataFrame(paper_published_in_journal).to_csv(os.path.join(csv_folder_path, "paper_published_in_journal.csv"), index=False)
    # pd.DataFrame(editor_assign_reviewer).to_csv(os.path.join(csv_folder_path, "editor_assign_reviewer.csv"), index=False)
    # Create the DataFrame
    editor_assign_reviewer_df = pd.DataFrame(editor_assign_reviewer)
    # Drop rows with any NaN values
    editor_assign_reviewer_df_cleaned = editor_assign_reviewer_df.dropna()
    editor_assign_reviewer_df_cleaned['END_ID'] = editor_assign_reviewer_df_cleaned['END_ID'].astype(int)
    # Save the cleaned DataFrame to CSV
    editor_assign_reviewer_df_cleaned.to_csv(os.path.join(csv_folder_path, "editor_assign_reviewer.csv"), index=False)


    print("Journals, paper_published_in_journal, and editor_assign_reviewer data saved.")
  
def extract_and_save_conferences(json_data, csv_folder_path):
    print("Creating conference and chair assignment data...")
    conferences = []
    paper_presented_in_conference = []
    chair_assign_reviewer = []

    for paper in json_data:
        paper_id = paper.get("paperId", "")
        publication_venue = paper.get("publicationVenue", {}) if paper.get("publicationVenue") is not None else {}
        publication_type = publication_venue.get("type", "").lower() if publication_venue else ""
        venue = paper.get("venue", "")
        
        # Skip if the publication name is "workshop"
        if publication_type == "conference" and not "workshop" in publication_venue.get("name", "").lower():
            publication_id = publication_venue.get("id", "")
            name = publication_venue.get("name", "")
            year = paper.get("year", "")
            issn = publication_venue.get("issn", "") if "issn" in publication_venue else ""
            url = publication_venue.get("url", "") if "url" in publication_venue else ""
            edition = random.randint(1, 30)
            conference_chair = fake.name()

            conferences.append({
                "publicationId": publication_id,
                # "Conference/Workshop": publication_type,
                "name": name,
                "year": year,
                "venue": venue,
                "issn": issn,
                "url": url,
                "edition": edition,
                "conferenceChair": conference_chair
            })

            paper_presented_in_conference.append({
                "START_ID": paper_id,
                "END_ID": publication_id
            })

            review_policy = random.randint(3, 5)
            selected_reviewers = authors_df.sample(n=review_policy)['authorId'].tolist()
            for reviewer_id in selected_reviewers:
                chair_assign_reviewer.append({
                    "START_ID": publication_id,
                    "END_ID": reviewer_id,
                    "conferenceChair": conference_chair,
                    "reviewPolicy": review_policy
                })

    # Create and clean the DataFrame
    chair_assign_reviewer_df = pd.DataFrame(chair_assign_reviewer)
    chair_assign_reviewer_df.dropna(inplace=True)
    chair_assign_reviewer_df['END_ID'] = chair_assign_reviewer_df['END_ID'].astype(int)

    # Save to CSV
    pd.DataFrame(conferences).to_csv(os.path.join(csv_folder_path, "conferences.csv"), index=False)
    pd.DataFrame(paper_presented_in_conference).to_csv(os.path.join(csv_folder_path, "paper_presented_in_conference.csv"), index=False)
    chair_assign_reviewer_df.to_csv(os.path.join(csv_folder_path, "chair_assign_reviewer.csv"), index=False)

    print("Conferences, paper_presented_in_conference, and chair_assign_reviewer data saved.")


def extract_and_save_workshop(json_data, csv_folder_path):
    print("Creating workshop node...")
    workshops = []
    paper_presented_in_workshop = []
    workshop_chair_assign_reviewer = []

    for paper in json_data:
        paper_id = paper.get("paperId", "")
        publication_venue = paper.get("publicationVenue", {}) if paper.get("publicationVenue") is not None else {}
        venue = paper.get("venue", "")
        # publication_type = publication_venue.get("type", "").lower() if publication_venue else ""
        # Adjusted condition: Check if 'name' contains 'Workshop' irrespective of 'type'
        venue_name_contains_workshop = "workshop" in publication_venue.get("name", "").lower()
        
        if venue_name_contains_workshop:  # Changed condition to check name for 'Workshop'
            publication_id = publication_venue.get("id", "")
            name = publication_venue.get("name", "")
            year = paper.get("year", "")
            issn = publication_venue.get("issn", "") if "issn" in publication_venue else ""
            url = publication_venue.get("url", "") if "url" in publication_venue else ""
            edition = random.randint(1, 20)  # Randomly assign an edition number
            work_conference_chair = fake.name()
            
            workshops.append({
                "publicationId": publication_id,
                # "publicationType": publication_type,  # Still keep the original type for record
                "name": name,
                "year": year,
                "venue": venue,
                "issn": issn,
                "url": url,
                "edition": edition,
                 "workshopChair": work_conference_chair
            })

            paper_presented_in_workshop.append({
                "START_ID": paper_id,
                "END_ID": publication_id
            })
            
                # Assigning review policy specifically for chair assignments
            review_policy = random.randint(3, 5)  # Randomly assign review policy between 3 and 5

            # Selecting reviewer IDs from authors_df randomly based on the review policy
            selected_reviewers = authors_df.sample(n=review_policy)['authorId'].tolist()
            for reviewer_id in selected_reviewers:
                workshop_chair_assign_reviewer.append({
                    "START_ID": publication_id,
                    "END_ID": reviewer_id,
                    "conferenceChair": work_conference_chair,  # Optionally, keep track of the chair
                    "reviewPolicy": review_policy  # Assign review policy here
                })

    # Convert to DataFrame and save to CSV
    df_workshops = pd.DataFrame(workshops)
    df_workshops.to_csv(os.path.join(csv_folder_path, "workshops.csv"), index=False)

    df_paper_presented_in_workshop = pd.DataFrame(paper_presented_in_workshop)
    df_paper_presented_in_workshop.to_csv(os.path.join(csv_folder_path, "paper_presented_in_workshop.csv"), index=False)

    print("Workshop and paper_presented_in_workshop data saved.")

   
def generate_conferences_proceedings_and_mapping(json_data, csv_folder_path):
    print("Creating proceedings and mappings...")
    proceedings = []
    conference_part_of_proceedings = []
    workshop_part_of_proceedings = []

    # Assuming workshops have been extracted and saved previously
    workshops_df = pd.read_csv(os.path.join(csv_folder_path, "workshops.csv"))
    workshop_ids = workshops_df["publicationId"]

    for paper in json_data:
        if paper.get("publicationVenue"):
            publication_venue = paper["publicationVenue"]
            venue_id = publication_venue.get("id", "")
            venue_name = publication_venue.get("name", "Unknown Venue")
            venue_type = publication_venue.get("type", "").lower()
            city = fake.city()  # Generate a random city name for the proceeding

            # Check if venue_id corresponds to a workshop
            is_workshop = venue_id in workshop_ids

            # Proceeding data
            proc_id = str(uuid.uuid4())
            proceedings.append({
                "ID": proc_id,
                "name": venue_name,
                "city": city
            })

            # Mapping based on venue type or workshop check
            if venue_type == "conference" or is_workshop:
                mapping = {
                    "START_ID": venue_id,
                    "END_ID": proc_id
                }
                if venue_type == "conference":
                    conference_part_of_proceedings.append(mapping)
                # elif is_workshop:
                #     workshop_part_of_proceedings.append(mapping)

    # Convert lists to pandas DataFrames
    df_proceedings = pd.DataFrame(proceedings)
    df_conference_part_of_proceedings = pd.DataFrame(conference_part_of_proceedings)
    # df_workshop_part_of_proceedings = pd.DataFrame(workshop_part_of_proceedings)

    # Save to CSV
    proceedings_csv_path = os.path.join(csv_folder_path, "proceedings.csv")
    conference_part_of_proceedings_csv_path = os.path.join(csv_folder_path, "conference_part_of_proceedings.csv")
    workshop_part_of_proceedings_csv_path = os.path.join(csv_folder_path, "workshop_part_of_proceedings.csv")

    df_proceedings.to_csv(proceedings_csv_path, index=False)
    df_conference_part_of_proceedings.to_csv(conference_part_of_proceedings_csv_path, index=False)
    # df_workshop_part_of_proceedings.to_csv(workshop_part_of_proceedings_csv_path, index=False)

    print("Proceedings and mappings data saved.")


def link_workshops_to_proceedings(csv_folder_path):
    print("Linking workshops to proceedings...")

    # Load existing workshops
    workshops_df = pd.read_csv(os.path.join(csv_folder_path, "workshops.csv"))
    # Assuming each workshop corresponds to a unique proceeding, for simplicity
    proceedings_df = pd.read_csv(os.path.join(csv_folder_path, "proceedings.csv"))

    workshop_part_of_proceedings = []

    # Map each workshop to a proceeding based on some criteria
    for _, workshop in workshops_df.iterrows():
        # For this example, let's link workshops to proceedings based on a matching name or other criteria
        for _, proceeding in proceedings_df.iterrows():
            if workshop['name'] in proceeding['name']:  # This is a simplistic approach; adjust as needed
                workshop_part_of_proceedings.append({
                    "START_ID": workshop['publicationId'],  # Workshop ID
                    "END_ID": proceeding['ID']  # Proceeding ID
                })
                break  # Assuming one workshop links to one proceeding; remove if multiple links are possible

    # Convert to DataFrame and save to CSV
    workshop_part_of_proceedings_df = pd.DataFrame(workshop_part_of_proceedings)
    workshop_part_of_proceedings_csv_path = os.path.join(csv_folder_path, "workshop_part_of_proceedings.csv")
    workshop_part_of_proceedings_df.to_csv(workshop_part_of_proceedings_csv_path, index=False)

    print("Link data between workshops and proceedings saved.")

if __name__ == "__main__":
    # Hardcoded paths for demonstration purposes
    root_path = "D:/BDMA/UPC/SDM/LAB/LAB1/project/"
    json_path= os.path.join(root_path, "detailed_paper_info.json")
    papers_csv_path= os.path.join(root_path, "papers.csv")
    authors_csv_path= os.path.join(root_path, "authors.csv")
    keywords_csv_path= os.path.join(root_path, "keywords.csv")
    paper_keyword_csv_path= os.path.join(root_path, "paper_keyword.csv")
    citations_csv_path= os.path.join(root_path, "paper_cite_paper.csv")
    # csv_folder_path = "/home/pce/Pictures/data"
    
     # Make sure this has 'publicationId'
    

    json_data = load_json(json_path)
    flattened_data = flatten_data(json_data)

    extract_and_save_authors(json_data, root_path)
    authors_df = pd.read_csv(authors_csv_path)

    # Load the authors data from CSV
    authors_df = pd.read_csv("D:/BDMA/UPC/SDM/LAB/LAB1/project/authors.csv")
    authors_df = authors_df.dropna(subset=['authorId'])

    papers_df = pd.DataFrame({
        "paperId": authors_df["paperId"].unique()  # Extract unique paper IDs from authors data
    })

    extract_and_process_paper_keyword_data(json_data, papers_csv_path, keywords_csv_path, paper_keyword_csv_path)
    papers_df = pd.read_csv(papers_csv_path) 

    extract_citations_and_save(json_data, citations_csv_path)
    process_journal_data(json_data, root_path)
    extract_and_save_conferences(json_data, root_path)
    extract_and_save_workshop(json_data, root_path)
    generate_conferences_proceedings_and_mapping(json_data, root_path)
    link_workshops_to_proceedings(root_path)

    editor_csv = 'D:/BDMA/UPC/SDM/LAB/LAB1/project/editor_assign_reviewer.csv'
    chair_csv = 'D:/BDMA/UPC/SDM/LAB/LAB1/project/chair_assign_reviewer.csv'

    papers_with_policies_df = load_review_policies(editor_csv, chair_csv, papers_df)
    reviews_df = assign_reviews_with_decisions(authors_df, papers_with_policies_df)
    reviews_df.dropna()
    reviews_df.to_csv('D:/BDMA/UPC/SDM/LAB/LAB1/project/reviews_with_decisions.csv', index=False)
    print("Review data with decisions and majority acceptance saved.")