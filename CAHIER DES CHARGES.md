# CAHIER DES CHARGES

**Project Title:** Four-Platform OTT & Global Box Office Intelligence System

**Author:** Lead Data Analyst

**Target Architecture:** Python (Pandas) / SQL Staging Engine & Power BI Desktop

## 1. Project Context & Business Drivers

### 1.1 Business Context

The contemporary entertainment market is starkly split between subscription-based digital streaming platforms (Over-The-Top / OTT) and traditional cinematic theatrical windows. Content acquisition managers, studio executives, and media distribution teams must routinely commit millions of dollars to license catalogs or greenlight international theatrical productions without a unified view of the market.

### 1.2 The Core Problem

Critical performance data is currently highly fragmented and siloed:

* Catalog metadata resides inside independent platform tracking files.
* Theatrical financial trackers operate completely isolated from digital streaming statistics.
* Inconsistent naming conventions, nested categories, and missing financial parameters prevent companies from understanding the lifecycle of a title from the theater to the streaming screen.

### 1.3 Project Purpose

This project delivers an end-to-end data engineering pipeline and an interactive Power BI analytics warehouse. By unifying data from **four competing streaming platforms** and  **two major cinematic box office regions (Hollywood & Bollywood)** , the system enables data-driven content licensing, competitive platform mapping, and clear investment ROI analysis.

## 2. Project Scope & Boundary Conditions

### 2.1 In-Scope Functional Areas

* **Platform Benchmarking:** Cross-analyzing content catalog depth, type ratios (Movies vs. TV Shows), and qualitative audience score distributions.
* **Financial ROI Tracking:** Evaluating the correlation between production budgets and global box office gross returns across Western and South Asian markets.
* **Trend & Saturation Analysis:** Isolating structural timeline shifts in content duration and regional output density from 2000 to the present day.

### 2.2 Out-of-Scope (Phase 2 Restrictions)

* Live web scraping of active user profiles.
* Real-time pricing adjustment automation or real-time streaming recommendation engine deployment.
* Predictive machine learning models for user churn forecasting.

## 3. Data Inventory & Mapping Specifications

The project architecture relies exclusively on the ingestion and normalization of six raw core tabular data files:

### 3.1 The Streaming Catalog Domain

* **`Netflix.csv`** : Contains complete platform library fields including type, director, cast arrays, production countries, and explicit binary genre flags.
* **`amazon_prime_titles.csv`** : Holds Amazon's metadata architecture, mirroring the fundamental catalog parameters found in the Netflix schema.
* **`apple.csv`** : Provides advanced qualitative metrics for Apple TV+ properties, including `age_certification`, `runtime`, `imdb_score`, `imdb_votes`, and `tmdb_popularity`.
* **`hotstar.csv`** : Tracks Disney+ Hotstar titles, managing structural running times and regional content type flags.

### 3.2 The Cinematic Box Office Domain

* **`Final Hollywood.csv`** : Financial tracking ledger for Western blockbusters, containing release dates, languages, production budgets, worldwide gross revenues, and localized audience rankings.
* *Data Quality Anomaly:* This file features a missing first-row header structure that must be programmatically rectified during ingestion.
* **`Final Bollywood.csv`** : Financial tracking ledger for the Indian cinematic market, capturing movie budgets, revenue generation matrices, original language parameters, and audience scores.

## 4. Technical Architecture & Medallion Pipeline Blueprint

To guarantee data consistency, lineage traceability, and high report-rendering performance, data moves sequentially through a structured, three-zone  **Medallion Architecture** .

```
  DATA SOURCES             INGEST (Bronze)             TRANSFORM (Silver)             STORE & MODEL (Gold)          VISUALIZATION
 ┌──────────────┐         ┌───────────────┐           ┌──────────────────┐           ┌────────────────────┐        ┌──────────────┐
 │ 4 Streaming  │ ──────► │  Raw Source   │  ───────► │ Clean data types │  ───────► │ Consolidated Fact  │ ─────► │   Power BI   │
 │ Files (CSVs) │         │   CSV Files   │  [Python/ │ Fix broken rows  │  [Star    │ & Summary Tables   │        │ Interactive  │
 ├──────────────┤         └───────────────┘  Power Q] │ Standardize keys │  Schema]  ├────────────────────┤        │  Dashboard   │
 │ Hollywood /  │                                     └──────────────────┘           │ Unified Relational │        │ (Final.pbix) │
 │ Bollywood    │                                                                    │ Data Model         │        └──────────────┘
 └──────────────┘                                                                    └────────────────────┘
```

### 4.1 Ingest Zone (Bronze / Raw Landing)

* **Objective:** Immediate file landing with zero structural manipulation.
* **Storage Rule:** Raw CSV file storage preserving all original null fields, multi-valued string lists, text encodings, and missing headers.

### 4.2 Transform Zone (Silver / Cleansing & Normalization)

