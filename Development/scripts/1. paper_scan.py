import arxiv
from scholarly import scholarly
import csv
import os
from pathlib import Path
from datetime import datetime
import json

#========================================
#=========== Arxiv paper scan ===========
#========================================
date_stamp = datetime.today().strftime('%Y-%m-%d')
queries = [
  # these words only in queries
    "software engineering",
]
# https://arxiv.org/help/api/user-manual#query_detail
# https://github.com/lukasschwab/arxiv.py/blob/debug-failing-ci/arxiv/arxiv.py
all_result_list = []
for q in queries:
  search = arxiv.Search(
      # query = f"abs:{q} AND cat:cs.se",
      # query = f"ti:{q} AND cat:cs.se",
      query = f"ti:{q}",
      # query = f"abs:{q}",
      max_results = 20,
      sort_by = arxiv.SortCriterion.SubmittedDate
      )
  result_list = [x for x in arxiv.Client().results(search)]
  print(len(result_list))
  all_result_list.extend(result_list)
print(len(all_result_list))
unique_list = []
unique_titles = []
all_result_list_1 = [x for x in all_result_list if "cs.SE" in str(x.primary_category)]
all_result_list_2 = [x for x in all_result_list if "cs.AI" in str(x.primary_category)]
all_result_list= all_result_list_1 + all_result_list_2
# print(all_result_list[0].__dict__)


for result in all_result_list:
  title = str(result.title)
  if not title in unique_titles:
    unique_list.append(result)
    unique_titles.append(result.title)
print("total unique paper count",len(unique_list))

filename = Path(f"Development/paper_list/software_engineering_{date_stamp}.jsonl")



for result in unique_list:
    # see all category here:https://arxiv.org/category_taxonomy
    # if "cs." not in str(result.primary_category):
      # remove non-Software engineering result
      # continue
    first_author = str(result.authors[0])
    last_author = str(result.authors[-1])
    result_row = {"title":result.title,"category":result.primary_category,"affiliation":"","updated_date":str(result.updated),"author":first_author,"director":last_author,"director_cited_count":0,"paper_link":str(result), "abstract":result.summary}
    try:
      search_query = scholarly.search_author(first_author)
      first_author_result = next(search_query)
      first_author_affiliation = first_author_result["affiliation"]
    except:
      first_author_affiliation=""
    try:
      search_query = scholarly.search_author(last_author)
      last_author_result = next(search_query)
      last_author_affiliation = last_author_result["affiliation"]
      last_author_ciated = last_author_result["citedby"]
    except:
      last_author_affiliation=""
      last_author_ciated=0

    result_row["affiliation"] = first_author_affiliation +", "+last_author_affiliation
    result_row["director_cited_count"] = last_author_ciated
    with open(filename, 'a') as file:
      json.dump(result_row, file)
      file.write('\n')