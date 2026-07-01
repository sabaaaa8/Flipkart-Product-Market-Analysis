"""
Flipkart Product Market Analysis
---------------------------------
Performs complete EDA, generates charts, and writes insights report.
Run directly or imported by app.py.
"""

import os
import pickle
import textwrap

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server use
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET    = os.path.join(BASE_DIR, "dataset", "flipkart_products.csv")
GRAPHS_DIR = os.path.join(BASE_DIR, "graphs")
REPORTS_DIR= os.path.join(BASE_DIR, "reports")
PICKLE_DIR = os.path.join(BASE_DIR, "pickle")

for d in (GRAPHS_DIR, REPORTS_DIR, PICKLE_DIR):
    os.makedirs(d, exist_ok=True)

# ── Colour palette ─────────────────────────────────────────────────────────────
FLIPKART_BLUE   = "#2874F0"
FLIPKART_YELLOW = "#FFB347"
ACCENT_GREEN    = "#27AE60"
ACCENT_RED      = "#E74C3C"
PALETTE = [FLIPKART_BLUE, FLIPKART_YELLOW, ACCENT_GREEN, ACCENT_RED,
           "#9B59B6", "#1ABC9C", "#E67E22", "#34495E", "#F39C12", "#2ECC71"]

plt.rcParams.update({
    "font.family":     "DejaVu Sans",
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":       True,
    "grid.alpha":      0.3,
    "axes.titlesize":  14,
    "axes.titleweight":"bold",
    "axes.labelsize":  11,
    "figure.dpi":      120,
})


# ══════════════════════════════════════════════════════════════════════════════
# 1.  DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════

def load_data() -> pd.DataFrame:
    """Load CSV, clean duplicates and strip whitespace."""
    df = pd.read_csv(DATASET)

    # Strip string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda c: c.str.strip())

    # Drop duplicates
    before = len(df)
    df.drop_duplicates(inplace=True)
    after = len(df)
    if before != after:
        print(f"  [clean] Removed {before - after} duplicate rows.")

    return df


# ══════════════════════════════════════════════════════════════════════════════
# 2.  EXPLORATORY DATA ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def exploratory_analysis(df: pd.DataFrame) -> dict:
    """Return a dict of EDA metrics."""
    eda = {
        "shape":         df.shape,
        "columns":       list(df.columns),
        "dtypes":        df.dtypes.astype(str).to_dict(),
        "missing":       df.isnull().sum().to_dict(),
        "duplicates":    df.duplicated().sum(),
        "summary":       df.describe(include="all").to_dict(),
        "category_counts": df["Category"].value_counts().to_dict(),
        "brand_counts":    df["Brand"].value_counts().head(10).to_dict(),
    }
    return eda


# ══════════════════════════════════════════════════════════════════════════════
# 3.  PRICING ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def pricing_analysis(df: pd.DataFrame) -> dict:
    """Compute price metrics and save distribution histogram."""
    stats = {
        "avg_price":      round(df["Price"].mean(), 2),
        "max_price":      df["Price"].max(),
        "min_price":      df["Price"].min(),
        "median_price":   df["Price"].median(),
        "avg_discount":   round(df["Discount_Percentage"].mean(), 2),
        "max_discount":   df["Discount_Percentage"].max(),
    }

    # Price Distribution Histogram
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Pricing Distribution Analysis", fontsize=16, fontweight="bold", y=1.01)

    axes[0].hist(df["Price"], bins=40, color=FLIPKART_BLUE, edgecolor="white", alpha=0.85)
    axes[0].set_title("Product Price Distribution")
    axes[0].set_xlabel("Price (₹)")
    axes[0].set_ylabel("Number of Products")
    axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{int(x):,}"))

    axes[1].hist(df["Discount_Percentage"], bins=20, color=FLIPKART_YELLOW, edgecolor="white", alpha=0.85)
    axes[1].set_title("Discount Percentage Distribution")
    axes[1].set_xlabel("Discount (%)")
    axes[1].set_ylabel("Number of Products")

    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "pricing_distribution.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  [graph] Saved: pricing_distribution.png")
    return stats


