from bs4 import BeautifulSoup
import asyncio
from crawl4ai import AsyncWebCrawler
import re

BASE_URL = "https://registry.terraform.io"

url = "https://registry.terraform.io/providers/hashicorp/aws/latest/docs"

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:

        result = await crawler.arun(url=url, delay_before_return_html=5)

        html = result.html

        print("HTML LENGTH:", len(html))

        soup = BeautifulSoup(html, "html.parser")

        links = []

        for a in soup.find_all("a", href=True):
            href = a["href"]

            if "providers/hashicorp/aws/latest/docs" in href:
                full_url = BASE_URL + href if href.startswith("/") else href
                links.append(full_url)

        links = list(set(links))

        print(f"Found {len(links)} links \n")

        for link in links[:30]: print(link)

        """

        scripts = soup.find_all("script")

        print(f"Found {len(scripts)} script tags")
        print(scripts)

        for script in scripts:
            if script.string and "aws_instance" in script.string:
                print(script.string[:5000])
                break"""

asyncio.run(main())