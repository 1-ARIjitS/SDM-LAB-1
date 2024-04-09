import pandas as pd
from neo4j import GraphDatabase
import os

uri = "neo4j://localhost:7687"
user = "neo4j"
password = "1*@#Saymyname"
driver = GraphDatabase.driver(uri, auth=(user, password))

def create_community_and_keywords():
    query = """
    CREATE (c:ResearchCommunity {name: 'Database'})
    WITH c
    UNWIND ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying'] AS keywordName
    MERGE (k:Keyword {name: keywordName})
    WITH k, c
    MERGE (k)-[:part_of]->(c);
    """
    with driver.session() as session:
        session.run(query)
    print("Research Community and keywords associated with it created.")

def run_query_and_export_to_csv(query, query_name, root_path, print_result=True):
    print(f"Executing query: {query_name}")
    results = []
    with driver.session() as session:
        for record in session.run(query):
            results.append(record.data())
            if print_result:
                print(record.data())
    
    recommender_res_folder_path= os.path.join(root_path, "RECOMMENDER_RESULTS")
    if not os.path.exists(recommender_res_folder_path):
                os.makedirs(recommender_res_folder_path)
    csv_file_path= os.path.join(recommender_res_folder_path,f"{query_name}.csv")
    df = pd.DataFrame(results)
    df.to_csv(csv_file_path, index=False)
    print(f"Query '{query_name}' completed and saved to '{csv_file_path}'")

def drop_and_create_index():
    with driver.session() as session:
        node_index_query_description = "Dropping node lookup indexes"
        node_index_query= """DROP INDEX node_lookup_index IF EXISTS;"""
        print(node_index_query_description)
        result= session.run(node_index_query)
        records = list(result)
        for record in records:
            print(record)

        rel_index_query_description = "Dropping realtion lookup indexes"
        rel_index_query= """DROP INDEX rel_lookup_index IF EXISTS;"""
        print(rel_index_query_description)
        result= session.run(rel_index_query)
        records = list(result)
        for record in records:
            print(record)

        node_index_query_description = "Creating node lookup indexes"
        node_index_query= """CREATE LOOKUP INDEX node_lookup_index IF NOT EXISTS FOR (n) ON EACH labels(n);"""
        print(node_index_query_description)
        result= session.run(node_index_query)
        records = list(result)
        for record in records:
            print(record)

        rel_index_query_description = "Creating realtion lookup indexes"
        rel_index_query= """CREATE LOOKUP INDEX rel_lookup_index IF NOT EXISTS FOR ()-[r]-() ON EACH type(r);"""
        print(rel_index_query_description)
        result= session.run(rel_index_query)
        records = list(result)
        for record in records:
            print(record)
    

if __name__ == "__main__":
    create_community_and_keywords()
    drop_and_create_index()
    root_path= "D:/BDMA/UPC/SDM/LAB/LAB1/project" 

    tag_database_specific_publications_query = """
        MATCH (k:Keyword)-[:part_of]->(:ResearchCommunity {name: 'Database'}),
        (k)<-[:has]-(p:Paper),
        (p)-[:published_in|presented_in]->(pub)
        WITH pub, COUNT(DISTINCT p) AS papersInCommunity, COLLECT(DISTINCT p) AS papers
        MATCH (pub)<-[:published_in|presented_in]-(allP:Paper)
        WITH pub, papersInCommunity, COUNT(DISTINCT allP) AS totalPapers, LABELS(pub) AS labels
        WHERE papersInCommunity / totalPapers >= 0.9
        SET pub:DatabaseSpecific
        RETURN distinct (pub.name) AS Publication, papersInCommunity, totalPapers,
        [label IN labels WHERE label IN ['Conference', 'Journal']] AS Type;
        """
    run_query_and_export_to_csv(tag_database_specific_publications_query, "Tagging Database-Specific Publications", root_path)

    identify_top100_database_papers_query = """
    
        MATCH (p1:Paper)-[:published_in|presented_in]->(:DatabaseSpecific),
        (p2:Paper)-[:cites]->(p1)
        WHERE EXISTS((p2)-[:published_in|presented_in]->(:DatabaseSpecific))
        WITH p1, COUNT(DISTINCT p2) AS citations
        ORDER BY citations DESC
        LIMIT 100
        SET p1:Top100DatabasePaper
        RETURN p1.title AS TopPapers, citations
        ORDER BY citations DESC;
        """
    run_query_and_export_to_csv(identify_top100_database_papers_query,"Top 100 Database Paper", root_path)
    
    potential_reviewers_query = """
            MATCH (p:Top100DatabasePaper)<-[:writes]-(author:Author)
            SET author:PotentialReviewer
            MERGE (author)-[:pontential_reviewer_for]->(community)
            WITH author, COLLECT(p.title) AS paperTitles
            RETURN author.name AS AuthorName, paperTitles, SIZE(paperTitles) AS TopPapersCount
            """
    run_query_and_export_to_csv(potential_reviewers_query, "Identifing Potential Reviewers", root_path)


    gurus_query = """
        MATCH (author:Author)-[:writes]->(paper:Top100DatabasePaper)
        WITH author, COLLECT(DISTINCT paper.title) AS paperTitles, COUNT(DISTINCT paper) AS topPapers
        WHERE topPapers >= 2
        SET author:Guru
        RETURN distinct author.name AS GuruName, paperTitles, topPapers
        ORDER BY topPapers DESC, GuruName;
    """
    run_query_and_export_to_csv(gurus_query, "Guru in the Database Communities", root_path)

    driver.close()