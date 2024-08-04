import fitz, os
file_name_pdf = "paper_2407.08176v1.pdf"
doc = fitz.open(f'Development/paper_list/{file_name_pdf}')
imgcount = 0
total_image_list=[]

for page in doc:
  # get a list of images on that page
  imglist = page.get_images(full=True)
  print(f'Found {len(imglist)} images on page {page.number}')
  total_image_list.extend(imglist)
  
total_image_list.sort(key=lambda x: x[2] * x[3], reverse=True)
total_image_list = total_image_list[:3]

for img in total_image_list:
  xref = img[0]
  base_image = doc.extract_image(xref)
  image_bytes = base_image["image"]
  try:
    # write image to folder
    image_path = f'Development/images/image_{imgcount}.png'
    #
    with open(image_path, 'wb') as f:
        f.write(image_bytes)
    imgcount += 1
  except Exception as e:
    print(f'Error: {e}')
    
