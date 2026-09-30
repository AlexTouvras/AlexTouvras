# Architecture

## Storytelling robot

`robot.js` is viewport chrome. It is not part of the decision card. The same module is inlined at the bottom of `index.html`, because Orbit publishes only that file to `https://alextouvras.com/field-card/` (`public/field-card/index.html`). A separate `robot.js` request 404s there.

On each visit it resolves `AlexTouvras/storytelling` `main`, then loads that commit together:

| Piece | Source in storytelling |
|---|---|
| `robot.riv` | `src/illustrations/robot.riv` |
| Artboard, size, view-model keys | `export const ROBOT` in `src/illustrations/robot.ts` |
| Bubble line, tuck hit box, reduced-motion settle | `src/components/director/AiFieldCard.tsx` |
| Rive canvas runtime + wasm | `@rive-app/canvas` in `package.json`, from jsDelivr |

The canvas does not take clicks, so the card's links keep working. A button over the character fires the file's poke trigger. `presence` from the view model moves that button between the open pose and the tucked corner.

When the page is inside an iframe (the story at `/stories/ai-card` already overlays the same robot), the script does not mount a second one. Print hides it.

`scripts/check-robot.mjs` reads that commit and fails if the contract or host file can no longer be parsed. The page falls back to the last known contract only when a fetch fails.

No `robot.riv` is stored in this repo.
