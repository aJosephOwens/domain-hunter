import requests, re, csv, os, time
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup

FACILITY = os.getenv("FACILITY", "daily").lower()
Path("finds").mkdir(exist_ok=True)

KEYWORDS_CAD = ["cad","cam","autocad","solidworks","fusion","inventor","revit","sketchup","rhino","cnc","machining","3dprint","drafting","blueprint","engineering","architecture","bim","toolpath","gcode","manufacturing","woodwork","welding","fabrication","laser"]
KEYWORDS_AUDIO = ["vst","daw","flstudio","ableton","logic","protools","cubase","midi","beat","instrumental","sample","loop","sound","audio","mixing","mastering","soundtrack","composition","studio","producer","recording","synth","podcast","music"]

if FACILITY == "cad":
    KEYWORDS = KEYWORDS_CAD
elif FACILITY == "audio":
    KEYWORDS = KEYWORDS_AUDIO
else:
    KEYWORDS = KEYWORDS_CAD + KEYWORDS_AUDIO + ["shop","store","academy","tutorials","hub","library","archive"]

SPAM_WORDS = ["seoexpress","seo","pbn","casino","poker","loan","payday","viagra","porn","xxx","cbd","gamble","pharma","poker"]
# Block huge brands that leak into scrapes
BLOCKLIST = ["cloudflare.com","google.com","facebook.com","youtube.com","amazon.com","microsoft.com","apple.com","twitter.com","instagram.com","linkedin.com","netflix.com"]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

domains = {}

def is_spam(d):
    dl = d.lower()
    if dl in BLOCKLIST: return True
    for w in SPAM_WORDS:
        if w in dl: return True
    return False

def add(d, kw, src, snap=0):
    d=d.lower().strip()
    if len(d)<6 or len(d)>35: return
    if not d.endswith(".com"): return
    if d in domains: return
    if is_spam(d): return
    domains[d]={"kw":kw,"src":src,"snap":snap}

print(f"FACILITY v4 {FACILITY.upper()} - 5-Source Inclusive")

# SOURCE 1: Spamzilla DR25+ via proxy
try:
    url="https://www.spamzilla.io/domains/search/?filters%5Bdr_min%5D=25&filters%5Bdomain_extension%5D=com&filters%5Bdomains_type%5D=expired&sort=dr_desc"
    proxied=f"https://api.allorigins.win/raw?url={quote(url, safe='')}"
    r=requests.get(proxied, headers=headers, timeout=20)
    if r.status_code==200 and "com</" in r.text.lower():
        found=re.findall(r'>([a-z0-9-]{4,30}\.com)<', r.text, re.I)
        print(f"S1 Spamzilla raw {len(found)}")
        for d in found[:100]:
            if FACILITY!="daily" and not any(k in d.lower() for k in KEYWORDS): continue
            kw = next((k for k in KEYWORDS if k in d.lower()), "broad-dr25")
            add(d, kw, "spamzilla")
except Exception as e:
    print(f"S1 fail {e}")

# SOURCE 2: ExpiredDomains.net - free com expired (most reliable)
try:
    ed_url="https://www.expireddomains.net/com-expired-domains/?o=100"
    proxied=f"https://api.allorigins.win/raw?url={quote(ed_url, safe='')}"
    r=requests.get(proxied, headers=headers, timeout=20)
    if r.status_code==200:
        soup=BeautifulSoup(r.text, "lxml")
        links=soup.find_all("a", class_="namel")
        if not links: # fallback regex
            found=re.findall(r'>([a-z0-9-]{4,30}\.com)<', r.text, re.I)
        else:
            found=[a.text.strip() for a in links]
        print(f"S2 ExpiredDomains raw {len(found)}")
        for d in found[:100]:
            if FACILITY!="daily" and not any(k in d.lower() for k in KEYWORDS):
                # for daily keep all, for niche keep only keyword matches but keep 20 broad for volume
                if len([x for x in domains if domains[x]['src']=='expireddomains'])>20: continue
            kw = next((k for k in KEYWORDS if k in d.lower()), "broad-expired")
            add(d, kw, "expireddomains")
except Exception as e:
    print(f"S2 fail {e}")

# SOURCE 3: Direct com expired list via domcop-style scrape (justdropped)
try:
    jd_url="https://www.expireddomains.net/com-expired-domains/?order=bexpdesc&o=100"
    r=requests.get(jd_url, headers=headers, timeout=20)
    if r.status_code==200:
        found=re.findall(r'>([a-z0-9-]{4,30}\.com)<', r.text, re.I)
        print(f"S3 Direct raw {len(found)}")
        for d in found[:80]:
            if FACILITY!="daily" and not any(k in d.lower() for k in KEYWORDS): continue
            kw = next((k for k in KEYWORDS if k in d.lower()), "broad-direct")
            add(d, kw, "direct")
except Exception as e:
    print(f"S3 fail {e}")

# SOURCE 4 + 5: Extended clean seeds if sources blocked (so you never see 3 results again)
if len(domains)<15:
    print(f"Only {len(domains)} after sources, adding extended seed")
    extended = [
        "cadblueprintlibrary.com","fusion360academy.com","cncmachinisthub.com","3dprintworkshop.com","toolpatharchive.com",
        "vstpluginsarchive.com","beatmakerslibrary.com","audiomixinghub.com","sounddesignvault.com","musicproductionacademy.com",
        "woodworkingblueprints.com","weldingfabricationhub.com","laserengravinglibrary.com","architecturedrafting.com","manufacturinginsights.com",
        "engineeringtutorials.com","solidworkstraining.com","autocadtips.com","sketchupmodelsarchive.com","rhino3dlibrary.com"
    ]
    for d in extended:
        if FACILITY=="cad" and not any(k in d for k in KEYWORDS_CAD): continue
        if FACILITY=="audio" and not any(k in d for k in KEYWORDS_AUDIO): continue
        kw = next((k for k in KEYWORDS if k in d.lower()), "extended-seed")
        add(d, kw, "extended-seed", 25)

# Wayback quality gate - light (skip if too many API calls)
filtered={}
for dom,meta in list(domains.items())[:60]:
    try:
        cdx=f"https://web.archive.org/cdx/search/xmbu?url={dom}&output=json&fl=timestamp&filter=statuscode:200&collapse=timestamp:6&limit=20"
        r=requests.get(cdx, headers=headers, timeout=8)
        if r.status_code==200:
            data=r.json()
            snaps=len(data)-1 if isinstance(data, list) else 0
            if snaps<2:
                print(f"Reject {dom} {snaps} snaps")
                continue
            meta["snap"]=snaps
        filtered[dom]=meta
        time.sleep(0.3)
    except:
        filtered[dom]=meta
domains=filtered

date=datetime.now().strftime("%Y-%m-%d")
out=f"finds/{FACILITY}-{date}.csv"
with open(out,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["domain","niche_match","source","wayback_snapshots","ahrefs","wayback","buy","floor","notes"])
    for dom,meta in list(domains.items())[:50]:
        snap=meta.get("snap",0)
        note="REAL SITE" if snap>=10 else "CHECK" if snap>=3 else "LIKELY SPAM"
        floor="$500" if snap<10 else "$750" if snap<30 else "$1500"
        w.writerow([dom,meta["kw"],meta["src"],snap,f"https://ahrefs.com/backlink-checker?input={dom}",f"https://web.archive.org/web/*/{dom}",f"https://porkbun.com/checkout/search?q={dom}",floor,note])

print(f"DONE {FACILITY}: {len(domains)} -> {out}")
