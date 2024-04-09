from neo4j import GraphDatabase
import pandas as pd
import os

def execute_queries(uri, user, password, root_path):
    driver = GraphDatabase.driver(uri, auth=(user, password))
      
    with driver.session() as session:
      def run_query_and_export_to_csv(query, csv_file_name, query_description, root_path):
            print(f"\nExecuting query: {query_description}")
            result= session.run(query)
            records = list(result)
            df = pd.DataFrame(records)
            csv_folder_path= os.path.join(root_path, "ALGORITHM_RESULTS")
            if not os.path.exists(csv_folder_path):
                os.makedirs(csv_folder_path)
            csv_file_path = os.path.join(csv_folder_path, f"{csv_file_name}.csv")
            # Print the DataFrame to console
            print(f"Results for '{query_description}':")
            print(df)
            # Save the DataFrame to a CSV file
            df.to_csv(csv_file_path, index=False)
            print(f"Query '{query_description}' completed and saved to '{csv_file_path}'")

      # ALGORITHM 1- using the node similarity algorithm to find papers that have the similar keywords
      print("--------------------------------------")
      print("ALGORITHM 1- Node Similarity RESULTS")
      print("--------------------------------------")
      print("deleting projection of the graph before creaating it for querying...")
      del_proj_query1="""CALL gds.graph.exists('proj_paper_cites')
                      YIELD exists
                      WITH exists
                      WHERE exists
                      CALL gds.graph.drop('proj_paper_cites')
                      YIELD graphName AS droppedGraphName
                      RETURN droppedGraphName;
                  """
      result= session.run(del_proj_query1)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

      print("creating projection of the graph for querying...")
      proj_query1="""CALL gds.graph.project(
                      'proj_paper_cites',
                      'Paper',
                      'cites',
                      {}
                    )
                  """
      result= session.run(proj_query1)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

      print("Running the graph algorithm on the projected graph...")
      algo_query1= """CALL gds.nodeSimilarity.stream('proj_paper_cites', { topK: 1 })
                  YIELD node1, node2, similarity
                  WHERE similarity<1.0
                  RETURN distinct gds.util.asNode(node1).title AS paper1, gds.util.asNode(node2).title AS paper2, similarity
                  ORDER BY similarity DESC;
                """
      run_query_and_export_to_csv(algo_query1, "similarity", "node similarity algorithm", root_path)

      # ALGORITHM 2- using Dijkstra's shortest path (source to target) to find the shortest path between authors on how they are interconnected through their publications and citations (if you want to use any other source or target paper just change the paper name in the query)
      print("------------------------------------------------------------------")
      print("ALGORITHM 2- Dijkstra's shortest path (source to target) RESULTS")
      print("------------------------------------------------------------------")
      print("deleting projection of the graph before creaating it for querying...")
      delete_proj_query2="""CALL gds.graph.exists('proj_author_paper_cites')
                            YIELD exists
                            WITH exists
                            WHERE exists
                            CALL gds.graph.drop('proj_author_paper_cites')
                            YIELD graphName AS droppedGraphName
                            RETURN droppedGraphName;
                          """
      result= session.run(delete_proj_query2)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)
      
      print("creating projection of the graph for querying...")
      proj_query2="""CALL gds.graph.project(
                    'proj_author_paper_cites', 
                    {
                      Author: {
                        label: 'Author'
                      }, 
                      Paper: {
                        label: 'Paper'
                      }
                    }, 
                    {
                      writes: {
                        type: 'writes',
                        orientation: 'UNDIRECTED'
                      },
                      cites: {
                        type: 'cites',
                        orientation: 'UNDIRECTED'
                      }
                    }
                  )
                  """
      result= session.run(proj_query2)
      records = list(result)
      summary = result.consume()
      for record in records:
         print(record)

      print("Running the graph algorithm on the projected graph...")
      algo_query2= """MATCH (source:Author {ID: "145261717"}), 
                      (target:Author {ID: "24195448"})
                      CALL gds.shortestPath.dijkstra.stream('proj_author_paper_cites', {
                          sourceNode: source,
                          targetNode: target
                      })
                      YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
                      RETURN
                          distinct
                          index,
                          gds.util.asNode(sourceNode).name AS source_author_name,
                          gds.util.asNode(targetNode).name AS target_author_name,
                          totalCost,
                          [nodeId IN nodeIds | 
                              CASE 
                                  WHEN 'Author' IN labels(gds.util.asNode(nodeId)) THEN gds.util.asNode(nodeId).name
                                  ELSE gds.util.asNode(nodeId).title
                              END] AS intermediate_names,
                          costs,
                          [idx IN range(0, size(nodes(path))-1) | {nodeNum:idx, name:nodes(path)[idx].name, authorId: nodes(path)[idx].authorId}] as path
                      ORDER BY totalCost
                   """      
      run_query_and_export_to_csv(algo_query2, "Dijkstar's_shortest_path_source_to_target", "Dijkstra's shortest path (source to target) algorithm", root_path)

      # ALGORITHM 3- using Dijkstra's shortest path (SSSP) to find the shortest path in the citation network from a particular source paper to all other papers in the network (if you want to use any other source paper just change the paper name in the query)
      print("----------------------------------------------------------")
      print("ALGORITHM 3- Dijkstra's shortest path (SSSP) RESULTS")
      print("----------------------------------------------------------")
      print("Running the graph algorithm on the projected graph...")
      algo_query3= """MATCH (source:Paper {title: "Machine learning pipeline for battery state-of-health estimation"})
                      CALL gds.allShortestPaths.dijkstra.stream('proj_paper_cite', {
                          sourceNode: source
                      })
                      YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
                      RETURN
                          distinct
                          index,
                          gds.util.asNode(sourceNode).title AS source_paper_title,
                          gds.util.asNode(targetNode).title AS target_paper_title,
                          totalCost,
                          [nodeId IN nodeIds | gds.util.asNode(nodeId).title] AS intermediate_paper_titles,
                          costs,
                          [idx IN range(0, size(nodes(path))-1) | {nodeNum:idx, title: nodes(path)[idx].title, paperId: nodes(path)[idx].ID}] as path
                      ORDER BY totalCost 
                   """
      run_query_and_export_to_csv(algo_query3, "Dijkstar's_SSSP", "Dijkstra's shortest path (SSSP) algorithm", root_path)

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "1*@#Saymyname"  
    root_path= "D:/BDMA/UPC/SDM/LAB/LAB1/project"
    execute_queries(uri, user, password, root_path)