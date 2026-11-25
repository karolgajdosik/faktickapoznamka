import type { APIRoute } from "astro";
import { currentIds } from "../../lib/data";
import { C, frame, png, hallSvg } from "../../lib/og";
export const GET: APIRoute = () => png(frame(`
  <text x="64" y="260" font-size="68" font-weight="800" fill="${C.text}">Kto ako hlasuje</text>
  <text x="64" y="340" font-size="68" font-weight="800" fill="${C.text}">v parlamente</text>
  <text x="64" y="410" font-size="28" font-weight="400" fill="${C.muted}">Hlasovania, poslanci, zákony a rozprava NR SR</text>
  ${hallSvg({ ids: [...currentIds], x: 712, y: 250, w: 440 })}
`));
