import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("AIzaSyC4gI5TnEwFwJWMR3cO85F8nbde91dY9j8"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Talking Rabbitt AI", layout="wide")

# ---------- UI STYLE ----------
st.markdown("""
<style>
.main-title{
font-size:40px;
font-weight:700;
color:#4F46E5;
}
.insight-box{
padding:15px;
background:#F9FAFB;
border-left:6px solid #4F46E5;
border-radius:5px;
margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Talking Rabbitt – AI Data Copilot</p>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV",
    type=["csv"]
)

# ---------- DATA LOADING ----------
df = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.sidebar.success("Dataset loaded")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Summary")

    st.write("Rows:", df.shape[0])
    st.write("Columns:", list(df.columns))

# ---------- SUGGESTED QUERIES ----------
suggested_queries = [
    "Which region has the highest revenue?",
    "Show revenue by region",
    "Revenue trend over time",
    "Which product sells the most?"
]

st.sidebar.subheader("Suggested Queries")

for q in suggested_queries:
    if st.sidebar.button(q):
        st.session_state["query"] = q

# ---------- USER QUERY ----------
query = st.text_input(
    "Ask a question about your dataset",
    value=st.session_state.get("query","")
)

# ---------- AI QUERY INTERPRETER ----------
def interpret_query(question, columns):

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

    response = model.generate_content(prompt)

    text = response.text.replace("```json","").replace("```","")

    try:
        plan = json.loads(text)
    except:
        plan = {
            "group_by": columns[0],
            "metric": columns[1],
            "chart": "bar"
        }

    return plan

# ---------- RUN QUERY ----------
if query and df is not None:

    plan = interpret_query(query, list(df.columns))

    group = plan["group_by"]
    metric = plan["metric"]
    chart_type = plan["chart"]

    result = (
        df.groupby(group)[metric]
        .sum()
        .reset_index()
    )

    st.subheader("AI Insight")

    best = result.loc[result[metric].idxmax()][group]

    st.markdown(
        f'<div class="insight-box">{best} has the highest {metric}</div>',
        unsafe_allow_html=True
    )

    st.subheader("Visualization")

    fig, ax = plt.subplots()

    if chart_type == "line":
        sns.lineplot(data=result, x=group, y=metric, ax=ax)

    elif chart_type == "pie":
        ax.pie(result[metric], labels=result[group], autopct="%1.1f%%")

    else:
        sns.barplot(data=result, x=group, y=metric, ax=ax)

    st.pyplot(fig)