import datetime
import streamlit as st

from utils.theme import render_topbar, apply_page_style
from utils.data_loader import load_raw_data, load_clean_data
from utils.ml_utils import load_models_and_results, best_model_name


# ============================================================
# PAGE SETUP
# ============================================================

apply_page_style("Report", page_icon="📄")

render_topbar(active="Report")

st.title("📄 Project Report")

st.markdown(
    "<p class='section-caption'>An auto-generated summary of the dataset, the cleaning "
    "pipeline, and model performance — download it as Markdown or PDF below.</p>",
    unsafe_allow_html=True,
)


# ============================================================
# LOAD DATA
# ============================================================

raw = load_raw_data()
df = load_clean_data()
models, results_df, meta = load_models_and_results()

best_name = best_model_name(results_df)
best_row = results_df[results_df["Model"] == best_name].iloc[0]


# ============================================================
# CALCULATED METRICS
# ============================================================

top_brand = df["Make"].value_counts().idxmax()
top_brand_share = df["Make"].value_counts(normalize=True).max() * 100

top_state = df["State"].value_counts().idxmax()
top_body = df["Body"].value_counts().idxmax()

avg_age = df["car_age"].mean()
avg_price = df["SellingPrice"].mean()
avg_mmr = df["MMR"].mean()

price_vs_mmr = (avg_price - avg_mmr) / avg_mmr * 100

monthly = df.groupby("SaleMonth")["SellingPrice"].count()

peak_month = monthly.idxmax()
low_month = monthly.idxmin()

generated_on = datetime.date.today().strftime("%Y-%m-%d")


# ============================================================
# ON-SCREEN REPORT
# ============================================================

st.markdown("## 1. Executive Summary")

st.write(
    f"This report covers **{len(df):,}** cleaned vehicle sale records "
    f"(from **{len(raw):,}** raw records) spanning "
    f"**{df['SaleDate'].dt.year.min()}–{df['SaleDate'].dt.year.max()}**. "
    f"The average selling price is **${avg_price:,.0f}**, "
    f"about **{price_vs_mmr:+.1f}%** relative to the average MMR "
    f"(${avg_mmr:,.0f}). The best-performing model, **{best_name}**, explains "
    f"**{best_row['Test_R2'] * 100:.1f}%** of the variance in log-price on unseen data."
)


st.markdown("## 2. Dataset Overview")

st.write(
    f"- **{len(df):,}** records, **{df['Make'].nunique()}** brands, "
    f"**{df['Model'].nunique()}** models, **{df['State'].nunique()}** states.\n"
    f"- Most common brand: **{top_brand.title()}** (**{top_brand_share:.1f}%** of sales).\n"
    f"- Most common state: **{top_state.upper()}**.\n"
    f"- Most common body type: **{top_body}**.\n"
    f"- Average car age at sale: **{avg_age:.1f} years**.\n"
    f"- Sales peak in month **{int(peak_month)}** and are lowest in month **{int(low_month)}**."
)


st.markdown("## 3. Data Cleaning Summary")

st.write(
    f"Of the **{len(raw):,}** raw records, **{len(raw) - len(df):,}** were removed "
    f"(missing Make/Model or VIN). Remaining gaps in Body, Transmission, Condition, "
    f"Odometer, Color, Interior, MMR, SellingPrice, and SaleDate were imputed using "
    f"Make/Model-level medians and modes — see the **Data Description** page for the "
    f"full step-by-step breakdown."
)


st.markdown("## 4. Model Performance")

st.dataframe(
    results_df,
    use_container_width=True
)

st.write(
    f"**{best_name}** is the best model by Test R² "
    f"(**{best_row['Test_R2']:.3f}**), with a test MAE of "
    f"**{best_row['Test_MAE']:.3f}** and RMSE of "
    f"**{best_row['Test_RMSE']:.3f}** "
    f"on the log-price scale."
)


st.markdown("## 5. Key Takeaways")

