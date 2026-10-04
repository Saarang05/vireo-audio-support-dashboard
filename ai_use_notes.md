# AI use notes

The submitted analysis was developed interactively with ChatGPT.

Useful tasks:
- converting the client brief into explicit metric/QA decisions;
- identifying the legacy UTC/IST timestamp issue;
- checking queue/Tier 2 confounding;
- drafting the memo and submission language;
- iterating the local Streamlit/pandas implementation.

Deliberately not used at runtime:
- per-ticket LLM classification;
- free-text sentiment scoring;
- a single opaque agent-performance score.

Reason: the core dashboard can be deterministic, cheaper, and easier to audit.
