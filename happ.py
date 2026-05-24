import streamlit as st
import joblib
import numpy as np

model = joblib.load(r'C:\Users\gnana\heart_disease_model.pkl')

st.set_page_config(
    page_title="Heart Disease Risk Screener",
    page_icon="❤️",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

.stApp {
    background-color: #0a0a0f;
}

h1, h2, h3 {
    color: #f0f0f8 !important;
}

.stSlider > div > div {
    background-color: #e05555 !important;
}

.stRadio > label {
    color: #9999bb !important;
    font-size: 13px;
}

div[data-testid="stRadio"] > div {
    gap: 10px;
}

div.stButton > button {
    width: 100%;
    background-color: #e05555;
    color: white;
    border: none;
    padding: 14px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    margin-top: 1rem;
    transition: all 0.2s;
}

div.stButton > button:hover {
    background-color: #c94444;
}

.card {
    background: #13131f;
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

.section-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #e05555;
    margin-bottom: 0.8rem;
    margin-top: 1.2rem;
}

.hero-title {
    text-align: center;
    font-size: 26px;
    font-weight: 500;
    color: #f0f0f8;
    margin-bottom: 0.4rem;
}

.hero-sub {
    text-align: center;
    font-size: 14px;
    color: #8888aa;
    margin-bottom: 1.5rem;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #e05555, transparent);
    margin: 1.2rem 0;
    opacity: 0.4;
}

.result-box {
    background: #13131f;
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: 1.2rem;
}

.disclaimer {
    background: #1a1a10;
    border: 0.5px solid rgba(240,160,48,0.2);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    font-size: 12px;
    color: #888866;
    line-height: 1.6;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ECG background animation
st.markdown("""
<canvas id="ecg-canvas" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:0.15;"></canvas>
<script>
const canvas = document.getElementById('ecg-canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
const lines = [
    {y: window.innerHeight * 0.25, offset: 0,   speed: 0.8},
    {y: window.innerHeight * 0.50, offset: 120, speed: 0.95},
    {y: window.innerHeight * 0.75, offset: 240, speed: 0.7}
];
function ecgY(x, offset) {
    const phase = ((x + offset) % 200) / 200;
    if (phase < 0.30) return 0;
    if (phase < 0.35) return -10 * Math.sin((phase-0.30)/0.05*Math.PI);
    if (phase < 0.40) return 0;
    if (phase < 0.44) return -80 * Math.sin((phase-0.40)/0.04*Math.PI);
    if (phase < 0.50) return  30 * Math.sin((phase-0.44)/0.06*Math.PI);
    if (phase < 0.55) return 0;
    if (phase < 0.65) return -15 * Math.sin((phase-0.55)/0.10*Math.PI);
    return 0;
}
let t = 0;
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    lines.forEach(line => {
        ctx.beginPath();
        ctx.strokeStyle = '#e05555';
        ctx.lineWidth = 1.2;
        for (let x = 0; x <= canvas.width; x += 2) {
            const y = line.y + ecgY(x - t * line.speed * 60, line.offset);
            x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke();
    });
    t += 0.016;
    requestAnimationFrame(draw);
}
draw();
</script>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem;">
    <div style="font-size:64px; animation: pulse 1.1s ease-in-out infinite; display:inline-block;">❤️</div>
    <div class="hero-title">Heart Disease Risk Screener</div>
    <div class="hero-sub">Answer 8 simple lifestyle questions — no lab tests needed.</div>
</div>
<style>
@keyframes pulse {
    0%   { transform: scale(1);    }
    14%  { transform: scale(1.18); }
    28%  { transform: scale(1);    }
    42%  { transform: scale(1.12); }
    56%  { transform: scale(1);    }
    100% { transform: scale(1);    }
}
</style>
<div class="divider"></div>
""", unsafe_allow_html=True)

# Inputs
st.markdown('<div class="section-label">Personal Info</div>', unsafe_allow_html=True)
age    = st.slider("Age", 18, 90, 30)
gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

st.markdown('<div class="section-label">Health Status</div>', unsafe_allow_html=True)
bp      = st.radio("Do you have high blood pressure?",    ["Yes", "No"], horizontal=True)
diabetic= st.radio("Are you diabetic?",                   ["Yes", "No"], horizontal=True, index=1)
family  = st.radio("Family history of heart disease?",    ["Yes", "No"], horizontal=True, index=1)

st.markdown('<div class="section-label">Lifestyle</div>', unsafe_allow_html=True)
smoker   = st.radio("Do you smoke?",                          ["Yes", "No"], horizontal=True, index=1)
exercise = st.radio("Do you exercise regularly?",             ["Yes", "No"], horizontal=True)
chest    = st.radio("Chest pain during physical activity?",   ["Yes", "No"], horizontal=True, index=1)

# Predict button
if st.button("❤️ Check My Heart Risk"):

    # Convert inputs to numbers
    gender_val   = 1 if gender   == "Male" else 0
    bp_val       = 1 if bp       == "Yes"  else 0
    diabetic_val = 1 if diabetic == "Yes"  else 0
    family_val   = 1 if family   == "Yes"  else 0
    smoker_val   = 1 if smoker   == "Yes"  else 0
    exercise_val = 1 if exercise == "Yes"  else 0
    chest_val    = 1 if chest    == "Yes"  else 0

    # Build input array for model
    input_data = np.array([[
        age,
        gender_val,
        chest_val,
        120,
        200,
        diabetic_val,
        0,
        150,
        exercise_val,
        1.0,
        1,
        family_val,
        smoker_val + bp_val + 2
    ]])

    # Get prediction
    probability = model.predict_proba(input_data)[0][1] * 100
    probability = round(probability)

    # Determine risk level
    if probability < 30:
        risk_level = "Low Risk"
        color      = "#5ecb6e"
        bg_color   = "#1a3a1a"
        rec        = "Your heart health looks good! Keep exercising regularly, eat a balanced diet, avoid smoking, and stay hydrated. Routine annual checkups are still recommended."
    elif probability < 60:
        risk_level = "Medium Risk"
        color      = "#f0a030"
        bg_color   = "#3a2e0a"
        rec        = "You have a moderate risk. Consider reducing stress, increasing physical activity, cutting down on smoking, and scheduling a routine checkup with your doctor soon."
    else:
        risk_level = "High Risk"
        color      = "#f05555"
        bg_color   = "#3a0a0a"
        rec        = "You have a high estimated risk. Please consult a doctor as soon as possible for a thorough medical evaluation. Do not ignore symptoms like chest pain or breathlessness."

    # Display results
    st.markdown(f"""
    <div class="result-box">
        <div style="display:inline-block; padding:6px 18px; border-radius:20px;
                    background:{bg_color}; color:{color};
                    border:0.5px solid {color}44;
                    font-size:13px; font-weight:500;
                    letter-spacing:0.5px; margin-bottom:1rem;">
            {risk_level}
        </div>
        <div style="display:flex; align-items:baseline; gap:10px; margin-bottom:1rem;">
            <span style="font-size:44px; font-weight:500; color:{color}; line-height:1;">{probability}%</span>
            <span style="font-size:13px; color:#6666aa;">estimated risk score</span>
        </div>
        <div style="height:6px; background:#ffffff10; border-radius:3px; overflow:hidden; margin-bottom:1.2rem;">
            <div style="height:100%; width:{probability}%; background:{color}; border-radius:3px;"></div>
        </div>
        <div style="background:#0e0e1a; border-radius:10px; padding:1rem 1.1rem;
                    font-size:13px; color:#9999bb; line-height:1.65;
                    border-left:2px solid {color};">
            {rec}
        </div>
        <div class="disclaimer">
            ⚠ Disclaimer: This tool is for educational purposes only and does not replace
            professional medical advice. Please consult a qualified doctor for proper
            diagnosis and treatment.
        </div>
    </div>
    """, unsafe_allow_html=True)