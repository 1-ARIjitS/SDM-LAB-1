# from graphviz import Digraph

# # Instantiate Digraph object
# dot = Digraph('ResearchPublications')
# dot.attr(rankdir='LR')  # Top to Bottom graph


# # Define nodes for metadata schema
# dot.node('Author', '<<b>Author</b><br/>- id<br/>- name<br/>- email>', shape='ellipse', style='filled', fillcolor='lightblue')
# dot.node('Paper', '<<b>Paper</b><br/>- id<br/>- title<br/>- abstract<br/>- pages<br/>- DOI<br/>- link<br/>- date>', shape='ellipse', style='filled', fillcolor='pink')
# dot.node('Keyword', '<<b>Keyword</b><br/>- id<br/>- name<br/>- domain>', shape='ellipse', style='filled', fillcolor='orange')
# dot.node('Journal', '<<b>Journal</b><br/>- id<br/>- name<br/>- venue<br/>- publicationType<br/>- year<br/>- volume<br/>- issn<br/>- url<br/>- JournalEditor>', shape='ellipse', style='filled', fillcolor='red')
# dot.node('Conference', '<<b>Conference</b><br/>- id<br/>- name<br/>- year<br/>- venue<br/>- edition<br/>- issn<br/>- url<br/>- conferenceChair>', shape='ellipse', style='filled', fillcolor='green')
# dot.node('Workshop', '<<b>Workshop</b><br/>- id<br/>- name<br/>- year<br/>- venue<br/>- edition<br/>- issn<br/>- url<br/>- WorkshopChair>', shape='ellipse', style='filled', fillcolor='green')
# dot.node('Proceeding', '<<b>Proceeding</b><br/>- id<br/>- name<br/>- city>', shape='ellipse', style='filled', fillcolor='yellow')
# dot.node('Organization', '<<b>Organization</b><br/>- id<br/>- name<br/>- affiliation_type>', shape='ellipse', style='filled', fillcolor='blue')



# # Define edges for metadata schema
# dot.edge('Author', 'Paper', 'writes\n- corresponding author')
# dot.edge('Author', 'Organization', 'affiliated_with')
# dot.edge('Paper', 'Journal', 'published_in')
# dot.edge('Paper', 'Conference', 'presented_in')
# dot.edge('Paper', 'Workshop', 'presented_in')
# dot.edge('Paper', 'Keyword', 'has')
# dot.edge('Paper', 'Paper', 'cites')
# dot.edge('Author', 'Paper', 'reviews\n- ReviewContent\n- Decision')
# dot.edge('Conference', 'Proceeding', 'is_part')
# dot.edge('Workshop', 'Proceeding', 'is_part')
# dot.edge('Conference', 'Author', 'conferencechair_assign_reviewer')
# dot.edge('Workshop', 'Author', 'workshopchair_assign_reviewer')
# dot.edge('Journal', 'Author', 'editor_assign_reviewer')



# # Save and render the graph
# dot.render('ResearchPublications_graph_evolve', view=True, format='pdf')


# from graphviz import Digraph

# # Instantiate Digraph object
# dot = Digraph('ResearchPublications')
# dot.attr(rankdir='LR')  # Left to Right graph

# # Define nodes for metadata schema
# dot.node('Author', '<<b>Author</b><br/>- id<br/>- name<br/>- email>', shape='ellipse', style='filled', fillcolor='lightblue')
# dot.node('Paper', '<<b>Paper</b><br/>- id<br/>- title<br/>- abstract<br/>- pages<br/>- DOI<br/>- link<br/>- date>', shape='ellipse', style='filled', fillcolor='pink')
# dot.node('Keyword', '<<b>Keyword</b><br/>- id<br/>- name<br/>- domain>', shape='ellipse', style='filled', fillcolor='orange')
# dot.node('Journal', '<<b>Journal</b><br/>- id<br/>- name<br/>- venue<br/>- publicationType<br/>- year<br/>- volume<br/>- issn<br/>- url<br/>- JournalEditor>', shape='ellipse', style='filled', fillcolor='red')
# dot.node('Conference', '<<b>Conference</b><br/>- id<br/>- name<br/>- year<br/>- venue<br/>- edition<br/>- issn<br/>- url<br/>- conferenceChair>', shape='ellipse', style='filled', fillcolor='green')
# dot.node('Workshop', '<<b>Workshop</b><br/>- id<br/>- name<br/>- year<br/>- venue<br/>- edition<br/>- issn<br/>- url<br/>- WorkshopChair>', shape='ellipse', style='filled', fillcolor='green')
# dot.node('Proceeding', '<<b>Proceeding</b><br/>- id<br/>- name<br/>- city>', shape='ellipse', style='filled', fillcolor='yellow')
# dot.node('Organization', '<<b>Organization</b><br/>- id<br/>- name<br/>- affiliation_type>', shape='ellipse', style='filled', fillcolor='blue')

