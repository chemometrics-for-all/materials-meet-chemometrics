import streamlit as st
import numpy as np
import pandas as pd
import requests
import io
import plotly.graph_objects as go
import random

# ================================
# CONFIG
# ================================
st.set_page_config(page_title="Spectral Mastery SaaS", layout="wide")

# ================================
# STYLE (Premium UI)
# ================================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}
.title {
    font-size: 42px;
    font-weight: bold;
    color: #38bdf8;
}
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ================================
# SESSION STATE
# ================================
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1

# ================================
# HEADER
# ================================
st.markdown('<p class="title">Spectral Mastery Platform</p>', unsafe_allow_html=True)

st.write("""
### 🎯 Learning Path
1. Learn normal spectrum (simulation)  
2. Apply checklist  
3. Test on REAL datasets  
""")

# ================================
# DATA LOADER (REAL)
# ================================
@st.cache_data
def load_mango_real():
    url = "https://data.mendeley.com/public-files/datasets/b9d6s7hr33/files/sample.xlsx"
    r = requests.get(url)
    df = pd.read_excel(io.BytesIO(r.content))
    return df

# fallback generator
def generate_spectrum():
    x = np.linspace(400, 2500, 300)
    y = np.exp(-((x - 1400)/200)**2) + np.exp(-((x - 1900)/250)**2)
    y += np.random.normal(0, 0.01, len(x))
    return x, y

# ================================
# PLOT
# ================================
def plot_spectrum(x, y, anomaly=False):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        line=dict(width=3)
    ))

    if anomaly:
        fig.add_annotation(
            x=x[len(x)//2],
            y=max(y),
            text="⚠ anomaly detected",
            showarrow=True
        )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    return fig

# ================================
# CHECKLIST ENGINE
# ================================
def checklist():
    st.write("### 🔍 Checklist")

    c1 = st.checkbox("Smooth shape")
    c2 = st.checkbox("Low noise")
    c3 = st.checkbox("Stable baseline")
    c4 = st.checkbox("Realistic peaks")

    return c1, c2, c3, c4

# ================================
# MODE
# ================================
mode = st.radio("Choose Mode", ["Training", "Real Test"])

# ================================
# TRAINING
# ================================
if mode == "Training":

    st.subheader("🎓 Learn Normal Spectrum")

    x, y = generate_spectrum()

    st.plotly_chart(plot_spectrum(x, y))

    c1, c2, c3, c4 = checklist()

    answer = st.radio("Decision", ["Normal", "Not Normal"])

    if st.button("Validate"):

        if answer == "Normal":
            st.success("Correct")
            st.session_state.score += 10
        else:
            st.error("Wrong")

        # explanation
        st.markdown("""
        ✔ Smooth curve  
        ✔ No noise  
        ✔ Stable baseline  
        """)

# ================================
# REAL TEST
# ================================
if mode == "Real Test":

    domain = st.selectbox("Choose domain", ["Fruit", "Oil", "Milk"])

    st.write("### 📊 Dataset Info")

    if domain == "Fruit":
        st.info("Mango NIR dataset: chemical composition")
        try:
            df = load_mango_real()
            sample = df.sample(1)

            y = sample.values.flatten()
            x = np.arange(len(y))
        except:
            x, y = generate_spectrum()

    else:
        x, y = generate_spectrum()

    # introduce anomaly
    is_normal = random.choice([True, False])

    if not is_normal:
        y += np.random.normal(0, 0.15, len(y))

    st.plotly_chart(plot_spectrum(x, y, anomaly=not is_normal))

    # checklist guidance
    st.write("### 🧠 Apply checklist step by step")

    c1, c2, c3, c4 = checklist()

    decision = st.radio("Final decision", ["Normal", "Not Normal"])

    if st.button("Validate Test"):

        correct = (
            (decision == "Normal" and is_normal) or
            (decision == "Not Normal" and not is_normal)
        )

        if correct:
            st.success("Correct decision")
            st.session_state.score += 20
        else:
            st.error("Wrong decision")

        # 🔍 explain visually
        if is_normal:
            st.markdown("✔ This is NORMAL → smooth, stable")
        else:
            st.markdown("❌ NOT NORMAL → noise/distortion detected")

# ================================
# SIDEBAR (Gamification)
# ================================
st.sidebar.title("Progress")

st.sidebar.metric("Score", st.session_state.score)
st.sidebar.metric("Level", st.session_state.level)
