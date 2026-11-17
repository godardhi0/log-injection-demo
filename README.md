# Log injection demo (OWASP A09:2025)

Small Flask project made for a school report on
**A09:2025 Security Logging and Alerting Failures**.

It shows two versions of the same login page:

- `/vulnerable/login`: writes user input directly in the log (CWE-117).
  It does not count failed attempts (CWE-778).
- `/secure/login`: cleans the input before logging, counts failed
  attempts and writes an alert after too many failures.

## Warning

This project is **intentionally vulnerable**. It is for learning only.
Run it only on your own computer (`localhost`). Never deploy it on a
public server and never test the attack on a real website.

## Installation

    python -m venv venv
    source venv/bin/activate      # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python run.py

Then open:

- http://127.0.0.1:5000/vulnerable/login
- http://127.0.0.1:5000/secure/login

Test account (demo only): `client42` / `Secret!2026`

## Demonstration of the attack

A browser removes line breaks from a text field, so the attack is sent
directly with curl. `%0A` is a line break.

    curl -X POST http://127.0.0.1:5000/vulnerable/login --data "username=client42%0A2026-11-16%2010:05:00%20INFO%20Compte%20client42%20d%C3%A9bloqu%C3%A9%20par%20:%20m.dupont&password=x"

Then compare `logs/vulnerable.log` and `logs/secure.log`.
On Windows PowerShell, use `curl.exe` or Git Bash.

## Tests

    python -m pytest

## Project structure

    app/
      routes/      vulnerable.py, secure.py
      services/    auth_service.py, log_sanitizer.py, rate_limiter.py
      templates/   base.html, login.html
    config.py      settings
    run.py         entry point
    tests/         unit tests

## Limits

- Users are stored in a Python dictionary, not in a database.
- The failure counter is in memory and is lost at restart.
- Logs are written locally, not sent to a separate server.
