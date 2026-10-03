# Grok Bot tools — reference

Harness map when running **baoyu-design** inside **Grok Bot** (Prompt Architect / any Justin assistant). Upstream `system-prompt.md` names capabilities; this doc gives the exact Grok tools.

## Tool map

| Capability | Grok Bot equivalent |
|---|---|
| Ask clarifying questions | `SendToUser` with `type: "widget"` (options + optional `allowCustom` / `multiSelect`). Ends the turn — wait for the user's next message. Prefer widgets over plain-text menus. |
| Show deliverable / screenshot | `SendToUser` with text + `images:[{url:"file://…"}]` for screenshots; attach HTML/PPTX via `type:"attachment"` `url:"file:///…"`. Never markdown `![](...)`. |
| Preview HTML over HTTP | Start `python3 -m http.server 4311 --directory designs` via `Shell` with `block_until_ms: 0`. Open URL with a **computerUse** subagent (`Task` subagent_type `computerUse`). Do **not** rely on `file://` for multi-file prototypes. |
| Screenshots of preview | Read-only `Screenshot` on the box desktop, or have computerUse capture; then attach the `file://` path with `SendToUser`. |
| AI images | Cursor `GenerateImage` via `CallDynamicTool` namespace `cursor` — only when the user asks for an image asset. Prefer [baoyu-infographic](sand-workflow:baoyu-infographic) for finance boards and [visual-director](sand-workflow:visual-director) for general art. |
| Web search / fetch | `CallDynamicTool` `WebSearch` / `WebFetch` (namespace `cursor`) |
| Subagent verify | `Task` with `executor` or `computerUse` — see `agents/fork-verifier-agent.md` |
| File read/write | `Read`, `Shell` (mkdir/cp/write via heredoc). Package root: `/home/box/agent-data/workflows/baoyu-design/` |
| User voice | **Only** `SendToUser`. Plain assistant text is invisible. First action on a user turn: text ack via SendToUser. |

## Output folder

Default: `/workspace/designs/<descriptive-project-name>/` on the box. Ask where to save on first project if ambiguous. Keep all HTML + assets self-contained in that folder. Never scatter in repo root.

## Preview server

```bash
mkdir -p /workspace/designs
python3 -m http.server 4311 --directory /workspace/designs
```

URL pattern: `http://127.0.0.1:4311/<project>/<file>.html`

Reuse one server per session. Delegate browser open/click to **computerUse**; you stay in chat and deliver screenshots + file attachments to Justin.

## PPTX / PDF / video export

Follow `built-in-skills/export-as-pptx-editable.md` (default for decks), `export-as-pptx-screenshots.md` only if pixel-perfect requested, `save-as-pdf.md`, `export-as-video.md`. Run Node agents under `agents/` with `Shell` from the skill directory. Attach the resulting `.pptx` / `.pdf` / `.mp4` with `SendToUser` type attachment.

## When NOT to use this skill

| Need | Use instead |
|------|-------------|
| Finance / HK market KPI infographic image | [baoyu-infographic](sand-workflow:baoyu-infographic) |
| Cream-paper educational sketchnote | [sketchnote-infographic](sand-workflow:sketchnote-infographic) |
| Formal print resume / letter / long PDF via Kami stack | [kami](sand-workflow:kami) |
| Quick 3-look image pitch (poster/avatar) | [visual-director](sand-workflow:visual-director) |

baoyu-design wins for: interactive HTML mockups, slide **decks** (HTML→PPTX), wireframes, landing pages, prototypes, design systems.

## Design-system scripts

`node agents/compile-design-system.mjs`, `check-design-system.mjs`, `build-preview.mjs`, `import-design-system.mjs`, `record-asset.mjs`, `import-figma.mjs` — run from `/home/box/agent-data/workflows/baoyu-design/` with `Shell`. Need Node.js available on the box.
