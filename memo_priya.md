# Memo to Priya Raman — Vireo Audio Support

## Executive summary

The data support a targeted intervention, but not a blind “bottom ten = retrain” rule.

**Business goal:** reduce the H1 2026 replacement issuance rate from **22.3% to 15%**. At roughly **650 tickets/week**, that is about **613 fewer replacements per quarter**. Using the H1 2026 average planning cost of **Rs 1,806 per replacement** (unit cost + Rs 340 logistics), the direct planning-cost opportunity is about **Rs 1,107,093 per quarter**, if ticket mix stays similar.

CSAT also deteriorated: the average was **3.47 in 2025** versus **3.16 in H1 2026**.

## What the dashboard shows

The Tier 1 bottom-ten screening list is based on CSAT, with at least 100 survey responses, and shows handle time and team context beside it. The ten names/IDs should be treated as **review flags**, not a retraining verdict.

Four of the lowest-CSAT Tier 1 agents are in Chat Frontline and sit roughly **0.44–0.50 CSAT points below their team average**. Logistics and Returns Desk are also represented, but those teams have materially different work patterns. Tier 2 is shown separately because the operating policy says Tier 2 cases are multi-touch and should not be compared with Tier 1 on volume metrics; the email thread also warns that hardware triage receives angrier customers by design.

## Recommended action

Use the dashboard to select a small review cohort, then inspect representative tickets before spending the training budget. Start with the strongest agent-level outliers rather than treating the raw bottom ten as causally responsible.

Track two outcomes over the next quarter:
1. replacement issuance rate, with a 15% target;
2. CSAT, while monitoring survey response rate and queue mix.

## Data quality checks

- 11,750 tickets and 44 agent IDs loaded; all ticket agent IDs matched the roster.
- CSAT response rate is **44.2%**, consistent with the policy's statement that around 45% respond.
- 2,309 legacy tickets initially produced negative handle times if resolution timestamps were treated as IST. The policy says legacy resolution timestamps came from UTC event logs, so they were shifted +05:30; after that, **0 negative handle times** remained.
- A 500-ticket independent recomputation produced **0 handle-time discrepancies**.
- Six tickets contain both a refund and a replacement, which the policy says must not happen; these are surfaced separately.

## What I did not use

I did not use the free-text fields to score agents. The email thread says roughly 40 customer messages contain failed IVR junk, and a text classifier would add cost and another error source without being necessary for the requested dashboard.

I also did not treat the email's approximate “30% volume / 100% replacement” statements as the measurement basis. The supplied data are the source of truth for the dashboard.
