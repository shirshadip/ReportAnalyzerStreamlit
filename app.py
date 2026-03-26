# Imports 
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from analysis import StudentAnalyzer, SUBJECTS, TOTAL_MAX

# ── Local in-memory storage ───────────────────────────────
if "students" not in st.session_state:
    st.session_state["students"] = pd.DataFrame(
        columns=["id", "name", "1st-subject", "2nd-subject", "3rd-subject", "4th-subject", "5th-subject"]
    )

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.metric-card {
    background: linear-gradient(135deg, #1e3a56, #162840);
    border: 1px solid rgba(0,180,216,0.2);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.5rem;
}
.metric-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(255,255,255,0.5);
    font-weight: 700;
    margin-bottom: 0.25rem;
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f0f6ff;
    line-height: 1.1;
}
.metric-sub {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.45);
    margin-top: 0.2rem;
}
.metric-card.gold  { border-color: rgba(244,197,66,0.4); }
.metric-card.green { border-color: rgba(46,204,113,0.4); }
.metric-card.red   { border-color: rgba(231,76,60,0.4);  }
.metric-card.blue  { border-color: rgba(33,150,243,0.4); }

.section-header {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #00b4d8;
    margin: 1.5rem 0 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(0,180,216,0.2);
}
.topper-banner {
    background: linear-gradient(135deg, rgba(244,197,66,0.15), rgba(255,170,0,0.08));
    border: 1px solid rgba(244,197,66,0.35);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: metric card HTML ───────────────────────────────────────────────
def metric_card(label, value, sub="", variant=""):
    return f"""
    <div class="metric-card {variant}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {"<div class='metric-sub'>" + sub + "</div>" if sub else ""}
    </div>
    """


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎓 Student Analyzer")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "➕ Add Students", "📥 Upload CSV", "🗑️ Manage Students"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


# ── Cache the raw data (cleared on refresh) ───────────────────────────────
def get_analysis():
    df = st.session_state["students"]
    if df.empty:
        return None, df
    analyzer = StudentAnalyzer(df)
    return analyzer.full_analysis(), df


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.title("Class Performance Dashboard")

    analysis, raw_df = get_analysis()

    if analysis is None:
        st.info("No student data yet. Go to **Add Students** or **Upload CSV** to get started.")
        st.stop()

    s = analysis["summary"]

    # ── Topper Banner ──────────────────────────────────────
    topper = analysis["topper"]
    st.markdown(f"""
    <div class="topper-banner">
        <span style="font-size:2rem">🏆</span>
        <div>
            <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;
                        color:rgba(244,197,66,0.8);font-weight:700">Class Topper</div>
            <div style="font-size:1.25rem;font-weight:700;color:#f0f6ff">{topper['name']}</div>
            <div style="font-size:0.82rem;color:rgba(255,255,255,0.55)">
                {topper['total']} / {TOTAL_MAX} &nbsp;·&nbsp;
                {topper['percentage']}% &nbsp;·&nbsp; Grade {topper['grade']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat Cards ─────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(metric_card("Total Students", s["total_students"], variant="blue"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("Class Average", f"{s['class_average_percentage']}%",
                                f"Total: {s['class_average_total']}", "blue"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("Highest Score", f"{s['highest_percentage']}%",
                                analysis["highest_scorer"]["name"], "green"), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("Lowest Score", f"{s['lowest_percentage']}%",
                                analysis["lowest_scorer"]["name"], "red"), unsafe_allow_html=True)
    with c5:
        pass_rate = round(s["pass_count"] / s["total_students"] * 100) if s["total_students"] else 0
        st.markdown(metric_card("Pass Rate", f"{pass_rate}%",
                                f"{s['pass_count']} passed · {s['fail_count']} failed", "green"),
                    unsafe_allow_html=True)

    st.markdown("---")

    # ── Charts Row 1 ───────────────────────────────────────
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="section-header">Subject Averages</div>', unsafe_allow_html=True)
        subj_df = pd.DataFrame([
            {"Subject": k, "Average": v}
            for k, v in analysis["subject_averages"].items()
        ])
        fig_subj = px.bar(
            subj_df, x="Subject", y="Average",
            color="Average",
            color_continuous_scale=["#1d6fa4", "#00b4d8", "#90e0ef"],
            range_y=[0, 100],
            text="Average",
        )
        fig_subj.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_subj.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#f0f6ff", coloraxis_showscale=False,
            margin=dict(t=10, b=10, l=0, r=0), height=280,
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig_subj, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-header">Grade Distribution</div>', unsafe_allow_html=True)
        grade_order = ["A+", "A", "B+", "B", "C", "D", "F"]
        grade_colors = {"A+": "#2ecc71", "A": "#27ae60", "B+": "#3498db",
                        "B": "#2980b9", "C": "#f4c542", "D": "#e67e22", "F": "#e74c3c"}
        gd = analysis["grade_distribution"]
        grade_df = pd.DataFrame([
            {"Grade": g, "Count": gd.get(g, 0), "Color": grade_colors[g]}
            for g in grade_order if gd.get(g, 0) > 0
        ])
        fig_grade = px.bar(
            grade_df, x="Grade", y="Count",
            color="Grade",
            color_discrete_map={g: grade_colors[g] for g in grade_order},
            text="Count",
        )
        fig_grade.update_traces(textposition="outside")
        fig_grade.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#f0f6ff", showlegend=False,
            margin=dict(t=10, b=10, l=0, r=0), height=280,
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig_grade, use_container_width=True)

    # ── Charts Row 2 ───────────────────────────────────────
    col_l2, col_r2 = st.columns(2)

    with col_l2:
        st.markdown('<div class="section-header">Subject Radar</div>', unsafe_allow_html=True)
        subj_avgs = analysis["subject_averages"]
        labels = list(subj_avgs.keys())
        values = list(subj_avgs.values())
        fig_radar = go.Figure(go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            line_color="#00b4d8",
            fillcolor="rgba(0,180,216,0.18)",
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.1)",
                                tickfont=dict(color="rgba(255,255,255,0.4)", size=9)),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.1)",
                                 tickfont=dict(color="#f0f6ff", size=11)),
            ),
            paper_bgcolor="rgba(0,0,0,0)", font_color="#f0f6ff",
            margin=dict(t=20, b=20, l=40, r=40), height=280,
            showlegend=False,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_r2:
        st.markdown('<div class="section-header">Score Distribution</div>', unsafe_allow_html=True)
        analyzer_obj = StudentAnalyzer(raw_df)
        enriched = analyzer_obj.df
        fig_hist = px.histogram(
            enriched, x="percentage", nbins=10,
            color_discrete_sequence=["#2196f3"],
            labels={"percentage": "Percentage Score", "count": "Students"},
        )
        fig_hist.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#f0f6ff", showlegend=False,
            margin=dict(t=10, b=10, l=0, r=0), height=280,
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Students"),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # ── Ranking Table ──────────────────────────────────────
    st.markdown('<div class="section-header">Student Rankings</div>', unsafe_allow_html=True)

    ranked = pd.DataFrame(analysis["ranked_students"])
    display_df = ranked[["rank", "name", "1st-subject", "2nd-subject", "3rd-subject", "4th-subject", "5th-subject", "total", "percentage", "grade"]].copy()
    display_df.columns = ["Rank", "Name", "1st-subject", "2nd-subject", "3rd-subject", "4th-subject", "5th-subject", "Total", "%", "Grade"]

    def color_pct(val):
        if val >= 80: return "color: #2ecc71; font-weight: 700"
        if val < 40:  return "color: #e74c3c; font-weight: 700"
        return ""

    def color_grade(val):
        colors = {"A+": "#2ecc71", "A": "#27ae60", "B+": "#3498db",
                  "B": "#2980b9", "C": "#f4c542", "D": "#e67e22", "F": "#e74c3c"}
        c = colors.get(val, "")
        return f"color: {c}; font-weight: 700" if c else ""

    styled = (
        display_df.style
        .applymap(color_pct, subset=["%"])
        .applymap(color_grade, subset=["Grade"])
        .set_properties(**{"text-align": "center"})
        .set_table_styles([{
            "selector": "th",
            "props": [("background-color", "#1a3c5e"), ("color", "white"),
                      ("font-size", "0.78rem"), ("text-transform", "uppercase"),
                      ("letter-spacing", "0.06em"), ("text-align", "center")]
        }])
        .highlight_max(subset=["Total"], color="rgba(46,204,113,0.15)")
        .highlight_min(subset=["Total"], color="rgba(231,76,60,0.1)")
        .format({"%": "{:.2f}"})
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # ── Download Button ────────────────────────────────────
    st.markdown("---")
    analyzer_dl = StudentAnalyzer(raw_df)
    excel_bytes = analyzer_dl.generate_excel_report_bytes()
    st.download_button(
        label="⬇️ Download Excel Report",
        data=excel_bytes,
        file_name="student_performance_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: ADD STUDENTS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "➕ Add Students":
    st.title("Add Student")

    with st.form("add_student_form", clear_on_submit=True):
        name = st.text_input("Student Name", placeholder="e.g. Alex Johnson")

        c1, c2, c3 = st.columns(3)
        with c1:
            s1 = st.number_input("1st-subject", min_value=0, max_value=100, step=1)
            s2 = st.number_input("2nd-subject", min_value=0, max_value=100, step=1)
        with c2:
            s3 = st.number_input("3rd-subject", min_value=0, max_value=100, step=1)
            s4 = st.number_input("4th-subject", min_value=0, max_value=100, step=1)
        with c3:
            s5 = st.number_input("5th-subject", min_value=0, max_value=100, step=1)

        # Live preview
        total = s1 + s2 + s3 + s4 + s5
        pct   = round(total / TOTAL_MAX * 100, 2)
        st.info(f"**Preview →** Total: {total} / {TOTAL_MAX} &nbsp;|&nbsp; Percentage: {pct}%")

        submitted = st.form_submit_button("➕ Add Student", use_container_width=True)
        if submitted:
            if not name.strip():
                st.error("Name is required.")
            else:
                try:
                    df = st.session_state["students"]

                    new_id = 1 if df.empty else int(df["id"].max()) + 1

                    new_row = pd.DataFrame([{
                        "id": new_id,
                        "name": name,
                        "1st-subject": int(s1),
                        "2nd-subject": int(s2),
                        "3rd-subject": int(s3),
                        "4th-subject": int(s4),
                        "5th-subject": int(s5),
                    }])

                    st.session_state["students"] = pd.concat([df, new_row], ignore_index=True)
                    st.cache_data.clear()
                    st.success(f"✅ **{name}** added successfully!")
                except Exception as e:
                    st.error(f"Failed to add student: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: UPLOAD CSV
# ═══════════════════════════════════════════════════════════════════════════
elif page == "📥 Upload CSV":
    st.title("Upload CSV or xlsx")

    st.markdown("""
    Upload a `.csv` file with the following columns:
    ```
    name,1st-subject,2nd-subject,3rd-subject,4th-subject,5th-subject
    Alex,78,65,89,70,82
    Bob,90,88,95,85,91
    ```
    """)

    uploaded = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded:
        try:
            if uploaded.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded)
            else:
                df = pd.read_csv(uploaded)

            df.columns = df.columns.str.lower().str.strip()
            required = {"name", "1st-subject", "2nd-subject", "3rd-subject", "4th-subject", "5th-subject"}

            if not required.issubset(set(df.columns)):
                st.error(f"File must contain columns: {required}")
            else:
                df = df[["name", "1st-subject", "2nd-subject", "3rd-subject", "4th-subject", "5th-subject"]]

                st.subheader(f"Preview — {len(df)} students")
                st.dataframe(df, use_container_width=True, hide_index=True)

                if st.button("⬆️ Upload to Database", use_container_width=True, type="primary"):
                    records = df.to_dict(orient="records")
                    df.insert(0, "id", range(1, len(df) + 1))
                    st.session_state["students"] = df
                    st.cache_data.clear()
                    st.success(f"✅ Successfully uploaded **{len(records)} students**!")
                    st.balloons()

        except Exception as e:
            st.error(f"Error reading file: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE: MANAGE STUDENTS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🗑️ Manage Students":
    st.title("Manage Students")

    _, raw_df = get_analysis()

    if raw_df.empty:
        st.info("No students in the database.")
        st.stop()

    st.dataframe(
        raw_df[["id", "name", "1st-subject", "2nd-subject", "3rd-subject", "4th-subject", "5th-subject"]],
        use_container_width=True, hide_index=True
    )

    st.markdown("---")
    st.subheader("Delete a Student")

    name_map = {f"{r['name']} (ID: {r['id']})": r["id"] for _, r in raw_df.iterrows()}
    selected = st.selectbox("Select student to delete", list(name_map.keys()))

    if st.button("🗑️ Delete Student", type="primary"):
        try:
            student_id = name_map[selected]
            df = st.session_state["students"]
            st.session_state["students"] = df[df["id"] != student_id].reset_index(drop=True)
            st.cache_data.clear()
            st.success(f"Deleted **{selected}**")
            st.rerun()
        except Exception as e:
            st.error(f"Delete failed: {e}")

    st.markdown("---")
    st.subheader("⚠️ Clear All Students")
    confirm = st.checkbox("I understand this will delete ALL student records")
    if confirm:
        if st.button("🗑️ Clear All", type="primary"):
            try:
                st.session_state["students"] = pd.DataFrame(
                    columns=["id", "name", "1st-subject", "2nd-subject", "3rd-subject", "4th-subject", "5th-subject"]
                )
                st.cache_data.clear()
                st.success("All student records cleared.")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")