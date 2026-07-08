# Security Policy

## Reporting a vulnerability

If you believe you've found a security issue in Rayfall, please **do not open
a public issue**. Instead, open a
[private security advisory](https://github.com/moose25/Rayfall/security/advisories/new)
so the report stays private until a fix is available.

Please include:

- A description of the issue and the impact
- Steps to reproduce (or a proof-of-concept if you have one)
- The version / commit you tested against

You should get an acknowledgement within a few days. Fixes will be released as
soon as reasonably possible depending on severity.

## Scope

Rayfall runs as a small FastAPI service and a single-page frontend. Reports
about:

- The **Rayfall server** (`main.py`, share/embed endpoints) — in scope
- The **hosted instance** at [rayfall.me](https://rayfall.me) — in scope
- **QRZ Logbook** or **Leaflet/OSM tile servers** — out of scope; report those
  to their respective maintainers
