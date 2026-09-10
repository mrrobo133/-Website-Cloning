import sys
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string

# ANSI Color Codes
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
C = '\033[96m'
W = '\033[0m'
BOLD = '\033[1m'

app = Flask(__name__)
CACHED_CONTENT = ""

def fix_and_mirror_content(target_url):
    print(f"\n{C}[*] Fetching and repairing assets from: {Y}{target_url}{W}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(target_url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML using BeautifulSoup to fix broken paths
        soup = BeautifulSoup(response.text, 'html.parser')

        # Inject Base Tag so relative CSS, JS, and Images load correctly from target server
        if not soup.find('base'):
            base_tag = soup.new_tag('base', href=target_url)
            if soup.head:
                soup.head.insert(0, base_tag)
            else:
                new_head = soup.new_tag('head')
                new_head.insert(0, base_tag)
                soup.insert(0, new_head)

        return str(soup)

    except Exception as e:
        print(f"\n{R}{BOLD}[!] Failed to fetch or repair target URL: {str(e)}{W}")
        return None

@app.route('/')
def serve_mirrored_page():
    global CACHED_CONTENT
    if CACHED_CONTENT:
        return render_template_string(CACHED_CONTENT)
    return "<h1>No content loaded yet.</h1>", 404

def main():
    global CACHED_CONTENT
    print(f"\n{Y}===================================================={W}")
    print(f"{C}{BOLD}    UPGRADED WEBSITE MIRRORING & ASSET FIXER        {W}")
    print(f"{Y}===================================================={W}")

    target_url = input(f"{B}[?] Enter Target URL (e.g., https://example.com): {W}").strip()
    if not target_url.startswith(('http://', 'https://')):
        print(f"{R}[!] Invalid URL format. Must start with http:// or https://{W}")
        sys.exit(1)

    CACHED_CONTENT = fix_and_mirror_content(target_url)
    if not CACHED_CONTENT:
        sys.exit(1)

    print(f"\n{G}{BOLD}[SUCCESS] Assets repaired and page ready!{W}")
    print(f"{C}{BOLD}[+] Localhost Server: {W}{Y}http://127.0.0.1:5000{W}")
    print(f"{R}[!] Press Ctrl+C to stop the server anytime.\n{W}")

    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print(f"\n{R}[!] Server stopped safely.{W}")

if __name__ == '__main__':
    main()
