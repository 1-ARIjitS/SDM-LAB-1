from neo4j import GraphDatabase
import pandas as pd
import os

# Define Neo4j connection parameters
uri = "bolt://localhost:7687"  # default bolt port
username = "neo4j"
password = "1*@#xxxx"  # default password is "neo4j"

# Function to create authors
def create_authors(tx, authors):
    query = """
    UNWIND $authors AS author
    MERGE (a:Author {id: author.author_id, name: author.author_name})
    """
    tx.run(query, authors=authors)

# Function to create papers
def create_papers(tx, papers):
    query = """
    UNWIND $papers AS paper
    MERGE (p:Paper {id: paper.paperId, title: paper.title})
    """
    tx.run(query, papers=papers)

# Function to create relationships between authors and papers
def create_relationships(tx, relationships):
    query = """
    UNWIND $relationships AS rel
    MATCH (a:Author {id: rel.author_id}), (p:Paper {id: rel.paper_id})
    MERGE (a)-[:WROTE]->(p)
    """
    tx.run(query, relationships=relationships)

def delete_node(tx):
    query = f"""
    MATCH (n:{'Paper'})
    DELETE n
    """
    tx.run(query)

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

# file paths
root_path= "D:/BDMA/UPC/SDM/LAB/LAB1"
csv_folder_path= os.path.join(root_path,"CSV_files")
csv_file_path= os.path.join(root_path, "updated_data.csv")
df= pd.read_csv(csv_file_path)

# Create authors, papers, and relationships
with driver.session() as session:
    session.write_transaction(create_authors, df[['author_id', 'author_name']])
    session.write_transaction(create_papers, df[['paperId', 'title']])
    # session.write_transaction(delete_node)
    # session.write_transaction(create_relationships, df[['author_id', 'paper_id']])

# Close Neo4j driver
driver.close()