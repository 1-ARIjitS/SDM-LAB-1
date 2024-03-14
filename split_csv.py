import os
import pandas as pd
import ast

def node_papers(df, csv_folder_path):
  print("creating papers node...")
  df_papers= df.copy()
  df_papers= df_papers[['paperId', 'title', 'abstract', 'year', 'venue', 'citationCount', 'referenceCount', 'fieldsOfStudy']]
  df_papers.to_csv(os.path.join(csv_folder_path, "node_papers.csv"), index=False)

def node_authors(df, csv_folder_path):
  print("creating authors node...")
  author_pool=[]
  for author_list in df['authors']:
      author_pool.extend(ast.literal_eval(author_list))
  print(author_pool)
  df_authors=pd.DataFrame(author_pool)
  df_authors.to_csv(os.path.join(csv_folder_path, "node_authors.csv"), index=False)

def node_keywords(df, csv_folder_path):
    print("Creating keywords node...")
    keywords_pool=[]
    for i in df['keywords']:
        keywords_pool.extend(ast.literal_eval(i))
    columns=['keywords']
    df_keywords= pd.DataFrame(keywords_pool, columns=columns)
    df_keywords.to_csv(os.path.join(csv_folder_path, "node_keywords.csv"), index=False)

def node_journal(df, csv_folder_path):
    print("Creating journal node...")
    columns=['publicationId', 'publicationType', 'name', 'venue', 'year', 'issn', 'url', 'volume']
    df_journal=pd.DataFrame(columns= columns)
    for index, row in df.iterrows():
      publication_type= row['publicationType']
      if publication_type=='journal':
        try:
          publication_dict= ast.literal_eval(row['publicationVenue'])
          publication_journal_info= ast.literal_eval(row['journal'])
          df_journal.at[index, 'publicationId']= publication_dict['id']
          df_journal.at[index, 'publicationType'] = publication_type
          df_journal.at[index, 'name']= publication_dict['name']
          df_journal.at[index, 'venue']= row['venue']
          df_journal.at[index, 'year']= row['year']
          if 'issn' in publication_dict.keys():
            df_journal.at[index, 'issn']= publication_dict['issn']
          else:
            df_journal.at[index, 'issn']= ''
          if 'url' in publication_dict.keys():
            df_journal.at[index, 'url']= publication_dict['url']
          else:
            df_journal.at[index, 'url']= ''
          if 'volume' in publication_journal_info.keys():
            df_journal.at[index, 'volume']= publication_journal_info['volume']
          else:
            df_journal.at[index, 'volume']= '1'
        except:
          pass
      else:
        pass
    df_journal.to_csv(os.path.join(csv_folder_path, "node_journal.csv"), index=False)

def node_conference(df, csv_folder_path):
    print("Creating conferences node...")
    columns=['publicationId', 'publicationType', 'name', 'venue', 'year', 'issn', 'url']
    df_conference=pd.DataFrame(columns= columns)
    for index, row in df.iterrows():
      publication_type= row['publicationType']
      if publication_type=='conference':
        try:
          publication_dict= ast.literal_eval(row['publicationVenue'])
          df_conference.at[index, 'publicationId']= publication_dict['id']
          df_conference.at[index, 'publicationType'] = publication_type
          df_conference.at[index, 'name']= publication_dict['name']
          df_conference.at[index, 'venue']= row['venue']
          df_conference.at[index, 'year']= row['year']
          if 'issn' in publication_dict.keys():
            df_conference.at[index, 'issn']= publication_dict['issn']
          else:
            df_conference.at[index, 'issn']= ''
          if 'url' in publication_dict.keys():
            df_conference.at[index, 'url']= publication_dict['url']
          else:
            df_conference.at[index, 'url']= ''
        except:
          pass
      else:
        pass
    df_conference.to_csv(os.path.join(csv_folder_path, "node_conference.csv"), index=False)

def node_workshop(df, csv_folder_path):
    print("Creating workshops node...")
    columns=['publicationId', 'publicationType', 'name', 'venue', 'year', 'issn', 'url']
    df_workshop=pd.DataFrame(columns= columns)
    for index, row in df.iterrows():
      publication_type= row['publicationType']
      if publication_type=='workshop':
        try:
          publication_dict= ast.literal_eval(row['publicationVenue'])
          df_workshop.at[index, 'publicationId']= publication_dict['id']
          df_workshop.at[index, 'publicationType'] = publication_type
          df_workshop.at[index, 'name']= publication_dict['name']
          df_workshop.at[index, 'venue']= row['venue']
          df_workshop.at[index, 'year']= row['year']
          if 'issn' in publication_dict.keys():
            df_workshop.at[index, 'issn']= publication_dict['issn']
          else:
            df_workshop.at[index, 'issn']= ''
          if 'url' in publication_dict.keys():
            df_workshop.at[index, 'url']= publication_dict['url']
          else:
            df_workshop.at[index, 'url']= ''
        except:
          pass
      else:
        pass
    df_workshop.to_csv(os.path.join(csv_folder_path, "node_workshop.csv"), index=False)

root_path= "D:/BDMA/UPC/SDM/LAB/LAB1"
csv_folder_path= os.path.join(root_path, "CSV_files")
csv_file_path= os.path.join(csv_folder_path, "ml_updated_data.csv")

df= pd.read_csv(csv_file_path)
print(f"shape: {df.shape}")

# Nodes creation
node_papers(df, csv_folder_path)
node_authors(df, csv_folder_path)
node_keywords(df, csv_folder_path)
node_journal(df, csv_folder_path)
node_conference(df, csv_folder_path)
node_workshop(df, csv_folder_path)

# relation creation
