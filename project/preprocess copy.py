
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

    

# Load the authors data from CSV
authors_df = pd.read_csv("/home/pce/Pictures/data/authors.csv")
authors_df = authors_df.dropna(subset=['authorId'])

# Assuming we have a DataFrame papers_df for papers from your JSON data
# For demonstration, let's create a mock papers_df
papers_df = pd.DataFrame({
    "paperId": authors_df["paperId"].unique()  # Extract unique paper IDs from authors data
})

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



editor_csv = '/home/pce/Pictures/data/editor_assign_reviewer.csv'
chair_csv = '/home/pce/Pictures/data/chair_assign_reviewer.csv'

papers_with_policies_df = load_review_policies(editor_csv, chair_csv, papers_df)
reviews_df = assign_reviews_with_decisions(authors_df, papers_with_policies_df)
reviews_df.dropna()
reviews_df.to_csv('/home/pce/Pictures/data/reviews_with_decisions.csv', index=False)
print("Review data with decisions and majority acceptance saved.")



def extract_keywords(abstract):
    if not abstract:
        return []
    doc = nlp(abstract)
    return [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]


def add_keywords(df):
    df['keywords'] = df['abstract'].apply(extract_keywords)
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
        # reference_count = paper.get("referenceCount", 0)
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
            # "referenceCount": reference_count,
            "date": date,
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


    # pd.DataFrame(papers).to_csv(papers_csv_path, index=False)
    
    paper_df_1 = pd.DataFrame(papers)
    paper_df_1['citationCount'] = paper_df_1['citationCount'].fillna(0)
    paper_df_1['citationCount'] = paper_df_1['citationCount'].astype(int)

    # Save the cleaned DataFrame to CSV
    paper_df_1.to_csv(papers_csv_path, index=False)
    
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
            review_policy = random.randint(3, 5)  # Randomly assign review policy between 2 and 4

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
            review_policy = random.randint(3, 5)  # Randomly assign review policy between 2 and 4

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
    root_path = "/home/pce/Pictures/data/"
    json_path = "/home/pce/Pictures/data/JSON_files/detailed_paper_info.json"
    papers_csv_path = "/home/pce/Pictures/data/papers.csv"  # Define where to save the papers CSV
    keywords_csv_path = "/home/pce/Pictures/data/keywords.csv"  # Define where to save the keywords CSV
    paper_keyword_csv_path = "/home/pce/Pictures/data/paper_keyword.csv"
    citations_csv_path = "/home/pce/Pictures/data/paper_cite_paper.csv"
    csv_folder_path = "/home/pce/Pictures/data"
    
    papers_df = pd.read_csv("/home/pce/Pictures/data/papers.csv")  # Make sure this has 'publicationId'
    authors_df = pd.read_csv('/home/pce/Pictures/data/authors.csv')

    json_data = load_json(json_path)
    flattened_data = flatten_data(json_data)
    extract_and_save_authors(json_data, root_path)
    extract_and_process_paper_keyword_data(json_data, papers_csv_path, keywords_csv_path, paper_keyword_csv_path)
    extract_citations_and_save(json_data, papers_csv_path, citations_csv_path)
    process_journal_data(json_data, csv_folder_path)
    extract_and_save_conferences(json_data, root_path)
    extract_and_save_workshop(json_data, csv_folder_path)
    generate_conferences_proceedings_and_mapping(json_data, csv_folder_path)
    link_workshops_to_proceedings(csv_folder_path)




  

