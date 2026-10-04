
import os
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Vireo Audio Support Dashboard", layout="wide")

DATA_DIR = Path(os.environ.get("VIREO_DATA_DIR", "data"))

@st.cache_data
def load_data(data_dir: str):
    d = Path(data_dir)
    tickets = pd.read_csv(d / "tickets.csv")
    agents = pd.read_csv(d / "agents.csv")
    products = pd.read_csv(d / "products.csv")
    for c in ["created_at", "first_response_at", "resolved_at"]:
        tickets[c] = pd.to_datetime(tickets[c], errors="coerce")

    # Policy v3.2: helpdesk timestamps are IST; legacy resolution timestamps were
    # reconstructed from a UTC legacy event log. Convert legacy resolution to IST.
    legacy = tickets["source_system"].eq("legacy_fd")
    tickets["resolved_at_ist"] = tickets["resolved_at"]
    tickets.loc[legacy, "resolved_at_ist"] = tickets.loc[legacy, "resolved_at"] + pd.Timedelta(hours=5, minutes=30)
    tickets["handle_h"] = (tickets["resolved_at_ist"] - tickets["first_response_at"]).dt.total_seconds() / 3600

    targets = {"chat": 15, "voice": 120, "social": 240, "email": 480}
    tickets["target_min"] = tickets["channel"].map(targets)
    tickets["breach"] = tickets["first_response_at"] > (
        tickets["created_at"] + pd.to_timedelta(tickets["target_min"], unit="m")
    )
    tickets["attendance"] = tickets["status"].isin(["resolved", "closed"])

    a = tickets.groupby("agent_id").agg(
        tickets=("ticket_id", "size"),
        csat_responses=("csat_score", lambda x: x.notna().sum()),
        csat=("csat_score", "mean"),
        mean_handle_h=("handle_h", "mean"),
        median_handle_h=("handle_h", "median"),
        breaches=("breach", "sum"),
        replacements=("replacement_issued", lambda x: (x == "Y").sum()),
    ).reset_index()
    a["csat_response_rate"] = a["csat_responses"] / a["tickets"]
    a["breach_rate"] = a["breaches"] / a["tickets"]
    a["replacement_rate"] = a["replacements"] / a["tickets"]
    a = a.merge(agents[["agent_id", "name", "site", "team", "shift", "tier"]], on="agent_id", how="left")
    team = a.groupby("team").agg(team_csat=("csat", "mean"), team_handle_h=("mean_handle_h", "mean")).reset_index()
    a = a.merge(team, on="team", how="left")
    a["csat_delta_vs_team"] = a["csat"] - a["team_csat"]
    return tickets, a

st.title("Vireo Audio — Support Tickets")
st.caption("Deterministic dashboard; no per-ticket model/API calls. Agent IDs are the join key.")

try:
    tickets, agents = load_data(str(DATA_DIR))
except Exception as e:
    st.error(f"Could not load the data pack from {DATA_DIR.resolve()}. Put the CSV files in data/ or set VIREO_DATA_DIR.")
    st.exception(e)
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Tickets", f"{len(tickets):,}")
c2.metric("CSAT", f"{tickets.csat_score.mean():.2f}")
c3.metric("CSAT response", f"{tickets.csat_score.notna().mean():.1%}")
h1_2026 = tickets[tickets.created_at.between("2026-01-01", "2026-06-30 23:59:59")]; c4.metric("H1 2026 replacement rate", f"{h1_2026.replacement_issued.eq('Y').mean():.1%}")

st.info("Bottom-ten is a screening list: Tier 2 is shown separately, because the policy says Tier 2 is not to be compared with Tier 1 on volume metrics, and the operations email warns that its queue is deliberately harder.")

tier_choice = st.radio("Comparison population", ["Tier 1", "Tier 2"], horizontal=True)
min_responses = st.number_input("Minimum CSAT responses for agent flagging", min_value=1, value=100, step=10)

view = agents[agents.tier.eq(1 if tier_choice == "Tier 1" else 2)].copy()
flagged = view[view.csat_responses >= min_responses].sort_values("csat").copy()

st.subheader(f"{tier_choice}: agent metrics")
cols = ["agent_id", "name", "team", "tickets", "csat_responses", "csat",
        "mean_handle_h", "median_handle_h", "breach_rate", "replacement_rate",
        "csat_delta_vs_team"]
st.dataframe(
    flagged[cols].style.format({
        "csat": "{:.2f}", "mean_handle_h": "{:.1f}", "median_handle_h": "{:.1f}",
        "breach_rate": "{:.1%}", "replacement_rate": "{:.1%}", "csat_delta_vs_team": "{:+.2f}"
    }),
    use_container_width=True, hide_index=True
)

if tier_choice == "Tier 1":
    st.subheader("Bottom 10 screening flags")
    st.dataframe(
        flagged.head(10)[cols].style.format({
            "csat": "{:.2f}", "mean_handle_h": "{:.1f}", "median_handle_h": "{:.1f}",
            "breach_rate": "{:.1%}", "replacement_rate": "{:.1%}", "csat_delta_vs_team": "{:+.2f}"
        }),
        use_container_width=True, hide_index=True
    )

st.subheader("Trend")
monthly = tickets.assign(month=tickets.created_at.dt.to_period("M").astype(str)).groupby("month").agg(
    tickets=("ticket_id", "size"),
    csat=("csat_score", "mean"),
    replacement_rate=("replacement_issued", lambda x: (x == "Y").mean()),
    breach_rate=("breach", "mean"),
).reset_index()
st.line_chart(monthly.set_index("month")[["csat"]])
st.line_chart(monthly.set_index("month")[["replacement_rate", "breach_rate"]])

st.caption("Handle time = first human response to resolution. Blank CSAT is excluded. Legacy resolution timestamps are shifted +5:30 to align with the helpdesk's IST display.")
