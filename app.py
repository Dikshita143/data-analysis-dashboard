import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import re
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Sales, Employee & Customer Data Analysis",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely before data upload
if 'data' not in st.session_state or st.session_state.data is None:
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>', unsafe_allow_html=True)

# Load external CSS
if os.path.exists("utils/style.css"):
    with open("utils/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Session State
if 'data' not in st.session_state: st.session_state.data = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'step' not in st.session_state: st.session_state.step = 0
if 'greeted' not in st.session_state: st.session_state.greeted = False

# --- SIDEBAR: DATA ASSISTANT ---
with st.sidebar:
    st.markdown('<h2 style="text-align:center;">Data Assistant</h2>', unsafe_allow_html=True)
    if st.session_state.data is not None:
        with st.expander("Dataset Info", expanded=False):
            st.write(f"**Rows:** {len(st.session_state.data)} | **Cols:** {len(st.session_state.data.columns)}")
            st.write(f"**Columns:** {', '.join(st.session_state.data.columns.tolist())}")
            if st.button("Upload New File"):
                st.session_state.data = None
                st.session_state.chat_history = []
                st.session_state.step = 0
                st.session_state.greeted = False
                st.rerun()
        st.markdown("---")
        df = st.session_state.data
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        all_cols = df.columns.tolist()
        if not st.session_state.greeted:
            g = f"**Hello!** Your dataset has **{len(df)}** records and **{len(all_cols)}** columns.\n\n"
            g += f"**Numeric:** {', '.join(num_cols[:5])}\n" if num_cols else ""
            g += f"**Text:** {', '.join(cat_cols[:5])}\n\n" if cat_cols else ""
            g += "Ask me: *'summary', 'average salary', 'top 5', 'distribution of department', 'outliers', 'correlation'*"
            st.session_state.chat_history.append({"role": "assistant", "content": g})
            st.session_state.greeted = True
        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.write(chat["content"])
        user_input = st.chat_input("Ask about your data...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            q = user_input.lower()
            response = ""
            def find_col(query, clist):
                for c in clist:
                    if c.lower() in query: return c
                for c in clist:
                    for w in c.lower().replace("_"," ").split():
                        if len(w) > 2 and w in query: return c
                return None
            mn = find_col(q, num_cols)
            mc = find_col(q, cat_cols)
            try:
                if "column" in q or "field" in q:
                    response = f"**Numeric:** {', '.join(num_cols)}\n\n**Text:** {', '.join(cat_cols)}"
                elif "missing" in q or "null" in q or "empty" in q:
                    ms = df.isnull().sum(); t = ms.sum()
                    if t == 0: response = "Zero missing values. Data quality is excellent."
                    else:
                        response = f"**Total Missing:** {t}\n\n"
                        for c in ms[ms>0].index: response += f"- **{c}:** {ms[c]} ({ms[c]/len(df)*100:.1f}%)\n"
                elif "unique" in q or "distinct" in q or "categories" in q:
                    col = find_col(q, all_cols) or (cat_cols[0] if cat_cols else None)
                    if col:
                        u = df[col].nunique(); vals = df[col].unique()[:15]
                        response = f"**{col}** has **{u}** unique values:\n{', '.join(str(v) for v in vals)}"
                    else: response = "Specify a column name."
                elif "distribut" in q or "breakdown" in q or "split" in q:
                    col = mc or (cat_cols[0] if cat_cols else None)
                    if col:
                        vc = df[col].value_counts()
                        response = f"### Distribution of {col}\n"
                        for v, cnt in vc.head(10).items(): response += f"- **{v}:** {cnt} ({cnt/len(df)*100:.1f}%)\n"
                    else: response = "Specify a text column."
                elif "correlat" in q or "relationship" in q:
                    if len(num_cols) >= 2:
                        c1 = mn or num_cols[0]; c2 = num_cols[1] if c1 == num_cols[0] else num_cols[0]
                        for nc in num_cols:
                            if nc != c1 and nc.lower() in q: c2 = nc; break
                        corr = df[c1].corr(df[c2])
                        s = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.4 else "Weak"
                        response = f"**{c1}** vs **{c2}**: Correlation = **{corr:.3f}** ({s} {'positive' if corr>0 else 'negative'})"
                    else: response = "Need 2+ numeric columns."
                elif "trend" in q or "over time" in q or "growth" in q:
                    dc = [c for c in all_cols if 'date' in c.lower() or 'time' in c.lower()]
                    if dc and num_cols:
                        nc = mn or num_cols[0]; df[dc[0]] = pd.to_datetime(df[dc[0]])
                        s = df.sort_values(dc[0]); diff = s[nc].iloc[-1] - s[nc].iloc[0]
                        response = f"**{nc}** trend: {'Growth' if diff>0 else 'Decline'} of **{abs(diff):,.2f}** ({diff/s[nc].iloc[0]*100:+.1f}%)" if s[nc].iloc[0] != 0 else f"**{nc}** changed by **{diff:,.2f}**"
                    else: response = "No date column found for trend analysis."
                elif "top" in q or "highest" in q or "best" in q or "max" in q:
                    nc = mn or (num_cols[0] if num_cols else None)
                    if nc:
                        n = 5
                        for w in q.split():
                            if w.isdigit(): n = int(w); break
                        top = df.nlargest(n, nc)
                        response = f"### Top {n} by {nc}\n"
                        for _, r in top.iterrows():
                            lbl = r[cat_cols[0]] if cat_cols else f"Row"
                            response += f"- **{lbl}:** {r[nc]:,.2f}\n"
                    else: response = "No numeric column found."
                elif "bottom" in q or "lowest" in q or "worst" in q or "min" in q:
                    nc = mn or (num_cols[0] if num_cols else None)
                    if nc:
                        n = 5
                        for w in q.split():
                            if w.isdigit(): n = int(w); break
                        bot = df.nsmallest(n, nc)
                        response = f"### Bottom {n} by {nc}\n"
                        for _, r in bot.iterrows():
                            lbl = r[cat_cols[0]] if cat_cols else "Row"
                            response += f"- **{lbl}:** {r[nc]:,.2f}\n"
                    else: response = "No numeric column found."
                elif "average" in q or "mean" in q or "avg" in q:
                    nc = mn or (num_cols[0] if num_cols else None)
                    if nc:
                        if mc:
                            grp = df.groupby(mc)[nc].mean().sort_values(ascending=False)
                            response = f"### Average {nc} by {mc}\n"
                            for v, a in grp.head(10).items(): response += f"- **{v}:** {a:,.2f}\n"
                        else: response = f"**Average {nc}:** {df[nc].mean():,.2f}\n**Median:** {df[nc].median():,.2f}\n**Std Dev:** {df[nc].std():,.2f}"
                    else: response = "No numeric column found."
                elif "total" in q or "sum" in q:
                    nc = mn or (num_cols[0] if num_cols else None)
                    if nc:
                        if mc:
                            grp = df.groupby(mc)[nc].sum().sort_values(ascending=False)
                            response = f"### Total {nc} by {mc}\n"
                            for v, s in grp.head(10).items(): response += f"- **{v}:** {s:,.2f}\n"
                        else: response = f"**Total {nc}:** {df[nc].sum():,.2f}"
                    else: response = "No numeric column found."
                elif "outlier" in q or "anomal" in q or "unusual" in q:
                    nc = mn or (num_cols[0] if num_cols else None)
                    if nc:
                        q1, q3 = df[nc].quantile(0.25), df[nc].quantile(0.75); iqr = q3-q1
                        out = df[(df[nc] < q1-1.5*iqr) | (df[nc] > q3+1.5*iqr)]
                        response = f"**{nc}:** {len(out)} outliers found (range: {q1-1.5*iqr:,.2f} to {q3+1.5*iqr:,.2f})"
                    else: response = "No numeric column found."
                elif "how many" in q or "count" in q:
                    if mc:
                        vc = df[mc].value_counts()
                        response = f"### Count by {mc}\n"
                        for v, c in vc.head(10).items(): response += f"- **{v}:** {c}\n"
                    else: response = f"**Total Records:** {len(df)}"
                elif "summary" in q or "overview" in q or "describe" in q or "snapshot" in q or "insight" in q or "analyze" in q:
                    response = f"### Executive Summary\n**Dataset:** {len(df)} records, {len(all_cols)} columns\n**Missing:** {df.isnull().sum().sum()}\n\n"
                    if num_cols:
                        response += "**Numeric Highlights:**\n"
                        for nc in num_cols[:4]: response += f"- **{nc}:** Min {df[nc].min():,.2f} | Avg {df[nc].mean():,.2f} | Max {df[nc].max():,.2f}\n"
                    if cat_cols:
                        response += "\n**Categories:**\n"
                        for cc in cat_cols[:3]: response += f"- **{cc}:** {df[cc].nunique()} unique (top: {df[cc].value_counts().idxmax()})\n"
                else:
                    response = "I can answer:\n- *'summary'* - Full overview\n- *'columns'* - List columns\n- *'missing values'* - Data quality\n"
                    if num_cols: response += f"- *'average {num_cols[0]}'* - Column stats\n- *'top 5 by {num_cols[0]}'* - Rankings\n"
                    if cat_cols: response += f"- *'distribution of {cat_cols[0]}'* - Breakdown\n"
                    response += "- *'correlation'* - Relationships\n- *'outliers'* - Anomalies\n- *'trends'* - Time analysis"
            except Exception as e:
                response = f"Error: {str(e)}"
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    else:
        st.info("Upload a CSV file to start chatting with your data.")


# --- MAIN CONTENT ---
if st.session_state.data is None:
    # LANDING PAGE
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Sales, Employee & Customer Data Analysis</h1>
        <p class="hero-subtitle">Transform your CSV data into beautiful, interactive dashboards instantly</p>
    </div>
    """, unsafe_allow_html=True)

    # Upload Section
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center;">Upload Your CSV File</h3>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#888;">Start by uploading your business data to unlock all features</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Drag and drop your CSV file here", type=["csv"], label_visibility="collapsed")
    if uploaded:
        st.session_state.data = pd.read_csv(uploaded)
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # How It Works
    st.markdown('<h2 class="section-title">How It Works</h2>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="feature-card">
            <div class="feature-icon">1</div>
            <h4>Upload Data</h4>
            <p>Upload any CSV file — sales records, employee data, customer lists, or student scores.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="feature-card">
            <div class="feature-icon">2</div>
            <h4>Auto Analysis</h4>
            <p>The system instantly generates KPIs, charts, business summaries, and trend predictions.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="feature-card">
            <div class="feature-icon">3</div>
            <h4>Visualize & Export</h4>
            <p>Explore interactive charts, query your data using the assistant, and export reports.</p>
        </div>""", unsafe_allow_html=True)

    # Features
    st.markdown('<h2 class="section-title">Features</h2>', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown('<div class="feature-card"><div class="feature-icon">A</div><h4>Auto Charts</h4><p>Bar, scatter, pie charts generated automatically from your data.</p></div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="feature-card"><div class="feature-icon">P</div><h4>Predictions</h4><p>Statistical predictions based on your dataset patterns.</p></div>', unsafe_allow_html=True)
    with f3:
        st.markdown('<div class="feature-card"><div class="feature-icon">S</div><h4>Smart Search</h4><p>Search, filter, and sort through your entire dataset instantly.</p></div>', unsafe_allow_html=True)
    with f4:
        st.markdown('<div class="feature-card"><div class="feature-icon">C</div><h4>Data Assistant</h4><p>Ask questions about your data in plain English and get instant answers.</p></div>', unsafe_allow_html=True)

    # FAQ
    st.markdown('<h2 class="section-title">Frequently Asked Questions</h2>', unsafe_allow_html=True)
    with st.expander("Is my data safe?"): st.write("Yes! All processing happens locally in your browser session. No data is stored.")
    with st.expander("What file formats do you support?"): st.write("Currently we support CSV (.csv) files. Excel support coming soon!")
    with st.expander("Can I export the charts?"): st.write("Yes! All Plotly charts have a built-in download button for PNG export.")

    # Footer
    st.markdown("""<div class="footer">
        <p>&copy; 2026 Sales, Employee & Customer Data Analysis | Made by Dikshita | Built with Streamlit & Python</p>
    </div>""", unsafe_allow_html=True)

else:
    # DASHBOARD VIEW
    # Top bar with file info and Start New button
    top1, top2 = st.columns([4, 1])
    with top1:
        st.markdown(f'<h3 style="margin:0;">Sales, Employee & Customer Data Analysis</h3>', unsafe_allow_html=True)
    with top2:
        if st.button("Start New", use_container_width=True):
            st.session_state.data = None
            st.session_state.chat_history = []
            st.session_state.step = 0
            st.session_state.greeted = False
            st.rerun()
    st.markdown("---")

    df = st.session_state.data
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()

    # Step 1: Data Explorer
    if st.session_state.step >= 1:
        st.markdown('<h2 class="section-title">Data Explorer</h2>', unsafe_allow_html=True)
        search = st.text_input("Search any value...", "")
        if search:
            escaped = re.escape(search)
            fdf = df[df.apply(lambda r: r.astype(str).str.contains(escaped, case=False).any(), axis=1)]
        else:
            fdf = df
        col_sort = st.selectbox("Sort by", df.columns)
        order = st.radio("Order", ["Ascending", "Descending"], horizontal=True)
        st.dataframe(fdf.sort_values(col_sort, ascending=(order == "Ascending")), use_container_width=True, height=300)
        if st.session_state.step == 1:
            if st.button("Analyze Insights", use_container_width=True): st.session_state.step = 2; st.rerun()

    # Step 2: Key Insights
    if st.session_state.step >= 2:
        st.markdown("---")
        st.markdown('<h2 class="section-title">Key Insights</h2>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(f'<div class="metric-card"><h6>Records</h6><h3>{len(df)}</h3></div>', unsafe_allow_html=True)
        with k2:
            if num_cols: st.markdown(f'<div class="metric-card"><h6>Sum {num_cols[0]}</h6><h3>{df[num_cols[0]].sum():,.0f}</h3></div>', unsafe_allow_html=True)
        with k3:
            if num_cols: st.markdown(f'<div class="metric-card"><h6>Avg {num_cols[0]}</h6><h3>{df[num_cols[0]].mean():,.1f}</h3></div>', unsafe_allow_html=True)
        with k4:
            if cat_cols: st.markdown(f'<div class="metric-card"><h6>Categories</h6><h3>{df[cat_cols[0]].nunique()}</h3></div>', unsafe_allow_html=True)
        if num_cols and cat_cols:
            top = df.groupby(cat_cols[0])[num_cols[0]].sum().idxmax()
            st.success(f"**Insight:** Best performing category is **{top}**. Focus resources here for maximum ROI.")
        if st.session_state.step == 2:
            if st.button("Generate Visuals", use_container_width=True): st.session_state.step = 3; st.rerun()

    # Step 3: Visual Analytics
    if st.session_state.step >= 3:
        st.markdown("---")
        st.markdown('<h2 class="section-title">Visual Analytics</h2>', unsafe_allow_html=True)
        v1, v2 = st.columns(2)
        with v1:
            if num_cols and cat_cols:
                fig = px.bar(df, x=cat_cols[0], y=num_cols[0], color=cat_cols[0], title=f"{num_cols[0]} by {cat_cols[0]}")
                fig.update_layout(template="plotly_dark"); st.plotly_chart(fig, use_container_width=True)
        with v2:
            if len(num_cols) >= 2:
                fig = px.scatter(df, x=num_cols[0], y=num_cols[1], title=f"{num_cols[0]} vs {num_cols[1]}")
                fig.update_layout(template="plotly_dark"); st.plotly_chart(fig, use_container_width=True)
        if st.session_state.step == 3:
            if st.button("Run Predictions", use_container_width=True): st.session_state.step = 4; st.rerun()

    # Step 4: Predictions
    if st.session_state.step >= 4:
        st.markdown("---")
        st.markdown('<h2 class="section-title">Predictive Analysis</h2>', unsafe_allow_html=True)
        if len(num_cols) >= 2:
            try:
                pred_df = df[[num_cols[0], num_cols[1]]].dropna()
                if len(pred_df) > 1:
                    model = LinearRegression()
                    model.fit(pred_df[[num_cols[0]]], pred_df[num_cols[1]])
                    val = st.number_input(f"Enter {num_cols[0]}", value=float(pred_df[num_cols[0]].mean()))
                    st.metric(f"Predicted {num_cols[1]}", f"{model.predict([[val]])[0]:,.2f}")
                    st.info("Prediction uses Linear Regression model trained on your data.")
            except Exception as e: st.error(f"Prediction Error: {e}")
        else: st.warning("Need at least 2 numeric columns for predictions.")

    st.markdown("""<div class="footer"><p>&copy; 2026 Sales, Employee & Customer Data Analysis | Made by Dikshita</p></div>""", unsafe_allow_html=True)
