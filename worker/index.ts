/// <reference types="@cloudflare/workers-types" />
// Static assets are served directly by Cloudflare (free, not counted as Worker
// requests). This Worker only runs for paths with no matching file.
interface Env { ASSETS: Fetcher }

export default {
  async fetch(req: Request, env: Env) {
    const url = new URL(req.url);
    if (url.hostname.startsWith("www.")) {
      url.hostname = url.hostname.slice(4);
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(req);
  },
} satisfies ExportedHandler<Env>;