st.write(
    f"- Selling price tracks MMR closely, confirming MMR is the strongest single "
    f"signal for price.\n"
    f"- Car age and odometer both show a negative relationship with price, as "
    f"expected.\n"
    f"- **{top_brand.title()}** dominates sales volume; average price varies "
    f"meaningfully by brand and body type (see **Car Analysis**).\n"
    f"- Tree-based/boosted models capture non-linear pricing effects that plain "
    f"linear regression misses — compare Train vs Test R² on the **ML Models** page "
    f"to check for overfitting before deploying any single model."
)


st.markdown("---")


# ============================================================
# MARKDOWN REPORT
# ============================================================

def build_markdown_report() -> str:

    lines = [
        "# Car Sales Intelligence — Project Report",
        f"*Generated on {generated_on}*",
        "",
        "## 1. Executive Summary",
        f"{len(df):,} cleaned records ({len(raw):,} raw) covering "
        f"{df['SaleDate'].dt.year.min()}–{df['SaleDate'].dt.year.max()}. "
        f"Average selling price ${avg_price:,.0f} ({price_vs_mmr:+.1f}% vs average MMR "
        f"${avg_mmr:,.0f}). Best model: **{best_name}** "
        f"(Test R² {best_row['Test_R2']:.3f}).",
        "",
        "## 2. Dataset Overview",
        f"- Records: {len(df):,}",
        f"- Brands: {df['Make'].nunique()}  |  Models: {df['Model'].nunique()}  |  States: {df['State'].nunique()}",
        f"- Top brand: {top_brand.title()} ({top_brand_share:.1f}% of sales)",
        f"- Top state: {top_state.upper()}",
        f"- Top body type: {top_body}",
        f"- Average car age at sale: {avg_age:.1f} years",
        f"- Peak sales month: {int(peak_month)}  |  Lowest sales month: {int(low_month)}",
        "",
        "## 3. Data Cleaning Summary",
        f"{len(raw) - len(df):,} of {len(raw):,} raw rows were dropped "
        f"(missing Make/Model or VIN). Remaining gaps were imputed using Make/Model-level "
        f"medians and modes for Body, Transmission, Condition, Odometer, Color, "
        f"Interior, MMR, SellingPrice, and SaleDate.",
        "",
        "## 4. Model Performance",
        "",
        "| Model | Train R2 | Train MAE | Train RMSE | Test R2 | Test MAE | Test RMSE |",
        "|---|---|---|---|---|---|---|",
    ]

    for _, row in results_df.iterrows():

        lines.append(
            f"| {row['Model']} | "
            f"{row['Train_R2']:.4f} | "
            f"{row['Train_MAE']:.4f} | "
            f"{row['Train_RMSE']:.4f} | "
            f"{row['Test_R2']:.4f} | "
            f"{row['Test_MAE']:.4f} | "
            f"{row['Test_RMSE']:.4f} |"
        )

    lines += [
        "",
        f"Best model: **{best_name}** "
        f"(Test R² {best_row['Test_R2']:.3f}, "
        f"Test MAE {best_row['Test_MAE']:.3f}, "
        f"Test RMSE {best_row['Test_RMSE']:.3f}).",
        "",
        "## 5. Key Takeaways",
        "- Selling price tracks MMR closely; MMR is the strongest single price signal.",
        "- Car age and odometer both correlate negatively with price.",
        f"- {top_brand.title()} dominates sales volume; price varies by brand and body type.",
        "- Compare Train vs Test R² before deploying any single model, to check for overfitting.",
    ]

    return "\n".join(lines)


# ============================================================
# PDF HELPERS
# ============================================================

