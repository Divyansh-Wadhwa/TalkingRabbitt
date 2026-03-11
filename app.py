import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Talking Rabbitt AI", layout="wide", initial_sidebar_state="expanded")

# ---------- MODERN PROFESSIONAL UI ----------
st.markdown("""
<style>
/* Global Reset */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff;
}

/* Main Container */
.main-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

/* Professional Header */
.pro-header {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    text-align: center;
}

.pro-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff, #e0e0e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.pro-subtitle {
    font-size: 1.2rem;
    color: #e0e0e0;
    font-weight: 400;
}

/* Sidebar */
.css-1d391kg {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    padding: 2rem;
}

.sidebar-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 2rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Stats Cards */
.stats-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.5s ease;
}

.stat-card:hover::before {
    left: 100%;
}

.stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 255, 255, 0.4);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}

.stat-label {
    font-size: 0.9rem;
    color: #e0e0e0;
    text-transform: uppercase;
    letter-spacing: 1px;
    position: relative;
    z-index: 1;
}

/* Content Sections */
.content-section {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    position: relative;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.section-icon {
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

/* Query Input - Enhanced Big Search Bar */
.query-input-container {
    background: rgba(255, 255, 255, 0.15);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
}

.query-input-container:hover {
    border-color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.2);
}

.query-text {
    font-size: 1.3rem;
    color: #ffffff;
    margin-bottom: 1.5rem;
    font-weight: 600;
    text-align: center;
}

/* Quick Actions Grid */
.quick-actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.action-button {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 1.2rem;
    font-size: 0.95rem;
    color: #ffffff;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    font-weight: 600;
}

.action-button:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.4);
    transform: translateY(-2px);
}

/* Results */
.result-highlight {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
    border-left: 5px solid #ffffff;
    border-radius: 0 16px 16px 0;
    padding: 2rem;
    margin-bottom: 2rem;
    position: relative;
}

.result-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 1rem;
}

.result-text {
    font-size: 1.1rem;
    color: #e0e0e0;
    line-height: 1.6;
}

/* Chart Container */
.chart-container {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
}

/* Data Table */
.data-table {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    overflow: hidden;
}

/* Column Tags */
.column-tag {
    display: inline-block;
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Welcome State */
.welcome-container {
    text-align: center;
    padding: 6rem 3rem;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    margin: 2rem 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.welcome-icon {
    font-size: 5rem;
    margin-bottom: 2rem;
    opacity: 0.8;
}

.welcome-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 1rem;
}

.welcome-text {
    font-size: 1.2rem;
    color: #e0e0e0;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Streamlit Overrides */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 1rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 1.5rem;
    font-size: 1.2rem;
    color: #ffffff;
    transition: all 0.3s ease;
    height: 60px;
    font-weight: 500;
}

.stTextInput > div > div > input:focus {
    border-color: #60a5fa;
    outline: none;
    box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.3);
    background: rgba(255, 255, 255, 0.15);
}

.stTextInput > div > div > input::placeholder {
    color: #b0b0b0;
    font-size: 1.1rem;
}

.stFileUploader {
    border: 2px dashed rgba(255, 255, 255, 0.3);
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.05);
    padding: 2rem;
    transition: all 0.3s ease;
}

.stFileUploader:hover {
    border-color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.1);
}

.stDataFrame {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    overflow: hidden;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.8rem 1.5rem;
    font-size: 0.95rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
    .stats-container {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .quick-actions-grid {
        grid-template-columns: 1fr;
    }
    
    .pro-title {
        font-size: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- PROFESSIONAL HEADER ----------
st.markdown("""
<div class="pro-header">
    <h1 class="pro-title">Talking Rabbitt AI</h1>
    <p class="pro-subtitle">Advanced Data Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# ---------- MODERN SIDEBAR ----------
st.sidebar.markdown("""
<div class="sidebar-header">
    Data Intelligence
</div>
""", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset",
    type=["csv"],
    help="Choose your CSV file to begin analysis"
)

# ---------- QUERY VARIABLE ----------
query = st.session_state.get("query", "")

# ---------- ENHANCED DASHBOARD FUNCTIONS ----------
def create_comprehensive_dashboard(df):
    """Create a comprehensive dashboard with multiple visualizations"""
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    dashboard_data = {}
    
    # 1. Distribution Analysis
    if numeric_cols:
        dashboard_data['distributions'] = {}
        for col in numeric_cols[:3]:  # Limit to first 3 numeric columns
            dashboard_data['distributions'][col] = {
                'histogram': df[col].describe(),
                'outliers': df[col][(df[col] < df[col].quantile(0.25) - 1.5*(df[col].quantile(0.75)-df[col].quantile(0.25))) | 
                           (df[col] > df[col].quantile(0.75) + 1.5*(df[col].quantile(0.75)-df[col].quantile(0.25)))].count()
            }
    
    # 2. Correlation Analysis
    if len(numeric_cols) >= 2:
        correlation_matrix = df[numeric_cols].corr()
        high_correlations = correlation_matrix[(correlation_matrix > 0.7) & (correlation_matrix < 1.0)].stack()
        dashboard_data['correlations'] = {
            'matrix': correlation_matrix,
            'high_corr_pairs': high_correlations.tolist()[:5]
        }
    
    # 3. Categorical Analysis
    if categorical_cols:
        dashboard_data['categorical'] = {}
        for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
            value_counts = df[col].value_counts()
            dashboard_data['categorical'][col] = {
                'counts': value_counts,
                'unique_count': len(value_counts),
                'top_category': value_counts.index[0] if len(value_counts) > 0 else None,
                'top_percentage': (value_counts.iloc[0] / len(df) * 100) if len(value_counts) > 0 else 0
            }
    
    # 4. Trend Analysis (if date columns exist)
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    if date_cols and numeric_cols:
        dashboard_data['trends'] = {}
        date_col = date_cols[0]
        for num_col in numeric_cols[:2]:
            trend_data = df.groupby(df[date_col].dt.to_period('M'))[num_col].mean()
            dashboard_data['trends'][f'{num_col}_by_{date_col}'] = trend_data
    
    # 5. Missing Data Analysis
    missing_data = df.isnull().sum()
    dashboard_data['missing_data'] = {
        'total_missing': missing_data.sum(),
        'missing_percentage': (missing_data / len(df) * 100).round(2),
        'columns_with_missing': missing_data[missing_data > 0].to_dict()
    }
    
    return dashboard_data

def create_multi_chart_visualization(df, dashboard_data):
    """Create multiple charts using Plotly for better interactivity"""
    charts = []
    
    # 1. Distribution Charts
    if 'distributions' in dashboard_data:
        for col, data in dashboard_data['distributions'].items():
            fig = px.histogram(df, x=col, title=f'Distribution of {col}', 
                             color_discrete_sequence=['#60a5fa'])
            fig.update_layout(showlegend=False, height=300)
            charts.append(('Distribution', fig))
    
    # 2. Correlation Heatmap
    if 'correlations' in dashboard_data:
        corr_matrix = dashboard_data['correlations']['matrix']
        fig = px.imshow(corr_matrix, title='Correlation Matrix', 
                       color_continuous_scale='RdBu_r', aspect='auto')
        fig.update_layout(height=400)
        charts.append(('Correlation', fig))
    
    # 3. Categorical Charts
    if 'categorical' in dashboard_data:
        for col, data in dashboard_data['categorical'].items():
            if len(data['counts']) <= 10:  # Only show if not too many categories
                fig = px.bar(x=data['counts'].index, y=data['counts'].values, 
                           title=f'Count by {col}', labels={'x': col, 'y': 'Count'},
                           color_discrete_sequence=['#60a5fa'])
                fig.update_layout(height=300)
                charts.append(('Categorical', fig))
    
    # 4. Trend Charts
    if 'trends' in dashboard_data:
        for name, trend_data in dashboard_data['trends'].items():
            fig = px.line(x=trend_data.index.astype(str), y=trend_data.values, 
                        title=f'Trend: {name}', labels={'x': 'Period', 'y': 'Value'})
            fig.update_layout(height=300)
            charts.append(('Trend', fig))
    
    # 5. Missing Data Chart
    if 'missing_data' in dashboard_data:
        missing_df = pd.DataFrame(dashboard_data['missing_data']['columns_with_missing'].items(), 
                                 columns=['Column', 'Missing Count'])
        if len(missing_df) > 0:
            fig = px.bar(missing_df, x='Column', y='Missing Count', 
                        title='Missing Data by Column',
                        color_discrete_sequence=['#ef4444'])
            fig.update_layout(height=300)
            charts.append(('Missing Data', fig))
    
    return charts

def create_summary_statistics(df):
    """Create comprehensive summary statistics"""
    stats = {
        'dataset_info': {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB",
            'numeric_columns': len(df.select_dtypes(include=['number']).columns),
            'categorical_columns': len(df.select_dtypes(include=['object']).columns),
            'datetime_columns': len(df.select_dtypes(include=['datetime64']).columns)
        },
        'data_quality': {
            'duplicate_rows': df.duplicated().sum(),
            'total_missing': df.isnull().sum().sum(),
            'missing_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100).round(2),
            'columns_with_missing': df.isnull().sum()[df.isnull().sum() > 0].to_dict()
        }
    }
    
    # Column-wise statistics
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        stats['numeric_summary'] = df[numeric_cols].describe().round(2).to_dict()
    
    return stats

def interpret_query(question, columns):
    """Convert user question to JSON for analysis"""
    prompt = f"""
You are a data analyst.

Dataset columns:
{columns}

Convert the user question into JSON.

Return only JSON:

{{
"group_by":"column",
"metric":"column",
"chart":"bar|line|pie"
}}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    text = response.choices[0].message.content.replace("```json","").replace("```","")

    try:
        plan = json.loads(text)
        if 'group_by' not in plan or 'metric' not in plan or 'chart' not in plan:
            plan = {
                "group_by": columns[0],
                "metric": columns[1],
                "chart": "bar"
            }
    except:
        plan = {
            "group_by": columns[0],
            "metric": columns[1],
            "chart": "bar"
        }

    return plan

# ---------- MAIN LAYOUT ----------
df = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Success notification
    st.sidebar.success("Dataset loaded successfully!")
    st.sidebar.success("✓ Dataset loaded")
    
    # Enhanced stats row
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">{}</div>
            <div class="stat-label">Rows</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{}</div>
            <div class="stat-label">Columns</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{}</div>
            <div class="stat-label">Size</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{}</div>
            <div class="stat-label">Numeric</div>
        </div>
    </div>
    """.format(df.shape[0], df.shape[1], f"{df.memory_usage(deep=True).sum() / 1024:.0f}KB", len(df.select_dtypes(include=['number']).columns)), unsafe_allow_html=True)
    
    # Generate comprehensive dashboard
    dashboard_data = create_comprehensive_dashboard(df)
    charts = create_multi_chart_visualization(df, dashboard_data)
    summary_stats = create_summary_statistics(df)
    
    # Enhanced layout with three columns
    col_data, col_query, col_insights = st.columns([2, 1, 1])
    
    with col_data:
        # Data preview section
        st.markdown("""
        <div class="content-section">
            <div class="section-title">
                <div class="section-icon">📊</div>
                Data Preview
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(df.head(), use_container_width=True)
        
        # Column information
        st.markdown("""
        <div class="content-section">
            <div class="section-title">
                <div class="section-icon">📋</div>
                Columns & Types
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for col in df.columns:
            dtype = str(df[col].dtype)
            st.markdown(f"""
            <span class="column-tag">{col} ({dtype})</span>
            """, unsafe_allow_html=True)
    
    with col_query:
        # Enhanced query section with big search bar
        st.markdown("""
        <div class="content-section">
            <div class="section-title">
                <div class="section-icon">🔍</div>
                AI Query Interface
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="query-input-container">
            <div class="query-text">💬 Ask questions about your data in natural language</div>
        </div>
        """, unsafe_allow_html=True)
        
        query = st.text_input(
            "🔍 Search your data...",
            value=st.session_state.get("query", ""),
            placeholder="e.g., 'Show me the least selling products' or 'What are the top performing regions?'",
            key="main_query"
        )
        
        # Quick actions
        st.markdown("""
        <div class="section-title">
            <div class="section-icon">⚡</div>
            Quick Actions
        </div>
        """, unsafe_allow_html=True)
        
        suggested_queries = [
            "Revenue by region",
            "Top products",
            "Sales trends",
            "Regional analysis"
        ]
        
        for q in suggested_queries:
            if st.button(q, key=f"quick_{q}", use_container_width=True):
                st.session_state["query"] = q
                st.rerun()
    
    with col_insights:
        # Quick insights
        st.markdown("""
        <div class="content-section">
            <div class="section-title">
                <div class="section-icon">💡</div>
                Quick Insights
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Dataset quality score
        quality_score = 100 - summary_stats['data_quality']['missing_percentage']
        st.metric("Data Quality", f"{quality_score:.1f}%", 
                 delta=f"Missing: {summary_stats['data_quality']['missing_percentage']:.1f}%")
        
        # Key statistics
        if 'distributions' in dashboard_data:
            for col, data in list(dashboard_data['distributions'].items())[:2]:
                st.metric(f"{col} Mean", f"{data['histogram']['mean']:.2f}")
        
        # Top category info
        if 'categorical' in dashboard_data:
            for col, data in list(dashboard_data['categorical'].items())[:2]:
                if data['top_category']:
                    st.metric(f"Top {col}", data['top_category'], 
                             f"{data['top_percentage']:.1f}%")
    
    # Comprehensive Dashboard Section
    st.markdown("""
    <div class="content-section">
        <div class="section-title">
            <div class="section-icon">📈</div>
            Comprehensive Analytics Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display multiple charts in a grid
    if charts:
        # Create tabs for different chart categories
        chart_categories = {}
        for chart_type, fig in charts:
            if chart_type not in chart_categories:
                chart_categories[chart_type] = []
            chart_categories[chart_type].append(fig)
        
        # Display charts in tabs
        tab_names = list(chart_categories.keys())
        if tab_names:
            tabs = st.tabs(tab_names)
            
            for i, (tab_name, figs) in enumerate(chart_categories.items()):
                with tabs[i]:
                    for fig in figs:
                        st.plotly_chart(fig, use_container_width=True)
    
    # Summary Statistics Section
    st.markdown("""
    <div class="content-section">
        <div class="section-title">
            <div class="section-icon">📊</div>
            Summary Statistics
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display summary statistics in expandable sections
    with st.expander("Dataset Overview", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Rows", summary_stats['dataset_info']['total_rows'])
            st.metric("Total Columns", summary_stats['dataset_info']['total_columns'])
        
        with col2:
            st.metric("Memory Usage", summary_stats['dataset_info']['memory_usage'])
            st.metric("Numeric Columns", summary_stats['dataset_info']['numeric_columns'])
        
        with col3:
            st.metric("Categorical Columns", summary_stats['dataset_info']['categorical_columns'])
            st.metric("Duplicate Rows", summary_stats['data_quality']['duplicate_rows'])
    
    with st.expander("Data Quality"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Missing", summary_stats['data_quality']['total_missing'])
            st.metric("Missing %", f"{summary_stats['data_quality']['missing_percentage']:.2f}%")
        
        with col2:
            if summary_stats['data_quality']['total_missing'] > 0:
                missing_df = pd.DataFrame(list(summary_stats['data_quality']['columns_with_missing'].items()), 
                                       columns=['Column', 'Missing Count'])
                st.dataframe(missing_df, use_container_width=True)
            else:
                st.success("✓ No missing data found!")
    
    if 'numeric_summary' in summary_stats:
        with st.expander("Numeric Column Statistics"):
            stats_df = pd.DataFrame(summary_stats['numeric_summary'])
            st.dataframe(stats_df, use_container_width=True)

# ---------- RESULTS DISPLAY ----------
if query and df is not None:
    
    # Show loading state
    with st.spinner('🔍 Analyzing your data...'):
        plan = interpret_query(query, list(df.columns))
        
        group = plan["group_by"]
        metric = plan["metric"]
        chart_type = plan["chart"]
        
        result = (
            df.groupby(group)[metric]
            .sum()
            .reset_index()
        )
        
        # Smart insight display based on query intent
        best = result.loc[result[metric].idxmax()][group]
        worst = result.loc[result[metric].idxmin()][group]
        
        # Determine user intent from query
        query_lower = query.lower()
        if any(word in query_lower for word in ['least', 'lowest', 'worst', 'minimum', 'bottom', 'fewest', 'poor', 'underperforming']):
            insight_value = result.loc[result[metric].idxmin()][metric]
            insight_label = worst
            insight_type = "Lowest"
        elif any(word in query_lower for word in ['highest', 'most', 'best', 'maximum', 'top', 'greatest', 'excellent', 'outstanding']):
            insight_value = result.loc[result[metric].idxmax()][metric]
            insight_label = best
            insight_type = "Highest"
        else:
            # Default to showing highest
            insight_value = result.loc[result[metric].idxmax()][metric]
            insight_label = best
            insight_type = "Highest"
        
        st.markdown(f"""
        <div class="result-highlight">
            <div class="result-title">🎯 Analysis Result</div>
            <div class="result-text">
                <strong>{insight_label}</strong> has the {insight_type} {metric} ({insight_value:,.2f})
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Chart section
        st.markdown("""
        <div class="chart-container">
            <div class="section-title">
                <div class="section-icon">📊</div>
                Visualization
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional chart styling
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Set dark theme colors
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#2d3748')
        
        if chart_type == "line":
            sns.lineplot(data=result, x=group, y=metric, ax=ax, 
                        color='#60a5fa', linewidth=3, marker='o', markersize=8,
                        markerfacecolor='#a78bfa', markeredgewidth=2)
            ax.fill_between(result[group], result[metric], alpha=0.3, color='#60a5fa')
        elif chart_type == "pie":
            colors = ['#60a5fa', '#a78bfa', '#f472b6', '#10b981', '#f59e0b', '#ef4444']
            wedges, texts, autotexts = ax.pie(result[metric], labels=result[group], autopct="%1.1f%%", 
                   colors=colors[:len(result)], startangle=90, 
                   textprops={'color': 'white', 'fontweight': 'bold'})
        else:
            sns.barplot(data=result, x=group, y=metric, ax=ax, 
                       palette=['#60a5fa', '#a78bfa', '#f472b6', '#10b981', '#f59e0b', '#ef4444'][:len(result)])
        
        # Professional chart styling
        ax.set_xlabel(group.replace('_', ' ').title(), color='#f1f5f9', fontsize=12, fontweight='600')
        ax.set_ylabel(metric.replace('_', ' ').title(), color='#f1f5f9', fontsize=12, fontweight='600')
        ax.set_title(f'{metric.replace("_", " ").title()} Analysis by {group.replace("_", " ").title()}', 
                    color='#60a5fa', fontsize=14, fontweight='700', pad=20)
        
        # Neon grid and spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#60a5fa')
        ax.spines['bottom'].set_color('#60a5fa')
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)
        ax.grid(True, alpha=0.2, color='#60a5fa', linestyle='--')
        ax.tick_params(colors='#f1f5f9')
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        
        # Results table
        st.markdown("""
        <div class="content-section">
            <div class="section-title">
                <div class="section-icon">📋</div>
                Analysis Results
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Format results
        formatted_result = result.copy()
        formatted_result[metric] = formatted_result[metric].apply(lambda x: f"{x:,.2f}")
        st.dataframe(formatted_result, use_container_width=True)
        
        # Export options
        st.markdown("""
        <div class="content-section">
            <div class="section-title">
                <div class="section-icon">💾</div>
                Export Options
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Results",
                data=result.to_csv(index=False).encode('utf-8'),
                file_name=f'analysis_{metric}_by_{group}.csv',
                mime='text/csv'
            )
        
        with col2:
            st.download_button(
                label="📊 Export Chart",
                data='',
                file_name='',
                mime='',
                disabled=True
            )
            
else:
    # Welcome state
    if not uploaded_file:
        st.markdown("""
        <div class="welcome-container">
            <div class="welcome-icon">🚀</div>
            <div class="welcome-title">Advanced Data Intelligence</div>
            <div class="welcome-text">
                Upload your CSV dataset to unlock powerful AI-driven insights.
                Get comprehensive analysis, visualizations, and actionable intelligence.
            </div>
        </div>
        """, unsafe_allow_html=True)
