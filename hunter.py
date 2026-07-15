import requests, csv, re, os, time
from datetime import datetime
from pathlib import Path

KEYWORDS = ["cad","cam","autocad","solidworks","fusion360","fusion","drafting","autodesk","mastercam","vst","flstudio","ableton","logicpro","protools","beat","midi","splice","soundtrack","daw"]

# Setup
Path("finds").mkdir(exist_ok=True)
found = []

print("Fetching expired.com list...")
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
try:
    # This page is public for first 100 without login
    r = requests.get("https://www.expireddomains.net/domains/expired/com/", headers=headers, timeout=30)
    domains = re.findall(r'/whois/com/([^"]+)\.html', r.text)
    print(f"Found {len(domains)} expired domains to filter")
    # Filter for your niche first to save time
    relevant = [d for d in domains if any(k in d.lower() for k in KEYWORDS)]
    print(f"{len(relevant)} match your CAD/music keywords: {relevant[:10]}")

    # Check each relevant with free openpagerank if key exists, else just list them
    opr_key = os.getenv("OPENPAGERANK_KEY")
    for domain in relevant[:50]: # limit to 50 per run to avoid timeouts
        print(f" -> {domain}")
        if opr_key:
            try:
                resp = requests.get(f"https://openpagerank.io/api/v1.0/getDomainRank?domains%5B%5D={domain}",
                                     headers={"API-OPR": opr_key}, timeout=10).json()
                rank = resp.get("response",[{}])[0].get("page_rank_rk",0)
                print(f" OPR rank: {rank}")
                if rank >= 4.0: # ~DR40+
                    found.append((domain, rank))
            except Exception as e:
                print(f" error {e}")
                found.append((domain, 0))
        else:
            found.append((domain, 0))
        time.sleep(1)

except Exception as e:
    print(f"Fetch failed, using fallback: {e}")
    # Fallback if expireddomains blocks
    found = [("example-cad-resource.com",0)]

# Save with clickable vet links
date = datetime.now().strftime("%Y-%m-%d")
out_path = f"finds/{date}.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["domain","opr_rank","ahrefs_check","wayback_check","buy_link"])
    for dom, rank in found:
        w.writerow([
            dom, rank,
            f"https://ahrefs.com/backlink-checker?input={dom}&mode=domain",
            f"https://web.archive.org/web/*/{dom}",
            f"https://porkbun.com/checkout/search?q={dom}"
        ])

print(f"DONE. Saved {len(found)} domains to {out_path}")
