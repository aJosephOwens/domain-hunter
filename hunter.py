import requests, re, csv, time
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

KEYWORDS_CAD = ["cad","cam","autocad","solidworks","fusion","inventor","revit","sketchup","rhino","cnc","machining","3dprint","drafting","blueprint","engineering","architecture","bim","toolpath","gcode"]
KEYWORDS_AUDIO = ["vst","daw","flstudio","ableton","logic","protools","cubase","midi","beat","instrumental","sample","loop","sound","audio","mixing","mastering","soundtrack","composition","studio","producer","recording","synth"]
ALL_KEYWORDS = KEYWORDS_CAD + KEYWORDS_AUDIO
Path("finds").mkdir(exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537"}
domains = {}

def add_domain(d, kw, src):
    d = d.lower().strip()
    if len(d) < 6 or len(d) > 35: return
    if "." not in d or not d.endswith(".com"): return
    if d in domains: return
    domains[d] = {"kw": kw, "src": src}

print("FACILITY HUNTER - Inclusive Mode")

for page in [1]:
    try:
        url = f"https://www.spamzilla.io/domains/search/?filters%5Bdr_min%5D=30&filters%5Bdomain_extension%5D=com&filters%5Bdomains_type%5D=expired&sort=dr_desc&page={page}"
        proxied = f"https://api.allorigins.win/raw?url={quote(url, safe='')}"
        r = requests.get(proxied, headers=headers, timeout=30)
        if r.status_code == 200:
            found1 = re.findall(r'/domains/view/([a-z0-9-]+\.com)', r.text, re.I)
            found2 = re.findall(r'>([a-z0-9-]+\.com)<', r.text, re.I)
            for d in set(found1 + found2):
                kw_match = next((k for k in ALL_KEYWORDS if k in d.lower()), "broad-dr30")
                add_domain(d, kw_match, "spamzilla-dr30")
            print(f"Spamzilla broad: {len(found1)+len(found2)} raw, {len(domains)} kept")
        time.sleep(1)
    except Exception as e:
        print(f"Spamzilla broad failed: {e}")

for kw in ALL_KEYWORDS[:12]:
    try:
        url = f"https://www.spamzilla.io/domains/search/?filters%5Bsearch_keywords%5D={kw}&filters%5Bdr_min%5D=25&filters%5Bdomain_extension%5D=com&filters%5Bdomains_type%5D=expired&sort=dr_desc"
        proxied = f"https://api.allorigins.win/raw?url={quote(url, safe='')}"
        r = requests.get(proxied, headers=headers, timeout=25)
        found = re.findall(r'>([a-z0-9-]+\.com)<', r.text, re.I)
        for d in found:
            add_domain(d, kw, f"spamzilla-{kw}")
        time.sleep(1)
    except: pass

try:
    url = "https://www.expireddomains.net/domains/expired/com/?o=rpopdsc&r=d"
    proxied = f"https://api.allorigins.win/raw?url={quote(url, safe='')}"
    r = requests.get(proxied, headers=headers, timeout=25)
    found = re.findall(r'/whois/com/([a-z0-9-]+\.com)\.html', r.text, re.I)[:150]
    for d in found:
        kw_match = next((k for k in ALL_KEYWORDS if k in d.lower()), "broad-pop")
        add_domain(d, kw_match, "expireddomains")
    print(f"ExpiredDomains fallback: {len(found)}")
except Exception as e:
    print(f"ExpiredDomains failed: {e}")

if len(domains) < 5:
    print("Sources blocked, using curated facility seed list")
    seed = ["blueprintarchive.com","cnc-tool-library.com","draftingstandards.com","3dprintblueprints.com","beatmakingacademy.com","vstvault.com","mixingmasterclass.com","sounddesignarchive.com","audioproductionhub.com","fusion360tutorials.net"]
    for d in seed:
        add_domain(d, "seed-facility", "seed")

date = datetime.now().strftime("%Y-%m-%d")
out = f"finds/{date}.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["domain","niche_match","dr_filter","source","ahrefs","wayback","buy_link","valuation_floor"])
    for dom, meta in list(domains.items())[:100]:
        niche = "CAD/CAM" if meta['kw'] in KEYWORDS_CAD or "cad" in meta['kw'] else "AUDIO/MUSIC" if meta['kw'] in KEYWORDS_AUDIO else "BROAD-DR30"
        w.writerow([dom, meta['kw'], "DR25+", meta['src'], f"https://ahrefs.com/backlink-checker?input={dom}", f"https://web.archive.org/web/*/{dom}", f"https://porkbun.com/checkout/search?q={dom}", "$500"])

print(f"DONE: Saved {len(domains)} domains to {out}")