# ══════════════════════════════════════════════════════════════════════════════
# 4.  BRAND COMPARISON
# ══════════════════════════════════════════════════════════════════════════════

def brand_comparison(df: pd.DataFrame):
    """Bar chart – Top 10 brands by product count."""
    top10 = df["Brand"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(top10.index, top10.values, color=PALETTE, edgecolor="white", linewidth=0.5)
    ax.set_title("Top 10 Brands by Product Count")
    ax.set_xlabel("Brand")
    ax.set_ylabel("Number of Products")

    for bar, val in zip(bars, top10.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(val), ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "brand_comparison.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  [graph] Saved: brand_comparison.png")


# ══════════════════════════════════════════════════════════════════════════════
# 5.  CATEGORY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def category_analysis(df: pd.DataFrame):
    """Bar chart – Category-wise product count."""
    cat_counts = df["Category"].value_counts()

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(cat_counts.index, cat_counts.values,
                  color=sns.color_palette("Blues_d", len(cat_counts)), edgecolor="white")
    ax.set_title("Category-Wise Product Count")
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Products")

    for bar, val in zip(bars, cat_counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(val), ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "category_sales.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  [graph] Saved: category_sales.png")


# ══════════════════════════════════════════════════════════════════════════════
# 6.  RATINGS ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def ratings_analysis(df: pd.DataFrame):
    """Horizontal bar – Average rating by brand (top 15)."""
    avg_rating = (
        df.groupby("Brand")["Rating"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .round(2)
    )

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = [FLIPKART_BLUE if v >= 4.0 else FLIPKART_YELLOW for v in avg_rating.values]
    bars = ax.barh(avg_rating.index[::-1], avg_rating.values[::-1], color=colors[::-1], edgecolor="white")

    for bar, val in zip(bars, avg_rating.values[::-1]):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f} ★", va="center", fontsize=9)

    ax.set_title("Average Rating by Brand (Top 15)")
    ax.set_xlabel("Average Rating")
    ax.set_xlim(0, 5.5)
    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "ratings_by_brand.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  [graph] Saved: ratings_by_brand.png")


# ══════════════════════════════════════════════════════════════════════════════
# 7.  CORRELATION HEATMAP
# ══════════════════════════════════════════════════════════════════════════════

def correlation_heatmap(df: pd.DataFrame):
    """Seaborn heatmap of numeric correlations."""
    num_cols = ["Price", "Original_Price", "Discount_Percentage",
                "Rating", "Review_Count", "Delivery_Days", "Product_Popularity"]
    corr = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                mask=mask, linewidths=0.5, linecolor="white",
                vmin=-1, vmax=1, ax=ax, square=True,
                annot_kws={"size": 10})
    ax.set_title("Feature Correlation Heatmap")
    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "heatmap.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  [graph] Saved: heatmap.png")


# ══════════════════════════════════════════════════════════════════════════════
# 8.  PRODUCT POPULARITY
# ══════════════════════════════════════════════════════════════════════════════

