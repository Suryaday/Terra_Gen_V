from bs4 import BeautifulSoup
import requests
import asyncio
import json
import os
from crawl4ai import AsyncWebCrawler

BASE_URL = "https://registry.terraform.io"

url = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs"

html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

links = []

for a in soup.find_all("a", href=True):
    href = a["href"]

    if "providers/hashicorp/aws/latest/docs" in href:
        full_url = BASE_URL + href if href.startswith("/") else href
        links.append(full_url)

links = list(set(links))

for link in links[:20]:
    print(link)

KEYWORDS = [
    "instance",
    "vpc",
    "subnet",
    "security_group",
    "iam",
    "s3",
    "alb",
    "lb",
    "rds",
]

filtered_links = []

for link in links:
    if any(keyword in link for keyword in KEYWORDS):
        filtered_links.append(link)

print(len(filtered_links))

URLS = filtered_links

OUTPUT_DIR = "data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def scrape_page(crawler, url):
    try:
        result = await crawler.arun(url=url)

        data = {
            "url": url,
            "title": result.metadata.get("title", ""),
            "content": result.markdown
        }

        filename = url.split("/")[-2] + ".json"

        with open(f"{OUTPUT_DIR}/{filename}", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Saved: {filename}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        tasks = [scrape_page(crawler, url) for url in URLS]
        await asyncio.gather(*tasks)

asyncio.run(main())