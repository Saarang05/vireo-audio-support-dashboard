
import argparse
from pathlib import Path
import pandas as pd
import json

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", default="data")
    p.add_argument("--out-dir", default="outputs")
    args = p.parse_args()
    d, o = Path(args.data_dir), Path(args.out_dir)
    o.mkdir(parents=True, exist_ok=True)

    tickets = pd.read_csv(d / "tickets.csv")
    agents = pd.read_csv(d / "agents.csv")
    products = pd.read_csv(d / "products.csv")
    for c in ["created_at", "first_response_at", "resolved_at"]:
        tickets[c] = pd.to_datetime(tickets[c], errors="coerce")

    legacy = tickets["source_system"].eq("legacy_fd")
    tickets["resolved_at_ist"] = tickets["resolved_at"]
    tickets.loc[legacy, "resolved_at_ist"] = tickets.loc[legacy, "resolved_at"] + pd.Timedelta(hours=5, minutes=30)
    tickets["handle_h"] = (tickets["resolved_at_ist"] - tickets["first_response_at"]).dt.total_seconds() / 3600

    targets = {"chat": 15, "voice": 120, "social": 240, "email": 480}
    tickets["target_min"] = tickets["channel"].map(targets)
    tickets["breach"] = tickets["first_response_at"] > tickets["created_at"] + pd.to_timedelta(tickets["target_min"], unit="m")

    a = tickets.groupby("agent_id").agg(
        tickets=("ticket_id", "size"),
        attendance=("status", lambda x: x.isin(["resolved", "closed"]).sum()),
        csat_responses=("csat_score", lambda x: x.notna().sum()),
        csat=("csat_score", "mean"),
        handle_n=("handle_h", lambda x: x.notna().sum()),
        mean_handle_h=("handle_h", "mean"),
        median_handle_h=("handle_h", "median"),
        breaches=("breach", "sum"),
        replacements=("replacement_issued", lambda x: (x == "Y").sum()),
    ).reset_index()
    a["csat_response_rate"] = a.csat_responses / a.tickets
    a["breach_rate"] = a.breaches / a.tickets
    a["replacement_rate"] = a.replacements / a.tickets
    a = a.merge(agents[["agent_id", "name", "site", "team", "shift", "tier"]], on="agent_id", how="left")
    team = a.groupby("team").agg(team_csat=("csat", "mean"), team_handle_h=("mean_handle_h", "mean")).reset_index()
    a = a.merge(team, on="team", how="left")
    a["csat_delta_vs_team"] = a.csat - a.team_csat
    a["handle_delta_vs_team_h"] = a.mean_handle_h - a.team_handle_h

    a.to_csv(o / "agent_dashboard.csv", index=False)
    bottom = a[(a.tier == 1) & (a.csat_responses >= 100)].sort_values(["csat", "csat_responses"], ascending=[True, False]).head(10)
    bottom.to_csv(o / "bottom10_tier1.csv", index=False)

    print("Wrote agent_dashboard.csv and bottom10_tier1.csv")
    print(bottom[["agent_id","name","team","csat_responses","csat","mean_handle_h"]].to_string(index=False))

if __name__ == "__main__":
    main()
