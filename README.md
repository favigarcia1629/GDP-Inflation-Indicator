# GDP & Inflation Indicator Explorer 📈
**Portfolio Project #03 | EDA & Statistics | Python | FRED API**

## Results at a Glance

| Relationship | Correlation | Theory | Verdict |
|--------------|-------------|--------|---------|
| Inflation vs Unemployment (Phillips Curve) | -0.34 | Negative expected | ✅ Confirmed but weak |
| GDP vs Unemployment (Okun's Law) | -0.27 | Negative expected | ✅ Confirmed but weak |
| GDP vs Inflation | +0.15 | Positive expected | ⚠️ Near zero — modern macro puzzle |

Both the Phillips Curve and Okun's Law exist in the data but are **significantly weaker than textbook models predict** — consistent with post-1990 macroeconomic literature.

---

## Overview

This project retrieves 35 years of macroeconomic data from the Federal Reserve FRED database and tests two foundational economic theories against real data. It reveals that classical relationships — while directionally correct — have weakened significantly since the 1990s, raising important questions about modern monetary policy effectiveness.

The 2025 data captured a live policy dilemma: inflation still above the Fed's 2% target while unemployment ticks upward — the conditions that define **stagflation risk**.

---

## Dataset

**Source:** Federal Reserve Economic Data (FRED) — free API, 800,000+ series

| Indicator | FRED Code | Frequency | Economic Role |
|-----------|-----------|-----------|---------------|
| GDP | GDP | Quarterly | Broadest measure of economic output |
| CPI (inflation proxy) | CPIAUCSL | Monthly | Price level — converted to YoY % change |
| Unemployment Rate | UNRATE | Monthly | Labor market slack — lagging indicator |

---

## Methodology

**1. Data Retrieval**
All three series pulled via `fredapi` from 1990 to present. No manual downloads required.

**2. Frequency Alignment**
Quarterly GDP resampled to monthly using forward-fill — each quarter's value applies to all 3 months in that quarter, avoiding interpolation of unobserved data.

**3. Inflation Rate Engineering**
Raw CPI converted to year-over-year % change using `pct_change(12)` — the standard format used by the Fed, IMF, and financial media.

**4. Correlation Analysis**
Full pairwise correlation matrix computed across all three aligned monthly series.

**5. Visualization**
Three-panel time series with annotated recession periods and Fed 2% target line, plus scatter plots testing both economic relationships with OLS trend lines.

---

## Key Findings

- **Phillips Curve (-0.34)** — confirms the theoretical direction but reflects the well-documented post-1990 flattening driven by globalization and anchored inflation expectations
- **Okun's Law (-0.27)** — holds directionally but weakened by automation, productivity gains, and the rise of gig economy employment
- **GDP-Inflation (+0.15)** — near zero, reflecting the central puzzle of modern macroeconomics: strong growth no longer reliably causes inflation
- **2025 signal** — inflation above the 2% target while unemployment rises is a live stagflation warning visible in the dashboard

---

## How to Run

Requires a free FRED API key from [fred.stlouisfed.org](https://fred.stlouisfed.org/)

```bash
pip install fredapi pandas matplotlib seaborn statsmodels
# Add your FRED_API_KEY to the config cell in the notebook
jupyter notebook gdp_inflation_explorer.ipynb
```

---

## Tools & Libraries

- Python 3.12
- `fredapi` — FRED data retrieval
- `pandas` — frequency alignment and feature engineering
- `matplotlib` / `seaborn` — time series and correlation visualization
- `statsmodels` — trend line fitting

---

## About

Built as part of an Economics portfolio by an economics major exploring machine learning applications in finance and policy.
