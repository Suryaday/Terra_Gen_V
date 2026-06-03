from bs4 import BeautifulSoup
import requests

url = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs"

html = requests.get(url).text

print(html)