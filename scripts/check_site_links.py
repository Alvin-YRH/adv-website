#!/usr/bin/env python3
"""Internal-link governance check. Run before every push that adds or renames a page.

Every indexable page in sitemap.xml must be:
  1. linked (visible <a href>) from the homepage,
  2. linked from at least 2 other pages,
  3. listed in llms.txt,
  4. registered in scripts/build_llms_full.py,
  5. if it is a Tier-3 content page: linked from /guides AND in the /guides CollectionPage schema.
Exits 1 and prints every gap if anything is missing.
"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://advmarketing.biz"
TIER2 = {"/meta-ads-agency-malaysia", "/google-ads-agency-malaysia", "/seo-agency-kuala-lumpur", "/ai-marketing-automation-malaysia"}
SKIP_GUIDES = {"/", "/about", "/guides"} | TIER2

def file_for(url):
    if url == "/": return ROOT / "index.html"
    for cand in (ROOT / (url.strip("/") + ".html"), ROOT / "statistics_pages" / (url.strip("/") + ".html")):
        if cand.exists(): return cand
    return None

def body_links(html):
    html = re.sub(r"<head>.*?</head>|<script.*?</script>", "", html, flags=re.S)
    out = set()
    for h in re.findall(r'<a [^>]*href="([^"#?]+)', html):
        h = h.replace(BASE, "") or "/"
        h = h.rstrip("/") or "/"
        if h.endswith(".html"): h = h[:-5]
        if h.startswith("/"): out.add(h)
    return out

sitemap = (ROOT / "sitemap.xml").read_text()
urls = [u.replace(BASE, "") or "/" for u in re.findall(r"<loc>([^<]+)</loc>", sitemap)]
links = {u: body_links(f.read_text()) for u in urls if (f := file_for(u))}
llms = (ROOT / "llms.txt").read_text()
builder = (ROOT / "scripts" / "build_llms_full.py").read_text()
guides_html = (ROOT / "guides.html").read_text()
schema_urls = set()
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', guides_html, re.S):
    d = json.loads(b)
    if d.get("@type") == "CollectionPage":
        schema_urls = {x["url"].replace(BASE, "") for x in d.get("hasPart", [])}
gaps = []
for u in urls:
    if u not in links: gaps.append(f"{u}: in sitemap but no matching .html file"); continue
    inbound = [v for v in links if v != u and u in links[v]]
    if u != "/" and u not in links["/"]: gaps.append(f"{u}: not linked from the homepage")
    if u != "/" and len(inbound) < 2: gaps.append(f"{u}: only {len(inbound)} inbound link(s) {inbound}")
    if u not in ("/",) and (BASE + u) not in llms: gaps.append(f"{u}: missing from llms.txt")
    if (BASE + u) not in builder and u != "/": gaps.append(f"{u}: not registered in build_llms_full.py")
    if u not in SKIP_GUIDES:  # Tier-3 content: must be in the /guides directory and its schema
        if u not in links.get("/guides", set()): gaps.append(f"{u}: not linked from /guides")
        if u not in schema_urls: gaps.append(f"{u}: not in /guides CollectionPage schema")
for f in ROOT.glob("*.html"):
    u = "/" + f.stem if f.stem != "index" else "/"
    if u not in urls and "noindex" not in f.read_text()[:3000] and f.stem != "404":
        gaps.append(f"{u}: indexable .html file not in sitemap.xml")
if gaps:
    print("LINK CHECK FAILED:"); [print("  ✗", g) for g in gaps]; sys.exit(1)
print(f"LINK CHECK OK — {len(urls)} pages, every one reachable from home, /guides (Tier 3), llms.txt and llms-full.")
