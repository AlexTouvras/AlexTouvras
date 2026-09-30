# Weekly Write draft reference

## `data/weekly-write-draft.json`

```json
{
  "id": "ww-YYYY-MM-DD-ide",
  "status": "pending",
  "createdAt": "<ISO-8601>",
  "weekOf": "YYYY-MM-DD",
  "slug": "kebab-case-title",
  "title": "Essay title",
  "summary": "One sentence.",
  "category": "Delivery",
  "tags": ["Delivery", "Learning"],
  "mdx": "---\ntitle: \"...\"\nsummary: \"...\"\ndate: \"YYYY-MM-DD\"\ncategory: \"Delivery\"\nfeatured: false\ntags: [\"...\"]\n---\n\n## The question\n\n...",
  "preview": "Title\n\nSummary\n\nInspired by: <primary signal title>",
  "intake": {},
  "source": "ide"
}
```

- `category`: one of `Career` | `Data` | `AI` | `Delivery` | `Learning`. Match the **decision rule**, not the tool stack. Prefer rotation; do not default to `Data`/`AI` Power BI.
- `intake`: copy verbatim from `data/weekly-write-ide-brief.json`.
- `mdx.date`: usually `weekOf`.
- Prefer `featured: false` for weekly drafts (hub featured is curated separately).

## CLI

| Command | Purpose |
|---------|---------|
| `npm run weekly:draft` | Intake + generate (may write IDE brief if Gemini fails) |
| `npm run weekly:notify` | Generate + Slack (or IDE brief) |
| `npm run weekly:notify-draft` | Slack an existing pending local draft (persists to GitHub default branch when `GITHUB_TOKEN` is set; Slack includes the full essay body) |
| `npm run weekly:notify -- --force` | Replace pending draft |

## Essay skeleton (Orbit)

```mdx
## The question
…

## What the signal is really saying
… (link primary; define jargon once)

## What people get wrong
…

## … (1–3 more sections: Delivery / Learning / Career / general data / AI as the thesis requires)

## Takeaway
…
```

Adjust section titles to the thesis; keep `## The question` first. Gloss workshop nicknames. Pass the stranger test in `docs/essay-voice.md`.

## After Approve

Slack **Approve & publish** → confirm POST → GitHub commit of MDX → Vercel redeploy. Agent does not need to push unless the user asks.
