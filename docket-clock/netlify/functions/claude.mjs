// Server-side relay for the AI features on the hosted site.
// The OpenRouter key lives only in the Netlify environment variable OPENROUTER_API_KEY; it never reaches the browser.
// Set a credit limit on that key at openrouter.ai: it is the real cap on what this endpoint can spend.

const OR_URL = "https://openrouter.ai/api/v1/chat/completions";
const MODEL = "anthropic/claude-sonnet-5.5"; // fixed here, so callers can't pick a pricier model
const MAX_PROMPT = 20000;                    // characters; the page sends at most ~17k
const MAX_TOKENS = 2000;
const PER_MINUTE = 6;                        // per visitor IP, per function instance (best effort)

const hits = new Map();
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });

function limited(ip){
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter(t => now - t < 60000);
  recent.push(now); hits.set(ip, recent);
  if (hits.size > 5000) hits.clear();
  return recent.length > PER_MINUTE;
}

export default async (req, context) => {
  const env = (name) => globalThis.Netlify?.env.get(name) ?? process.env[name];
  // GET lets the page check whether the relay is set up
  if (req.method === "GET") return json({ ok: !!env("OPENROUTER_API_KEY") });
  if (req.method !== "POST") return json({ error: "bad_request" }, 405);

  // only the site itself may call this (blocks other websites; the credit limit covers everything else)
  const site = env("URL"), origin = req.headers.get("origin");
  if (site && origin && origin !== site && origin !== env("DEPLOY_PRIME_URL")) return json({ error: "forbidden" }, 403);

  const key = env("OPENROUTER_API_KEY");
  if (!key) return json({ error: "site_not_configured" }, 500);
  if (limited(context?.ip || req.headers.get("x-nf-client-connection-ip") || "unknown")) return json({ error: "rate_limited" }, 429);

  let prompt;
  try { prompt = (await req.json())?.prompt; } catch (e) { return json({ error: "bad_request" }, 400); }
  if (typeof prompt !== "string" || !prompt.trim()) return json({ error: "bad_request" }, 400);
  if (prompt.length > MAX_PROMPT) return json({ error: "prompt_too_large" }, 413);

  let r;
  try {
    r = await fetch(OR_URL, {
      method: "POST",
      headers: { "Authorization": "Bearer " + key, "Content-Type": "application/json", "X-Title": "Docket Clock" },
      body: JSON.stringify({ model: MODEL, max_tokens: MAX_TOKENS, messages: [{ role: "user", content: prompt }] }),
    });
  } catch (e) { return json({ error: "upstream_unreachable" }, 502); }

  if (!r.ok){
    const code = r.status === 401 ? "site_key" : r.status === 402 ? "site_no_credit" : r.status === 429 ? "rate_limited" : "api_error";
    return json({ error: code }, r.status === 429 ? 429 : 502);
  }
  const data = await r.json().catch(() => null);
  const choice = data?.choices?.[0];
  const text = typeof choice?.message?.content === "string" ? choice.message.content : "";
  if (!text) return json({ error: "empty_completion" }, 502);
  return json({ text, truncated: choice.finish_reason === "length" });
};

export const config = { path: "/api/claude" };
