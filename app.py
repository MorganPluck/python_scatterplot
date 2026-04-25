import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Morgan's Data Viz Gallery",
    page_icon="📊",
    layout="wide",
)

# ── Minimal dark-themed CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    code, .stCode { font-family: 'JetBrains Mono', monospace; }

    .stApp { background: #0d1117; color: #e6edf3; }
    .block-container { padding: 2rem 2.5rem; max-width: 1200px; }

    .gallery-header {
        border-left: 3px solid #58a6ff;
        padding: 0.4rem 1rem;
        margin-bottom: 1.5rem;
        background: #161b22;
        border-radius: 0 6px 6px 0;
    }
    .gallery-header h1 { margin: 0; font-size: 1.6rem; color: #e6edf3; }
    .gallery-header p  { margin: 0.2rem 0 0; color: #8b949e; font-size: 0.9rem; }

    .demo-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
        cursor: pointer;
    }
    .demo-card:hover { border-color: #58a6ff; }
    .demo-card .title { font-weight: 600; color: #58a6ff; font-size: 0.95rem; }
    .demo-card .desc  { color: #8b949e; font-size: 0.82rem; margin-top: 0.2rem; }
    .demo-card .tags  { margin-top: 0.5rem; }
    .tag {
        display: inline-block;
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 1px 8px;
        font-size: 0.74rem;
        color: #8b949e;
        margin-right: 4px;
    }

    [data-testid="stSidebar"] {
        background: #161b22;
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] label { color: #e6edf3 !important; }

    .stButton > button {
        background: #21262d;
        color: #58a6ff;
        border: 1px solid #30363d;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
    }
    .stButton > button:hover { border-color: #58a6ff; }
</style>
""", unsafe_allow_html=True)

# ── Demo registry ─────────────────────────────────────────────────────────────
DEMOS = {
    "🛒 Mall Customers — Income vs Spending": {
        "file": "pd_plotting_groups.py",
        "desc": "Scatter plot comparing male vs female income distributions across age groups using real mall customer data.",
        "tags": ["pandas", "matplotlib", "real data", "scatter"],
        "category": "Pandas",
    },
    "📊 Mall Customers — Group Aggregates": {
        "file": "pd_group_aggregates.py",
        "desc": "GroupBy operations with mean, std, and len aggregations on mall customer gender groups.",
        "tags": ["pandas", "groupby", "aggregation"],
        "category": "Pandas",
    },
    "🔍 Mall Customers — Filtering": {
        "file": "pd_filtering.py",
        "desc": "Boolean indexing on NumPy arrays and DataFrames, filtering by gender and age.",
        "tags": ["pandas", "numpy", "filtering"],
        "category": "Pandas",
    },
    "📦 Price Binning (pd.qcut)": {
        "file": "pd_binning.py",
        "desc": "Quantile-based binning of random price data into Low / Middle / High categories.",
        "tags": ["pandas", "qcut", "binning"],
        "category": "Pandas",
    },
    "〰️ Trig Functions — Multiple Lines": {
        "file": "plt_multiple.py",
        "desc": "Overlaid sin(x) and cos(x) on a single axes with legends.",
        "tags": ["matplotlib", "line chart"],
        "category": "Matplotlib",
    },
    "🪟 Trig Functions — Subplots": {
        "file": "plt_subplots.py",
        "desc": "sin(x) and cos(x) laid out in a 3×2 subplot grid (positions 1 and 6).",
        "tags": ["matplotlib", "subplots"],
        "category": "Matplotlib",
    },
    "🔵 Scatter Plot — Random Data": {
        "file": "plt_scatter.py",
        "desc": "1 000-point scatter with alpha, custom colours, and edge colours.",
        "tags": ["matplotlib", "scatter"],
        "category": "Matplotlib",
    },
    "📉 Histogram": {
        "file": "plt_histograms.py",
        "desc": "Histogram of 10 000 Gaussian samples with custom bin edges and white edge colour.",
        "tags": ["matplotlib", "histogram"],
        "category": "Matplotlib",
    },
    "🌐 3D Plots — Scatter & Helix": {
        "file": "plt_3d.py",
        "desc": "Two 3D subplots: a random scatter cloud and a cos/sin helix spiral.",
        "tags": ["matplotlib", "3d", "mplot3d"],
        "category": "Matplotlib",
    },
    "📖 Word Frequency (Great Expectations)": {
        "file": "wordcounts.txt",
        "desc": "Top-50 word frequency bar chart from a word-count dataset (Great Expectations).",
        "tags": ["pandas", "bar chart", "text data"],
        "category": "Data",
    },
    "📏 Word Length Distribution": {
        "file": "wordlengths.csv",
        "desc": "Bar chart of word-length frequencies showing the most common word lengths.",
        "tags": ["pandas", "bar chart", "csv"],
        "category": "Data",
    },
}

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📂 Gallery")
    categories = ["All"] + sorted(set(d["category"] for d in DEMOS.values()))
    cat_filter = st.selectbox("Filter by category", categories)

    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "A portfolio showcase of matplotlib & pandas demos. "
        "Select any script to view its source and live output."
    )

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gallery-header">
  <h1>📊 Data Viz Gallery</h1>
  <p>Interactive demos · matplotlib · pandas · NumPy</p>
</div>
""", unsafe_allow_html=True)

# ── Filter demos ──────────────────────────────────────────────────────────────
filtered = {k: v for k, v in DEMOS.items()
            if cat_filter == "All" or v["category"] == cat_filter}

demo_name = st.selectbox(
    "Choose a demo",
    list(filtered.keys()),
    format_func=lambda x: x,
)
demo = filtered[demo_name]

st.markdown("---")

# ── Two-column layout: code | output ─────────────────────────────────────────
col_code, col_out = st.columns([1, 1], gap="large")

# ── Helper: load source ───────────────────────────────────────────────────────
import os

UPLOAD_DIR = "/mnt/user-data/uploads"

def load_source(filename):
    path = os.path.join(UPLOAD_DIR, filename)
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return f"# File not found: {filename}"

# ── Source code panel ─────────────────────────────────────────────────────────
with col_code:
    st.markdown(f"### 📄 `{demo['file']}`")
    for tag in demo["tags"]:
        st.markdown(f"`{tag}` ", unsafe_allow_html=False)

    src = load_source(demo["file"])
    st.code(src, language="python" if demo["file"].endswith(".py") else "text")

    st.caption(demo["desc"])

# ── Live output panel ─────────────────────────────────────────────────────────
with col_out:
    st.markdown("### ▶ Live Output")

    # ── Matplotlib helper ─────────────────────────────────────────────────────
    def show_fig(fig):
        fig.patch.set_facecolor("#0d1117")
        for ax in fig.get_axes():
            ax.set_facecolor("#161b22")
            ax.tick_params(colors="#8b949e")
            ax.xaxis.label.set_color("#8b949e")
            ax.yaxis.label.set_color("#8b949e")
            ax.title.set_color("#e6edf3")
            for spine in ax.spines.values():
                spine.set_edgecolor("#30363d")
        st.pyplot(fig)
        plt.close(fig)

    # ── Run each demo ─────────────────────────────────────────────────────────
    name = demo_name

    if name == "〰️ Trig Functions — Multiple Lines":
        x = np.linspace(0, 20, 1000)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x, np.sin(x), color="#58a6ff", label="sin(x)")
        ax.plot(x, np.cos(x), color="#f78166", label="cos(x)")
        ax.set_title("Trig Functions"); ax.set_xlabel("x"); ax.set_ylabel("y")
        ax.legend(facecolor="#21262d", edgecolor="#30363d", labelcolor="#e6edf3")
        show_fig(fig)

    elif name == "🪟 Trig Functions — Subplots":
        x = np.linspace(9, 20, 1000)
        fig = plt.figure(figsize=(9, 5))
        fig.suptitle("Trig Functions", color="#e6edf3")
        ax1 = fig.add_subplot(321)
        ax1.plot(x, np.sin(x), color="#58a6ff")
        ax1.set_title("sin(x)"); ax1.set_xlabel("x"); ax1.set_ylabel("y")
        ax2 = fig.add_subplot(326)
        ax2.plot(x, np.cos(x), color="#f78166")
        ax2.set_title("cos(x)"); ax2.set_xlabel("x"); ax2.set_ylabel("y")
        show_fig(fig)

    elif name == "🔵 Scatter Plot — Random Data":
        np.random.seed(42)
        x, y = np.random.randn(1000), np.random.randn(1000)
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(-5, 5); ax.set_ylim(-5, 5)
        ax.scatter(x, y, alpha=0.5, color="#ffa657", s=30, edgecolors="#f78166", linewidths=0.3)
        ax.set_title("Random Scatter (n=1 000)")
        show_fig(fig)

    elif name == "📉 Histogram":
        np.random.seed(0)
        x = np.random.randn(10000)
        fig, ax = plt.subplots(figsize=(7, 4))
        n, bins, patches = ax.hist(x, bins=[-5, -1, 1, 5], edgecolor="#0d1117", color="#58a6ff")
        ax.set_title("Gaussian Histogram (n=10 000)")
        ax.set_xlabel("Value"); ax.set_ylabel("Count")
        st.caption(f"Counts per bin: {list(n.astype(int))}")
        show_fig(fig)

    elif name == "🌐 3D Plots — Scatter & Helix":
        np.random.seed(7)
        fig = plt.figure(figsize=(7, 9))
        ax1 = fig.add_subplot(211, projection="3d")
        ax1.scatter(*[np.random.randn(500) for _ in range(3)],
                    c="#58a6ff", alpha=0.5, s=10)
        ax1.set_title("3D Random Scatter"); ax1.set_xlabel("x"); ax1.set_ylabel("y"); ax1.set_zlabel("z")

        ax2 = fig.add_subplot(212, projection="3d")
        z = np.linspace(0, 20, 1000)
        ax2.plot(np.cos(z), np.sin(z), z, color="#ffa657")
        ax2.set_title("Helix")
        for ax in [ax1, ax2]:
            ax.set_facecolor("#161b22")
            ax.tick_params(colors="#8b949e")
            ax.title.set_color("#e6edf3")
        fig.patch.set_facecolor("#0d1117")
        st.pyplot(fig); plt.close(fig)

    elif name == "🛒 Mall Customers — Income vs Spending":
        path = os.path.join(UPLOAD_DIR, "mall_customers.csv")
        df = pd.read_csv(path, index_col=0)
        df.columns = ["Gender", "Age", "Income", "Spending"]
        grp = df.groupby(["Gender", "Age"])["Income"].mean()
        male, female = grp.loc["Male"], grp.loc["Female"]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(male.index, male.values, color="#58a6ff", label="Male", s=60)
        ax.scatter(female.index, female.values, color="#f78166", label="Female", s=60)
        ax.set_title("Mall Customers: Avg Income by Age & Gender")
        ax.set_xlabel("Age"); ax.set_ylabel("Annual Income (k$)")
        ax.legend(facecolor="#21262d", edgecolor="#30363d", labelcolor="#e6edf3")
        show_fig(fig)

        st.markdown("**Income std by gender:**")
        st.dataframe(
            df.groupby("Gender")["Income"].std().rename("Std Dev (k$)").reset_index(),
            hide_index=True, use_container_width=True
        )

    elif name == "📊 Mall Customers — Group Aggregates":
        path = os.path.join(UPLOAD_DIR, "mall_customers.csv")
        df = pd.read_csv(path, index_col=0)
        df.columns = ["Gender", "Age", "Income", "Spending"]
        gp = df.groupby("Gender")

        st.markdown("**Group means:**")
        st.dataframe(gp.mean().round(2), use_container_width=True)

        st.markdown("**Aggregated stats (Income):**")
        st.dataframe(
            gp["Income"].agg([np.std, np.mean, len]).round(2),
            use_container_width=True
        )

    elif name == "🔍 Mall Customers — Filtering":
        path = os.path.join(UPLOAD_DIR, "mall_customers.csv")
        df = pd.read_csv(path, index_col=0)
        df.columns = ["Gender", "Age", "Income", "Spending"]

        np.random.seed(42)
        values = np.random.randint(0, 100, 100)
        above_48 = values[values > 48]

        st.markdown(f"**Values > 48 (first 10):** `{list(above_48[:10])}`")
        st.markdown("**Female customers aged 32:**")
        result = df.loc[(df["Gender"] == "Female") & (df["Age"] == 32)]
        st.dataframe(result, use_container_width=True)

    elif name == "📦 Price Binning (pd.qcut)":
        np.random.seed(1)
        df = pd.DataFrame(np.random.randn(20), columns=["Price"])
        df["Category"] = pd.qcut(df["Price"], 3, labels=["Low", "Middle", "High"])

        fig, ax = plt.subplots(figsize=(5, 4))
        counts = df.groupby("Category", observed=True)["Price"].count()
        ax.bar(counts.index, counts.values,
               color=["#f78166", "#ffa657", "#58a6ff"], edgecolor="#0d1117")
        ax.set_title("Price Category Counts")
        ax.set_ylabel("Count")
        show_fig(fig)
        st.dataframe(df.sort_values("Price").reset_index(drop=True),
                     use_container_width=True)

    elif name == "📖 Word Frequency (Great Expectations)":
        path = os.path.join(UPLOAD_DIR, "wordcounts.txt")
        rows = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if "," in line:
                    word, count = line.rsplit(",", 1)
                    try:
                        rows.append((word.strip(), int(count.strip())))
                    except ValueError:
                        pass
        wdf = pd.DataFrame(rows, columns=["word", "count"]).nlargest(50, "count")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(wdf["word"][::-1], wdf["count"][::-1], color="#58a6ff")
        ax.set_title("Top-50 Words — Great Expectations")
        ax.set_xlabel("Frequency")
        ax.tick_params(axis="y", labelsize=8)
        show_fig(fig)
        st.caption(f"Total unique words: {len(rows):,}")

    elif name == "📏 Word Length Distribution":
        path = os.path.join(UPLOAD_DIR, "wordlengths.csv")
        wldf = pd.read_csv(path, header=None, names=["length", "count"])
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(wldf["length"], wldf["count"], color="#ffa657", edgecolor="#0d1117")
        ax.set_title("Word Length Distribution")
        ax.set_xlabel("Word length (chars)")
        ax.set_ylabel("Frequency")
        show_fig(fig)
        st.dataframe(wldf.set_index("length"), use_container_width=True)

st.markdown("---")
st.caption("Built with Streamlit · matplotlib · pandas · NumPy")
