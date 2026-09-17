import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.theme import (
    apply_page_style,
    render_topbar,
    get_base64_image,
    icon,
    PLOTLY_LAYOUT,
)
from utils.data_loader import load_clean_data

apply_page_style("Home", page_icon="🚗")
render_topbar(active="Home", spacer=False)

df = load_clean_data()

NEON_BLUE = "#4C8DFF"
NEON_CYAN = "#35D9F5"
NEON_VIOLET = "#A66BFF"
NEON_PINK = "#F05CC8"
NEON_MINT = "#3FE0B0"
DONUT_COLORS = [NEON_BLUE, NEON_VIOLET, NEON_PINK, NEON_MINT, NEON_CYAN]


def mini_layout(**overrides):
    """PLOTLY_LAYOUT with per-chart overrides (margin merged, not duplicated)."""
    layout = dict(PLOTLY_LAYOUT)
    margin = dict(layout.get("margin", {}))
    margin.update(overrides.pop("margin", {}))
    layout["margin"] = margin
    # Plotly prints "undefined" above a chart when a title font is set without a
    # title, so blank the title explicitly on these mini charts.
    font = layout.pop("title_font", None)
    layout["title"] = dict(text="", font=font) if font else dict(text="")
    layout.update(overrides)
    return layout


def pct_change(series):
    """Last period vs. the one before it, as a percentage."""
    if len(series) < 2 or not series.iloc[-2]:
        return None
    return (series.iloc[-1] - series.iloc[-2]) / series.iloc[-2] * 100


def delta_block(value, label="vs. last month"):
    if value is None:
        return '<div class="kpi-delta"><em>Live dataset</em></div>'
    down = value < 0
    return (
        f'<div class="kpi-delta{" down" if down else ""}">'
        f'{"↓" if down else "↑"} {abs(value):.1f}% <em>{label}</em></div>'
    )