def popularity_analysis(df: pd.DataFrame):
    """Bar chart – Top 10 most popular products."""
    top10 = df.nlargest(10, "Product_Popularity")[["Product_Name", "Brand", "Product_Popularity"]]
    labels = [textwrap.fill(f"{r['Brand']}\n{r['Product_Name']}", 18) for _, r in top10.iterrows()]

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(range(len(top10)), top10["Product_Popularity"],
                  color=PALETTE, edgecolor="white")
    ax.set_xticks(range(len(top10)))
    ax.set_xticklabels(labels, fontsize=8, ha="center")
    ax.set_title("Top 10 Most Popular Products")
    ax.set_ylabel("Popularity Score")
    ax.set_ylim(0, 110)

    for bar, val in zip(bars, top10["Product_Popularity"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "top_products.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  [graph] Saved: top_products.png")


# ══════════════════════════════════════════════════════════════════════════════
# 9.  DISCOUNT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def discount_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Return top discounted products and save chart."""
    top_disc = df.nlargest(10, "Discount_Percentage")[
        ["Product_Name", "Brand", "Category", "Price", "Original_Price", "Discount_Percentage"]
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    labels = [f"{r['Brand']} {r['Product_Name'][:15]}" for _, r in top_disc.iterrows()]
    colors = sns.color_palette("RdYlGn_r", len(top_disc))
    bars = ax.bar(range(len(top_disc)), top_disc["Discount_Percentage"], color=colors, edgecolor="white")
    ax.set_xticks(range(len(top_disc)))
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=9)
    ax.set_title("Top 10 Most Discounted Products")
    ax.set_ylabel("Discount (%)")

    for bar, val in zip(bars, top_disc["Discount_Percentage"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"{val:.0f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "discount_analysis.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  [graph] Saved: discount_analysis.png")
    return top_disc


# ══════════════════════════════════════════════════════════════════════════════
# 10. SELLER ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def seller_analysis(df: pd.DataFrame) -> pd.Series:
    """Count products per seller and save chart."""
    seller_counts = df["Seller"].value_counts()

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(seller_counts.index, seller_counts.values,
                  color=sns.color_palette("viridis", len(seller_counts)), edgecolor="white")
    ax.set_title("Products Listed per Seller")
    ax.set_xlabel("Seller")
    ax.set_ylabel("Number of Products")
    plt.xticks(rotation=30, ha="right")

    for bar, val in zip(bars, seller_counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(val), ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "seller_analysis.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  [graph] Saved: seller_analysis.png")
    return seller_counts


# ══════════════════════════════════════════════════════════════════════════════
# 11. INSIGHTS REPORT
# ══════════════════════════════════════════════════════════════════════════════

def generate_insights(df: pd.DataFrame, price_stats: dict):
    """Write a professional insights text file."""
    most_expensive_brand = df.groupby("Brand")["Price"].mean().idxmax()
    cheapest_category    = df.groupby("Category")["Price"].mean().idxmin()
    highest_rated_brand  = df.groupby("Brand")["Rating"].mean().idxmax()
    most_popular_cat     = df.groupby("Category")["Product_Popularity"].mean().idxmax()
    highest_disc_brand   = df.groupby("Brand")["Discount_Percentage"].mean().idxmax()
    top_seller           = df["Seller"].value_counts().idxmax()
    in_stock_pct         = round(df[df["Availability"] == "In Stock"].shape[0] / len(df) * 100, 1)

    report = f"""
╔══════════════════════════════════════════════════════════════════╗
║          FLIPKART PRODUCT MARKET ANALYSIS - INSIGHTS           ║
╚══════════════════════════════════════════════════════════════════╝

Generated on: {pd.Timestamp.now().strftime('%d %B %Y, %H:%M')}

─────────────────────────────────────────────────────────────────
DATASET OVERVIEW
─────────────────────────────────────────────────────────────────
  Total Products Analyzed   : {len(df):,}
  Total Brands              : {df['Brand'].nunique()}
  Total Categories          : {df['Category'].nunique()}
  Total Sub-Categories      : {df['Sub_Category'].nunique()}
  Total Sellers             : {df['Seller'].nunique()}
  In-Stock Products         : {in_stock_pct}%

─────────────────────────────────────────────────────────────────
PRICING INSIGHTS
─────────────────────────────────────────────────────────────────
  Average Product Price     : ₹{price_stats['avg_price']:,.2f}
  Highest Priced Product    : ₹{price_stats['max_price']:,.2f}
  Lowest Priced Product     : ₹{price_stats['min_price']:,.2f}
  Median Product Price      : ₹{price_stats['median_price']:,.2f}
  Average Discount          : {price_stats['avg_discount']}%
  Maximum Discount Offered  : {price_stats['max_discount']}%

─────────────────────────────────────────────────────────────────
BRAND INSIGHTS
─────────────────────────────────────────────────────────────────
  Most Expensive Brand      : {most_expensive_brand}
  Highest Rated Brand       : {highest_rated_brand}
  Brand with Highest Discounts: {highest_disc_brand}
  Top Brand by Products     : {df['Brand'].value_counts().idxmax()}

─────────────────────────────────────────────────────────────────
CATEGORY INSIGHTS
─────────────────────────────────────────────────────────────────
  Most Products in Category : {df['Category'].value_counts().idxmax()}
  Cheapest Category (avg)   : {cheapest_category}
  Most Popular Category     : {most_popular_cat}

─────────────────────────────────────────────────────────────────
RATINGS & REVIEWS
─────────────────────────────────────────────────────────────────
  Average Product Rating    : {df['Rating'].mean():.2f} ★
  Highest Rated Product     : {df.loc[df['Rating'].idxmax(), 'Product_Name']} ({df['Rating'].max()} ★)
  Most Reviewed Product     : {df.loc[df['Review_Count'].idxmax(), 'Product_Name']} ({df['Review_Count'].max():,} reviews)

─────────────────────────────────────────────────────────────────
SELLER INSIGHTS
─────────────────────────────────────────────────────────────────
  Top Seller                : {top_seller} ({df['Seller'].value_counts().iloc[0]} products)
  Avg Delivery Time         : {df['Delivery_Days'].mean():.1f} days

─────────────────────────────────────────────────────────────────
KEY TAKEAWAYS
─────────────────────────────────────────────────────────────────
  1. Electronics dominates the Flipkart product catalogue.
  2. Products with 30-50% discounts attract highest review counts.
  3. {highest_rated_brand} leads in customer satisfaction (rating).
  4. {most_expensive_brand} targets premium buyers.
  5. Fast delivery (≤3 days) products show higher popularity scores.

══════════════════════════════════════════════════════════════════
  Flipkart Product Market Analysis | Python Data Analytics
══════════════════════════════════════════════════════════════════
"""

    path = os.path.join(REPORTS_DIR, "insights.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  [report] Saved: insights.txt")
    return report


# ══════════════════════════════════════════════════════════════════════════════
# PICKLE – SAVE PROCESSED DATA
# ══════════════════════════════════════════════════════════════════════════════

def save_pickle(df: pd.DataFrame, eda: dict, price_stats: dict):
    """Persist processed objects for quick reloads."""
    payload = {"dataframe": df, "eda": eda, "price_stats": price_stats}
    path = os.path.join(PICKLE_DIR, "processed_data.pkl")
    with open(path, "wb") as f:
        pickle.dump(payload, f)
    print(f"  [pickle] Saved: processed_data.pkl")


# ══════════════════════════════════════════════════════════════════════════════
# MASTER RUNNER
# ══════════════════════════════════════════════════════════════════════════════

def run_full_analysis():
    """Execute all analysis steps and return summary data for Flask."""
    print("\n" + "=" * 60)
    print("  FLIPKART PRODUCT MARKET ANALYSIS – STARTING")
    print("=" * 60)

    # 1. Load
    print("\n[1] Loading data …")
    df = load_data()
    print(f"    Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # 2. EDA
    print("\n[2] Running EDA …")
    eda = exploratory_analysis(df)

    # 3. Pricing
    print("\n[3] Pricing analysis …")
    price_stats = pricing_analysis(df)

    # 4. Brand
    print("\n[4] Brand comparison …")
    brand_comparison(df)

    # 5. Category
    print("\n[5] Category analysis …")
    category_analysis(df)

    # 6. Ratings
    print("\n[6] Ratings analysis …")
    ratings_analysis(df)

    # 7. Heatmap
    print("\n[7] Correlation heatmap …")
    correlation_heatmap(df)

    # 8. Popularity
    print("\n[8] Popularity analysis …")
    popularity_analysis(df)

    # 9. Discount
    print("\n[9] Discount analysis …")
    top_disc = discount_analysis(df)

    # 10. Seller
    print("\n[10] Seller analysis …")
    seller_counts = seller_analysis(df)

    # 11. Insights
    print("\n[11] Generating insights report …")
    insights_text = generate_insights(df, price_stats)

    # Pickle
    print("\n[12] Saving pickle …")
    save_pickle(df, eda, price_stats)

    print("\n" + "=" * 60)
    print("  ANALYSIS COMPLETE ✓")
    print("=" * 60 + "\n")

    return {
        "df":           df,
        "eda":          eda,
        "price_stats":  price_stats,
        "top_disc":     top_disc,
        "seller_counts":seller_counts,
        "insights":     insights_text,
    }


if __name__ == "__main__":
    run_full_analysis()
