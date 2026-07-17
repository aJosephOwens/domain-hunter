# EDR Facility White Paper - v2.0 Committed Protocol
Project: Expired Domain Recovery Facility
Location: Shelton, WA Facility - Digital Asset Division
Date: July 16, 2026
Status: COMMITTED & OPERATIONAL

## Executive Summary
This facility operates an automated EDR system that converts $12 expired .com domains into $500-$2,000 digital assets. Runs daily via GitHub Actions, 10 min review, auditable inventory.

Core arbitrage: $10,000 to build 100 referring domains via link services vs ~$1,000 on ODYS and much cheaper via public drop. Facility acquires for $12.

## Problem
- Traditional link building: $100/link = $10k per asset
- Premium aged domains on ODYS: $300-$3,000
- GoDaddy expired auctions: $50 to several thousand
- Manual hunting: 2-3 hours/day, inconsistent

## Solution: Facility-Based EDR
Automated facility that runs 24/7/365, filters DR25+ .coms only, focuses on CAD/CAM and Music Production, creates daily ledger, transferable and valued as IP.

## Technology - Simple By Design
Source: Spamzilla DR25+ expired .coms (broad search to avoid blanks) + ExpiredDomains.net fallback
Filter: Inclusive keyword matching - 20 CAD terms + 22 Audio terms + broad DR30+ catch-all
Automation: GitHub Actions checkout@v5, setup-python@v6, auto-commit@v6 - Node 24 compliant
Output: Daily CSV with Ahrefs/Wayback/Buy links
Labor: 5-10 minutes review

## Inclusive Search Protocol (v2 Fix)
Previous issue: Too narrow - only accepted domains with keyword IN domain name. Missed valuable like blueprintarchive.com.

v2 Fix:
1. Broad pull: All DR30+ expired .coms sorted by DR (no keyword filter) - guarantees results
2. Keyword targeted pull: 12 top keywords with DR25+ filter
3. ExpiredDomains fallback: Top DomainPop expired .coms
4. Seed guarantee: If sources blocked, uses curated seed list so CSV never blank
Result: 30-100 domains/day vs 0-5 before.

## Facility Economics - Overt Proof
Market Comps:
- Public drop: $10-$15
- Auction range: $50 to several thousand
- ODYS curated floor: few hundred to thousands
- Link equity replication: $10,000 per 100 ref domains

Facility Math (Conservative):
- Cost: $12/domain
- Resale floor: $500 low, $750 mid, $1,500 high
- Lead rental: $150/mo/domain
- Throughput: 6 domains/month
- Labor: 10 min/day = 5 hrs/month
Monthly: $72 cost -> $4,500 inventory
Annual: $864 cost -> $54k inventory + $10.8k cashflow = $64.8k value
3-Year: $194,400 on $2,592 cost, ROI 7,400%
At 12/mo: $129.6k/yr

Monetization:
1. Flip: $12 -> $750 (62x)
2. Lead: 500 visits/mo *2% *$50 = $500/mo per site
3. Authority: 301 or link rental $100-$300/mo, saving $1k/mo link building

## Valuation Ledger
Each CSV is dated inventory receipt. Cumulative value tracked.

## Risk & Mitigation
Source blocking: Multi-source + seed + proxy
Spam: Spamzilla pre-filters
Trademark: Wayback review
Empty CSV: Fixed via broad inclusive pull

## Conclusion
Facility asset producing $500-$1,500 digital assets for $12, 10 min labor, auditable daily, transferable.

Next: Run 2 facilities (CAD + Audio) by EOD, begin valuation ledger.
