import csv
import pandas as pd
from urllib.request import Request, urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = "http://www.imdb.com/search/title?sort=num_votes,desc&start=1&title_type=feature&year=1950,2012"

# Set the User-Agent header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
req = Request(my_url, headers=headers)
uClient = uReq(req)

page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

# Find all movie containers
containers = page_soup.findAll("div", {"class": "sc-1e00898e-0 jyXHpt"})

filename = "imdb_m.csv"
with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Year", "Runtime"])

    for container in containers:
        # Extracting movie name without the number
        name_element = container.find("h3", {"class": "ipc-title__text"})
        name = name_element.text.strip().split(".")[1].strip() if name_element else ""

        # Extracting year
        year_span = container.find("span", {"class": "sc-1e00898e-8", "class": "hsHAHC", "class": "dli-title-metadata-item"})
        year = year_span.text.strip() if year_span else ""

        # Extracting runtime
        runtime_span = container.find_all("span", {"class": "sc-1e00898e-8", "class": "hsHAHC", "class": "dli-title-metadata-item"})
        runtime = runtime_span[1].text.strip() if len(runtime_span) > 1 else ""

        # Write data to the CSV file
        writer.writerow([name, year, runtime])

# Read the CSV file into a DataFrame
imdb = pd.read_csv("imdb_m.csv", encoding="utf-8")

# Display the first few rows of the DataFrame
print(imdb.head())
