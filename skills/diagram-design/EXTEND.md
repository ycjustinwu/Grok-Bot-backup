# EXTEND — Justin / Grok Bot defaults for diagram-design

## When to use
Editorial HTML/SVG diagrams: process, timeline, quadrant, swimlane, sankey, pyramid, org, journey, loop.
Prefer this over Mermaid ASCII for anything Justin will show someone.

## Prefer other skills instead
- Dense finance KPI / market-brief image boards → baoyu-infographic
- Slide decks / UI mockups / PPTX export → baoyu-design
- Formal print parchment PDF → kami

## Justin-relevant types (default lean)
flowchart, process, timeline, swimlane, quadrant, pyramid/funnel, sankey, tree, org chart, layers, venn, loop/flywheel, journey, kanban, radar, bar, line, gantt, scatter, high-level

## Deprioritize unless asked
UML class, database schema, deployment, medallion, DP security matrix, ER (coding-heavy)

## Grok delivery
- Save under `/workspace/diagrams/<slug>/` as self-contained HTML
- Preview: `python3 -m http.server` + computerUse, or attach HTML; Screenshot for chat
- Ask style-guide gate via SendToUser widget on first project diagram
- Language: match request (繁體中文 labels OK when source is Chinese)
