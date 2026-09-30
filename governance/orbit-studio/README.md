# Orbit Studio directives page

Private read-only view of this archive for `AlexTouvras/Orbit` at `/studio/directives`.

Studio stays owner-only (`isStudioAccessible`, `noindex`). The public site does not list these directives. Editing still happens in this archive. The JSON file is a published snapshot, not a second editor.

## Files to copy onto Orbit

| This path | Orbit path |
| --- | --- |
| `src/app/studio/directives/page.tsx` | `src/app/studio/directives/page.tsx` |
| `src/app/studio/page.tsx` | `src/app/studio/page.tsx` |
| `src/components/studio/DirectiveArchive.tsx` | `src/components/studio/DirectiveArchive.tsx` |
| `src/lib/directives.ts` | `src/lib/directives.ts` |
| `src/lib/directive-types.ts` | `src/lib/directive-types.ts` |
| `data/directive-archive.json` | `data/directive-archive.json` |

`src/app/studio/page.tsx` is the Studio home with a Directives card added. Refresh the snapshot before copying:

```bash
python3 governance/export_studio_snapshot.py --published-at 2026-09-30
```

A local Orbit commit of these files exists as `149120d` on `cursor/studio-directives-5895`. Push to `AlexTouvras/Orbit` was denied for this agent (HTTP 403). The live site does not include `/studio/directives` until someone who can write to that repository pushes the branch.
