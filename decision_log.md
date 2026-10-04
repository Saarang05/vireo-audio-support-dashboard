# Decision Log

- Agent join key: `agent_id`, never name.
- CSAT: mean of nonblank scores only.
- Handle time: first response → resolution.
- Legacy resolution: shift +05:30 because policy says legacy event log is UTC while helpdesk display/export is IST.
- Tier 2: separate population, not mixed with Tier 1.
- Bottom ten: Tier 1, >=100 CSAT responses, sorted by CSAT ascending.
- Bottom ten is a screening list, not a retraining verdict.
- Free text not used for agent scoring because the email warns about failed IVR transcripts.
- No per-ticket model calls.
- Primary business target: 22.3% H1 2026 replacement rate → 15%, with savings calculated using policy replacement cost.
