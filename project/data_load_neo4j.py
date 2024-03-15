from neo4j import GraphDatabase

def execute_load_queries(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        load_queries = [
            # Load Authors
            """LOAD CSV WITH HEADERS FROM 'file:///authors.csv' AS line
            CREATE (:Author {
                ID: line.authorId,
                name: line.name,
                email: line.email
        })""",
            
            # Load Papers
              """
        LOAD CSV WITH HEADERS FROM 'file:///papers.csv' AS line
        CREATE (:Paper {
            ID: line.paperId,
            title: line.title,
            abstract: line.abstract,
            pages: line.pages,
            doi: line.doi,
            link: line.link,
            citation_count: toInteger(line.citation_count),
            reference_count: toInteger(line.reference_count),
            date: line.date
        })
        """,
            
            # Load Keywords
             """LOAD CSV WITH HEADERS FROM 'file:///keywords.csv' AS line
            CREATE (:Keyword {
                ID: line.ID,
                name: line.name,
                domain: line.domain,
                keyword_abstract:line.keyword_abstract
        })""",
            
            # Load Conferences
             """LOAD CSV WITH HEADERS FROM 'file:///conferences.csv' AS line
            CREATE (:Conference {
                ID: line.publicationId,
                name: line.name,
                venue: line.venue,
                publication_type:line.publicationType,
                year: toInteger(line.year),
                edition: toInteger(line.edition),
                issn:toInteger(line.issn),
                url:line.url
                
        })""",
            
            # Load Journals
            """LOAD CSV WITH HEADERS FROM 'file:///journal.csv' AS line
            CREATE (:Journal {
               ID: line.publicationId,                
                name: line.name,
                venue: line.venue,
                publication_type:line.publicationType,
                year: toInteger(line.year),
                volume: toInteger(line.volume),
                issn:toInteger(line.issn),
                url:line.url
        })""",
            
            # Load Proceedings
        """LOAD CSV WITH HEADERS FROM 'file:///proceedings.csv' AS line
                CREATE (:Proceeding {
                ID: line.ID,
                name: line.name,
                city: line.city
        })""",
            
            # Author Writes Paper
            """LOAD CSV WITH HEADERS FROM 'file:///author_writes.csv' AS line
            MATCH (author:Author {ID: line.start_id})
            WITH author, line
            MATCH (paper:Paper {ID: line.end_id})
            CREATE (author)-[w:writes]->(paper)
            SET w.corresponding_author = toBoolean(line.corresponding_author)""",
            
            # Author Reviews Paper
            """LOAD CSV WITH HEADERS FROM 'file:///author_review_papers.csv' AS line
            MATCH (author:Author {ID: line.paperId})
            WITH author, line
            MATCH (paper:Paper {ID: line.reviewerId})
            CREATE (author) - [:reviews] -> (paper)""",
            
            # Paper Cites Paper
            """LOAD CSV WITH HEADERS FROM 'file:///paper_cite_paper.csv' AS line
            MATCH (paper:Paper {ID: line.paper_id})
            WITH paper, line
            MATCH (citedPaper:Paper {ID: line.cited_paper_id})
            CREATE (paper) - [:cites] -> (citedPaper)""",
            
            # Paper Has Keyword
            """LOAD CSV WITH HEADERS FROM 'file:///paper_keyword.csv' AS line
            MATCH (paper:Paper {ID: line.START_ID})
            WITH paper, line
            MATCH (keyword:Keyword {ID: line.END_ID})
            CREATE (paper) - [:has] -> (keyword)""",
            
            # Paper Published In Journal
            """LOAD CSV WITH HEADERS FROM 'file:///paper_published_in_journal.csv' AS line
            MATCH (paper:Paper {ID: line.START_ID})
            WITH paper, line
            MATCH (jour:Journal {ID: line.END_ID})
            CREATE (paper) - [r:published_in] -> (jour)""",
            
            # Paper Presented In Conference
            """LOAD CSV WITH HEADERS FROM 'file:///paper_presented_in_conference.csv' AS line
            MATCH (paper:Paper {ID: line.START_ID})
            WITH paper, line
            MATCH (conf:Conference {ID: line.END_ID})
            CREATE (paper) - [:presented_in] -> (conf)""",
            
            
            # Conference Part Of Proceeding
            """LOAD CSV WITH HEADERS FROM 'file:///conference_part_of_proceedings.csv' AS line
            MATCH (conf:Conference {ID: line.START_ID})
            WITH conf, line
            MATCH (proc:Proceeding {ID: line.END_ID})
            CREATE (conf)-[:is_part]->(proc)"""
        ]

        for query in load_queries:
            session.run(query)

        print("All CSV files have been loaded into Neo4j.")

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "XXXXX"  
    execute_load_queries(uri, user, password)








