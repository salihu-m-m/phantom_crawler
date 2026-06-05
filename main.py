import sys
import crawl
import asyncio
from json_report import write_json_report



async def main():
    if len(sys.argv) < 4:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    

    base_url = sys.argv[1]
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])
    page_data = await crawl.crawl_site_async(base_url, max_concurrency, max_pages)
    print(f"Starting async crawl of: {base_url}")

    for page in page_data.values():
        print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")

    write_json_report(page_data)
    sys.exit(0)
if __name__ == "__main__":
    asyncio.run(main())
