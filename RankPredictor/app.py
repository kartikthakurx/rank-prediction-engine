import streamlit as st
import pandas as pd
import pickle
import os

# --- PAGE CONFIG ---
st.set_page_config(layout="centered", page_title="Rank Prediction Engine")

# --- ROBUST MODEL LOADING ---
@st.cache_resource
def load_model():
    if not os.path.exists('rank_predictor_model.pkl'):
        return None, "🚨 ERROR: 'rank_predictor_model.pkl'."
    try:
        with open('rank_predictor_model.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
        return loaded_model, "SUCCESS"
    except Exception as e:
        return None, f"🚨 ERROR: {e}"

model, model_status = load_model()

# --- LOGIC FUNCTIONS ---
def get_tier_info(rating):
    if rating < 1400: return "1★ (Beginner)", "#666666"
    elif rating < 1600: return "2★ (Basic)", "#1E7D22"
    elif rating < 1800: return "3★ (Intermediate)", "#3366CC"
    elif rating < 2000: return "4★ (Strong)", "#684273"
    elif rating < 2200: return "5★ (Advanced)", "#FFBF00"
    elif rating < 2500: return "6★ (Expert)", "#FF7F00"
    else: return "7★ (Elite)", "#D0011B"

def calculate_potential(current, highest):
    if highest <= 0: return 0
    return min(100, int((current / highest) * 100))

# --- STATE MANAGEMENT ---
if 'predicted_rank' not in st.session_state:
    st.session_state.predicted_rank = "---"
if 'current_tier' not in st.session_state:
    st.session_state.current_tier = "Waiting"
if 'tier_color' not in st.session_state:
    st.session_state.tier_color = "#4CAF50"
if 'potential' not in st.session_state:
    st.session_state.potential = "0"

# --- CSS STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #12141a; color: white; }
    .header-container { display: flex; justify-content: space-between; align-items: flex-end; padding: 20px 0; margin-bottom: 20px; border-bottom: 1px solid #2d3442; }
    .top-stats-grid { display: flex; gap: 30px; }
    .stat-box { display: flex; flex-direction: column; gap: 5px; }
    .stat-label { font-size: 11px; color: #a0a4ab; text-transform: uppercase; letter-spacing: 0.5px; }
    .stat-value { font-size: 16px; font-weight: bold; color: white; }
    .main-card { background: #171b23; border-radius: 16px; padding: 60px 20px; position: relative; text-align: center; overflow: hidden; margin-bottom: 30px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border: 1px solid #2d3442; }
    .card-content { z-index: 1; display: flex; flex-direction: column; align-items: center; }
    .label-text { color: #a0a4ab; font-size: 14px; letter-spacing: 0.5px; margin-bottom: 5px; text-transform: uppercase; }
    .rank-text { font-size: 64px; font-weight: 800; margin: 10px 0 20px 0; color: white; text-shadow: 0 0 20px rgba(255,255,255,0.1); }
    .badge-custom { border: 2px solid #4CAF50; color: white; padding: 6px 24px; border-radius: 20px; font-size: 12px; font-weight: 700; letter-spacing: 1px; background: rgba(76, 175, 80, 0.05); }
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #a3c2ff !important; border-radius: 5px !important; width: 12px !important; height: 24px !important; }
    .stSlider [data-testid="stTickBar"] { display: flex !important; color: #a0a4ab !important; font-size: 10px !important; }
    div[data-testid="stThumbValue"] { color: #a3c2ff !important; font-weight: bold; }
    .stButton > button { background: #1f242d; color: #a0a4ab; border: 1px solid #2d3442; border-radius: 8px; width: 100%; height: 50px; margin-top: 15px; font-weight: bold; transition: 0.3s; }
    .stButton > button:hover { border-color: #4CAF50; color: white; box-shadow: 0 0 15px rgba(76, 175, 80, 0.2); }
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SHOW ERROR IF MODEL FAILS TO LOAD ---
if model_status != "SUCCESS":
    st.error(model_status)

# --- HEADER SECTION ---
st.markdown(f"""
<div class="header-container">
    <div style="font-size: 20px; font-weight: bold; color: #ffffff;">Rank Prediction Engine</div>
    <div class="top-stats-grid">
        <div class="stat-box">
            <div class="stat-label">Predicted Rank</div>
            <div class="stat-value">#{st.session_state.predicted_rank}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Tier</div>
            <div class="stat-value" style="color:{st.session_state.tier_color};">{st.session_state.current_tier}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Potential</div>
            <div class="stat-value">{st.session_state.potential}%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- MAIN PREDICTION CARD ---
st.markdown(f"""
<div class="main-card">
    <div class="card-content">
        <div class="label-text">PREDICTED GLOBAL RANK</div>
        <div class="rank-text">{st.session_state.predicted_rank}</div>
        <div class="badge-custom" style="border-color: {st.session_state.tier_color}; color: {st.session_state.tier_color};">
            {st.session_state.current_tier.upper()}
        </div>
        <p style="color:#a0a4ab; font-size:12px; margin-top:20px;">Based on Current Performance Metrics</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Model Performance")

col1, col2 = st.columns(2)

with col1:
    st.metric("MAE", "±14.44", help="Average error in predicted rank")
    st.metric("RMSE", "27.84", help="Standard deviation of prediction error")

with col2:
    st.metric("MSE", "775.03", help="Squared error")
    st.metric("R2 Score", "0.9999", help="Closer to 1 means better model")
    
    
# --- CONTROLS / INPUT AREA (Slider + Typing Synced) ---
defaults = {'rating': 2000, 'highest': 2100, 'fully_solved': 120, 'partially_solved': 10}
for k, v in defaults.items():
    if f"{k}_slider" not in st.session_state:
        st.session_state[f"{k}_slider"] = v
    if f"{k}_input" not in st.session_state:
        st.session_state[f"{k}_input"] = v

def sync(key, source):
    val = st.session_state[f"{key}_{source}"]
    other = "input" if source == "slider" else "slider"
    st.session_state[f"{key}_{other}"] = val
    if key == "rating" and st.session_state["highest_input"] < val:
        st.session_state["highest_input"] = val
        st.session_state["highest_slider"] = val

col1, col2 = st.columns(2)

with col1:
    st.number_input("Current Rating (Type)", min_value=1000, max_value=3713, key="rating_input", on_change=sync, args=("rating", "input"))
    st.slider("Current Rating", 1000, 3713, key="rating_slider", on_change=sync, args=("rating", "slider"), label_visibility="collapsed")

    st.number_input("Fully Solved Problems (Type)", min_value=0, max_value=5000, key="fully_solved_input", on_change=sync, args=("fully_solved", "input"))
    st.slider("Fully Solved Problems", 0, 5000, key="fully_solved_slider", on_change=sync, args=("fully_solved", "slider"), label_visibility="collapsed")

rating = st.session_state["rating_input"]

with col2:
    st.number_input("Highest Rating (Type)", min_value=rating, max_value=3713, key="highest_input", on_change=sync, args=("highest", "input"))
    if rating < 3713:
        st.slider("Highest Rating", rating, 3713, key="highest_slider", on_change=sync, args=("highest", "slider"), label_visibility="collapsed")
    else:
        st.slider("Highest Rating", 1000, 3713, 3713, disabled=True, label_visibility="collapsed")

    st.number_input("Partially Solved Problems (Type)", min_value=0, max_value=1000, key="partially_solved_input", on_change=sync, args=("partially_solved", "input"))
    st.slider("Partially Solved Problems", 0, 1000, key="partially_solved_slider", on_change=sync, args=("partially_solved", "slider"), label_visibility="collapsed")

highest = st.session_state["highest_input"]
fully_solved = st.session_state["fully_solved_input"]
partially_solved = st.session_state["partially_solved_input"]

if rating < 1700:
    st.warning("⚠️ Note: This model is trained on the top 9,846 coders, so ratings below 1700 may cap around rank ~9,800.")
    
    
# --- PREDICT BUTTON ---
if st.button("REFRESH PREDICTION"):
    tier_name, tier_color = get_tier_info(rating)
    st.session_state.current_tier = tier_name
    st.session_state.tier_color = tier_color
    st.session_state.potential = str(calculate_potential(rating, highest))

    if model:
        try:
            # Data format exactly matching your training setup
            performance_score = rating / highest if highest != 0 else 0

            input_df = pd.DataFrame({
                'Rating': [rating],
                'Highest Rating': [highest],
                'Fully Solved': [fully_solved],
                'Partially Solved': [partially_solved],
                'Performance Score': [performance_score]
            })

            res = model.predict(input_df)
            st.session_state.predicted_rank = str(max(1, int(res[0])))

        except Exception as e:
            st.error(f"Prediction failed! Error: {e}")
    else:
        st.warning("⚠️ Model is not loaded")

    st.rerun()