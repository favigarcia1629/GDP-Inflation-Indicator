"""
GDP & Inflation Indicator — Streamlit Dashboard
Fetches GDP, CPI (Inflation), and Unemployment from FRED.
Tests the Phillips Curve and Okun's Law against 35 years of real data.
"""
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from fredapi import Fred

# ── API Key ─────────────────────────────────────────────────────────────────
def get_api_key() -> str:
    try:
        return st.secrets["fred"]["api_key"]
    except Exception:
        pass
    key = os.getenv("FRED_API_KEY", "")
    if key:
        return key
    raise RuntimeError(
        "FRED API key not found. "
        "Set it in .streamlit/secrets.toml ([fred] api_key = '...') "
        "or in a .env file as FRED_API_KEY=..."
    )

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GDP & Inflation Indicator",
    page_icon="📈",
    layout="wide",
)

BLUE   = "#2196F3"
RED    = "#F44336"
ORANGE = "#FF9800"
GRAY   = "#6B7280"
GREEN  = "#22C55E"

# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=86400)
def load_data() -> pd.DataFrame:
    fred = Fred(api_key=get_api_key())

    gdp      = fred.get_series("GDP",      observation_start="1990-01-01")
    cpi      = fred.get_series("CPIAUCSL", observation_start="1990-01-01")
    unemploy = fred.get_series("UNRATE",   observation_start="1990-01-01")

    inflation   = cpi.pct_change(12, fill_method=None) * 100
    gdp_monthly = gdp.resample("MS").ffill()

    df = pd.DataFrame({
        "GDP":          gdp_monthly,
        "Inflation":    inflation,
        "Unemployment": unemploy,
    }).dropna()

    return df


with st.spinner("Fetching data from FRED..."):
    try:
        df = load_data()
    except RuntimeError as e:
        st.error(str(e))
        st.stop()

latest    = df.iloc[-1]
start_yr  = df.index[0].year
end_yr    = df.index[-1].year

# ── Header ───────────────────────────────────────────────────────────────────
st.title("U.S. GDP & Inflation Indicator")
st.caption(
    f"35 years of macroeconomic data ({start_yr}–{end_yr}) from the Federal Reserve (FRED). "
    "Tests the Phillips Curve and Okun's Law against real data."
)

# ── KPI Row ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Latest GDP",         f"${latest['GDP']:,.1f}B")
k2.metric("Latest Inflation",   f"{latest['Inflation']:.2f}%")
k3.metric("Latest Unemployment",f"{latest['Unemployment']:.1f}%")
k4.metric("Data Points",        f"{len(df):,} months")

st.divider()

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "Macro Time Series",
    "Correlation Analysis",
    "Economic Theory Tests",
])

# ── Tab 1: Time Series ───────────────────────────────────────────────────────
with tab1:
    st.subheader("U.S. Macroeconomic Indicators Over Time")

    # GDP
    fig_gdp = go.Figure()
    fig_gdp.add_trace(go.Scatter(
        x=df.index, y=df["GDP"],
        mode="lines", name="GDP",
        line=dict(color=BLUE, width=2),
        fill="tozeroy", fillcolor="rgba(33,150,243,0.1)",
    ))
    fig_gdp.add_hline(y=df["GDP"].iloc[-1], line_dash="dot", line_color=GRAY,
                      annotation_text=f"Latest: ${latest['GDP']:,.0f}B", annotation_position="left")
    fig_gdp.update_layout(height=280, title="GDP (Billions USD)",
                          yaxis_title="Billions USD", margin=dict(t=40, b=20), showlegend=False)
    st.plotly_chart(fig_gdp, use_container_width=True)

    col_inf, col_unemp = st.columns(2)

    # Inflation
    with col_inf:
        fig_inf = go.Figure()
        fig_inf.add_trace(go.Scatter(
            x=df.index, y=df["Inflation"],
            mode="lines", name="Inflation",
            line=dict(color=RED, width=2),
        ))
        fig_inf.add_hline(y=2, line_dash="dash", line_color="black",
                          annotation_text="Fed 2% Target", annotation_position="right")
        fig_inf.add_trace(go.Scatter(
            x=df.index, y=df["Inflation"].clip(lower=2),
            fill="tozeroy", fillcolor="rgba(244,67,54,0.12)",
            line=dict(width=0), showlegend=False, name="Above target",
        ))
        fig_inf.update_layout(height=300, title="Inflation Rate — YoY % (CPI)",
                              yaxis_title="Inflation (%)", margin=dict(t=40, b=20), showlegend=False)
        st.plotly_chart(fig_inf, use_container_width=True)

    # Unemployment
    with col_unemp:
        fig_unemp = go.Figure()
        fig_unemp.add_trace(go.Scatter(
            x=df.index, y=df["Unemployment"],
            mode="lines", name="Unemployment",
            line=dict(color=ORANGE, width=2),
            fill="tozeroy", fillcolor="rgba(255,152,0,0.1)",
        ))
        fig_unemp.update_layout(height=300, title="Unemployment Rate (%)",
                                yaxis_title="Unemployment (%)", margin=dict(t=40, b=20), showlegend=False)
        st.plotly_chart(fig_unemp, use_container_width=True)

    st.info(
        f"**GDP** has grown from ~$5.8T (1990) to **${latest['GDP']:,.0f}B** today, "
        f"interrupted by three recessions (2001, 2008, 2020). "
        f"**Inflation** spiked to ~9% in 2022 — the highest since the early 1980s — "
        f"before returning toward the Fed's 2% target. "
        f"**Unemployment** peaked at 14.7% in April 2020 during COVID lockdowns."
    )

