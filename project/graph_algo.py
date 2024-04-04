from neo4j import GraphDatabase

def execute_queries(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
      
    with driver.session() as session:

      # ALGORITHM 1- using the node similarity algorithm to find papers that have the similar keywords
      print("--------------------------------------")
      print("ALGORITHM 1- Node Similarity RESULTS")
      print("--------------------------------------")
      print("creating projection of the graph for querying...")
      proj_query1="""CALL gds.graph.project(
                  'proj_paper_keyword', 
                  ['Paper','Keyword'],
                  {has:{}}
                  );
                """
      result= session.run(proj_query1)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)
      print("Running the graph algorithm on the projected graph...")
      algo_query1= """CALL gds.nodeSimilarity.stream('proj_paper_keyword', { topK: 1 })
                  YIELD node1, node2, similarity
                  WHERE similarity>0.5 and similarity<1.0
                  RETURN gds.util.asNode(node1).title AS paper1, gds.util.asNode(node2).title AS paper2, similarity
                  ORDER BY similarity DESC;
                """
      result= session.run(algo_query1)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

      # ALGORITHM 2- using Page rank algorithm to find the papers with most citations
      print("--------------------------------")
      print("ALGORITHM 2- Page Rank RESULTS")
      print("--------------------------------")
      print("creating projection of the graph for querying...")
      proj_query2="""CALL gds.graph.project(
                      'proj_paper_cite',
                      'Paper',
                      'cites',
                      {}
                    )
                  """
      result= session.run(proj_query2)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)
      print("Running the graph algorithm on the projected graph...")
      algo_query2= """CALL gds.pageRank.stream('proj_paper_cite')
                      YIELD nodeId, score
                        WHERE score > 0.0
                      RETURN gds.util.asNode(nodeId).title AS paper_title, score
                      ORDER BY score DESC
                   """
      result= session.run(algo_query2)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

     # ALGORITHM 3- algorithm for betweenness score it finds the node that controls the flow. i.e. here it is the node that is being cited by a lot of papers and cites a lot of paper itself and functions as a bridge between 2 papers. It also means that the nodes with high betweenness scores are mostly found as an intermediate paper in the shortest path from one paper to another.
      print("----------------------------------")
      print("ALGORITHM 3- betweenness RESULTS")
      print("----------------------------------") 
      print("Running the graph algorithm on the projected graph...")
      algo_query3= """CALL gds.betweenness.stream('proj_paper_cite')
                      YIELD nodeId, score
                      WHERE score > 0.0
                      RETURN gds.util.asNode(nodeId).title AS paper_title, score AS betweenness_score
                      ORDER BY score DESC
                   """
      result= session.run(algo_query3)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

      # ALGORITHM 4- algorithm for closeness score it finds the node that spreads information efficiently in the graph. It means that the nodes with high closeness scores are Papers that have the shortest distance to all other papers which is it can be thought of as the most referenced/cited paper which a lot of paper cites.
      print("--------------------------------")
      print("ALGORITHM 4- closeness RESULTS")
      print("--------------------------------") 
      print("Running the graph algorithm on the projected graph...")
      algo_query4= """CALL gds.closeness.stream('proj_paper_cite')
                      YIELD nodeId, score
                      WHERE score > 0.0
                      RETURN gds.util.asNode(nodeId).title AS paper_title, score AS AS closeness_score
                      ORDER BY score DESC
                   """
      result= session.run(algo_query4)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

      # ALGORITHM 5- using Dijkstra's shortest path (source to target) to find the shortest path in the citation networkn from a particular source paper to a particular target paper (if you want to use any other source or target paper just change the paper name in the query)
      print("------------------------------------------------------------------")
      print("ALGORITHM 5- Dijkstra's shortest path (source to target) RESULTS")
      print("------------------------------------------------------------------")
      print("Running the graph algorithm on the projected graph...")
      algo_query5= """MATCH (source:Paper {title: "Data Warehouse Refreshment"}), 
                      (target:Paper {title: "Data Warehouse Testing"})
                      CALL gds.shortestPath.dijkstra.stream('proj_paper_cite', {
                          sourceNode: source,
                          targetNode: target
                      })
                      YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
                      RETURN
                          index,
                          gds.util.asNode(sourceNode).title AS source_paper_title,
                          gds.util.asNode(targetNode).title AS target_paper_title,
                          totalCost,
                          [nodeId IN nodeIds | gds.util.asNode(nodeId).title] AS intermediate_paper_titles,
                          costs,
                          [idx IN range(0, size(nodes(path))-1) | {nodeNum:idx, title: nodes(path)[idx].title, paperId: nodes(path)[idx].ID}] as path
                      ORDER BY totalCost
                   """
      result= session.run(algo_query5)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

      # ALGORITHM 6- using Dijkstra's shortest path (SSSP) to find the shortest path in the citation network from a particular source paper to all other papers in the network (if you want to use any other source paper just change the paper name in the query)
      print("------------------------------------------------------------------------------")
      print("ALGORITHM 6- Dijkstra's shortest path (SSSP) RESULTS")
      print("------------------------------------------------------------------------------")
      print("Running the graph algorithm on the projected graph...")
      algo_query5= """MATCH (source:Paper {title: "Machine learning pipeline for battery state-of-health estimation"})
                      CALL gds.allShortestPaths.dijkstra.stream('proj_paper_cite', {
                          sourceNode: source
                      })
                      YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
                      // UNWIND range(0, nodes(path)-1) AS index
                      RETURN
                          index,
                          gds.util.asNode(sourceNode).title AS source_paper_title,
                          gds.util.asNode(targetNode).title AS target_paper_title,
                          totalCost,
                          [nodeId IN nodeIds | gds.util.asNode(nodeId).title] AS intermediate_paper_titles,
                          costs,
                          // [paper IN nodes(path)) | {nodeNum: title: paper.title, paperId: paper.ID}] as path
                          [idx IN range(0, size(nodes(path))-1) | {nodeNum:idx, title: nodes(path)[idx].title, paperId: nodes(path)[idx].ID}] as path
                      ORDER BY totalCost 
                   """
      result= session.run(algo_query5)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "xxxxxxxxxxxxxxx"  
    execute_queries(uri, user, password)