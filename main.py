import sys
import crawl
import asyncio


async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    

    base_url = sys.argv[1]

    print(f"Starting async crawl of: {base_url}")

    page_data = await crawl.crawl_site_async(base_url)

    for page in page_data.values():
        print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")

    sys.exit(0)
if __name__ == "__main__":
    asyncio.run(main())
