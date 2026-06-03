from bs4 import BeautifulSoup
import requests

BASE_URL = "https://registry.terraform.io"

url = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs"

html = requests.get(url).text
print(html)

soup = BeautifulSoup(html, "html.parser")

links = []

for a in soup.find_all("a", href=True):
    href = a["href"]
    print(href)

    if "providers/hashicorp/aws/latest/docs" in href:
        full_url = url + href if href.startswith("/") else href
        print(full_url)
        links.append(full_url)

links = list(set(links))

for link in links[:20]:
    print(link)