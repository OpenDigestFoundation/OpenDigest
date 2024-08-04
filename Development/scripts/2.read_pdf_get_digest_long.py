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
  paper_link = row['paper_link']
  abstract = row['abstract']
  paper_link.replace("abs","pdf")
  paper_id = paper_link.split("/")[-1]
  url = f"https://arxiv.org/pdf/{paper_id}.pdf"
  print(url)
  response = requests.get(url)
  # Save the PDF file
  pdf_path = Path(f"Development/paper_list/paper_{paper_id}.pdf")
  with open(pdf_path, "wb") as file:
    # write pdf content to file
    file.write(response.content)

  response = apis.output_review_from_file(pdf_path, style = "long")
  # response = apis.get_summary_from_abstract(abstract)

  txt_path = Path(f"Development/digest_full_paper_list/paper_{paper_id}.txt")
  with open(txt_path, "w") as file:
    file.write(response)