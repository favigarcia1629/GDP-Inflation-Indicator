# GDP & Inflation Indicator

**Do classical economic theories still hold in modern data?**

35 years of macroeconomic data (1990–2026) pulled from the Federal Reserve (FRED). Tests the Phillips Curve and Okun's Law against real data — finding both theories directionally correct but significantly weaker than textbook models predict.

---

## Results

| Relationship | Correlation | Theory | Verdict |
|---|---|---|---|
| Inflation vs Unemployment (Phillips Curve) | -0.34 | Negative expected | Confirmed but weak |
| GDP vs Unemployment (Okun's Law) | -0.27 | Negative expected | Confirmed but weak |
| GDP vs Inflation | +0.15 | Positive expected | Near zero — modern macro puzzle |

Both classical theories hold *directionally* but are **far weaker than textbook models predict** — consistent with post-1990 macroeconomic literature.

---

## Key Findings

- **Phillips Curve (-0.34)** — confirms the theoretical direction but reflects the well-documented post-1990 flattening driven by globalization and anchored inflation expectations
- **Okun's Law (-0.27)** — holds directionally; weakened by automation, productivity gains, and the rise of gig employment
- **GDP-Inflation (+0.15)** — near zero, reflecting the central puzzle of modern macroeconomics: strong growth no longer reliably causes inflation
- **2022 outlier** — unemployment fell rapidly while inflation surged, temporarily restoring the Phillips Curve pattern before supply chains normalized
- **2025 signal** — inflation still above the 2% target while unemployment ticks up — conditions consistent with stagflation risk

---

## Dashboard Tabs

| Tab | What It Shows |
|---|---|
| Macro Time Series | GDP, Inflation, and Unemployment plotted from 1990 to present with the Fed 2% target line |
| Correlation Analysis | Pairwise correlation heatmap with interpretation of each relationship |
| Economic Theory Tests | Scatter plots testing the Phillips Curve and Okun's Law with OLS trend lines |

---

## Data Sources

| Indicator | FRED Code | Frequency | Notes |
|---|---|---|---|
| GDP | `GDP` | Quarterly | Forward-filled to monthly |
| CPI | `CPIAUCSL` | Monthly | Converted to YoY % change |
| Unemployment | `UNRATE` | Monthly | — |

---

## Run Locally

Requires a free FRED API key from [fred.stlouisfed.org](https://fred.stlouisfed.org/)

```bash
git clone https://github.com/favigarcia1629/GDP-Inflation-Indicator.git
cd GDP-Inflation-Indicator
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your FRED_API_KEY
streamlit run app.py
```

Or set the key in `.streamlit/secrets.toml`:
```toml
[fred]
api_key = "your_key_here"
```

---

## Project Structure

```
gdp_inflation/
├── app.py              # Streamlit dashboard (3 tabs)
├── requirements.txt
├── .env.example        # API key template
└── README.md
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python (pandas, numpy) | Data wrangling and frequency alignment |
| fredapi | FRED API data retrieval |
| Plotly | Interactive time series and scatter charts |
| Streamlit | Live dashboard |

*Data: Federal Reserve Economic Data (FRED). Not financial advice — built for research and education.*
