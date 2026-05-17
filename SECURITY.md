# Security Policy

This Hermes companion utility reads local Hermes xAI OAuth state and sends a bearer token to grok.com to fetch the Grok subscription credit meter for SuperGrok or eligible X Premium+ accounts. It does not require a running Hermes process, but it does require Hermes' local `xai-oauth` auth plumbing and stored OAuth state.

## Reporting issues

If you open a public issue, do not include:

- OAuth access tokens or refresh tokens
- `~/.hermes/auth.json`
- shell history containing authorization headers
- packet captures with `Authorization` headers

The CLI refuses non-`grok.com` endpoints by default so a typo in `--endpoint` does not send the token to another host. Only use `--allow-non-grok-endpoint` for deliberate local debugging.
