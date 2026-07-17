# EDR Facility - Committed v2.0
Facility: Automated DR30+ expired .com acquisition
Protocol: See PROTOCOL.md
White Paper: See WHITEPAPER.md

Run at Will: Actions -> Daily DR40 Hunter -> Run workflow
Daily Output: finds/YYYY-MM-DD.csv - 20-100 DR25+ domains inclusive

Fix Blank CSV: v2 uses broad inclusive search: pulls ALL DR30+ expired .coms + keyword targeted + fallback. Never blank.

Fix Node 20 Warning: This version uses checkout@v5, setup-python@v6, auto-commit@v6 (Node 24 compliant). Commit these files.

Multiple Facilities:
- hunt.yml = All niches (7am)
- hunt-cad.yml = CAD/CAM only (8am)
- hunt-audio.yml = Audio only (9am)
