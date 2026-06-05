import json

def write_json_report(page_data, filename="crawl_report.json"):
    pages = sorted(page_data.values(), key=lambda x: x['url'])
    open(filename, "w", encoding="utf-8").write(json.dumps(pages, indent=2, ensure_ascii=False))