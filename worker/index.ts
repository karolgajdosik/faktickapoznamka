/// <reference types="@cloudflare/workers-types" />
// Static assets are served directly by Cloudflare (free, not counted). The Worker
// only runs for /api/* and for paths with no matching file.
//
// /api/updates — WebSocket used for the "new content" notice. Every `wrangler deploy`
// restarts the Durable Object, which closes all sockets; browsers reconnect, receive
// the new /version.json and show the reload notice. No polling, no shared secret.
import { DurableObject } from "cloudflare:workers";

interface Env { ASSETS: Fetcher; UPDATES: DurableObjectNamespace<Updates> }

export class Updates extends DurableObject<Env> {
  async fetch(req: Request) {
    const pair = new WebSocketPair();
    this.ctx.acceptWebSocket(pair[1]); // hibernation: idle sockets cost nothing
    const v = await this.env.ASSETS.fetch(new Request(new URL("/version.json", req.url))).then((r) => r.text()).catch(() => "{}");
    pair[1].send(v);
    return new Response(null, { status: 101, webSocket: pair[0] });
  }
  async webSocketMessage(ws: WebSocket, msg: string | ArrayBuffer) { if (msg === "ping") ws.send("pong"); }
  async webSocketClose(ws: WebSocket, code: number) { try { ws.close(code); } catch {} }
}

export default {
  async fetch(req: Request, env: Env) {
    const url = new URL(req.url);
    if (url.hostname.startsWith("www.")) {
      url.hostname = url.hostname.slice(4);
      return Response.redirect(url.toString(), 301);
    }
    if (url.pathname === "/api/updates") {
      if (req.headers.get("Upgrade") !== "websocket") return new Response("Expected WebSocket", { status: 426 });
      return env.UPDATES.get(env.UPDATES.idFromName("global")).fetch(req);
    }
    return env.ASSETS.fetch(req);
  },
} satisfies ExportedHandler<Env>;
