import pandas as pd
from neo4j import GraphDatabase

def execute_queries(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
      
    with driver.session() as session:
        def run_query_and_export_to_csv(query, csv_file_name, query_description):
            print(f"\nExecuting query: {query_description}")
            results = []
            with driver.session() as session:
                for record in session.run(query):
                    results.append(record.data())
                    # Convert the results to a DataFrame
            df = pd.DataFrame(results)
            csv_file_path = f"/home/pce/Pictures/data/query/{csv_file_name}.csv"
                    # Print the DataFrame to console
            print(f"Results for '{query_description}':")
            print(df)
                    # Save the DataFrame to a CSV file
            df.to_csv(csv_file_path, index=False)
            print(f"Query '{query_description}' completed and saved to '{csv_file_path}'")

        
        # QUERY 1
        query_1_description = "Top 3 Most Cited Papers of Each Conference"
        query_1 = """MATCH (p:Paper)-[:cites]->(citedPaper:Paper)-[:presented_in]->(c:Conference)
                     WITH c, citedPaper, count(*) AS numberOfCitations
                     ORDER BY c, numberOfCitations DESC
                     WITH c, COLLECT(citedPaper)[0..3] AS top3Papers
                     WHERE top3Papers[1].title <> 'None' AND top3Papers[2].title <> 'None'
                     RETURN distinct c.name AS conference, 
                     [paper IN top3Papers | paper.title] AS top3CitedPapers;"""
        run_query_and_export_to_csv(query_1, "query_1_top_3_cited_papers", query_1_description)
        
        # QUERY 2
        query_2_description = "Authors Published in At Least 4 Different Editions"
        query_2 = """MATCH (a:Author) - [:writes] -> (p:Paper) - [:presented_in] -> (c:Conference)
                     WITH a, c.name AS conferenceName, COUNT(DISTINCT c.edition) AS distinctEditions
                     WHERE distinctEditions >= 4
                     RETURN conferenceName, collect(a.name) AS CommunityMember, distinctEditions AS numOfEditionsPresented
                     ORDER BY numOfEditionsPresented DESC;"""
        run_query_and_export_to_csv(query_2, "query_2_authors_4_editions", query_2_description)
        
        # QUERY 3
        query_3_description = "Impact Factor Calculation"
        query_3 = """MATCH (p:Paper)-[:cites]->(citedP:Paper)-[:published_in]->(j:Journal)
                     WITH j, date(citedP.date).year AS yearPublished, COUNT(p) AS totalCitations
                     WHERE yearPublished >= date().year - 2 AND yearPublished <= date().year - 1
                     WITH j, yearPublished, totalCitations
                     MATCH (p2:Paper)-[:published_in]->(j2:Journal)
                     WHERE date(p2.date).year = yearPublished AND j2 = j
                     WITH j.name AS journalName, yearPublished + 1 AS yearOfCitation, SUM(totalCitations) AS citations, COUNT(p2) AS totalPublications
                     WHERE totalPublications > 0
                     RETURN journalName, yearOfCitation, toFloat(citations) / totalPublications AS impactFactor
                     ORDER BY impactFactor DESC;"""
        run_query_and_export_to_csv(query_3, "query_3_impact_factor", query_3_description)
        
        # QUERY 4
        query_4_description = "H-Index of Authors"
        query_4 = """MATCH (a:Author)-[:writes]->(p:Paper)
                     OPTIONAL MATCH (p)<-[:cites]-(citingPaper:Paper)
                     WITH a, p, COUNT(citingPaper) AS citations
                     ORDER BY citations DESC
                     WITH a, COLLECT(citations) AS citationCounts
                     UNWIND RANGE(1, SIZE(citationCounts)) AS idx
                     WITH a, idx AS potentialHIndex, citationCounts
                     WHERE citationCounts[idx-1] >= potentialHIndex
                     RETURN a.name AS authorName, MAX(potentialHIndex) AS hIndex
                     ORDER BY hIndex DESC;"""
        run_query_and_export_to_csv(query_4, "query_4_h_index", query_4_description)

    driver.close()

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "xxxx"  
    execute_queries(uri, user, password)
