import asyncio
import json
import os
from crawl4ai import AsyncWebCrawler

URLS = [
    "https://registry.terraform.io/providers/hashicorp/aws/latest/docs"
]

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