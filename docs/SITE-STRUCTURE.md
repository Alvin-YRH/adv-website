# ADV Website — Site & Link Structure

The rules for how pages connect. Any new page must slot into this structure —
no page ships without its tier assignment and the full checklist below.

## The three tiers

```
Tier 1 — NAV (sitewide, every page's header + footer)
  /                      Home
  (Services dropdown)    → the 4 Tier-2 service pages
  /live-results          Results
  /guides                Guides   ← the gateway to all Tier-3 content
  /about                 About

Tier 2 — SERVICES (money pages; in nav dropdown + homepage cards)
  /meta-ads-agency-malaysia
  /google-ads-agency-malaysia
  /seo-agency-kuala-lumpur
  /ai-marketing-automation-malaysia

Tier 3 — CONTENT (guides, data, proof; listed on /guides)
  /facebook-ads-malaysia               (guide → supports Meta service)
  /google-ads-malaysia                 (guide → supports Google service)
  /meta-ads-pricing-malaysia           (pricing → supports Meta service)
  /live-results                        (proof; also Tier 1 via nav)
  /malaysia-digital-marketing-statistics-2026  (research asset)
```

## Linking rules

1. **No orphans.** Every page must be reachable by at least 2 visible,
   clickable links from other pages (schema/sitemap references don't count).
2. **Tier 3 pages always appear on /guides** in the right category section
   (Facebook Ads / Google Ads / Data & Transparency — add a category if
   genuinely new).
3. **Tier 3 pages carry the back-bar** `← All guides & resources` → /guides.
   Tier 2 service pages keep `← Back to all services` → /.
4. **Guides link to their parent service page and vice versa** (e.g.
   facebook guide ↔ meta-ads service page).
5. **Every page links to /live-results** via the nav Results item + the
   floating pill (bottom-right; pill is on every page except /live-results).
6. **The homepage links Tier 3 only via nav + the results-section line** —
   don't stack content links on the homepage body.

## New-page checklist (all mandatory)

- [ ] Tier assigned; linked per the rules above (min. 2 visible inbound links)
- [ ] Clean URL added to `_redirects` (`/slug /slug.html 200`)
- [ ] `sitemap.xml` entry (weekly changefreq only if genuinely updated weekly)
- [ ] `llms.txt` entry with one-line description
- [ ] `/guides` category card/link if Tier 3
- [ ] Title ≤60 chars, meta description ≤155 chars, canonical, hreflang trio
- [ ] Schema: WebPage + Breadcrumb + Person minimum; Article + HowTo/FAQ
      as appropriate; all `@id` cross-referenced to `#organization` / `#alvin-yap`
- [ ] All JSON-LD parsed as valid JSON before deploy
- [ ] Geo meta tags (MY-14 / Kuala Lumpur block)
- [ ] Floating Live Results pill included (unless the page IS /live-results)
- [ ] WhatsApp links present → `generate_lead` gtag handler included
- [ ] No client brand names in anonymised performance content
- [ ] After deploy: verify 200, then request indexing in GSC

## Audit command

Run from repo root to check the inbound-link graph (flags orphans):
see the audit script pattern in git history (commit "Fix link structure"),
or ask Claude to re-run the link audit.
