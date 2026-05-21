# 🚀 DevSecOps Python Flask Application

A complete beginner-to-advanced DevSecOps project built using Python Flask, GitHub Actions, Docker, automated testing, and security scanning.

This project demonstrates:
- CI/CD Pipeline
- Docker Containerization
- Automated Testing
- GitHub Integration
- DevSecOps Workflow

---

# 📌 Project Features

✅ User Authentication  
✅ Dashboard  
✅ File Uploads  
✅ Search Functionality  
✅ Automated Testing  
✅ GitHub Actions CI/CD  
✅ Dockerized Application  
✅ Security Scanning  

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python Flask | Backend Web App |
| Git & GitHub | Version Control |
| GitHub Actions | CI/CD Pipeline |
| Docker | Containerization |
| Pytest | Automated Testing |
| HTML/CSS/JS | Frontend |
| SQLite | Database |

---

# 📂 Project Structure

```text
DEVSECOPS/
│
├── .github/workflows/
│   └── ci-cd.yml
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│
├── tests/
│   └── test_app.py
│
├── uploads/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
└── app.db
```

---

# ⚙️ Step-by-Step Complete Setup Guide

---

# 🔥 STEP 1 — Install Python

Download Python:

https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

---

# 🔥 STEP 2 — Install Git

Download Git:

https://git-scm.com/download/win

Verify installation:

```bash
git --version
```

---

# 🔥 STEP 3 — Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/DevSecOps-python-app.git
```

Go inside project folder:

```bash
cd DevSecOps-python-app
```

---

# 🔥 STEP 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔥 STEP 5 — Run Flask Application

```bash
python app.py
```

Application will run on:

```text
http://127.0.0.1:5000
```

---

# 🔥 STEP 6 — Initialize Git Repository

```bash
git init
```

---

# 🔥 STEP 7 — Add Files to Git

```bash
git add .
```

---

# 🔥 STEP 8 — Create Commit

```bash
git commit -m "first commit"
```

---

# 🔥 STEP 9 — Connect GitHub Repository

```bash
git remote add origin https://github.com/YOUR_USERNAME/DevSecOps-python-app.git
```

---

# 🔥 STEP 10 — Rename Main Branch

```bash
git branch -M main
```

---

# 🔥 STEP 11 — Push Code to GitHub

```bash
git push -u origin main
```

---

# 🔥 STEP 12 — Create GitHub Actions CI/CD Pipeline

Create folder:

```text
.github/workflows/
```

Create file:

```text
ci-cd.yml
```

Add this configuration:

```yaml
name: CI-CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build-and-test:

    runs-on: ubuntu-latest

    steps:

    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: 3.10

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest
```

---

# 🔥 STEP 13 — Install Docker

Download Docker Desktop:

https://www.docker.com/products/docker-desktop/

Verify installation:

```bash
docker --version
```

---

# 🔥 STEP 14 — Create Dockerfile

Create file:

```text
Dockerfile
```

Add this code:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
```

---

# 🔥 STEP 15 — Build Docker Image

```bash
docker build -t devsecops-app .
```

---

# 🔥 STEP 16 — Run Docker Container

```bash
docker run -p 5000:5000 devsecops-app
```

Open browser:

```text
http://localhost:5000
```

---

# 🔥 STEP 17 — Run Automated Tests

```bash
pytest
```

Expected output:

```text
1 passed
```

---

# 🔥 STEP 18 — Push Latest Changes

```bash
git add .
```

```bash
git commit -m "Updated Docker and CI/CD"
```

```bash
git push
```

---

# 🧪 Automated Testing

Test file location:

```text
tests/test_app.py
```

Example test:

```python
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

def test_home():

    client = app.test_client()

    response = client.get('/')

    assert response.status_code == 200
```

---

# 🐳 Docker Commands

Build image:

```bash
docker build -t devsecops-app .
```

Run container:

```bash
docker run -p 5000:5000 devsecops-app
```

Show running containers:

```bash
docker ps
```

Stop container:

```bash
CTRL + C
```

---

# 🔎 Security Vulnerability Analysis using Bandit (SAST)

This project uses **Bandit** for Static Application Security Testing (SAST) to identify insecure coding practices and vulnerabilities inside the Flask application.

## 🔧 Run Bandit Scan

Install Bandit:

```bash
pip install bandit
```

Run security scan:

```bash
python -m bandit -r .
```

---

# 🚨 Vulnerabilities Identified

## 1. SQL Injection (Critical)

- In `/login` route (line 78): Direct string concatenation with user input

```python
query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
```

- In `/register` route (line 56): Same vulnerability

```python
cur.execute("INSERT INTO users (username, password) VALUES ('%s', '%s')" % (username, password))
```

- In `/search` route (line 150): String concatenation vulnerability

```python
sql = "SELECT * FROM docs WHERE title LIKE '%" + q + "%' OR content LIKE '%" + q + "%'"
```

---

## 2. Hardcoded Weak Secret Key (High)

- Line 11:

```python
app.secret_key = 'devsecops-insecure-secret'
```

- Should never hardcode secrets; should use environment variables

---

## 3. Plaintext Password Storage (Critical)

- Passwords stored directly in database without hashing
- Demo admin user has password `admin` in plaintext (line 39)
- Line 54 comment explicitly states "storing plaintext"

---

## 4. Default/Weak Credentials (Critical)

- Demo admin credentials:
  - username: `admin`
  - password: `admin`
  - (line 39)

---

## 5. Debug Mode Enabled in Production (High)

- Line 155:

```python
debug=True
```

- Exposes sensitive information and allows arbitrary code execution

---

## 6. Missing Input Validation

- No validation on username, password, or search queries
- Relies only on `secure_filename()` for file uploads which can be bypassed for path traversal

---

## 7. Exposure to Cross-Site Scripting (XSS) via Error Messages

- Line 65:

```python
flash('Registration failed: ' + str(e), 'danger')
```

- Exception messages might contain user input and aren't sanitized

---

## 8. Information Disclosure

- Line 65: Stack traces exposed to users via flash messages
- Line 155: Running on `0.0.0.0` (all interfaces) with debug enabled

---

⚠️ These vulnerabilities are intentionally embedded for DevSecOps training and security demonstration purposes to teach secure coding, security scanning, and remediation techniques.

---


# 🔐 DevSecOps Workflow

```text
Developer Pushes Code
        ↓
GitHub Actions Trigger
        ↓
Install Dependencies
        ↓
Run Automated Tests
        ↓
Security Scanning
        ↓
Docker Build
        ↓
Deployment Ready
```

---

# 🚀 Future Improvements

- OWASP ZAP Integration
- Kubernetes Deployment
- JWT Authentication
- AWS Deployment
- Jenkins Pipeline
- Trivy Security Scanning
- Terraform Infrastructure
- Monitoring Dashboard

---

# 👨‍💻 Author

Manish

---

# ⭐ Support

If you found this project useful, give it a ⭐ on GitHub.
