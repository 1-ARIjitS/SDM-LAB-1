from neo4j import GraphDatabase

def execute_load_queries(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        load_queries = [
            # Load Authors
            """LOAD CSV WITH HEADERS FROM 'file:///authors.csv' AS line
            MATCH (author:Author {ID: line.authorId })
            SET author.department = line.department
            """,
            
            # Load Conferences
             """LOAD CSV WITH HEADERS FROM 'file:///conferences.csv' AS line
            MATCH (conf:Conference {ID: line.publicationId})
            SET conf.conferenceChair = line.conferenceChair
            """,
            
              # Load Workshop
             """LOAD CSV WITH HEADERS FROM 'file:///workshops.csv' AS line
            MATCH (work:Workshop {ID: line.publicationId})
            SET work.workshopChair = line.workshopChair
            """,
            
            # Load Journals
            """LOAD CSV WITH HEADERS FROM 'file:///journal.csv' AS line
            CREATE (jour:Journal {ID: line.publicationId})
            SET jour.JournalEditor = line.JournalEditor
            """,
        
        #Load Organisation
        """LOAD CSV WITH HEADERS FROM 'file:///organizations.csv' AS line
                CREATE(:Organisation {
                    ID: line.OrganizationID,
                    affiliation_name: line.affiliation_name,
                    affiliationType: line.affiliationType
                })""",
                
        #Load Author Affliated With Organisation
          """LOAD CSV WITH HEADERS FROM 'file:///organization_affiliated_with_author.csv' AS line
            MATCH (author:Author {ID: line.start_id})
            WITH author, line
            MATCH (organisation:Organisation {ID: line.end_id})
            CREATE (author)-[:is_affiliated]->(organisation)""",
            
        #Author Review Paper
        """LOAD CSV WITH HEADERS FROM 'file:///reviews_with_decisions.csv' AS line
        MATCH (author:Author {ID: line.reviewerId}) - [re:reviews] -> (paper:Paper {ID: line.paperId})
        SET re.reviewContent = line.reviewContent, re.majorityDecision = line.majorityDecision""",
        
        # Conference Chair assign reviewer
        """ LOAD CSV WITH HEADERS FROM 'file:///chair_assign_reviewer.csv' AS line
            MATCH (conference:Conference {ID: line.START_ID})-[j:chair_assigned_reviewer]->(author:Author {ID: line.END_ID})
            SET j.reviewPolicy= toInteger(line.reviewPolicy)""",
            
            
        # Journal Editor assign Reviewer
        """
        LOAD CSV WITH HEADERS FROM 'file:///editor_assign_reviewer.csv' AS line
            MATCH (journal:Journal {ID: line.START_ID})-[r:editor_assigned_reviewer]->(author:Author {ID: line.END_ID})
        SET r.reviewPolicy= toInteger(line.reviewPolicy)
        """
        ]

        for query in load_queries:
            session.run(query)

        print("AFTER EVOLUTION- All CSV files have been loaded into Neo4j.")

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "1*@#Saymyname"  
    execute_load_queries(uri, user, password)