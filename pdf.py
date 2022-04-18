from PyPDF2 import PdfFileReader
import io
import requests

def download_pdf(url, path, min_pages_num=10):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}
  res = requests.get(url, headers=headers)
  reader = PdfFileReader(io.BytesIO(res.content))
  if reader.getNumPages() >= min_pages_num:
    with open(path, 'wb') as fs:
      fs.write(res.content)

def download_pdf_with_list(items, path):
  for i, item in enumerate(items):
    print(i + ' / ', len(items))
    download_pdf(item['pdf_link'], path + item['pdf_name'])