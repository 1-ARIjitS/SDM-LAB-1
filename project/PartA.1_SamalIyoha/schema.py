from graphviz import Digraph

# Instantiate Digraph object
dot = Digraph('ResearchPublications')
dot.attr(rankdir='LR')  # Top to Bottom graph


# Define nodes for metadata schema
dot.node('Author', '<<b>Author</b><br/>- id<br/>- name<br/>- email>', shape='ellipse', style='filled', fillcolor='lightblue')
dot.node('Paper', '<<b>Paper</b><br/>- id<br/>- title<br/>- abstract<br/>- pages<br/>- DOI<br/>- link<br/>- date>', shape='ellipse', style='filled', fillcolor='pink')
dot.node('Keyword', '<<b>Keyword</b><br/>- id<br/>- name<br/>- domain>', shape='ellipse', style='filled', fillcolor='orange')
dot.node('Journal', '<<b>Journal</b><br/>- id<br/>- name<br/>- venue<br/>- publicationType<br/>- year<br/>- volume<br/>- issn<br/>- url<br/>- JournalEditor>', shape='ellipse', style='filled', fillcolor='red')
dot.node('Conference', '<<b>Conference</b><br/>- id<br/>- name<br/>- year<br/>- venue<br/>- edition<br/>- issn<br/>- url<br/>- conferenceChair>', shape='ellipse', style='filled', fillcolor='green')
dot.node('Workshop', '<<b>Workshop</b><br/>- id<br/>- name<br/>- year<br/>- venue<br/>- edition<br/>- issn<br/>- url<br/>- WorkshopChair>', shape='ellipse', style='filled', fillcolor='green')
dot.node('Proceeding', '<<b>Proceeding</b><br/>- id<br/>- name<br/>- city>', shape='ellipse', style='filled', fillcolor='yellow')



# Define edges for metadata schema
dot.edge('Author', 'Paper', label='<writes<br/><font color="blue">corresponding author</font>>', fontcolor='blue')
dot.edge('Paper', 'Journal', 'published_in')
dot.edge('Paper', 'Conference', 'presented_in')
dot.edge('Paper', 'Workshop', 'presented_in')
dot.edge('Paper', 'Keyword', 'has')
dot.edge('Paper', 'Paper', 'cites')
dot.edge('Author', 'Paper', 'reviews')
dot.edge('Conference', 'Proceeding', 'is_part')
dot.edge('Workshop', 'Proceeding', 'is_part')


# Save and render the graph
dot.render('ResearchPublications_graph', view=True, format='pdf')


