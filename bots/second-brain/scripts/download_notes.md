# Hermes pack download (Connector — not this script)

`hermes_soft_final.py` assumes the Hermes v5.5.2 pack is **already local**.

- Drive parent `US_Stock_Data`: `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY`
- Daily folder: `US_Stock_Data/<Mon D>/` (e.g. Nov 5) — must contain at least:
  - `verdicts_US.jsonl` (authoritative)
  - `L2_Input.csv`
  - `Contract_US.csv` (price truth; Date must match folder)
  - Prefer also: `Trigger_US.csv`, `index.md`, `Data_Quality_Report.csv`

Download via **Google Drive MCP / Connector** into e.g. `/workspace/second-brain/YYYY-MM-DD/hermes-<hint>/`, then:

```bash
python3 /workspace/second-brain/scripts/hermes_soft_final.py --pack-dir <that-dir>
```

Do not scrape Drive in-browser for the pack when Connector works.
