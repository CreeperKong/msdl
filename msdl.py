#!/usr/bin/env python3
import argparse
import requests
import re
import sys

def print_help():
    help_text = """
Usage:
  ./msdl.py [--lang LANGUAGES] --getlang id
  ./msdl.py --lang LANGUAGES --getlink id

Options:
  --help          Show this help message and exit
  --getlang       Retrieve all available languages
  --getlink       Retrieve download link(s) starting with https://download.microsoft.com/
  --lang          Specify language(s) (Required for --getlink, Troubleshooting-only for --getlang)

Examples:
  ./msdl.py --getlang 12345
  ./msdl.py --lang en-us --getlink 12345
  ./msdl.py --lang "en-us,zh-cn" --getlink 12345
"""
    print(help_text)

def fetch_page(lang, id_):
    url = f"https://www.microsoft.com/{lang}/download/details.aspx?id={id_}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0'
    }
    try:
        response = requests.get(url, headers=headers, timeout=120)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        sys.exit(1)

def extract_culture_codes(page_source):
    # Search for the <select> element with id="dropdown-select__options"
    select_match = re.search(r'<select[^>]+id=["\']dropdown-select__options["\'][^>]*>(.*?)</select>', page_source, re.DOTALL | re.IGNORECASE)
    if not select_match:
        print("[!] Could not find the language selection dropdown in the page.")
        return

    select_content = select_match.group(1)

    # Find all value attributes within the select element
    matches = re.findall(r'<option\s+value=["\']([^"\']+)["\']', select_content, re.IGNORECASE)
    if matches:
        unique_languages = sorted(set(lang.lower() for lang in matches))
        print(','.join(unique_languages))
    else:
        print("[!] No culture codes found.")
        sys.exit(1)

def extract_download_links(page_source):
    links = re.findall(r'https:\/\/download\.microsoft\.com\/[^\s\'"<>]+', page_source)
    if links:
        unique_links = sorted(set(links))
        for link in unique_links:
            print(link)
    else:
        print("[!] No download links found.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='store_true')
    parser.add_argument('--getlang', action='store_true')
    parser.add_argument('--getlink', action='store_true')
    parser.add_argument('--lang', type=str, default=None)
    parser.add_argument('id', nargs='?', type=str)

    args = parser.parse_args()

    if args.help or (not args.getlang and not args.getlink):
        print_help()
        sys.exit(0)

    if not args.id:
        print("[!] Error: You must provide an ID.")
        print_help()
        sys.exit(127)

    if args.getlang:
        lang = args.lang if args.lang else "en-us"
        page = fetch_page(lang, args.id)
        extract_culture_codes(page)

    elif args.getlink:
        langs = []
        if args.lang:
            langs = [l.strip() for l in args.lang.split(",")]
        else:
            langs = None  # Means fetch all

        if langs:
            for lang in langs:
                print(f"[*] Fetching links for language: {lang}")
                page = fetch_page(lang, args.id)
                extract_download_links(page)
        else:
            print("[!] Please specify language(s)")
            print("[!] Use --getlang to view the list of available languages")
            sys.exit(1)

if __name__ == "__main__":
    main()
