# grok-credits-tracker

Small read-only **Hermes companion utility** for the **grok.com SuperGrok credit meter**.

This was built because Hermes Agent can now use xAI/Grok subscription OAuth (`xai-oauth`) for Grok, including SuperGrok and eligible X Premium+ subscriptions. The tool answers a narrower question: “how much of the grok.com subscription credit meter has this account used?”

It does **not** use an xAI API key and does **not** estimate spend from Hermes logs. It reuses the Hermes-managed `xai-oauth` bearer token and calls the same gRPC-web method that grok.com uses for the Settings → Usage card.

It is a standalone CLI in the sense that it does not require a running Hermes chat, gateway, daemon, or main-model switch. It is **not** standalone from Hermes auth: the current implementation requires a local Hermes install/auth checkout that can resolve an `xai-oauth` token.

```text
POST https://grok.com/grok_api_v2.GrokBuildBilling/GetGrokCreditsConfig
Content-Type: application/grpc-web+proto
Authorization: Hermes xAI OAuth bearer token from local Hermes auth
```

The web bundle's protobuf descriptor names the response fields as:

- `credit_usage_percent`
- `billing_period_start`
- `billing_period_end`
- `on_demand_cap`
- `on_demand_used`
- `history`

This is the source of the UI text like:

```text
Free credits with SuperGrok Heavy
<1% used · Resets May 31
```

## Requirements

- Python 3.9+
- Hermes Agent installed locally or available via `HERMES_AGENT_SOURCE`
- Hermes xAI OAuth login for a subscribed Grok account — SuperGrok or eligible X Premium+:

```bash
hermes auth add xai-oauth
```

No `XAI_API_KEY` or xAI Management API key is used.

For X Premium+ subscriptions, authenticate the same X/Grok account that has Premium+ entitlement. If Grok/xAI does not see the subscription, link the X account from Grok settings/account first, then re-run the Hermes OAuth login.

If you want a non-Hermes version, this project would need a separate “bring your own bearer token” or direct OAuth flow. That is intentionally out of scope for now to avoid asking users to copy/paste subscription tokens.

## Install / run

From a checkout:

```bash
git clone <repo-url>
cd grok-credits-tracker
python grok_credits.py
```

Editable install:

```bash
python -m pip install -e .
grok-credits
```

If Hermes is not installed at `~/.hermes/hermes-agent`, point the CLI at the checkout:

```bash
HERMES_AGENT_SOURCE=/path/to/hermes-agent grok-credits
```

## Usage

```bash
grok-credits
grok-credits --json
grok-credits --waybar
grok-credits --version
```

Example plain output:

```text
Free credits with SuperGrok Heavy
<1% used · Resets May 31
Credit usage percent: 0.133333
Billing window: 2026-04-30T19:00:00-05:00 → 2026-05-31T19:00:00-05:00
Pay-as-you-go: disabled
```

## Waybar example

```jsonc
"custom/grok-credits": {
  "exec": "grok-credits --waybar",
  "interval": 300,
  "return-type": "json",
  "tooltip": true,
  "escape": true
}
```

## Security / privacy

- The CLI reads your local Hermes auth state and sends the resolved OAuth bearer token only to `https://grok.com` by default.
- `--endpoint` is guarded: non-`grok.com` hosts are refused unless you explicitly pass `--allow-non-grok-endpoint` for local debugging.
- The CLI prints derived meter fields only; it does not print the bearer token.
- Do not paste verbose errors, packet captures, shell history, or environment dumps into public issues unless you have checked that tokens are redacted.

## Tests

```bash
python -m compileall -q grok_credits.py tests
python -m unittest discover -s tests -v
python grok_credits.py --help
```

## Notes / limitations

- This is a Hermes companion utility, not a general xAI billing CLI.
- It does not require Hermes to be running, but it does require Hermes' local `xai-oauth` auth plumbing and stored OAuth state.
- It was added to make the new Hermes xAI/Grok subscription path observable without switching Hermes' main model/provider; that includes SuperGrok and eligible X Premium+ accounts when OAuth resolves the entitlement.
- This endpoint is used by the grok.com web app, not by the public xAI Management API.
- The public Management API currently requires a management key; the Hermes OAuth bearer is rejected there with `oauth2-auth-forbidden`.
- The public inference API (`https://api.x.ai/v1`) exposes models/responses/media, but `/usage` and `/billing` are not available there.
- If xAI changes the grok.com protobuf service path or response schema, update `grok_credits.py`'s endpoint/parser.
- This project is not affiliated with xAI, Grok, or Hermes Agent.

## License

MIT
