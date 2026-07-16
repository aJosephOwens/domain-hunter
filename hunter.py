import requests, re, csv, time
from pathlib import Path
from datetime import datetime

KEYWORDS = ["cad","cam","autocad","solidworks","fusion","vst","flstudio","ableton","beat","midi","daw","soundtrack","mixing"]
Path("finds").mkdir(exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
domains = {}

for kw in KEYWORDS:
    try:
        # Spamzilla free search with DR30+ - public page, no login needed for first page
        url = f"https://www.spamzilla.io/domains/search/?filters%5Bsearch_keywords%5D={kw}&filters%5Bdr_min%5D=30&filters%5Bdomain_extension%5D=com&filters%5Bdomains_type%5D=expired&sort=dr_desc"
        # Use proxy to avoid Cloudflare block on GitHub IPs
        proxied = f"https://api.allorigins.win/raw?url={requests.utils.quote(url, safe='')}"
        r = requests.get(proxied, headers=headers, timeout=25)
        if r.status_code == 200:
            # Spamzilla domains appear as >domain.com< in results
            found = re.findall(r'>([a-z0-9-]+\.com)<', r.text, re.I)
            for d in found:
                if kw in d.lower() and len(d) < 30 and d not in domains:
                    domains[d.lower()] = kw
        print(f"{kw}: total {len(domains)}")
        time.sleep(1.5)
    except Exception as e:
        print(f"{kw} error {e}")

# If Spamzilla blocks, fallback to ExpiredDomains
if len(domains) < 3:
    print("Spamzilla blocked, trying ExpiredDomains fallback")
    try:
        r = requests.get("https://api.allorigins.win/raw?url=https://www.expireddomains.net/domains/expired/com/?o=rpopdsc&r=d", headers=headers, timeout=25)
        found = re.findall(r'/whois/com/([a-z0-9-]{3,}\.com)\.html', r.text, re.I)[:200]
        for d in found:
            for kw in KEYWORDS:
                if kw in d.lower():
                    domains[d.lower()] = kw
    except Exception as e:
        print(f"Fallback failed {e}")

date = datetime.now().strftime("%Y-%m-%d")
with open(f"finds/{date}.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["domain","keyword","dr_min","ahrefs","wayback","buy"])
    for dom, kw in list(domains.items())[:100]:
        w.writerow([dom, kw, "30+", f"https://ahrefs.com/backlink-checker?input={dom}", f"https://web.archive.org/web/*/{dom}", f"https://porkbun.com/checkout/search?q={dom}"])

print(f"DONE: {len(domains)} domains saved")
