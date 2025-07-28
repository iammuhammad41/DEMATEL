# DEMATEL Explorer

A lightweight Streamlit app for performing DEMATEL (Decision‑Making Trial and Evaluation Laboratory) analysis on your own influence matrices.

## Features

* Upload any square CSV of direct influences among factors
* Automatically normalize the matrix
* Compute the Total Relation matrix
* Calculate each factor’s

  * **r** (influence given)
  * **c** (influence received)
  * **Prominence** (r + c)
  * **Net Effect** (r − c)
* Classify factors into **Cause** (net > 0) or **Effect** (net < 0) groups
* Interactive bar charts of Prominence and Net Effect

## Installation

```bash
pip install streamlit pandas numpy altair
```

## Usage

```bash
streamlit run dematel_app.py
```

1. **Upload** your CSV (rows & columns = factors; cell \[i,j] = degree of i→j influence).
2. View the **Direct**, **Normalized**, and **Total Relation** matrices.
3. Explore the Prominence/Net Effect table and charts.

## Input Format

* **CSV** with header row and column
* Square matrix (N × N) of numeric influence scores

Example:

|        |  F1 |  F2 |  F3 |
| ------ | --: | --: | --: |
| **F1** | 0.0 | 0.2 | 0.1 |
| **F2** | 0.5 | 0.0 | 0.3 |
| **F3** | 0.4 | 0.1 | 0.0 |

## Methodology

1. **Normalize** by dividing by max(sum of any row, sum of any column).
2. **Total Relation**: T = D\_norm · (I − D\_norm)⁻¹
3. **r** = ∑ row of T, **c** = ∑ column of T
4. **Prominence** = r + c, **Net Effect** = r − c


