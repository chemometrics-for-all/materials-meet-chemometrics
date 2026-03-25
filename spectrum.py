import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Spectral Trainer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# CUSTOM CSS (PREMIUM UI)
# -----------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    text-align: center;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

.metric-box {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-weight: bold;
}

button {
    border-radius: 12px !important;
    height: 3em;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.streak = 0
    st.session_state.level = 1

# -----------------------------
# HEADER
# -----------------------------


st.markdown("## ✦ Learn to SEE Spectra")
st.markdown("### Train your eye before modeling")

# -----------------------------
# GENERATE SPECTRUM
# -----------------------------
def generate_spectrum(level):
    x = np.linspace(0, 100, 500)

    base = (
        np.exp(-(x - 30)**2 / 50)
        + 0.7 * np.exp(-(x - 60)**2 / 80)
    )

    is_normal = np.random.rand() > (0.4 + level*0.1)

    if is_normal:
        return x, base, True

    noise = np.random.normal(0, 0.05 * level, len(x))
    drift = (0.05 * level) * (x / max(x))

    y = base + noise + drift

    return x, y, False

# -----------------------------
# LOAD CASE
# -----------------------------
if "current" not in st.session_state:
    st.session_state.current = generate_spectrum(st.session_state.level)

x, y, is_normal = st.session_state.current

# -----------------------------
# SPECTRUM CARD
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

fig, ax = plt.subplots()
ax.plot(x, y, linewidth=2)

ax.set_facecolor("#0f172a")
fig.patch.set_facecolor("#0f172a")

ax.set_xlabel("Wavelength", color="white")
ax.set_ylabel("Intensity", color="white")
ax.tick_params(colors='white')

st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# USER INPUT
# -----------------------------
st.markdown("### 🧠 Your Decision")

choice = st.radio(
    "Is this spectrum NORMAL?",
    ["Normal", "Not Normal"],
    horizontal=True
)

# -----------------------------
# VALIDATE BUTTON
# -----------------------------
col1, col2 = st.columns([1,1])

with col1:
    validate = st.button("✔ Validate")

with col2:
    next_case = st.button("➡ Next")

# -----------------------------
# VALIDATION LOGIC
# -----------------------------
if validate:
    st.session_state.total += 1

    correct = (
        (choice == "Normal" and is_normal) or
        (choice == "Not Normal" and not is_normal)
    )

    if correct:
        st.success("✨ Perfect! Your eye is improving.")
        st.session_state.score += 1
        st.session_state.streak += 1
    else:
        st.error("⚠ Not quite. Look more carefully.")

        if is_normal:
            st.info("👉 Smooth peaks + flat baseline = NORMAL")
        else:
            st.info("👉 Something disturbs the signal → NOT normal")

        st.session_state.streak = 0

# -----------------------------
# NEXT CASE
# -----------------------------
if next_case:
    st.session_state.current = generate_spectrum(st.session_state.level)
    st.rerun()

# -----------------------------
# METRICS (PREMIUM STYLE)
# -----------------------------
st.markdown("### 📊 Your Performance")

accuracy = (
    st.session_state.score / st.session_state.total * 100
    if st.session_state.total > 0 else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="metric-box">Score<br>{st.session_state.score}</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="metric-box">Accuracy<br>{accuracy:.1f}%</div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="metric-box">Streak 🔥<br>{st.session_state.streak}</div>', unsafe_allow_html=True)

# -----------------------------
# LEVEL SYSTEM
# -----------------------------
if st.session_state.streak >= 5:
    st.session_state.level += 1
    st.session_state.streak = 0
    st.success(f"🚀 Level Up! Welcome to Level {st.session_state.level}")
