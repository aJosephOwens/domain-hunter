import requests, csv, re, os, time
from datetime import datetime
from pathlib import Path
KEYWORDS = ["cad","cam","autocad","solidworks","fusion360","drafting","vst","flstudio","ableton","beat","midi","daw","mastercam","autodesk"]
Path("finds").mkdir(exist_ok=True)
headers = {"User-Agent":"Mozilla/5.0"}
print("Fetching expired domains...")
try:
    r = requests.get("https://www.expireddomains.net/domains/expired/com/", headers=headers, timeout=30)
    domains = re.findall(r'/whois/com/([^"]+)\.html', r.text)
    relevant = [d for d in domains if any(k in d.lower() for k in KEYWORDS)][:75]
except Exception as e:
    print(f"Fetch failed: {e}")
    relevant = []

date = datetime.now().strftime("%Y-%m-%d")
out_path = f"finds/{date}.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["domain","ahrefs_check","wayback_check","buy_link"])
    for dom in relevant:
        w.writerow([dom, f"https://ahrefs.com/backlink-checker?input={dom}", f"https://web.archive.org/web/*/{dom}", f"https://porkbun.com/checkout/search?q={dom}"])
print(f"Saved {len(relevant)} domains to {out_path}")
