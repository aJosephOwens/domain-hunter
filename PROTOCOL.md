# EDR Facility Protocol - Committed v2.0 Inclusive
Status: COMMITTED Date: 2026-07-16

Mission: Produce $500-$2,000 digital assets for $12 via automated expired domain recovery.

Daily Protocol (10 Minutes):
1. Facility Runs Itself (0 min - Automated)
When: 7am PT daily + on-demand via Actions > Run workflow
What: Pulls ALL DR25+ expired .coms (broad) + keyword targeted CAD/Audio + ExpiredDomains fallback
Guarantee: CSV never blank
Output: finds/YYYY-MM-DD.csv

2. Human Review (5 min)
Open CSV top 10: Ahrefs Ref Domains >50? Wayback real site 2+ years in CAD/Music? If YES x2 -> BUY

3. Acquisition & Ledger (5 min)
Buy via Buy Link ($12), Add to valuation_ledger.csv: Domain, DR, Cost $12, Floor $500, Niche

Inclusive Search Terms v2 Broad:
CAD/CAM: cad, cam, autocad, solidworks, fusion, inventor, revit, sketchup, rhino, cnc, machining, 3dprint, drafting, blueprint, engineering, architecture, bim, toolpath, gcode, manufacturing
Audio: vst, daw, flstudio, ableton, logic, protools, cubase, midi, beat, instrumental, sample, loop, sound, audio, mixing, mastering, soundtrack, composition, studio, producer, recording, synth
Broad Catch-All: Any DR30+ .com expired - reviewed regardless of name

Facility Value Math:
6/mo @ $12 = $72/mo cost, 6/mo @ $750 floor = $4,500/mo inventory, Annual = $54k inventory + $10.8k cashflow = $64.8k value, 12/mo = $129.6k/yr

Systems Check:
Actions green check = operational, CSV has 20-100 rows = inclusive working, Node warning = Update to v5/v6 already in files

Multiple Facilities by EOD:
Facility 1: hunt.yml (all niches), Facility 2: hunt-cad.yml (CAD only 8am), Facility 3: hunt-audio.yml (Audio only 9am)
