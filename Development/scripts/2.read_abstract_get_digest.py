import arxiv
from scholarly import scholarly
import csv
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
import apis
import requests
import json

date_stamp = datetime.today().strftime('%Y-%m-%d')
filename = Path(f"Development/paper_list/software_engineering_{date_stamp}.jsonl")
# read the jsonl file
with open(filename, "r") as file:
  lines = file.readlines()
  data = []
  for line in lines:
    try:
      data.append(json.loads(line))
    except json.JSONDecodeError:
      continue
print(len(lines))

# sort the data by the updated date
data = sorted(data, key=lambda x: x["updated_date"], reverse=True)

for index, row in enumerate(data):
  print(index)
  paper_link = row['paper_link']
  abstract = row['abstract']
  paper_id = paper_link.split("/")[-1]
  response = apis.get_summary_from_abstract(abstract)
  txt_path = Path(f"Development/digest_list/paper_{paper_id}.txt")
  with open(txt_path, "w") as file:
    file.write(response)