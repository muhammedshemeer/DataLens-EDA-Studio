import streamlit as st
import pandas as pd
import numpy as np
import os
from io import StringIO
from ydata_profiling import ProfileReport
import sweetviz as sv
import warnings

# Import our custom modules
from eda_charts import *
from preprocessing import *

warnings.filterwarnings('ignore')

st.set_page_config(page_title="DataLens", page_icon="🔍", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# CUSTOM CSS INJECTION
# ==========================================
st.markdown("""
<style>
/* 1. HIDE DEFAULT STREAMLIT ELEMENTS */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 2rem; padding-right: 2rem;}

/* 2. PAGE & BACKGROUND */
.stApp {background-color: #0a0f1e !important;}
[data-testid="stAppViewContainer"] {background-color: #0a0f1e !important;}
[data-testid="stHeader"] {background-color: transparent !important;}

/* 3. SIDEBAR */
[data-testid="stSidebar"] {background-color: #0d1117 !important;}
[data-testid="stSidebar"] > div:first-child {background-color: #0d1117 !important;}
[data-testid="stSidebar"] hr {border-bottom-color: #00d4ff33 !important;}
section[data-testid="stSidebar"] {border-right: 1px solid #00d4ff33 !important;}

/* 4. METRIC CARDS */
.custom-metric {
    background-color: #111827; border: 1px solid #00d4ff44; border-radius: 16px; 
    box-shadow: 0 0 20px rgba(0,212,255,0.08); padding: 20px; transition: all 0.3s ease; height: 100%;
}
.custom-metric:hover {box-shadow: 0 0 30px #00d4ff33;}
.metric-val {color: #00d4ff; font-size: 28px; font-weight: bold; margin-bottom: 5px;}
.metric-label {color: #9ca3af; font-size: 13px;}

/* 5. TABS */
.stTabs [data-baseweb="tab-list"] {background-color: transparent; gap: 20px;}
.stTabs [data-baseweb="tab"] {padding: 10px 0; color: #6b7280; font-size: 15px; border-bottom: 2px solid transparent;}
.stTabs [data-baseweb="tab"][aria-selected="true"] {color: white !important; font-weight: bold; border-bottom: 2px solid #00d4ff !important;}
.stTabs [data-baseweb="tab-highlight"] {display: none;}

/* 6. DATAFRAMES */
[data-testid="stDataFrame"] > div {background-color: #111827 !important; border: 1px solid #ffffff11; border-radius: 8px;}
[data-testid="stTable"] table {background-color: #111827 !important; color: white !important;}
[data-testid="stTable"] th {background-color: #1e2130 !important; color: #00d4ff !important; border-bottom: 1px solid #ffffff11 !important;}
[data-testid="stTable"] td {border-bottom: 1px solid #ffffff11 !important;}
[data-testid="stTable"] tr:hover {background-color: #1e293b !important;}

/* 7. BUTTONS & DOWNLOAD BUTTONS */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #00d4ff, #7c3aed) !important;
    color: white !important; font-weight: bold !important; border: none !important; border-radius: 8px !important;
    padding: 10px 24px !important; cursor: pointer !important; transition: all 0.3s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {opacity: 0.85 !important; transform: scale(1.02) !important;}

/* 8. GRADIENT TITLES */
.gradient-title {
    background: linear-gradient(135deg, #00d4ff, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-size: 48px; font-weight: 900; text-align: center; margin-bottom: 10px;
}
.sidebar-logo {
    background: linear-gradient(135deg, #00d4ff, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-size: 28px; font-weight: bold; margin-bottom: 20px;
}

/* 9. SECTION HEADERS */
.section-header {color: white; border-left: 4px solid #00d4ff; padding-left: 12px; margin-top: 32px; margin-bottom: 16px; font-size: 24px; font-weight: bold;}

/* 10. INPUT ELEMENTS */
.stSelectbox > div > div {background-color: #111827 !important; border: 1px solid #00d4ff44 !important; color: white !important;}
.stMultiSelect > div > div {background-color: #111827 !important; border: 1px solid #00d4ff44 !important;}
.stTextInput > div > div {background-color: #111827 !important; border: 1px solid #00d4ff44 !important; color: white;}
[data-testid="stFileUploader"] {background-color: #111827 !important; border: 2px dashed #00d4ff55 !important; border-radius: 12px; padding: 20px;}

/* 11. ALERTS */
[data-testid="stAlert"] {border-radius: 8px; border-width: 1px !important; border-style: solid !important;}
[data-baseweb="toast"] {background-color: #064e3b !important;}

/* 12. COLUMN TYPE BADGES */
.badge-Numerical {background-color: #1d4ed8; color: white; border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: 600; display: inline-block;}
.badge-Categorical {background-color: #065f46; color: white; border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: 600; display: inline-block;}
.badge-Datetime {background-color: #92400e; color: white; border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: 600; display: inline-block;}
.badge-Text {background-color: #7f1d1d; color: white; border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: 600; display: inline-block;}

/* 13. FEATURE CARDS (LANDING) */
.feature-card {
    background-color: #111827; border: 1px solid #00d4ff33; border-radius: 16px; padding: 24px;
    transition: all 0.3s ease; text-align: left; height: 100%;
}
.feature-card:hover {border-color: #00d4ff; box-shadow: 0 0 20px rgba(0,212,255,0.13);}
.feature-title {color: white; font-size: 18px; font-weight: bold; margin-bottom: 8px;}
.feature-desc {color: #9ca3af; font-size: 14px;}

/* 15. INSIGHT BOXES */
.insight-box {
    background-color: #0f172a; border-left: 4px solid #00d4ff; border-radius: 8px; padding: 12px 16px;
    color: #94a3b8; font-size: 14px; margin-top: 5px; margin-bottom: 25px;
}

/* MISC */
.dataset-score {font-size: 48px; font-weight: bold; text-align: center;}
.score-green {color: #10b981;}
.score-orange {color: #f59e0b;}
.score-red {color: #ef4444;}
.subtitle {color: #9ca3af; font-size: 18px; text-align: center; margin-bottom: 30px;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filename' not in st.session_state:
    st.session_state.filename = None

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def load_csv(file_obj, filename):
    try:
        df = pd.read_csv(file_obj, encoding='utf-8')
    except UnicodeDecodeError:
        file_obj.seek(0)
        df = pd.read_csv(file_obj, encoding='iso-8859-1')
    
    st.session_state.df = df
    st.session_state.filename = filename

def load_sample():
    if os.path.exists("sample_data/sample.csv"):
        try:
             df = pd.read_csv("sample_data/sample.csv")
             st.session_state.df = df
             st.session_state.filename = "sample.csv"
        except Exception as e:
             st.error(f"Error loading sample: {e}")
    else:
        st.error("Sample file not found. Have you run the generation script?")

# ==========================================
# LANDING PAGE
# ==========================================
if st.session_state.df is None:
    st.markdown('<div class="gradient-title">🔍 DataLens</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Upload your CSV. Explore your data instantly.</div>', unsafe_allow_html=True)
    st.markdown('<hr style="border-top: 1px solid #ffffff11; margin-bottom: 40px;">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📋 Dataset Overview</div>
            <div class="feature-desc">Shape, types, statistics at a glance</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🔀 SweetViz Reports</div>
            <div class="feature-desc">Visual EDA and dataset comparison</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📊 9 EDA Chart Types</div>
            <div class="feature-desc">Interactive Plotly charts with insights</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">⚙️ Smart Preprocessing</div>
            <div class="feature-desc">Clean data with before/after preview</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📈 Auto Profiling</div>
            <div class="feature-desc">Full ydata-profiling EDA report</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📥 Export Clean Data</div>
            <div class="feature-desc">Download your preprocessed CSV</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    up_col1, up_col2, up_col3 = st.columns([1, 2, 1])
    with up_col2:
        uploaded_file = st.file_uploader("", type=['csv'])
        st.markdown('<p style="text-align: center; color: #9ca3af; font-size: 12px;">Supports CSV files up to 200MB</p>', unsafe_allow_html=True)
        if uploaded_file is not None:
             load_csv(uploaded_file, uploaded_file.name)
             st.rerun()
             
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Or try with sample data →", use_container_width=True):
             load_sample()
             st.rerun()

else:
    # ==========================================
    # SIDEBAR
    # ==========================================
    df = st.session_state.df
    
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🔍 DataLens</div>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown(f"**📁 File:** {st.session_state.filename}")
        st.markdown(f"**📊 Rows:** {df.shape[0]}")
        st.markdown(f"**📋 Columns:** {df.shape[1]}")
        
        missing_count = df.isnull().sum().sum()
        total_cells = np.prod(df.shape)
        missing_pct = (missing_count / total_cells * 100) if total_cells > 0 else 0
        st.markdown(f"**⚠️ Missing:** {missing_count} ({missing_pct:.1f}%)")
        
        dup_count = df.duplicated().sum()
        st.markdown(f"**🔁 Duplicates:** {dup_count}")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        score = get_dataset_health_score(df)
        score_class = "score-green" if score >= 80 else "score-orange" if score >= 50 else "score-red"
        icon = "✅" if score >= 80 else "⚠️" if score >= 50 else "🔴"
        
        st.markdown("**Dataset Health Score:**")
        st.markdown(f'<div class="dataset-score {score_class}">{int(score)} {icon}</div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_data,
            file_name=f"cleaned_{st.session_state.filename}",
            mime='text/csv',
            use_container_width=True
        )
        
        if st.button("❌ Clear Data"):
             st.session_state.df = None
             st.session_state.filename = None
             st.rerun()

    # ==========================================
    # MAIN AREA
    # ==========================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
      "📋 Overview",
      "📊 EDA Charts", 
      "📈 Profiling Report",
      "🔀 SweetViz",
      "⚙️ Preprocessing"
    ])
    
    # ------------------
    # TAB 1 — OVERVIEW
    # ------------------
    with tab1:
        st.markdown('<div class="section-header">Dataset Overview</div>', unsafe_allow_html=True)
        
        # Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
             st.markdown(f"""
             <div class="custom-metric">
                <div class="metric-label">📊 Total Rows</div>
                <div class="metric-val">{df.shape[0]:,}</div>
             </div>
             """, unsafe_allow_html=True)
        with col2:
             st.markdown(f"""
             <div class="custom-metric">
                <div class="metric-label">📋 Total Columns</div>
                <div class="metric-val">{df.shape[1]:,}</div>
             </div>
             """, unsafe_allow_html=True)
        with col3:
             st.markdown(f"""
             <div class="custom-metric">
                <div class="metric-label">⚠️ Missing Values</div>
                <div class="metric-val">{missing_count:,} <span style="font-size: 16px">({missing_pct:.1f}%)</span></div>
             </div>
             """, unsafe_allow_html=True)
        with col4:
             st.markdown(f"""
             <div class="custom-metric">
                <div class="metric-label">🔁 Duplicate Rows</div>
                <div class="metric-val">{dup_count:,}</div>
             </div>
             """, unsafe_allow_html=True)
             
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Data Preview
        st.markdown('<h3 style="color:white; margin-bottom: 10px;">Data Preview</h3>', unsafe_allow_html=True)
        sub_t1, sub_t2, sub_t3, sub_t4 = st.tabs(["Head", "Tail", "Info", "Describe"])
        with sub_t1:
             st.dataframe(df.head(10), use_container_width=True)
        with sub_t2:
             st.dataframe(df.tail(5), use_container_width=True)
        with sub_t3:
             info_data = []
             for col in df.columns:
                  non_null = df[col].notnull().sum()
                  dtype = str(df[col].dtype)
                  sample = df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else "N/A"
                  info_data.append({"Column Name": col, "Data Type": dtype, "Non-Null Count": non_null, "Sample Value": sample})
             st.dataframe(pd.DataFrame(info_data), use_container_width=True)
        with sub_t4:
             st.dataframe(df.describe(include='all'), use_container_width=True)
             
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Column Analysis
        st.markdown('<h3 style="color:white; margin-bottom: 10px;">Column Analysis</h3>', unsafe_allow_html=True)
        col_types = detect_column_types(df)
        
        analysis_data = []
        for col in df.columns:
             ctype = col_types[col]
             m_count = df[col].isnull().sum()
             u_count = df[col].nunique()
             top_val = df[col].mode()[0] if m_count < len(df) and not pd.isna(df[col].mode().iloc[0]) else "N/A"
             if pd.api.types.is_numeric_dtype(df[col]) and ctype == "Numerical":
                 top_val = f"{df[col].mean():.2f}"
                 
             analysis_data.append({
                 "Column Name": col,
                 "Type": ctype,
                 "Missing": m_count,
                 "Unique": u_count,
                 "Top / Mean": top_val
             })
             
        # Rendering using HTML to support badges
        html = '<table style="width:100%; text-align:left; color:white; border-collapse: collapse;">'
        html += '<tr style="background-color:#1e2130; border-bottom:1px solid #ffffff11;"><th style="padding:10px; color:#00d4ff;">Column Name</th><th>Type</th><th>Missing</th><th>Unique</th><th>Top / Mean Val</th></tr>'
        for i, row in enumerate(analysis_data):
              bg = "#111827" if i % 2 == 0 else "#1e293b"
              html += f'<tr style="background-color:{bg}; border-bottom:1px solid #ffffff11;">'
              html += f'<td style="padding:10px;">{row["Column Name"]}</td>'
              html += f'<td><span class="badge-{row["Type"]}">{row["Type"]}</span></td>'
              html += f'<td>{row["Missing"]}</td>'
              html += f'<td>{row["Unique"]}</td>'
              html += f'<td>{row["Top / Mean"]}</td>'
              html += '</tr>'
        html += '</table>'
        st.markdown(html, unsafe_allow_html=True)

    # ------------------
    # TAB 2 — EDA CHARTS
    # ------------------
    with tab2:
        col_types = detect_column_types(df)
        num_cols = [k for k, v in col_types.items() if v == 'Numerical']
        cat_cols = [k for k, v in col_types.items() if v in ['Categorical', 'Text']]
        dt_cols = [k for k, v in col_types.items() if v == 'Datetime']
        
        if len(num_cols) == 0 and len(cat_cols) == 0:
             st.warning("Not enough columns to generate EDA.")
        else:
             # 1. DISTRIBUTION PLOT
             if num_cols:
                  st.markdown('<div class="section-header">📊 Distribution Plot</div>', unsafe_allow_html=True)
                  col = st.selectbox("Select Numerical Column to view Distribution", num_cols, key='dist_col')
                  fig = plot_distribution(df, col)
                  st.plotly_chart(fig, use_container_width=True)
                  st.markdown(f'<div class="insight-box">{get_insight(df, "Distribution", col)}</div>', unsafe_allow_html=True)
                  
             # 2. BOX PLOT
             if num_cols:
                  st.markdown('<div class="section-header">📦 Box Plot — Outlier Detection</div>', unsafe_allow_html=True)
                  col = st.selectbox("Select Numerical Column to view Box Plot", num_cols, key='box_col')
                  fig = plot_boxplot(df, col)
                  st.plotly_chart(fig, use_container_width=True)
                  st.markdown(f'<div class="insight-box">{get_insight(df, "Box Plot", col)}</div>', unsafe_allow_html=True)
                  
             # 3. BAR CHART
             if cat_cols:
                  st.markdown('<div class="section-header">📊 Bar Chart</div>', unsafe_allow_html=True)
                  col = st.selectbox("Select Categorical Column to view Categories", cat_cols, key='bar_col')
                  fig = plot_bar_chart(df, col)
                  st.plotly_chart(fig, use_container_width=True)
                  st.markdown(f'<div class="insight-box">{get_insight(df, "Bar Chart", col)}</div>', unsafe_allow_html=True)
                  
             # 4. CORRELATION HEATMAP
             if len(num_cols) > 1:
                  st.markdown('<div class="section-header">🌡️ Correlation Heatmap</div>', unsafe_allow_html=True)
                  fig = plot_correlation_heatmap(df)
                  st.plotly_chart(fig, use_container_width=True)
                  st.markdown(f'<div class="insight-box">{get_insight(df, "Correlation Heatmap")}</div>', unsafe_allow_html=True)
                  
             # 5. PAIRPLOT
             if len(num_cols) > 1:
                  st.markdown('<div class="section-header">🔗 Pairplot — Scatter Matrix</div>', unsafe_allow_html=True)
                  selected = st.multiselect("Select numerical columns (max 5)", num_cols, default=num_cols[:min(3, len(num_cols))], key='pair_cols')
                  if len(selected) > 0:
                       color_col = cat_cols[0] if cat_cols else None
                       fig = plot_pairplot(df, selected, color_col)
                       st.plotly_chart(fig, use_container_width=True)
                       st.markdown(f'<div class="insight-box">{get_insight(df, "Pairplot", selected)} Color grouped by: {color_col}</div>', unsafe_allow_html=True)
                       
             # 6. MISSING VALUE HEATMAP
             st.markdown('<div class="section-header">❓ Missing Value Heatmap</div>', unsafe_allow_html=True)
             fig = plot_missing_heatmap(df)
             st.plotly_chart(fig, use_container_width=True)
             st.markdown(f'<div class="insight-box">{get_insight(df, "Missing Value Heatmap")}</div>', unsafe_allow_html=True)
             
             # 7. SKEWNESS & KURTOSIS
             if num_cols:
                  st.markdown('<div class="section-header">📐 Skewness & Kurtosis</div>', unsafe_allow_html=True)
                  f_skew, f_kurt = plot_skewness_kurtosis(df)
                  c1, c2 = st.columns(2)
                  with c1: st.plotly_chart(f_skew, use_container_width=True)
                  with c2: st.plotly_chart(f_kurt, use_container_width=True)
                  st.markdown(f'<div class="insight-box">{get_insight(df, "Skewness & Kurtosis")}</div>', unsafe_allow_html=True)
                  
             # 8. COUNT PLOT
             if cat_cols:
                  st.markdown('<div class="section-header">🔢 Count Plot</div>', unsafe_allow_html=True)
                  col = st.selectbox("Select Categorical Column to view Counts", cat_cols, key='count_col')
                  fig = plot_count_plot(df, col)
                  st.plotly_chart(fig, use_container_width=True)
                  st.markdown(f'<div class="insight-box">{get_insight(df, "Count Plot", col)}</div>', unsafe_allow_html=True)
                  
             # 9. LINE PLOT
             st.markdown('<div class="section-header">📈 Line Plot — Time Series</div>', unsafe_allow_html=True)
             if dt_cols and num_cols:
                  dc = st.selectbox("Select Datetime Column", dt_cols, key='line_dt')
                  nc = st.selectbox("Select Numerical Column", num_cols, key='line_num')
                  fig = plot_line_chart(df, dc, nc)
                  st.plotly_chart(fig, use_container_width=True)
                  st.markdown(f'<div class="insight-box">{get_insight(df, "Line Plot")}</div>', unsafe_allow_html=True)
             else:
                  st.markdown('<div class="insight-box">ℹ️ No datetime column detected in this dataset, or missing numerical targets.</div>', unsafe_allow_html=True)

    # ------------------
    # TAB 3 — PROFILING
    # ------------------
    with tab3:
         st.markdown('<div class="section-header">📈 Automated Profiling Report</div>', unsafe_allow_html=True)
         st.markdown('<p style="color: #9ca3af;">Powered by ydata-profiling</p>', unsafe_allow_html=True)
         
         st.markdown("""
         <div class="feature-card" style="margin-bottom:20px;">
            <p><strong>This comprehensive report includes:</strong></p>
            <ul>
                <li>Dataset statistics</li>
                <li>Variable analysis</li>
                <li>Correlations</li>
                <li>Missing values</li>
                <li>Data alerts & issues</li>
            </ul>
         </div>
         """, unsafe_allow_html=True)
         
         if st.button("⚡ Generate Profiling Report", key='btn_prof'):
              with st.spinner("Generating report... this may take a moment"):
                   try:
                       profile = ProfileReport(df, explorative=True, minimal=False)
                       profile.to_file("profiling_report.html")
                       with open("profiling_report.html", "r", encoding='utf-8') as f:
                           html_report = f.read()
                       st.components.v1.html(html_report, height=800, scrolling=True)
                       
                       st.download_button("📥 Download Profiling Report", html_report, "profiling_report.html", "text/html", use_container_width=True)
                   except Exception as e:
                       st.error(f"Error generating profiling report: {str(e)}")

    # ------------------
    # TAB 4 — SWEETVIZ
    # ------------------
    with tab4:
         st.markdown('<div class="section-header">🔀 SweetViz Visual EDA</div>', unsafe_allow_html=True)
         choice = st.radio("", ["📊 Analyze Single Dataset", "🆚 Compare Two Datasets"], horizontal=True)
         
         if choice == "📊 Analyze Single Dataset":
              if st.button("⚡ Generate SweetViz Report", key='btn_sv_single'):
                   with st.spinner("Generating SweetViz report..."):
                        try:
                            # Using html export since it does not block the thread
                            report = sv.analyze(df)
                            report.show_html("sweetviz_report.html", open_browser=False)
                            with open("sweetviz_report.html", "r", encoding='utf-8') as f:
                                html_sv = f.read()
                            st.components.v1.html(html_sv, height=800, scrolling=True)
                            st.download_button("📥 Download SweetViz Report", html_sv, "sweetviz_report.html", "text/html", use_container_width=True)
                        except Exception as e:
                            st.error(f"Error generating SweetViz: {e}")
         else:
              df2_file = st.file_uploader("Upload Dataset B to compare against", type=['csv'])
              if df2_file is not None:
                   try:
                       df2 = pd.read_csv(df2_file)
                       st.success("Dataset B loaded")
                       if st.button("⚡ Compare Datasets", key='btn_sv_comp'):
                            with st.spinner("Generating Comparison..."):
                                report = sv.compare([df, "Dataset A"], [df2, "Dataset B"])
                                report.show_html("compare_report.html", open_browser=False)
                                with open("compare_report.html", "r", encoding='utf-8') as f:
                                    html_sv = f.read()
                                st.components.v1.html(html_sv, height=800, scrolling=True)
                                st.download_button("📥 Download Comparison Report", html_sv, "compare_report.html", "text/html", use_container_width=True)
                   except Exception as e:
                       st.error(f"Error loading second dataset or comparing: {e}")

    # ------------------
    # TAB 5 — PREPROCESS
    # ------------------
    with tab5:
         st.markdown('<div class="section-header">⚙️ Preprocessing</div>', unsafe_allow_html=True)
         st.markdown(f'<div style="background-color: #111827; padding: 10px; border-radius: 8px; border: 1px solid #00d4ff44; margin-bottom: 20px; color:#00d4ff; font-weight:bold;">Dataset: {df.shape[0]} rows × {df.shape[1]} columns</div>', unsafe_allow_html=True)
         
         # SECTION A — MISSING VALUES
         with st.expander("▸ SECTION A — MISSING VALUES"):
              missing_cols = df.columns[df.isnull().sum() > 0].tolist()
              if missing_cols:
                   miss_data = []
                   col_types = detect_column_types(df)
                   for c in missing_cols:
                        miss_data.append({"Column": c, "Type": col_types[c], "Missing Count": df[c].isnull().sum(), "Missing %": f"{(df[c].isnull().sum()/len(df)*100):.2f}%"})
                   st.dataframe(pd.DataFrame(miss_data), use_container_width=True)
                   
                   selected_miss_cols = st.multiselect("Select columns", missing_cols, key='miss_cols')
                   method_miss = st.radio("Treatment method", ["Drop rows with nulls", "Fill with Mean", "Fill with Median", "Fill with Mode", "Fill with Custom Value"], key='rad_miss')
                   
                   custom_val = None
                   if method_miss == "Fill with Custom Value":
                        custom_val = st.text_input("Enter custom value")
                        
                   if st.button("✅ Apply", key='btn_miss'):
                        if selected_miss_cols:
                             new_df, msg = handle_missing_values(df, selected_miss_cols, method_miss, custom_val)
                             st.success(msg)
                             c1, c2 = st.columns(2)
                             with c1:
                                  st.markdown("<h4 style='color:#ef4444'>Before</h4>", unsafe_allow_html=True)
                                  st.dataframe(df[selected_miss_cols].head())
                             with c2:
                                  st.markdown("<h4 style='color:#10b981'>After</h4>", unsafe_allow_html=True)
                                  st.dataframe(new_df[selected_miss_cols].head())
                             # Update session state df
                             st.session_state.df = new_df
                        else:
                             st.warning("Please select at least one column")
              else:
                   st.info("No missing values found in the dataset.")
                   
         # SECTION B — REMOVE DUPLICATES
         with st.expander("▸ SECTION B — REMOVE DUPLICATES"):
              st.markdown(f"Found **{df.duplicated().sum()}** duplicate rows.")
              if st.button("🗑️ Remove Duplicates", key='btn_dup', disabled=df.duplicated().sum()==0):
                   new_df, msg = remove_duplicates(df)
                   st.success(msg)
                   st.session_state.df = new_df
                   
         # SECTION C — ENCODE CATEGORICAL
         with st.expander("▸ SECTION C — ENCODE CATEGORICAL"):
              cat_cols = [k for k, v in detect_column_types(df).items() if v in ['Categorical', 'Text']]
              if cat_cols:
                   selected_enc = st.multiselect("Select categorical columns to encode", cat_cols, key='enc_cols')
                   enc_method = st.radio("Encoding Method", ["Label Encoding", "One-Hot Encoding"], key='rad_enc')
                   
                   st.markdown("""
                   <div style="background:#111827; padding:10px; border-left:3px solid #7c3aed; font-size:13px; color:#9ca3af; margin-bottom:15px;">
                   <strong>Label Encoding:</strong> converts categories to numbers (0,1,2)<br>
                   <strong>One-Hot Encoding:</strong> creates new binary column per category
                   </div>
                   """, unsafe_allow_html=True)
                   
                   if st.button("⚙️ Apply Encoding", key='btn_enc'):
                        if selected_enc:
                             new_df, msg = encode_categorical(df, selected_enc, enc_method)
                             st.success(msg)
                             c1, c2 = st.columns(2)
                             with c1:
                                  st.markdown("<h4 style='color:#ef4444'>Before</h4>", unsafe_allow_html=True)
                                  st.dataframe(df.head())
                             with c2:
                                  st.markdown("<h4 style='color:#10b981'>After</h4>", unsafe_allow_html=True)
                                  st.dataframe(new_df.head())
                             st.session_state.df = new_df
                        else:
                             st.warning("Please select at least one column")
              else:
                   st.info("No categorical columns detected.")
                   
         # SECTION D — SCALE NUMERICAL
         with st.expander("▸ SECTION D — SCALE NUMERICAL"):
              num_cols = [k for k, v in detect_column_types(df).items() if v == 'Numerical']
              if num_cols:
                   selected_scale = st.multiselect("Select numerical columns to scale", num_cols, key='scale_cols')
                   scale_method = st.radio("Scaling Method", ["Min-Max Normalization", "Standard Scaling (Z-score)"], key='rad_scale')
                   
                   st.markdown("""
                   <div style="background:#111827; padding:10px; border-left:3px solid #7c3aed; font-size:13px; color:#9ca3af; margin-bottom:15px;">
                   <strong>Min-Max:</strong> scales to range [0, 1]<br>
                   <strong>Z-score:</strong> standardizes to mean=0, std=1
                   </div>
                   """, unsafe_allow_html=True)
                   
                   if st.button("⚙️ Apply Scaling", key='btn_scale'):
                        if selected_scale:
                             new_df, msg = scale_numerical(df, selected_scale, scale_method)
                             st.success(msg)
                             c1, c2 = st.columns(2)
                             with c1:
                                  st.markdown("<h4 style='color:#ef4444'>Before</h4>", unsafe_allow_html=True)
                                  st.dataframe(df[selected_scale].head())
                             with c2:
                                  st.markdown("<h4 style='color:#10b981'>After</h4>", unsafe_allow_html=True)
                                  st.dataframe(new_df[selected_scale].head())
                             st.session_state.df = new_df
                        else:
                             st.warning("Please select at least one column")
              else:
                   st.info("No numerical columns detected.")
         
         # SECTION E — DOWNLOAD
         st.markdown("<br><hr>", unsafe_allow_html=True)
         csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
         st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_data,
            file_name=f"preprocessed_{st.session_state.filename}",
            mime='text/csv',
            use_container_width=True
         )
