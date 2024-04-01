import pandas as pd
from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
user = "neo4j"
password = "xxxxx"
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

def run_query_and_export_to_csv(query, csv_file_path, query_name, print_result=True):
    print(f"Executing query: {query_name}")
    results = []
    with driver.session() as session:
        for record in session.run(query):
            results.append(record.data())
            if print_result:
                print(record.data())
    
    df = pd.DataFrame(results)
    df.to_csv(csv_file_path, index=False)
    print(f"Query '{query_name}' completed and saved to '{csv_file_path}'")
    

if __name__ == "__main__":
    create_community_and_keywords()

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
    run_query_and_export_to_csv(tag_database_specific_publications_query, "/home/pce/Pictures/data/recommend/database_specific_publications.csv", "Tagging Database-Specific Publications")

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
    run_query_and_export_to_csv(identify_top100_database_papers_query, "/home/pce/Pictures/data/recommend/top_100_database_papers.csv","Top 100 Database Paper")
    
    potential_reviewers_query = """
            MATCH (p:Top100DatabasePaper)<-[:writes]-(author:Author)
            SET author:PotentialReviewer
            MERGE (author)-[:pontential_reviewer_for]->(community)
            WITH author, COLLECT(p.title) AS paperTitles
            RETURN author.name AS AuthorName, paperTitles, SIZE(paperTitles) AS TopPapersCount
            """
    run_query_and_export_to_csv(potential_reviewers_query, "/home/pce/Pictures/data/recommend/potential_reviewers.csv", "Identifing Potential Reviewers")


    gurus_query = """
        MATCH (author:Author)-[:writes]->(paper:Top100DatabasePaper)
        WITH author, COLLECT(DISTINCT paper.title) AS paperTitles, COUNT(DISTINCT paper) AS topPapers
        WHERE topPapers >= 2
        SET author:Guru
        RETURN distinct author.name AS GuruName, paperTitles, topPapers
        ORDER BY topPapers DESC, GuruName;
    """
    run_query_and_export_to_csv(gurus_query, "/home/pce/Pictures/data/recommend/gurus.csv","Guru in the Database Communities")

    driver.close()