def sanitize_for_pdf(text: str) -> str:
    """
    Convert Unicode characters that Helvetica/core PDF fonts
    cannot handle into safe Latin-1 characters.

    No external font is required.
    """

    replacements = {
        # Dashes
        "\u2013": "-",   # en dash
        "\u2014": "-",   # em dash
        "\u2012": "-",   # figure dash
        "\u2010": "-",   # hyphen
        "\u2212": "-",   # minus sign

        # Quotes
        "\u2018": "'",
        "\u2019": "'",
        "\u201a": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u201e": '"',

        # Math / symbols
        "\u00b2": "2",
        "\u00b3": "3",
        "\u00b9": "1",
        "\u2192": "->",
        "\u2190": "<-",
        "\u2194": "<->",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u2260": "!=",
        "\u00d7": "x",
        "\u00b1": "+/-",

        # Bullets and dots
        "\u2022": "-",
        "\u2023": "-",
        "\u2043": "-",
        "\u2026": "...",

        # Spaces
        "\u00a0": " ",
        "\t": "    ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Final safety conversion.
    # Helvetica is a Latin-1/core font.
    text = text.encode("latin-1", errors="replace").decode("latin-1")

    return text


def build_pdf_report(markdown_text: str) -> bytes:
    """
    Build a PDF using only FPDF core fonts.

    No external .ttf/.otf font is required.
    """

    from fpdf import FPDF

    pdf = FPDF()

    # Page configuration
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)
    pdf.add_page()

    # Core PDF font - no external font needed
    pdf.set_font("Helvetica", size=10)

    # Available page width
    available_width = (
        pdf.w
        - pdf.l_margin
        - pdf.r_margin
    )

    # Process every Markdown line
    for raw_line in markdown_text.splitlines():

        # Remove Markdown formatting
        line = (
            raw_line
            .replace("**", "")
            .replace("*", "")
            .replace("###", "")
            .replace("##", "")
            .replace("#", "")
        )

        # Turn Markdown table separators into normal text
        line = line.replace("|", " | ")

        # Remove/replace unsupported Unicode
        line = sanitize_for_pdf(line)

        # Empty line
        if not line.strip():
            pdf.ln(3)
            continue

        # ----------------------------------------------------
        # IMPORTANT:
        # Split very long strings manually.
        # This prevents:
        #
        # "Not enough horizontal space to render a single character"
        # ----------------------------------------------------

        max_chars = 80

        if len(line) > max_chars:

            chunks = [
                line[i:i + max_chars]
                for i in range(0, len(line), max_chars)
            ]

            for chunk in chunks:

                chunk = chunk.strip()

                if not chunk:
                    continue

                try:
                    # Newer fpdf2
                    pdf.multi_cell(
                        w=available_width,
                        h=6,
                        text=chunk,
                        wrapmode="CHAR",
                    )

                except TypeError:
                    # Compatibility with older fpdf2
                    pdf.multi_cell(
                        available_width,
                        6,
                        chunk,
                    )

        else:

            try:
                # Newer fpdf2
                pdf.multi_cell(
                    w=available_width,
                    h=6,
                    text=line,
                    wrapmode="CHAR",
                )

            except TypeError:
                # Compatibility with older fpdf2
                pdf.multi_cell(
                    available_width,
                    6,
                    line,
                )

    # Return PDF bytes
    return bytes(pdf.output())


# ============================================================
# DOWNLOADS
# ============================================================

md_report = build_markdown_report()

dl1, dl2 = st.columns(2)


# ------------------------------------------------------------
# MARKDOWN DOWNLOAD
# ------------------------------------------------------------

with dl1:

    st.download_button(
        "⬇️ Download report (Markdown)",
        data=md_report,
        file_name=f"car_sales_report_{generated_on}.md",
        mime="text/markdown",
        use_container_width=True,
    )


# ------------------------------------------------------------
# PDF DOWNLOAD
# ------------------------------------------------------------

with dl2:

    try:

        pdf_bytes = build_pdf_report(md_report)

        st.download_button(
            "⬇️ Download report (PDF)",
            data=pdf_bytes,
            file_name=f"car_sales_report_{generated_on}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    except ImportError:

        st.button(
            "⬇️ Download report (PDF) — install `fpdf2`",
            disabled=True,
            use_container_width=True,
        )

    except Exception as e:

        st.error(
            f"Could not generate PDF report: {str(e)}"
        )
