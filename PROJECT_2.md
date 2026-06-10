# 🎬 PROJECT 2 — IMDb Multi-Dataset Movie Analytics System

## 🎯 Project Title

**“Analyzing Movie Success Factors Using IMDb Relational Datasets”**

---

## 🧠 1. Why this project?

The movie industry depends on multiple factors:

* Ratings
* Cast
* Genres
* Runtime
* Audience votes

This project aims to answer:

> “What factors influence a movie’s success and popularity?”

### 🎯 Objectives:

* Analyze movie trends over time
* Study relationship between cast, genre, and ratings
* Build a relational dataset like a real database system
* Perform structured analytical joins

---

## 🌐 2. Data Sources (IMDb Dataset)

IMDb Public Dataset:

[https://datasets.imdbws.com/]()

---

## 🧱 3. Data Tables (Schema)

### 🎬 Table 1 — Movies (Core Table)

| column         | description  |
| -------------- | ------------ |
| tconst         | movie ID     |
| primaryTitle   | movie name   |
| startYear      | release year |
| runtimeMinutes | duration     |
| genres         | genre list   |

---

### ⭐ Table 2 — Ratings

| column        | description     |
| ------------- | --------------- |
| tconst        | movie ID        |
| averageRating | IMDb rating     |
| numVotes      | number of votes |

---

### 🎭 Table 3 — Cast & Crew

| column     | description               |
| ---------- | ------------------------- |
| tconst     | movie ID                  |
| nconst     | person ID                 |
| category   | actor / director / writer |
| characters | role                      |

---

### 👤 Table 4 — People

| column            | description         |
| ----------------- | ------------------- |
| nconst            | person ID           |
| primaryName       | actor/director name |
| birthYear         | birth year          |
| primaryProfession | profession          |

---

### 🎞 Table 5 — Alternative Titles

| column   | description     |
| -------- | --------------- |
| tconst   | movie ID        |
| region   | country         |
| language | language        |
| title    | localized title |

---

## 🔗 4. How data is joined

### 🧩 Keys:

* `tconst` → movie identifier
* `nconst` → person identifier

### 🔗 Join logic:

### Step 1:

Movies ↔ Ratings

<pre class="overflow-visible! px-0!" data-start="5370" data-end="5412"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>movies.tconst = ratings.tconst</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></div></pre>

### Step 2:

Movies ↔ Cast

<pre class="overflow-visible! px-0!" data-start="5440" data-end="5485"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>movies.tconst = principals.tconst</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></div></pre>

### Step 3:

Cast ↔ People

<pre class="overflow-visible! px-0!" data-start="5513" data-end="5558"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>principals.nconst = people.nconst</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></div></pre>

---

## ⚙️ 5. Project Architecture

1. Load TSV datasets (IMDb files)
2. Clean missing values
3. Normalize relational structure
4. Perform joins (SQL or pandas)
5. Create analytical dataset
6. Build dashboards (Power BI / Tableau)

---

## 📊 6. Final Analysis

You can answer:

* What genres have highest ratings?
* Which actors appear in most successful movies?
* Does runtime affect rating?
* How ratings evolved over time?
* Which countries produce highest-rated movies?

---

## 🏁 Summary

This project represents:

✔ Real relational database modeling

✔ Data engineering (joins at scale)

✔ Statistical analysis

✔ Business intelligence reporting

---

# ⚖️ FINAL COMPARISON (for your teacher decision)

| Feature          | Stock Sentiment Project | IMDb Project                   |
| ---------------- | ----------------------- | ------------------------------ |
| APIs             | Yes (multiple)          | No (dataset-based)             |
| Complexity       | High (time + NLP)       | Medium-High (relational joins) |
| Data Engineering | Strong                  | Very strong                    |
| NLP              | Yes                     | No                             |
| Best for         | modern AI/finance       | classical data analysis        |
| Difficulty       | harder                  | more structured                |