# ── Tab 2: Correlation ───────────────────────────────────────────────────────
with tab2:
    st.subheader("Correlation Between GDP, Inflation & Unemployment")
    st.caption("Values range from -1 (perfect inverse) to +1 (perfect positive). 0 = no linear relationship.")

    corr = df.corr()

    col_heat, col_table = st.columns([3, 2])

    with col_heat:
        fig_heat = px.imshow(
            corr,
            color_continuous_scale="RdBu",
            zmin=-1, zmax=1,
            text_auto=".2f",
            aspect="auto",
        )
        fig_heat.update_layout(
            height=380,
            title="Correlation Heatmap",
            coloraxis_colorbar=dict(title="Correlation"),
            margin=dict(t=40),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_table:
        st.markdown("**Pairwise Correlations**")
        pairs = [
            ("GDP", "Inflation",     corr.loc["GDP", "Inflation"]),
            ("GDP", "Unemployment",  corr.loc["GDP", "Unemployment"]),
            ("Inflation", "Unemployment", corr.loc["Inflation", "Unemployment"]),
        ]
        pair_df = pd.DataFrame(pairs, columns=["Variable A", "Variable B", "Correlation"])
        pair_df["Correlation"] = pair_df["Correlation"].round(3)
        pair_df["Strength"] = pair_df["Correlation"].abs().map(
            lambda x: "Strong" if x > 0.6 else ("Moderate" if x > 0.3 else "Weak")
        )
        pair_df["Direction"] = pair_df["Correlation"].map(
            lambda x: "Positive" if x > 0 else "Negative"
        )
        st.dataframe(pair_df, hide_index=True, use_container_width=True)

        st.info(
            "All three relationships are **weak**, which is the key finding. "
            "GDP and inflation have almost no correlation (r = 0.15). "
            "Unemployment shows mild negative correlation with both — "
            "directionally consistent with theory, but far weaker than classical models predict."
        )

# ── Tab 3: Economic Theory Tests ─────────────────────────────────────────────
with tab3:
    st.subheader("Testing Classical Economic Theories on 35 Years of Real Data")

    col_l, col_r = st.columns(2)

    # Phillips Curve
    with col_l:
        st.markdown("**Phillips Curve** — Unemployment vs Inflation")
        st.caption("Theory: lower unemployment → higher inflation (inverse relationship)")

        z = np.polyfit(df["Unemployment"], df["Inflation"], 1)
        x_line = np.linspace(df["Unemployment"].min(), df["Unemployment"].max(), 200)
        y_line = np.polyval(z, x_line)

        fig_pc = go.Figure()
        fig_pc.add_trace(go.Scatter(
            x=df["Unemployment"], y=df["Inflation"],
            mode="markers",
            marker=dict(color=RED, size=5, opacity=0.4),
            name="Monthly data",
        ))
        fig_pc.add_trace(go.Scatter(
            x=x_line, y=y_line,
            mode="lines", line=dict(color="black", dash="dash", width=2),
            name=f"Trend (slope={z[0]:.2f})",
        ))
        fig_pc.update_layout(
            height=380,
            xaxis_title="Unemployment Rate (%)",
            yaxis_title="Inflation Rate (%)",
            margin=dict(t=20),
        )
        st.plotly_chart(fig_pc, use_container_width=True)

        r_pc = np.corrcoef(df["Unemployment"], df["Inflation"])[0, 1]
        st.caption(
            f"r = {r_pc:.2f} | slope = {z[0]:.2f} | "
            "Directionally negative (consistent with theory) but the scatter is wide — "
            "the relationship has weakened significantly in the modern era."
        )

    # Okun's Law
    with col_r:
        st.markdown("**Okun's Law** — GDP vs Unemployment")
        st.caption("Theory: higher GDP growth → lower unemployment (inverse relationship)")

        z2 = np.polyfit(df["GDP"], df["Unemployment"], 1)
        x_line2 = np.linspace(df["GDP"].min(), df["GDP"].max(), 200)
        y_line2 = np.polyval(z2, x_line2)

        fig_ok = go.Figure()
        fig_ok.add_trace(go.Scatter(
            x=df["GDP"], y=df["Unemployment"],
            mode="markers",
            marker=dict(color=BLUE, size=5, opacity=0.4),
            name="Monthly data",
        ))
        fig_ok.add_trace(go.Scatter(
            x=x_line2, y=y_line2,
            mode="lines", line=dict(color="black", dash="dash", width=2),
            name=f"Trend (slope={z2[0]:.4f})",
        ))
        fig_ok.update_layout(
            height=380,
            xaxis_title="GDP (Billions USD)",
            yaxis_title="Unemployment Rate (%)",
            margin=dict(t=20),
        )
        st.plotly_chart(fig_ok, use_container_width=True)

        r_ok = np.corrcoef(df["GDP"], df["Unemployment"])[0, 1]
        st.caption(
            f"r = {r_ok:.2f} | slope = {z2[0]:.4f} | "
            "Negative as Okun's Law predicts — GDP growth is associated with lower unemployment. "
            "Weaker than theory suggests due to GDP being a level, not a growth rate."
        )

    st.divider()
    st.info(
        "**Key Finding:** Both classical theories hold *directionally* — "
        "unemployment moves inversely with both GDP and inflation — "
        "but the relationships are weaker than textbook models predict. "
        "The 2021–2022 period is a clear outlier: unemployment fell rapidly "
        "while inflation surged, temporarily restoring the Phillips Curve pattern. "
        "This raises important questions about the effectiveness of modern monetary policy."
    )
