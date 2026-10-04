# Vireo Audio — Support Tickets (Set B)

## What this builds
A small deterministic Streamlit dashboard plus a batch analysis script for:
- CSAT per agent
- mean and median handle time per agent
- first-response breach rate
- replacement rate
- Tier 1 bottom-ten screening list
- Tier 2 shown separately

No per-ticket LLM/API calls are made at runtime.

## Clean-machine setup

1. Put the Vireo data pack CSVs in `data/`:
   - `tickets.csv`
   - `agents.csv`
   - `orders.csv`
   - `customers.csv`
   - `products.csv`
   (`orders.csv` and `customers.csv` are not required by the dashboard, but are part of the pack.)
2. Create an environment:
   `python -m venv .venv`
3. Activate it.
4. Install:
   `pip install -r requirements.txt`
5. Run batch analysis:
   `python analyze.py --data-dir data --out-dir outputs`
6. Run dashboard:
   `streamlit run app.py`

If the data live elsewhere, set `VIREO_DATA_DIR=/path/to/pack`.

## Metric decisions
- Agent joins use `agent_id`, never display name.
- CSAT blanks are excluded.
- Handle time is first human response to resolution.
- Helpdesk timestamps are treated as IST.
- For `legacy_fd`, resolution timestamps are reconstructed from a UTC legacy event log; the policy says the helpdesk displays IST, so legacy resolution is shifted +05:30 before handle-time calculation.
- First-response targets: chat 15m, voice 2h, social 4h, email 8h.
- Tier 2 is not mixed into the Tier 1 bottom-ten screen.
- Bottom-ten screen uses Tier 1 agents with at least 100 CSAT responses; it is a review list, not an automatic retraining decision.

## Important limitation
The tool does not infer causality from free text. The supplied email says some IVR transcripts are junk, and the policy says Tier 2 work is different. Text is therefore not used to score agents.
