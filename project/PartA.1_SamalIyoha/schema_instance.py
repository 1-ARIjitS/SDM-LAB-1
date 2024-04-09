from graphviz import Digraph

# Instantiate Digraph object
dot = Digraph('ResearchPublicationsInstances')
dot.attr(rankdir='TB')  # Left to Right graph

# Define instance nodes
dot.node('A1', '<<b>Author</b><br/>id: 1<br/>name: John Brown<br/>email: johnbrown@saclay.com>', shape='ellipse', style='filled', fillcolor='lightblue')
dot.node('A2', '<<b>Author</b><br/>id: 2<br/>name: Jane Smith<br/>email: janesmith@ulb.com>', shape='ellipse', style='filled', fillcolor='lightblue')
dot.node('A3', '<<b>Author</b><br/>id: 3<br/>name: Iyoha Peace<br/>email: iyohapeace@upc.com>', shape='ellipse', style='filled', fillcolor='lightblue')
dot.node('A4', '<<b>Author</b><br/>id: 4<br/>name: Arijit Samal<br/>email: arijitsamal@nttdia.com>', shape='ellipse', style='filled', fillcolor='lightblue')
dot.node('P1', '<<b>Paper</b><br/>id: 101<br/>title: Big Data Challenges<br/>abstract: Overview of challenges<br/>DOI: 10.1001/bdc<br/>date: 2023<br/>url: paperurl_1.com>', shape='ellipse', style='filled', fillcolor='pink')
dot.node('P2', '<<b>Paper</b><br/>id: 102<br/>title: AI Techniques<br/>abstract: AI and ML Techniques<br/>DOI: 10.1002/ait<br/>date: 2022<br/>url: techurl.com>', shape='ellipse', style='filled', fillcolor='pink')
dot.node('P3', '<<b>Paper</b><br/>id: 103<br/>title: Quantum Computing<br/>abstract: Quantum Computing for big data<br/>DOI: 10.1003/qcb<br/>date: 2023<br/>url: computing.com>', shape='ellipse', style='filled', fillcolor='pink')
dot.node('P4', '<<b>Paper</b><br/>id: 104<br/>title: Internet of Things<br/>abstract: IoT applications<br/>DOI: 10.1004/iot<br/>date: 2023<br/>url: iotapp.com>', shape='ellipse', style='filled', fillcolor='pink')
dot.node('J', '<<b>Journal</b><br/>id: 201<br/>name: Journal of Data Science<br/>venue: Online<br/>year: 2022<br/>volume: 25>', shape='ellipse', style='filled', fillcolor='red')
dot.node('C', '<<b>Conference</b><br/>id: 301<br/>name: SIGMOD Conference<br/>year: 2023<br/>venue: New York>', shape='ellipse', style='filled', fillcolor='green')
dot.node('W', '<<b>Workshop</b><br/>id: 302<br/>name: Workshop on Data Privacy<br/>year: 2023<br/>venue: New York>', shape='ellipse', style='filled', fillcolor='green')
dot.node('Pr', '<<b>Proceeding</b><br/>id: 401<br/>name: Proceedings of SIGMOD<br/>city: New York>', shape='ellipse', style='filled', fillcolor='yellow')
dot.node('K1', '<<b>Keyword</b><br/>id: 501<br/>name: Big Data<br/>domain: Data Science>', shape='ellipse', style='filled', fillcolor='orange')
dot.node('K2', '<<b>Keyword</b><br/>id: 502<br/>name: Machine Learning<br/>domain: Computer Science>', shape='ellipse', style='filled', fillcolor='orange')
dot.node('K3', '<<b>Keyword</b><br/>id: 503<br/>name: Quantum Computing<br/>domain: Computer Science>', shape='ellipse', style='filled', fillcolor='orange')


# Define instance edges
dot.edge('A1', 'P1', 'writes\n- corresponding author: False')
dot.edge('A2', 'P1', 'writes\n- corresponding author: True')
dot.edge('A3', 'P3', 'writes\n- corresponding author: True')
dot.edge('A4', 'P4', 'writes\n- corresponding author: True')
dot.edge('P1', 'J', 'published_in')
dot.edge('P3', 'C', 'presented_in')
dot.edge('P4', 'W', 'presented_in')
dot.edge('P1', 'P2', 'cites')
dot.edge('P3', 'P4', 'cites')
dot.edge('A1', 'P3', 'reviews')
dot.edge('A4', 'P2', 'reviews')
dot.edge('C', 'Pr', 'is_part')
dot.edge('W', 'Pr', 'is_part')
dot.edge('P1', 'K1', 'has')
dot.edge('P2', 'K2', 'has')
dot.edge('P3', 'K3', 'has')
dot.edge('P4', 'K1', 'has')

# Save and render the graph
dot.render('ResearchPublications_instance_graph', view=True, format='pdf')
