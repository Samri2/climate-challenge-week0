# Solar Data Discovery: Week 0 — MoonLight Energy Solutions

## Overview
Analysis of solar farm data from **Benin**, **Sierra Leone**, and **Togo** to identify high-potential regions for solar installation.

## Project Structure

```
climate-challenge-week0/
├── .github/workflows/ci.yml   # CI/CD pipeline (GitHub Actions)
├── notebooks/                    # Jupyter notebooks for EDA per country
├── src/                          # Source modules (reusable code)
├── scripts/                      # Standalone processing scripts
├── tests/                        # Automated test suite (pytest)
├── app/                          # Streamlit dashboard (bonus task)
├── datas/                         # Local data files (NOT committed to Git)
├── requirements.txt              # Production dependencies
├── config.py                     # Environment configuration
├── pytest.ini                    # Pytest configuration
└── .gitignore                    # Files to exclude from Git
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/samri2/climate-challenge-week0.git
   cd week0
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run the tests**
   ```bash
   pytest
   ```

## Tasks

| Task | Branch | Deliverable |
| 1: Setup & Env |main | Root Directory
| 2: EDA (Ethiopia)|eda-ethiopia |
|Task 2: EDA (Tanzania) | eda-tanzania | notebooks/tanzania_eda.ipynb
|Task 2: EDA (Nigeria) | eda-nigeria | notebooks/nigeria_eda.ipynb
|Task 2: EDA (Sudan) | eda-sudan | notebooks/sudan_eda.ipynb
|Task 2: EDA (Kenya) | eda-kenya | notebooks/kenya_eda.ipynb
|Task 3: Cross-Country | compare-countries | notebooks/compare_countries.ipynb
|Bonus: Dashboard | dashboard-dev | app/main.py
## CI/CD Pipeline

Automated pipeline runs on every push via **GitHub Actions**:
- ✅ Installs dependencies
- ✅ Runs flake8 linter
- ✅ Runs pytest suite
