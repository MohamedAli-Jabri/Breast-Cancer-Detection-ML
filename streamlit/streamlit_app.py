import streamlit as st
import requests
import streamlit.components.v1 as components

# ======================
# API Configuration
# ======================
API_URL = "http://127.0.0.1:8000/predict"

# ======================
# Page Configuration
# ======================
st.set_page_config(
    page_title="OncoScan - AI Breast Cancer Detection",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default UI
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {padding: 0 !important; max-width: 100% !important;}
[data-testid="stAppViewContainer"] {padding: 0 !important;}
</style>
""", unsafe_allow_html=True)

# ======================
# Session State
# ======================
if "page" not in st.session_state:
    st.session_state.page = "landing"

# ======================
# Landing Page HTML
# ======================
LANDING_PAGE_HTML = """ 
<!-- HTML CONTENT EXACTEMENT COMME TON CODE (inchangé) -->
"""  # 👉 garde exactement ton HTML ici (il est OK)

# ======================
# Prediction Page CSS
# ======================
def load_prediction_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f9f7f4 0%, #f0ede8 100%) !important;
    }

    .main .block-container {
        padding-top: 2rem !important;
        max-width: 900px !important;
    }

    h1, h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #1a2332 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1a9988, #2ab5a2) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
    }

    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(26, 35, 50, 0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# ======================
# Landing Page
# ======================
def show_landing_page():
    components.html(LANDING_PAGE_HTML, height=2200, scrolling=True)

    if st.button("Start Analysis", type="primary"):
        st.session_state.page = "prediction"
        st.rerun()

# ======================
# Prediction Page
# ======================
def show_prediction_page():
    load_prediction_css()

    if st.button("← Back Home"):
        st.session_state.page = "landing"
        st.rerun()

    st.title("🩺 Breast Cancer Diagnosis")
    st.markdown("Enter tumor characteristics to predict malignancy.")

    with st.form("cancer_form"):
        features = {}

        def input_feature(label, value):
            return st.number_input(label, value=value)

        cols = st.columns(2)
        with cols[0]:
            features["radius_mean"] = input_feature("Radius Mean", 14.0)
            features["texture_mean"] = input_feature("Texture Mean", 19.0)
            features["perimeter_mean"] = input_feature("Perimeter Mean", 90.0)
            features["area_mean"] = input_feature("Area Mean", 600.0)
            features["smoothness_mean"] = input_feature("Smoothness Mean", 0.10)

        with cols[1]:
            features["compactness_mean"] = input_feature("Compactness Mean", 0.15)
            features["concavity_mean"] = input_feature("Concavity Mean", 0.10)
            features["concave_points_mean"] = input_feature("Concave Points Mean", 0.05)
            features["symmetry_mean"] = input_feature("Symmetry Mean", 0.18)
            features["fractal_dimension_mean"] = input_feature("Fractal Dimension Mean", 0.06)

        submit = st.form_submit_button("🔍 Predict", use_container_width=True)

    if submit:
        try:
            response = requests.post(API_URL, json=features)

            if response.status_code == 200:
                result = response.json()
                if result["prediction"] == "Malignant":
                    st.error(f"⚠️ Malignant Tumor\nConfidence: {result['confidence']:.2%}")
                else:
                    st.success(f"✅ Benign Tumor\nConfidence: {result['confidence']:.2%}")
            else:
                st.error("❌ API Error")

        except requests.exceptions.ConnectionError:
            st.error("❌ FastAPI server not running")

# ======================
# Router
# ======================
if st.session_state.page == "landing":
    show_landing_page()
else:
    show_prediction_page()