* **Objective:** Structural harmonization and type casting.
* **Execution Mechanisms:** Handled programmatically via Python (Pandas) or Power BI's Power Query ETL pipeline.
* **Key Engineering Actions:**
  * **Schema Correction:** Injecting missing headers into the `Final Hollywood.csv` staging layer to prevent data misalignment.
  * **Column Alignment:** Standardizing text keys into uniform target labels (e.g., merging `release_year` vs. `year`, and `running_time` vs. `duration`).
  * **Financial Cleansing:** Converting string text budget and revenue fields into clean, unformatted numerical fields (`Int64`/`Float64`).
  * **Text Normalization:** Pruning trailing spaces and standardizing variable inputs (e.g., uniform mapping of country names and primary language groups).

### 4.3 Store & Model Zone (Gold / Presentation Warehouse)

* **Objective:** Optimized semantic data modeling tailored for low-latency BI visualization.
* **Structure:** Star Schema architecture featuring a centralized fact catalog linked to optimized dimensional lookups.

## 5. Relational Data Modeling (Star Schema Design)

Inside the Power BI desktop engine, the cleared data assets are structured into a multi-fact star schema configuration to guarantee clean filter propagation and rapid calculation execution.

```
                       ┌──────────────────────────┐
                       │        dim_years         │
                       └────────────┬─────────────┘
                                    │ (1:N)
                                    ▼
┌──────────────────┐      ┌─────────★────────┐       ┌─────────────────┐
│  dim_platforms   │ ───► │ streaming_catalog │ ◄───  │   dim_genres    │
└──────────────────┘ (1:N)│   (Fact Table)   │(1:N)  └─────────────────┘
                          └─────────▲────────┘
                                    │ (1:N)
                          ┌─────────┴────────┐
                          │  dim_countries   │
                          └──────────────────┘
```

* **Central Fact Asset (`streaming_catalog`)** : Tracks core unique title IDs, active platform distribution channels, conformed content durations, clean budgets, gross earnings, and audience rating metrics.
* **Dimension Tables (`dim_platforms`, `dim_genres`, `dim_countries`, `dim_years`)** : Maintain structured lookup profiles to support seamless, non-blocking slicing across all chart elements.

## 6. Functional & Visualization Requirements

The final dashboard layout (`Final.pbix`) must feature a cohesive visual storytelling flow split into four highly filtered analytical views:

### 6.1 View 1: Platform Catalog Profiles

* **Visual Elements:** KPI Cards, Donut Charts, and Side-by-Side Clustered Histograms.
* **Functionality:** Displays active catalog volumes (Movies vs. TV Shows) split among Netflix, Amazon Prime, Hotstar, and Apple TV+, paired with a matrix tracking average platform IMDb scores.

### 6.2 View 2: Financial Box Office Insights

* **Visual Elements:** Interactive Scatter Plots, Grouped Bar Charts, and Detail Matrices.
* **Functionality:** Plots Production Budget vs. Worldwide Gross Revenue to instantly isolate profitability outliers. Includes toggles to switch analysis dynamically between Hollywood and Bollywood markets.

### 6.3 View 3: Historical Content Trajectories

* **Visual Elements:** Trend Line Visuals and Area Charts.
* **Functionality:** Tracks content production volume growth alongside changing average movie running times across a time slider spanning from 1980 to the present day.

### 6.4 View 4: Global Distribution Map

* **Visual Elements:** Filled Choropleth Map and Drop-Down Slicers.
* **Functionality:** Tracks geographic content generation density by country, exposing exactly which regional hubs feed specific platform catalogs.

## 7. Key Performance Indicators (KPIs) Defined

The reporting layer will automatically compute the following four metric domains via Power BI DAX:

* **Financial Return on Investment (ROI):**
  $$
  \text{Theatrical ROI} = \frac{\text{Worldwide Box Office Revenue}}{\text{Production Budget}}
  $$
* **Platform Content Overlap %:** Calculates the percentage of shared properties vs. exclusive intellectual properties hosted per catalog channel.
* **Acclaim Disconnect Vector:** Highlights the statistical delta variance between critical industry evaluation ranks (`tmdb_popularity`) and true audience rating metrics (`imdb_score`).
* **Library Saturation Index:** Measures production volume distribution grouped by primary genre and origin region to highlight underrepresented content opportunities.

## 8. Constraints, Risks, and Assumptions

* **String Collision Risks:** Variations in text typography and spelling formats across files can lead to orphaned rows during joins; title strings must be normalized (lowercase, punctuation stripped) before key-matching.
* **Sparsity of Financial Columns:** Digital streaming catalog files do not natively feature asset production budgets, making matching with box office financials critical for valid revenue insights.
* **Temporal Boundaries:** Analysis boundaries must remain rigid between 1980 and the present year to avoid skewing historical baseline trend lines with incomplete antique data.

## 9. Core Deliverables

1. **Gold Storage Directory** : Cleaned, verified Gold CSV files (`streaming_catalog.csv` accompanied by structured dimension tables) ready for automated pipeline refreshes.
2. **`Final.pbix` Core File** : A fully configured Power BI dashboard file embedding the Star Schema data model, verified relationships, DAX formulas, and interactive dashboard layouts.
3. **Data Lineage Guide** : Technical summary documentation outlining the transformation functions used to align the 6 source files.
