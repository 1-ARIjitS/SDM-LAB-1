from neo4j import GraphDatabase

def execute_queries(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
      
    with driver.session() as session:

      # QUERY 1- Find the top 3 most cited papers of each conference
      print("-------------------")
      print("QUERY 1 RESULTS")
      print("-------------------")
      query_1= """MATCH (p:Paper)-[:cites]->(citedPaper:Paper)-[:presented_in]->(c:Conference)
                  WITH c, citedPaper, count(*) AS numberOfCitations
                  ORDER BY c, numberOfCitations DESC
                  WITH c, COLLECT(citedPaper)[0..3] AS top3Papers
                  WHERE top3Papers[1].title <> 'None' AND top3Papers[2].title <> 'None'
                  RETURN distinct c.name AS conference, 
                  [paper IN top3Papers | paper.title] AS top3CitedPapers;"""
      result= session.run(query_1)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)
      
      # QUERY 2- Authors that have published papers on that conference in, at least, 4 different editions
      print("-------------------")
      print("QUERY 2 RESULTS")
      print("-------------------")
      query_2= """MATCH (a:Author) - [:writes] -> (p:Paper) - [:presented_in] -> (c:Conference)
                  WITH c.name as conferenceName, a, COUNT(DISTINCT c.edition) AS distinctEditions
                  WHERE distinctEditions >= 4
                  RETURN distinct a.name as authorName, conferenceName,
                  distinctEditions as numOfEditionsPresented;"""
      result= session.run(query_2)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)
      
      # QUERY 3- Impact factor
      # Impact factor = Citations(year1) / Publications(year1-1) + Publications(year1-2)
      print("-------------------")
      print("QUERY 3 RESULTS")
      print("-------------------")
      query_2= """MATCH(p:Paper) - [r1:cites] -> (citedP:Paper) - [r2:published_in] -> (j:Journal) 
                  WITH j, r2.year as currYear, COUNT(r1) AS totalCitations
                  MATCH (p2:Paper) - [r3:published_in] -> (j)
                  WHERE r3.year = currYear - 1 OR r3.year = currYear - 2
                  WITH j, currYear, totalCitations, COUNT(r3) AS totalPublications
                  WHERE totalPublications > 0
                  RETURN j.name AS journalName,
                  currYear AS yearOfPublication,
                  toFloat(totalCitations)/totalPublications AS impactFactor
                  ORDER BY impactFactor DESC;"""
      result= session.run(query_2)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

      # QUERY 3- H-Index
      # H-Index = at least h publications have h citations
      print("-------------------")
      print("QUERY 4 RESULTS")
      print("-------------------")
      query_2= """MATCH(a:Author) - [r1:writes] -> (p1:Paper) - [r2:cites] -> (p2:Paper)
                  WITH a, p2, COLLECT(p1) as papers
                  WITH a, p2, RANGE(1, SIZE(papers)) AS listOfPapers
                  UNWIND listOfPapers AS lp
                  WITH a, lp AS currHIndex, count(p2) AS citedPapers
                  WHERE currHIndex <= citedPapers
                  RETURN distinct a.name AS authorName,
                  currHIndex as hIndex
                  ORDER BY currHIndex DESC;"""
      result= session.run(query_2)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "xxxxxxxxx"  
    execute_queries(uri, user, password)