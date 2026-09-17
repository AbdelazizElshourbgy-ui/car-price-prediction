"""The 10 requested visualizations, ported 1:1 from the notebook (cells
10-28), reused by both the KPI Overview and Car Analysis pages."""

import plotly.express as px
from utils.theme import PLOTLY_LAYOUT, COLOR_SEQUENCE, MAIN_COLOR, ACCENT_COLOR, PINK_COLOR


def selling_price_distribution(df):
    fig = px.histogram(df, x="SellingPrice", nbins=50, color_discrete_sequence=[MAIN_COLOR])
    fig.update_layout(**PLOTLY_LAYOUT, title="Selling Price Distribution")
    return fig


def top_brands_by_sales(df, n=15):
    top_brands = df["Make"].value_counts().head(n).sort_values(ascending=True)
    fig = px.bar(
        x=top_brands.values, y=top_brands.index, orientation="h",
        title=f"Top {n} Most Sold Brands",
        labels={"x": "Number of Sales", "y": "Brand"},
        color=top_brands.values,
        color_continuous_scale=[MAIN_COLOR, ACCENT_COLOR, PINK_COLOR],
    )
    fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, yaxis_title="", xaxis_title="Number of Sales")
    fig.update_traces(marker_line_width=0, hovertemplate="<b>%{y}</b><br>Sales: %{x:,}<extra></extra>")
    return fig


def top_states_by_sales(df, n=15):
    top_states = df["State"].value_counts().head(n).sort_values(ascending=True)
    fig = px.bar(
        x=top_states.values, y=top_states.index, orientation="h",
        title=f"Top {n} States by Number of Sales",
        labels={"x": "Number of Sales", "y": "State"},
        color=top_states.values,
        color_continuous_scale=[ACCENT_COLOR, MAIN_COLOR, "#00E676"],
    )
    fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, yaxis_title="")
    fig.update_traces(marker_line_width=0, hovertemplate="<b>%{y}</b><br>Sales: %{x:,}<extra></extra>")
    return fig


def avg_price_by_top_brands(df, n=15):
    top_brands = df["Make"].value_counts().head(n).index
    brand_avg_price = (
        df[df["Make"].isin(top_brands)].groupby("Make")["SellingPrice"].mean().sort_values(ascending=False)
    )
    fig = px.bar(
        x=brand_avg_price.values, y=brand_avg_price.index, orientation="h",
        color_discrete_sequence=[MAIN_COLOR],
    )
    fig.update_layout(**PLOTLY_LAYOUT, title="Average Selling Price by Top Brands",
                       xaxis_title="Average Selling Price", yaxis_title="Brand")
    return fig


def monthly_sales_trend(df):
    monthly_sales = df.groupby("SaleMonth").size().reset_index(name="Sales")
    fig = px.line(monthly_sales, x="SaleMonth", y="Sales", title="Monthly Sales Trend", markers=True)
    fig.update_traces(
        line=dict(color=MAIN_COLOR, width=2),
        marker=dict(color=ACCENT_COLOR, size=7, line=dict(color="#FFFFFF", width=2)),
        hovertemplate="Month: %{x}<br>Sales: %{y:,}<extra></extra>",
    )
    fig.update_layout(**PLOTLY_LAYOUT, xaxis_title="Month", yaxis_title="Number of Sales")
    return fig


def price_by_transmission(df):
    fig = px.box(df, x="Transmission", y="SellingPrice", color="Transmission", color_discrete_sequence=COLOR_SEQUENCE)
    fig.update_layout(**PLOTLY_LAYOUT, title="Selling Price by Transmission",
                       xaxis_title="Transmission", yaxis_title="Selling Price", showlegend=False)
    fig.update_traces(marker=dict(outliercolor=PINK_COLOR))
    return fig


def price_by_body_type(df, n=8):
    top_body_types = df["Body"].value_counts().head(n).index
    body_data = df[df["Body"].isin(top_body_types)]
    fig = px.box(body_data, x="Body", y="SellingPrice", color="Body", color_discrete_sequence=COLOR_SEQUENCE)
    fig.update_layout(**PLOTLY_LAYOUT, title="Selling Price Distribution by Body Type",
                       xaxis_title="Body Type", yaxis_title="Selling Price", showlegend=False)
    fig.update_traces(marker=dict(outliercolor=PINK_COLOR))
    return fig


def car_age_vs_price(df, sample_size=20000, seed=42):
    sample = df.sample(min(sample_size, len(df)), random_state=seed)
    fig = px.scatter(sample, x="car_age", y="SellingPrice", color_discrete_sequence=[ACCENT_COLOR])
    fig.update_layout(**PLOTLY_LAYOUT, title="Car Age vs Selling Price",
                       xaxis_title="Car Age", yaxis_title="Selling Price")
    fig.update_traces(marker=dict(size=5, opacity=0.55))
    return fig


def odometer_vs_price(df, sample_size=20000, seed=42):
    sample = df.sample(min(sample_size, len(df)), random_state=seed)
    fig = px.scatter(sample, x="Odometer", y="SellingPrice", color_discrete_sequence=[MAIN_COLOR])
    fig.update_layout(**PLOTLY_LAYOUT, title="Odometer vs Selling Price",
                       xaxis_title="Odometer", yaxis_title="Selling Price")
    fig.update_traces(marker=dict(size=5, opacity=0.55))
    return fig


def mmr_vs_price(df, sample_size=20000, seed=42):
    sample = df.sample(min(sample_size, len(df)), random_state=seed)
    fig = px.scatter(sample, x="MMR", y="SellingPrice", color_discrete_sequence=[PINK_COLOR])
    fig.update_layout(**PLOTLY_LAYOUT, title="MMR vs Selling Price",
                       xaxis_title="MMR", yaxis_title="Selling Price")
    fig.update_traces(marker=dict(size=5, opacity=0.55))
    return fig
