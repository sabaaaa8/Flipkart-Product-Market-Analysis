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


## 🔮 Future Improvements

1. **Predictive Pricing** — Train a regression model to predict optimal sale price
2. **Sentiment Analysis** — Analyse review text for positive/negative sentiment
3. **Real-time Scraping** — Replace static CSV with live Flipkart data via API
4. **User Auth** — Add login to save personal analysis sessions
5. **Export to PDF** — Generate a full PDF report from the dashboard
6. **Time-series** — Track price changes over time per product
7. **Recommendation Engine** — Suggest similar products based on category + rating

---


**Python Data Analytics Internship Project**
Built with Python · Pandas · Seaborn · Flask · Bootstrap 5

---

## 📄 License

MIT License — free to use and modify for educational purposes.
