"""
Flipkart Product Market Analysis – Flask Dashboard
===================================================
Entry point. Run:  python app.py
Then open:        http://127.0.0.1:5000
"""

import os
import json
import pickle

from flask import Flask, render_template, send_file, jsonify

# ── Import our analysis module ─────────────────────────────────────────────
from analysis.analysis import run_full_analysis

app = Flask(__name__)

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
PICKLE_PATH = os.path.join(BASE_DIR, "pickle", "processed_data.pkl")
DATASET_PATH= os.path.join(BASE_DIR, "dataset", "flipkart_products.csv")
INSIGHTS_PATH = os.path.join(BASE_DIR, "reports", "insights.txt")

# ── Run / load analysis at startup ────────────────────────────────────────

def get_analysis_data():
    """Return cached data from pickle or run fresh analysis."""
    if os.path.exists(PICKLE_PATH):
        with open(PICKLE_PATH, "rb") as f:
            payload = pickle.load(f)
        return payload
    return run_full_analysis()


# Run analysis once at startup
print("\n  Starting Flipkart Market Analysis Dashboard …")
results = run_full_analysis()
df           = results["df"]
eda          = results["eda"]
price_stats  = results["price_stats"]
top_disc     = results["top_disc"]
seller_counts= results["seller_counts"]


# ── Helper: list available graph files ───────────────────────────────────

GRAPH_META = [
    {"file": "pricing_distribution.png", "title": "Pricing Distribution",  "desc": "Histogram of product prices and discount percentages"},
    {"file": "brand_comparison.png",     "title": "Brand Comparison",      "desc": "Top 10 brands by number of products listed"},
    {"file": "category_sales.png",       "title": "Category Analysis",     "desc": "Product count split across all categories"},
    {"file": "ratings_by_brand.png",     "title": "Ratings by Brand",      "desc": "Average customer rating for top 15 brands"},
    {"file": "heatmap.png",              "title": "Correlation Heatmap",   "desc": "Seaborn heatmap of numeric feature correlations"},
    {"file": "top_products.png",         "title": "Top Popular Products",  "desc": "Top 10 products ranked by popularity score"},
    {"file": "discount_analysis.png",    "title": "Discount Analysis",     "desc": "Products offering the highest discount percentages"},
    {"file": "seller_analysis.png",      "title": "Seller Analysis",       "desc": "Number of products listed by each seller"},
]


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """Home page – dataset overview and KPI cards."""
    category_dist = df["Category"].value_counts().to_dict()
    brand_top10   = df["Brand"].value_counts().head(10).to_dict()

    # Rating distribution buckets
    bins   = [0, 2, 3, 4, 5]
    labels = ["1-2 ★", "2-3 ★", "3-4 ★", "4-5 ★"]
    rating_dist = {}
    for i, lbl in enumerate(labels):
        rating_dist[lbl] = int(((df["Rating"] > bins[i]) & (df["Rating"] <= bins[i + 1])).sum())

    context = {
        "total_products":   f"{len(df):,}",
        "total_brands":     df["Brand"].nunique(),
        "total_categories": df["Category"].nunique(),
        "total_sellers":    df["Seller"].nunique(),
        "avg_price":        f"₹{price_stats['avg_price']:,.0f}",
        "avg_discount":     f"{price_stats['avg_discount']}%",
        "avg_rating":       f"{df['Rating'].mean():.2f}",
        "in_stock_pct":     f"{round(df[df['Availability']=='In Stock'].shape[0]/len(df)*100, 1)}%",
        # Chart data (JSON strings)
        "category_labels":  json.dumps(list(category_dist.keys())),
        "category_values":  json.dumps(list(category_dist.values())),
        "brand_labels":     json.dumps(list(brand_top10.keys())),
        "brand_values":     json.dumps(list(brand_top10.values())),
        "rating_labels":    json.dumps(list(rating_dist.keys())),
        "rating_values":    json.dumps(list(rating_dist.values())),
    }
    return render_template("index.html", **context)


@app.route("/report")
def report():
    """Analysis report page – displays all charts and insights."""
    # Top discounted products table
    top_disc_list = top_disc[
        ["Product_Name", "Brand", "Category", "Price", "Original_Price", "Discount_Percentage"]
    ].to_dict("records")

    # Seller counts table
    seller_table = [{"Seller": k, "Products": v} for k, v in seller_counts.items()]

    # Read insights text
    insights_text = ""
    if os.path.exists(INSIGHTS_PATH):
        with open(INSIGHTS_PATH, "r", encoding="utf-8") as f:
            insights_text = f.read()

    context = {
        "graphs":       GRAPH_META,
        "top_disc":     top_disc_list,
        "seller_table": seller_table,
        "insights":     insights_text,
        "eda_shape":    eda["shape"],
        "eda_missing":  eda["missing"],
        "price_stats":  price_stats,
    }
    return render_template("report.html", **context)


@app.route("/graphs/<filename>")
def serve_graph(filename):
    """Serve graph images."""
    graph_path = os.path.join(BASE_DIR, "graphs", filename)
    if os.path.exists(graph_path):
        return send_file(graph_path, mimetype="image/png")
    return "Graph not found", 404


@app.route("/download/dataset")
def download_dataset():
    """Download the CSV dataset."""
    return send_file(DATASET_PATH, as_attachment=True, download_name="flipkart_products.csv")


@app.route("/download/insights")
def download_insights():
    """Download the insights text report."""
    return send_file(INSIGHTS_PATH, as_attachment=True, download_name="flipkart_insights.txt")


@app.route("/api/stats")
def api_stats():
    """JSON endpoint for live KPI data."""
    return jsonify({
        "total_products":   len(df),
        "avg_price":        price_stats["avg_price"],
        "avg_discount":     price_stats["avg_discount"],
        "avg_rating":       round(df["Rating"].mean(), 2),
        "top_brand":        df["Brand"].value_counts().idxmax(),
        "top_category":     df["Category"].value_counts().idxmax(),
    })


# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n  Dashboard ready → http://127.0.0.1:5000\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
