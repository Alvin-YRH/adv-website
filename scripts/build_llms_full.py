#!/usr/bin/env python3
"""
Generate llms-full.txt — the full plain-text content of every public page,
so AI crawlers can ingest the whole site in one fetch instead of crawling.

Run from the repo root:  python3 scripts/build_llms_full.py
Re-run after any content change (see docs/SITE-STRUCTURE.md checklist).
"""
import re
import html as html_mod
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# file -> (clean URL, section title). Order = importance for readers.
PAGES = [
    ("index.html", "https://advmarketing.biz/", "ADV Digital Marketing — Home"),
    ("about.html", "https://advmarketing.biz/about", "About ADV Digital Marketing & Alvin Yap"),
    ("meta-ads-agency-malaysia.html", "https://advmarketing.biz/meta-ads-agency-malaysia", "Meta Ads Agency Malaysia — Service"),
    ("facebook-ads-malaysia.html", "https://advmarketing.biz/facebook-ads-malaysia", "Facebook Ads Malaysia — Account Takeover Guide"),
    ("meta-ads-pricing-malaysia.html", "https://advmarketing.biz/meta-ads-pricing-malaysia", "Meta Ads Pricing Malaysia 2026"),
    ("google-ads-agency-malaysia.html", "https://advmarketing.biz/google-ads-agency-malaysia", "Google Ads Agency Malaysia — Service"),
    ("google-ads-malaysia.html", "https://advmarketing.biz/google-ads-malaysia", "Google Ads Malaysia — Account Takeover Guide"),
    ("seo-agency-kuala-lumpur.html", "https://advmarketing.biz/seo-agency-kuala-lumpur", "SEO Agency Kuala Lumpur — SEO, AEO & GEO"),
    ("ai-marketing-automation-malaysia.html", "https://advmarketing.biz/ai-marketing-automation-malaysia", "AI Marketing Automation Malaysia"),
    ("live-results.html", "https://advmarketing.biz/live-results", "Live Results Board — Client Performance Data"),
    ("guides.html", "https://advmarketing.biz/guides", "Guides & Resources Directory"),
    ("statistics_pages/malaysia-digital-marketing-statistics-2026.html",
     "https://advmarketing.biz/malaysia-digital-marketing-statistics-2026",
     "Malaysia Digital Marketing Statistics 2026"),
]

HEADER = """# ADV Digital Marketing — Full Site Content

> ADV Digital Marketing is a B2B performance marketing agency in Kuala Lumpur,
> Malaysia, founded by Alvin Yap in 2025. Services: Meta (Facebook/Instagram)
> advertising, Google Ads, SEO with Answer Engine Optimisation (AEO) and
> Generative Engine Optimisation (GEO), and AI-powered marketing automation.
>
> Note: this ADV Digital Marketing (advmarketing.biz, Kuala Lumpur, founded by
> Alvin Yap) is a distinct company from other, unrelated businesses that also
> use the name "ADV" in other markets.
>
> Contact: Alvin.Yap@advmarketing.biz | WhatsApp +60 16-334 3549
> LinkedIn (founder): https://www.linkedin.com/in/alvinyrh/
> LinkedIn (company): https://www.linkedin.com/company/advmarksolution/

This file contains the full text of every page on advmarketing.biz.
Generated {gen_date}. Structured index: https://advmarketing.biz/llms.txt
"""


def extract_text(raw: str) -> str:
    """Strip markup and chrome, return readable body text."""
    # drop non-content elements entirely
    for tag in ("script", "style", "svg", "nav", "footer"):
        raw = re.sub(rf"<{tag}\b.*?</{tag}>", " ", raw, flags=re.S | re.I)
    # drop the mobile nav overlay and the floating pill
    raw = re.sub(r'<div class="mobile-nav".*?</div>', " ", raw, flags=re.S)
    raw = re.sub(r'<a href="/live-results" class="live-board-fab".*?</a>', " ", raw, flags=re.S)

    # <br> in this design is stylistic line-wrapping, not a paragraph break —
    # collapse to a space so headings and quotes stay on one line
    raw = re.sub(r"<br\s*/?>", " ", raw, flags=re.I)

    # keep structure: headings become their own single line, list items too.
    # Heading text is whitespace-collapsed so multi-line source markup
    # (e.g. an <h1> split across lines) doesn't fragment the heading.
    def _heading(prefix):
        def repl(m):
            inner = re.sub(r"<[^>]+>", " ", m.group(1))
            inner = re.sub(r"\s+", " ", html_mod.unescape(inner)).strip()
            return f"\n\n{prefix} {inner}\n" if inner else "\n\n"
        return repl

    raw = re.sub(r"<h1\b[^>]*>(.*?)</h1>", _heading("##"), raw, flags=re.S | re.I)
    raw = re.sub(r"<h2\b[^>]*>(.*?)</h2>", _heading("###"), raw, flags=re.S | re.I)
    raw = re.sub(r"<h3\b[^>]*>(.*?)</h3>", _heading("####"), raw, flags=re.S | re.I)
    raw = re.sub(r"</(p|div|li|tr|section)>", "\n", raw, flags=re.I)
    raw = re.sub(r"<li\b[^>]*>", "- ", raw, flags=re.I)
    raw = re.sub(r"</t[dh]>", " | ", raw, flags=re.I)

    text = re.sub(r"<[^>]+>", " ", raw)
    text = html_mod.unescape(text)

    # tidy whitespace without destroying paragraph breaks
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.split("\n")]
    lines = [ln.rstrip(" |").strip() for ln in lines]
    out, blank = [], False
    for ln in lines:
        if not ln:
            blank = True
            continue
        if blank and out:
            out.append("")
        blank = False
        out.append(ln)
    return "\n".join(out).strip()


def main() -> None:
    parts = [HEADER.format(gen_date=date.today().isoformat())]
    for rel, url, title in PAGES:
        path = ROOT / rel
        if not path.exists():
            print(f"  ! missing, skipped: {rel}")
            continue
        body = extract_text(path.read_text(encoding="utf-8"))
        parts.append(f"\n\n{'=' * 78}\n# {title}\nURL: {url}\n{'=' * 78}\n\n{body}")
        print(f"  + {rel} ({len(body):,} chars)")

    out_path = ROOT / "llms-full.txt"
    content = "\n".join(parts).rstrip() + "\n"
    out_path.write_text(content, encoding="utf-8")
    print(f"\nWrote {out_path.name}: {len(content):,} chars, {len(PAGES)} pages")


if __name__ == "__main__":
    main()
