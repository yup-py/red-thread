# 📊 PROJECT 1 — Financial Sentiment Impact on Stock Market Movements

## 🎯 Project Title

**“Analyzing the Impact of News and Social Media Sentiment on Stock Price Movements”**

---

## 🧠 1. Why this project?

Financial markets are not driven only by numbers, but also by  **human emotions and information flow** .

This project aims to study:

> “Do news headlines and social media discussions influence stock price movements?”

### 🎯 Objectives:

* Understand relationship between sentiment and stock price changes
* Measure how news and Reddit discussions affect market behavior
* Build a data pipeline combining multiple real-world APIs
* Create a unified dataset for financial analysis

---

## 🌐 2. Data Sources (APIs)

### 📊 Stock Data

* Alpha Vantage API

  [https://www.alphavantage.co/](https://www.alphavantage.co/)

Provides:

* Open, High, Low, Close prices
* Volume
* Daily time series

---

### 📰 News Data

* NewsAPI

  [https://newsapi.org/](https://newsapi.org/)

Provides:

* Articles about companies
* Titles, descriptions, dates, sources

---

### 💬 Social Media Data

* Reddit API (PRAW)

  [https://www.reddit.com/dev/api/](https://www.reddit.com/dev/api/)

Provides:

* Posts about companies
* Comments, upvotes, engagement

---

## 🧱 3. Data Tables (Schema)

### 📈 Table 1 — Stock Prices

| column | description                   |
| ------ | ----------------------------- |
| date   | trading date                  |
| symbol | company ticker (AAPL, TSLA…) |
| open   | opening price                 |
| close  | closing price                 |
| high   | daily high                    |
| low    | daily low                     |
| volume | trading volume                |

---

### 📰 Table 2 — News Articles

| column          | description      |
| --------------- | ---------------- |
| article_id      | unique id        |
| date            | publication date |
| company         | related company  |
| title           | headline         |
| description     | article summary  |
| sentiment_score | NLP result       |

---

### 💬 Table 3 — Reddit Posts

| column          | description     |
| --------------- | --------------- |
| post_id         | unique id       |
| date            | post date       |
| company         | mentioned stock |
| text            | post content    |
| upvotes         | engagement      |
| sentiment_score | NLP result      |

---

### 🧠 Table 4 — Derived Metrics (Final Dataset)

| column               | description          |
| -------------------- | -------------------- |
| date                 | aligned date         |
| symbol               | stock                |
| close_price          | stock value          |
| news_sentiment_avg   | aggregated sentiment |
| reddit_sentiment_avg | aggregated sentiment |
| news_volume          | number of articles   |
| reddit_hype_score    | engagement index     |
| return               | % price change       |

---

## 🔗 4. How data is joined

The core joins are based on:

### 🧩 Keys:

* `symbol` (company identifier)
* `date` (time alignment)

### 🔗 Join logic:

* Stock table is the **main reference table**
* News and Reddit are aggregated per:
* company
* day

### Example:

<pre class="overflow-visible! px-0!" data-start="2779" data-end="2877"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>Stock (AAPL, 2026-01-01)</span><br/><span>JOIN News (Apple, 2026-01-01)</span><br/><span>JOIN Reddit (Apple, 2026-01-01)</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></div></pre>

---

## ⚙️ 5. Project Architecture

1. Data extraction from APIs
2. Cleaning + preprocessing
3. Sentiment analysis (NLP)
4. Aggregation per company/day
5. Storage in database (SQLite/PostgreSQL)
6. Visualization dashboard (Power BI / Streamlit)

---

## 📊 6. Final Output

* Correlation between sentiment and stock price
* Time lag analysis (does sentiment predict price changes?)
* Market reaction to news vs social media
* Trend visualization dashboard

---

## 🏁 Summary

This project combines:

✔ Data Engineering (ETL pipeline)

✔ Data Analysis (time series)

✔ NLP (sentiment analysis)

✔ Business Intelligence (dashboard)
