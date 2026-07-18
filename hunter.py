import requests, re, csv, os, time
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

FACILITY = os.getenv("FACILITY", "daily").lower()
Path("finds").mkdir(exist_ok=True)

KEYWORDS_CAD = ["cad","cam","autocad","solidworks","fusion","inventor","revit","sketchup","rhino","cnc","machining","3dprint","drafting","blueprint","engineering","architecture","bim","toolpath","gcode","manufacturing"]
KEYWORDS_AUDIO = ["vst","daw","flstudio","ableton","logic","protools","cubase","midi","beat","instrumental","sample","loop","sound","audio","mixing","mastering","soundtrack","composition","studio","producer","recording","synth"]

if FACILITY == "cad":
    KEYWORDS = KEYWORDS_CAD
elif FACILITY == "audio":
    KEYWORDS = KEYWORDS_AUDIO
else:
    KEYWORDS = KEYWORDS_CAD + KEYWORDS_AUDIO

SPAM_WORDS = ["seoexpress","seo","pbn","casino","poker","loan","payday","viagra","porn","xxx","cbd","gamble"]

headers = {"User-Agent": "Mozilla/5.0"}
domains = {}

def is_spam(d):
    dl = d.lower()
    for w in SPAM_WORDS:
        if w in dl:
            return True
    return False

def add(d, kw, src, snap=0):
    d=d.lower().strip()
    if len(d)<6 or len(d)>35: return
    if not d.endswith(".com"): return
    if d in domains: return
    if is_spam(d): return
    domains[d]={"kw":kw,"src":src,"snap":snap}

print(f"FACILITY v3 {FACILITY.upper()} inclusive + spam filter")

try:
    url="https://www.spamzilla.io/domains/search/?filters%5Bdr_min%5D=25&filters%5Bdomain_extension%5D=com&filters%5Bdomains_type%5D=expired&sort=dr_desc"
    proxied=f"https://api.allorigins.win/raw?url={quote(url, safe='')}"
    r=requests.get(proxied, headers=headers, timeout=30)
    found=re.findall(r'>([a-z0-9-]+\.com)<', r.text, re.I)
    print(f"Raw {len(found)}")
    for d in found[:120]:
        if FACILITY!= "daily" and not any(k in d.lower() for k in KEYWORDS):
            continue
        if is_spam(d):
            continue
        kw_match = next((k for k in KEYWORDS if k in d.lower()), "broad-dr25")
        add(d, kw_match, "spamzilla")
except Exception as e:
    print(e)

# Wayback quality check
filtered = {}
for dom, meta in domains.items():
    try:
        cdx=f"https://web.archive.org/cdx/search/xmbu?url={dom}&output=json&fl=timestamp&filter=statuscode:200&collapse=timestamp:6&limit=30"
        r=requests.get(cdx, headers=headers, timeout=10)
        if r.status_code==200:
            data=r.json()
            snaps=len(data)-1 if isinstance(data, list) else 0
            if snaps < 3:
                print(f"Reject {dom} only {snaps} snaps")
                continue
            meta["snap"]=snaps
        filtered[dom]=meta
    except:
        filtered[dom]=meta
domains=filtered

if len(domains)<3:
    print("Using clean seed")
    seeds={"daily":["blueprintarchive.com","cnc-tool-library.com","vstvault.com"],"cad":["draftingstandards.com","fusion360tutorials.com","cnc-tool-library.com"],"audio":["beatmakingacademy.com","mixingmasterclass.com","sounddesignarchive.com"]}
    for d in seeds.get(FACILITY, seeds["daily"]):
        add(d,"clean-seed","seed",50)

date=datetime.now().strftime("%Y-%m-%d")
out=f"finds/{FACILITY}-{date}.csv"
with open(out,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["domain","niche_match","source","wayback_snapshots","ahrefs","wayback","buy","floor","notes"])
    for dom,meta in list(domains.items())[:60]:
        note="REAL SITE" if meta.get("snap",0)>=10 else "CHECK"
        if meta.get("snap",0)<5:
            note="LIKELY SPAM"
        w.writerow([dom,meta["kw"],meta["src"],meta.get("snap",""),f"https://ahrefs.com/backlink-checker?input={dom}",f"https://web.archive.org/web/*/{dom}",f"https://porkbun.com/checkout/search?q={dom}","$500",note])
print(f"Saved {len(domains)} to {out}")
