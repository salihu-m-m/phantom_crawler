import sys
import crawl


def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    
    print(f"starting crawl of {sys.argv[1]}")
    page_data = crawl.crawl_page(sys.argv[1])
    print(f"found {len(page_data)} pages")
    for page in page_data.values():
        print(page)



if __name__ == "__main__":
    main()
