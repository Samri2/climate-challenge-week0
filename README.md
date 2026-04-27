# COP32 Climate Intelligence: Multi-National Vulnerability Synthesis
# Project Overview
This repository contains a data-driven climate analysis commissioned for the 32nd Conference of the Parties (COP32) in Addis Ababa. Using a decade of NASA POWER meteorological data (2015–2026), we evaluate the climate resilience of five East African nations to inform the strategic allocation of international climate finance.

# trategic Framework: The Three-Layer Analysis
Our methodology follows a business-critical framework designed for policy impact:

Baseline Shifts: Tracking decadal increases in mean temperatures (T2M).

Precipitation Volatility: Identifying agricultural risk through rainfall standard deviation.

Extreme Scaling: Quantifying the frequency of lethal heatwaves (>35°C) and flash flood events.

# ngineering Excellence & CI/CD
This project adheres to professional software engineering standards to ensure Data Integrity and Reproducibility:

CI/CD Pipeline: Automated GitHub Actions run on every push to execute flake8 linting and pytest suites, ensuring code quality.

Environment Stability: Managed via an isolated Python 3.12 virtual environment.

Collaborative Workflow: Development followed a strict feature-branch strategy with peer-ready documentation and GitHub Issue tracking.

# pository Structure
climate-challenge-week0/
├── .github/workflows/ci.yml   # Automated CI/CD Pipeline
├── app/                       # Interactive Streamlit Dashboard (Bonus)
├── notebooks/                 # Exploratory Data Analysis & Synthesis
│   ├── ethiopia_eda.ipynb     # Baseline: Highland Thermal Stability
│   ├── sudan_eda.ipynb        # Hotspot: Extreme Heat Stress
│   └── compare_countries.ipynb# Final COP32 Position Paper Synthesis
├── reports/                   # Final PDF Blog-Style Report
├── tests/                     # Automated Validation Suite (Pytest)
├── .gitignore                 # Secure Data Exclusion (NASA Datasets)
└── requirements.txt           # Production Dependencies
# deployment & Setup
1. Clone & Initialize

git clone https://github.com/samri2/climate-challenge-week0.git
cd climate-challenge-week0
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
2. Validation
pytest  # Ensure all cleaning and ANOVA modules pass
# Summary of Findings (Task 3 Synthesis)
| Metric | Sudan | Nigeria | Tanzania | Kenya | Ethiopia |
|--------|-------|----------|----------|-------|-----------|
| Mean Temp | 28.76°C | 26.66°C | 26.80°C | 20.43°C | 16.07°C |
| Primary Risk | Extreme Heat | Flash Floods | Rain Volatility | Drought Cycles | Highland Erosion |
| Vulnerability | Critical | High | Medium-High | Medium | Stable/Low |
# Final Deliverables
Main Branch: Integrated source code and notebooks.

Final Report: Download the COP32 Blog-Style PDF

Dashboard: Screenshot available in dashboard_screenshots/.

Contact: Samrawit Worku — Information Systems Professional | Addis Ababa, Ethiopia