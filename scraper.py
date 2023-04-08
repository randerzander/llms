import requests
from bs4 import BeautifulSoup

# URL of the Dask documentation main page
#url = 'https://docs.dask.org/en/stable/'
#url = "https://distributed.dask.org/en/stable/"
url = "https://dask-sql.readthedocs.io/en/latest/"

# Send an HTTP GET request to the URL and get the content
response = requests.get(url)
content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Extract all the links with the class "reference internal" within the left sidebar
links = soup.find_all('a', {'class': 'reference internal'})

# If you want to make the links absolute (full URLs), you can use:
for link in links:
  new_url = url + link['href']
  print(new_url)
  response = requests.get(url)
  content = response.content

# Parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(content, 'html.parser')
  text_content = soup.get_text()
  fn = "dask_docs/sql/"+link["href"].replace("/", "_")
  with open(fn, "w") as fp:
    fp.write(text_content)
