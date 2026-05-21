# DevSecOps CI/CD Demo App (Flask)

This repository contains an intentionally vulnerable Flask application for CI/CD pipeline demonstrations with SAST/DAST tools.

WARNING: This app is intentionally insecure. Do NOT deploy to production or expose to the public internet.

Run locally:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The GitHub Actions workflow runs bandit (SAST) and pytest. There's a placeholder for a DAST scan using OWASP ZAP in the workflow.