# ------------------------------------------------------------------ hero ----
img_b64 = get_base64_image("hero_car.jpg")
st.markdown(
    f"""
<section class="home-hero">
  <img class="home-hero-bg" src="data:image/jpeg;base64,{img_b64}" alt="" />
  <div class="home-hero-overlay"></div>
  <div class="home-hero-content">
    <div class="hero-badge"><span class="badge-dot"></span> AI-Powered &nbsp;•&nbsp; Accurate &nbsp;•&nbsp; Fast</div>
    <h1>Welcome to<br><span>Car Price Prediction</span></h1>
    <p>Discover the value of your dream car with the power<br class="desktop-break">
       of data and machine learning.</p>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------- quick shortcuts ----
shortcuts = [
    ("car", "Car Analysis", "Explore pricing patterns", "Car_Analysis"),
    ("list", "Description", "Understand the dataset", "Data_Description"),
    ("brain", "Predict Price", "Get a live prediction", "Predict_Price"),
    ("doc", "Report", "View the full report", "Report"),
    ("nodes", "ML Models", "Compare trained models", "ML_Models"),
]

cards = "".join(
    f'<a class="home-shortcut" href="{href}" target="_self">'
    f'<span class="shortcut-icon">{icon(name, 32)}</span>'
    f'<span class="shortcut-copy"><strong>{title}</strong><small>{sub}</small></span>'
    f'<span class="shortcut-arrow">{icon("arrow", 20)}</span>'
    "</a>"
    for name, title, sub, href in shortcuts
)
st.markdown(f'<div class="shortcut-grid">{cards}</div>', unsafe_allow_html=True)

# ------------------------------------------------------------ kpi section ----
monthly = (
    df.groupby(["SaleYear", "SaleMonth"])
    .agg(sales=("Id", "count"), avg_price=("SellingPrice", "mean"))
    .reset_index()
    .sort_values(["SaleYear", "SaleMonth"])
)
trans = df["Transmission"].fillna("Unknown").str.title().value_counts().head(4)
trans_pct = trans / trans.sum() * 100
brand_avg = (
    df.groupby("Make")["SellingPrice"].mean().sort_values(ascending=False).head(5)
)

st.markdown(
    f"""
<div class="kpi-head">
  <div class="kpi-title">{icon("car", 24)} KPI Overview</div>
  <div class="live"><span class="badge-dot" style="width:7px;height:7px;background:#3FE0B0;
       box-shadow:0 0 10px #3FE0B0;margin-right:8px"></span>Live Data</div>
</div>
""",
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4, gap="medium")

# 1 — total cars ------------------------------------------------------------
with c1:
    with st.container(key="home_kpi_total"):
        st.markdown(
            f'<div class="kpi-card-title">'
            f'<span style="color:{NEON_BLUE}">{icon("car", 20)}</span> Total Cars Analyzed</div>'
            f'<div class="kpi-value">{len(df):,}</div>'
            + delta_block(pct_change(monthly["sales"])),
            unsafe_allow_html=True,
        )
        fig = go.Figure(
            go.Scatter(
                x=list(range(len(monthly))),
                y=monthly["sales"],
                mode="lines",
                line=dict(color=NEON_BLUE, width=3, shape="spline", smoothing=0.9),
                fill="tozeroy",
                fillcolor="rgba(76,141,255,.16)",
                hovertemplate="%{y:,} cars<extra></extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[len(monthly) - 1],
                y=[monthly["sales"].iloc[-1]],
                mode="markers",
                marker=dict(color="#FFFFFF", size=8, line=dict(color=NEON_VIOLET, width=3)),
                hoverinfo="skip",
            )
        )
        fig.update_layout(
            **mini_layout(
                height=132,
                showlegend=False,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=0, r=0, t=6, b=0),
            )
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# 2 — average price ---------------------------------------------------------
with c2:
    with st.container(key="home_kpi_avg"):
        st.markdown(
            f'<div class="kpi-card-title">'
            f'<span style="color:{NEON_VIOLET}">{icon("coins", 20)}</span> Average Price</div>'
            f'<div class="kpi-value">${df["SellingPrice"].mean():,.0f}</div>'
            + delta_block(pct_change(monthly["avg_price"])),
            unsafe_allow_html=True,
        )
        n = max(len(monthly), 1)
        bar_colors = [
            "rgba({:.0f},{:.0f},255,.92)".format(76 + (166 - 76) * t, 141 + (107 - 141) * t)
            for t in np.linspace(0, 1, n)
        ]
        fig = go.Figure(
            go.Bar(
                x=list(range(len(monthly))),
                y=monthly["avg_price"],
                marker=dict(color=bar_colors, line=dict(width=0)),
                hovertemplate="$%{y:,.0f}<extra></extra>",
            )
        )
        fig.update_layout(
            **mini_layout(
                height=132,
                showlegend=False,
                bargap=0.32,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=0, r=0, t=6, b=0),
            )
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# 3 — transmission mix ------------------------------------------------------
with c3:
    with st.container(key="home_kpi_mix"):
        st.markdown(
            f'<div class="kpi-card-title">'
            f'<span style="color:{NEON_CYAN}">{icon("drop", 20)}</span> Transmission Mix</div>',
            unsafe_allow_html=True,
        )
        d1, d2 = st.columns([1.05, 1])
        with d1:
            fig = go.Figure(
                go.Pie(
                    labels=list(trans.index),
                    values=list(trans.values),
                    hole=0.66,
                    sort=False,
                    textinfo="none",
                    marker=dict(
                        colors=DONUT_COLORS[: len(trans)],
                        line=dict(color="#070A18", width=3),
                    ),
                    hovertemplate="%{label}: %{percent}<extra></extra>",
                )
            )
            fig.update_layout(
                **mini_layout(
                    height=168,
                    showlegend=False,
                    margin=dict(l=0, r=0, t=4, b=4),
                )
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with d2:
            rows = "".join(
                f'<div class="legend-row"><i style="color:{DONUT_COLORS[i % len(DONUT_COLORS)]}"></i>'
                f"{label}<b>{pct:.0f}%</b></div>"
                for i, (label, pct) in enumerate(trans_pct.items())
            )
            st.markdown(f'<div class="legend">{rows}</div>', unsafe_allow_html=True)

# 4 — price by brand --------------------------------------------------------
with c4:
    with st.container(key="home_kpi_brand"):
        st.markdown(
            f'<div class="kpi-card-title">'
            f'<span style="color:#FFC857">{icon("star", 20)}</span> Price by Brand</div>',
            unsafe_allow_html=True,
        )
        top = brand_avg.max()
        gradients = [
            f"linear-gradient(90deg,{NEON_BLUE},{NEON_CYAN})",
            f"linear-gradient(90deg,{NEON_BLUE},{NEON_VIOLET})",
            f"linear-gradient(90deg,{NEON_VIOLET},{NEON_PINK})",
            f"linear-gradient(90deg,{NEON_CYAN},{NEON_BLUE})",
            f"linear-gradient(90deg,{NEON_MINT},{NEON_CYAN})",
        ]
        rows = "".join(
            f'<div class="brandrow"><span>{make.title()}</span>'
            f'<div><u style="width:{max(price / top * 100, 12):.0f}%;'
            f'background:{gradients[i % len(gradients)]}"></u></div>'
            f"<b>${price / 1000:.1f}K</b></div>"
            for i, (make, price) in enumerate(brand_avg.items())
        )
        st.markdown(f'<div class="brandlist">{rows}</div>', unsafe_allow_html=True)
