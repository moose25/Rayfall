# Contributing to Rayfall

Thanks for your interest in improving Rayfall! Whether you found a bug, want
a new feature, or want to send a patch, this page covers how.

## Reporting bugs and requesting features

Please open an [issue](https://github.com/moose25/Rayfall/issues) using one of
the provided templates. Good bug reports include:

- What you were trying to do
- What actually happened (with screenshots if it's a UI issue)
- Which browser you were using
- How you loaded your log (QRZ API vs. ADIF file)
- A minimal ADIF snippet that reproduces the problem, if relevant

## Sending a pull request

1. Fork the repo and clone your fork.
2. Create a feature or fix branch:
   ```bash
   git checkout -b feature/short-description
   ```
3. Make your changes. See **Development setup** below.
4. Test your change against a real log — the [QUICK_START_ADI.md](QUICK_START_ADI.md)
   guide covers loading an ADIF file locally.
5. Commit with a message that explains *why*, not just *what*.
6. Push your branch and open a PR against `main`. The PR template will prompt
   you for a summary and a test plan.

## Development setup

```bash
git clone https://github.com/moose25/Rayfall.git
cd Rayfall
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000 in your browser.

- Backend lives in [`main.py`](main.py) (FastAPI).
- The entire frontend — HTML, CSS, and JavaScript — lives in
  [`templates/index.html`](templates/index.html). No build step.
- Jinja auto-reloads templates; changes to `main.py` need a restart.

## Style

- Match the surrounding code — no formatters are enforced.
- Prefer small, focused commits.
- Keep dependencies minimal. If you need to add one, mention why in the PR.

## Code of Conduct

Participation in this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