# # Define edges with labels and colors
# dot.edge('Author', 'Paper', '<<b>writes</b><br/>- corresponding author: True>', color='blue', fontcolor='black')
# dot.edge('Author', 'Organization', '<<b>affiliated_with</b>', color='red', fontcolor='black')
# dot.edge('Paper', 'Journal', '<<b>published_in</b>', color='green', fontcolor='black')
# dot.edge('Paper', 'Conference', '<<b>presented_in</b>', color='purple', fontcolor='black')
# dot.edge('Paper', 'Workshop', '<<b>presented_in</b>', color='purple', fontcolor='black')
# dot.edge('Paper', 'Keyword', '<<b>has</b>', color='orange', fontcolor='black')
# dot.edge('Paper', 'Paper', '<<b>cites</b>', color='black', fontcolor='black')
# dot.edge('Author', 'Paper', '<<b>reviews</b><br/>- ReviewContent<br/>- Decision>', color='magenta', fontcolor='black')
# dot.edge('Conference', 'Proceeding', '<<b>is_part</b>', color='brown', fontcolor='black')
# dot.edge('Workshop', 'Proceeding', '<<b>is_part</b>', color='brown', fontcolor='black')
# dot.edge('Conference', 'Author', '<<b>conferencechair_assign_reviewer</b>', color='teal', fontcolor='black')
# dot.edge('Workshop', 'Author', '<<b>workshopchair_assign_reviewer</b>', color='teal', fontcolor='black')
# dot.edge('Journal', 'Author', '<<b>editor_assign_reviewer</b>', color='cyan', fontcolor='black')

# # Save and render the graph
# dot.render('ResearchPublications_graph_evolve', view=True, format='pdf')


from graphviz import Digraph

# Instantiate Digraph object
dot = Digraph('ResearchPublications')
dot.attr(rankdir='LR')  # Left to Right graph

# Define nodes for metadata schema
dot.node('Author', '<<b>Author</b><br/>- id<br/>- name<br/>- email>', shape='ellipse', style='filled', fillcolor='lightblue')
dot.node('Paper', '<<b>Paper</b><br/>- id<br/>- title<br/>- abstract<br/>- pages<br/>- DOI<br/>- link<br/>- date>', shape='ellipse', style='filled', fillcolor='pink')
dot.node('Keyword', '<<b>Keyword</b><br/>- id<br/>- name<br/>- domain>', shape='ellipse', style='filled', fillcolor='orange')
dot.node('Journal', '<<b>Journal</b><br/>- id<br/>- name<br/>- venue<br/>- publicationType<br/>- year<br/>- volume<br/>- issn<br/>- url<br/>- JournalEditor>', shape='ellipse', style='filled', fillcolor='red')
dot.node('Conference', '<<b>Conference</b><br/>- id<br/>- name<br/>- year<br/>- venue<br/>- edition<br/>- issn<br/>- url<br/>- conferenceChair>', shape='ellipse', style='filled', fillcolor='green')
dot.node('Workshop', '<<b>Workshop</b><br/>- id<br/>- name<br/>- year<br/>- venue<br/>- edition<br/>- issn<br/>- url<br/>- WorkshopChair>', shape='ellipse', style='filled', fillcolor='green')
dot.node('Proceeding', '<<b>Proceeding</b><br/>- id<br/>- name<br/>- city>', shape='ellipse', style='filled', fillcolor='yellow')
dot.node('Organization', '<<b>Organization</b><br/>- id<br/>- name<br/>- affiliation_type>', shape='ellipse', style='filled', fillcolor='purple')


# Define edges with HTML-like labels
dot.edge('Author', 'Paper','<<b>writes</b><br/>corresponding author>')
dot.edge('Author', 'Organization', 'affiliated_with', fontcolor='orange')
dot.edge('Paper', 'Journal', 'published_in')
dot.edge('Paper', 'Conference', 'presented_in')
dot.edge('Paper', 'Workshop', 'presented_in')
dot.edge('Paper', 'Keyword', 'has')
dot.edge('Paper', 'Paper', 'cites')
dot.edge('Author', 'Paper', label='<<b>reviews</b><br/><font color="orange">ReviewContent<br/>Decision</font>>', fontcolor='orange')
dot.edge('Conference', 'Proceeding', 'is_part')
dot.edge('Workshop', 'Proceeding', 'is_part')
dot.edge('Conference', 'Author', '<<b>conferencechair_assign_reviewer</b><br/><font color="orange">ConferenceChairName<br/>ReviewPolicy</font>>', fontcolor='orange')
dot.edge('Workshop', 'Author', '<<b>workshopchair_assign_reviewer</b><br/><font color="orange">WorkshopChairName<br/>ReviewPolicy</font>>', fontcolor='orange')
dot.edge('Journal', 'Author', '<<b>editor_assign_reviewer</b><br/><font color="orange">JournalEditorName<br/>ReviewPolicy</font>>', fontcolor='orange')

# Save and render the graph
dot.render('ResearchPublications_graph_evolve', view=True, format='pdf')
