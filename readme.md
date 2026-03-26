# 🎓 Student Performance Analyzer

A modern, interactive **Streamlit-based analytics dashboard** for analyzing student performance across multiple subjects — with **no database required**.

This project uses **in-memory data storage**, making it lightweight, fast, and easy to deploy anywhere.

---

## 🚀 Features

### 📊 Dashboard Analytics

* Class performance overview
* Topper identification 🏆
* Highest & lowest scorers
* Pass/Fail statistics
* Subject-wise averages

### 📈 Visualizations

* Bar charts (subject averages)
* Grade distribution charts
* Radar chart (subject comparison)
* Score histogram

### ➕ Data Input Options

* Manual student entry
* Upload CSV / Excel files

### 🗑️ Data Management

* Delete individual students
* Clear all records

### 📥 Export

* Download detailed **Excel report** with:

  * Summary sheet
  * Ranked student list
  * Grade distribution chart

---

## 🧠 System Design

### Architecture Overview

```
Streamlit UI
     ↓
Session State (DataFrame)
     ↓
StudentAnalyzer (Processing Engine)
     ↓
Visualizations + Excel Report
```

### Key Characteristics

* ❌ No database (Supabase removed)
* ⚡ Fully in-memory processing
* 🔒 No external dependencies
* 💻 Runs offline
* 📦 Easy deployment

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* OpenPyXL

---

## 📂 Project Structure

```
project/
│
├── app.py              # Main Streamlit application
├── analysis.py         # StudentAnalyzer logic
├── README.md
```

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install streamlit pandas plotly openpyxl
```

### 2. Run the app

```bash
streamlit run app.py
```

---

## 📥 File Upload Format

### Supported formats:

* `.csv`
* `.xlsx`

### Required columns:

```
name,1st-subject,2nd-subject,3rd-subject,4th-subject,5th-subject
```

### Example:

```
Alex,78,65,89,70,82
Bob,90,88,95,85,91
```

---

## 📊 Grading Logic

| Percentage | Grade |
| ---------- | ----- |
| ≥ 90       | A+    |
| ≥ 80       | A     |
| ≥ 70       | B+    |
| ≥ 60       | B     |
| ≥ 50       | C     |
| ≥ 40       | D     |
| < 40       | F     |

---

## ⚠️ Limitations

* Data is stored in memory only
* Data will reset on:

  * Page refresh
  * App restart

---

## 🔄 Future Improvements

* File-based persistence (CSV/JSON)
* Authentication system
* Custom subject configuration
* Advanced analytics (trend analysis, predictions)

---

## 💡 Engineering Insight

This project demonstrates:

* State management using `st.session_state`
* Data transformation pipelines with Pandas
* Separation of concerns (UI vs logic)
* Report generation using OpenPyXL

---

## 📌 Author

Built as a practical data analytics project using Streamlit.

---

## ⭐ If you like this project

Give it a star ⭐ and improve it further!
