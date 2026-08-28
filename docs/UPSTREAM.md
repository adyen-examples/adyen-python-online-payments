# Upstream foundation and attribution

Transact is not a payment application. It is a quality engineering platform built
around one, and the payment application is somebody else's work.

## What the upstream project is

| | |
|---|---|
| Project | [adyen-python-online-payments](https://github.com/adyen-examples/adyen-python-online-payments) |
| Maintained by | Adyen |
| License | MIT |
| Base commit | `a78d64f`, 16 June 2026 |
| What it demonstrates | The Adyen Sessions flow: a Flask backend opens a payment session, and Adyen's browser component handles the payment itself |

Adyen did not create Transact, has not reviewed it, and does not endorse it. The
upstream license text is preserved unchanged in `LICENSE`.

## Code that is not mine

Everything below existed before Transact and is credited to Adyen:

- the Flask application factory and routing in `app/app.py`
- the payment session integration in `app/main/sessions.py`
- HMAC signature verification on the webhook endpoint
- the configuration getters in `app/main/config.py`
- every Jinja template and static asset, including the browser side checkout wiring
- the `_archive/v5` folder, which holds the previous checkout version and is unused here

## Changes made to upstream files

Each entry names the file, the change, and the reason. This list is kept current
as the project moves through its phases.

### Phase 1

| File | Change | Why |
|---|---|---|
| `.github/workflows/e2e.yml` | Renamed to `e2e.yml.disabled` | It runs Adyen's own Playwright suite and requires Adyen test credentials as repository secrets. On a fork without those secrets it fails on every push, which makes the repository look broken. Transact builds its own pipeline in Phase 13. |
| `.gitignore` | Added entries for the virtual environment, caches, and generated reports | Generated output does not belong in version control. |

### Files added by Transact in Phase 1

| File | Purpose |
|---|---|
| `pyproject.toml` | Pins every runtime dependency and sets the minimum Python version. Upstream `requirements.txt` leaves Flask unpinned, which means two people can install two different applications. Transact does not use `requirements.txt`. |
| `.env.example` | Documents the configuration surface with placeholder values, so the project can be set up without anyone guessing which variables exist. |
| `docs/UPSTREAM.md` | This file. |

## Planned modifications, not yet made

Recorded here so the boundary stays honest as the project grows.

- a payment endpoint that accepts and validates a request body, because the upstream
  endpoint ignores its input and hard codes the amount, which leaves nothing to test
- a persistence layer for payment attempts and webhook events, because idempotency
  and duplicate detection are claims about stored state
- a configurable Adyen base URL and HTTP timeout, so tests can be pointed at a local
  stub and continuous integration can never reach a real payment provider
- idempotency key support, which the Adyen library already accepts and upstream never passes
- structured error responses on the webhook path, which currently returns HTTP 500
  for malformed input and for an invalid signature
