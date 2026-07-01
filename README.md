# 📊 Flipkart Product Market Analysis

A complete Python Data Analytics internship project developed by Sabahat that explores 
Flipkart product data to identify pricing trends, product popularity, brand performance, 
and category-wise insights — served through a professional Flask dashboard.
— served through a professional Flask dashboard.

---

## 🚀 Features

| Feature | Description |
|---|---|
| **Dataset** | 1,100 rows, 15 columns of realistic Flipkart product data |
| **EDA** | Shape, dtypes, missing values, summary statistics |
| **Pricing Analysis** | Avg/min/max price, discount distribution histogram |
| **Brand Comparison** | Top 10 brands bar chart |
| **Category Analysis** | Category-wise product count bar chart |
| **Ratings Analysis** | Average rating per brand — horizontal bar chart |
| **Correlation Heatmap** | Seaborn heatmap of numeric feature correlations |
| **Popularity Analysis** | Top 10 most popular products bar chart |
| **Discount Analysis** | Top discounted products chart + table |
| **Seller Analysis** | Products per seller chart + cards |
| **Insights Report** | Auto-generated `insights.txt` with 20+ key findings |
| **Flask Dashboard** | Responsive Bootstrap 5 web dashboard |
| **Pickle Cache** | Processed data saved for fast subsequent loads |

---

## 🗂️ Folder Structure

```
Flipkart_Product_Market_Analysis/
│
├── app.py                        # Flask application entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
│
├── dataset/
│   ├── flipkart_products.csv     # Main dataset (1,100 rows)
│   └── generate_dataset.py       # Dataset generation script
│
├── static/
│   └── style.css                 # Custom CSS with design tokens
│
├── templates/
│   ├── index.html                # Home page / dashboard overview
│   └── report.html               # Full analysis report page
│
├── analysis/
│   └── analysis.py               # Complete EDA + chart generation module
│
├── graphs/                       # Auto-generated PNG charts
│   ├── pricing_distribution.png
│   ├── brand_comparison.png
│   ├── category_sales.png
│   ├── ratings_by_brand.png
│   ├── heatmap.png
│   ├── top_products.png
│   ├── discount_analysis.png
│   └── seller_analysis.png
│
├── reports/
│   └── insights.txt              # Auto-generated insights report
│
└── pickle/
    └── processed_data.pkl        # Pickled dataframe + analysis results
```

---

## 🛠️ Technologies Used

- **Python 3.10+** — Core language
- **Pandas** — Data loading, cleaning, aggregation
- **NumPy** — Numerical operations
- **Matplotlib** — Core chart rendering
- **Seaborn** — Statistical visualizations (heatmap)
- **Flask** — Web server and routing
- **Pickle** — Caching processed data
- **Bootstrap 5** — Responsive UI framework
- **Chart.js** — Interactive JavaScript charts on home page
- **Bootstrap Icons** — Icon library

---

## 📋 Dataset Information

| Column | Type | Description |
|---|---|---|
| `Product_ID` | str | Unique product identifier (FLP1000+) |
| `Product_Name` | str | Brand + product type + variant |
| `Brand` | str | Product brand name |
| `Category` | str | 8 top-level categories |
| `Sub_Category` | str | 40+ sub-categories |
| `Price` | float | Discounted sale price (₹) |
| `Original_Price` | float | MRP before discount (₹) |
| `Discount_Percentage` | int | Discount % (0–70) |
| `Rating` | float | Customer rating (1.0–5.0) |
| `Review_Count` | int | Number of reviews |
| `Availability` | str | In Stock / Out of Stock / Limited Stock |
| `Seller` | str | Seller platform name |
| `Delivery_Days` | int | Estimated delivery (1–10 days) |
| `Product_Popularity` | float | Popularity score (0–100) |
| `Stock_Status` | str | Available / Low Stock / Sold Out |

**Categories:** Electronics · Fashion · Home & Kitchen · Beauty · Books · Sports · Toys · Groceries

---

## ⚙️ Installation & Setup

### 1. Clone / Extract the project
```bash
cd Flipkart_Product_Market_Analysis
```

### 2. (Recommended) Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

The analysis runs automatically on first launch — all charts and the insights report
are generated and cached. Subsequent launches load from pickle for speed.

---

## 🖥️ Dashboard Pages

| Route | Description |
|---|---|
| `GET /` | Home page — KPIs, interactive Chart.js charts |
| `GET /report` | Full EDA report — all Matplotlib/Seaborn charts + tables |
| `GET /graphs/<file>` | Serve individual chart PNG |
| `GET /download/dataset` | Download `flipkart_products.csv` |
| `GET /download/insights` | Download `insights.txt` |
| `GET /api/stats` | JSON endpoint with live KPIs |

---

## 📸 Screenshots

> Place screenshots of the running dashboard here:

- `screenshots/home.png` — KPI cards and Chart.js charts
- `screenshots/report.png` — Graph gallery and insights
- `screenshots/heatmap.png` — Correlation heatmap

---

## 🔮 Future Improvements

1. **Predictive Pricing** — Train a regression model to predict optimal sale price
2. **Sentiment Analysis** — Analyse review text for positive/negative sentiment
3. **Real-time Scraping** — Replace static CSV with live Flipkart data via API
4. **User Auth** — Add login to save personal analysis sessions
5. **Export to PDF** — Generate a full PDF report from the dashboard
6. **Time-series** — Track price changes over time per product
7. **Recommendation Engine** — Suggest similar products based on category + rating

---

## 👨‍💻 Author

**Python Data Analytics Internship Project**
Built with Python · Pandas · Seaborn · Flask · Bootstrap 5

---

## 📄 License

MIT License — free to use and modify for educational purposes.
