import streamlit as st
import requests
from PIL import Image
import io
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SMARTFORM_LOGO_PATH = os.path.join(BASE_DIR, "assets", "smartform_logo.png")
TEAM_LOGO_PATH = os.path.join(BASE_DIR, "assets", "team_logo.png")

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:8000"

# --- Page Setup ---
st.set_page_config(
    page_title="SmartFarm AI",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed")

# ---------------- THEME ----------------
if "dark" not in st.session_state:
    st.session_state.dark = False

def toggle_theme():
    st.session_state.dark = not st.session_state.dark

st.sidebar.button("🌗 Dark / Light Mode", on_click=toggle_theme)

if st.session_state.dark:
    st.markdown("""
        <style>
            body { background-color: #0e1117; color: white; }
            .card { background: #161b22; padding: 22px; border-radius: 16px; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .card { background: #f7f9fb; padding: 22px; border-radius: 16px; }
        </style>
    """, unsafe_allow_html=True)

# ---------------- HEADER ----------------
c1, c2 = st.columns([1, 6])
with c1:
    st.image(SMARTFORM_LOGO_PATH, width=85)
with c2:
    st.markdown("""
        <h1>SmartFarm AI 🌱</h1>
        <p>AI-powered crop & seed analysis with voice assistance</p>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- MAIN ----------------
left, right = st.columns(2)

# -------- LEFT PANEL --------
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📤 Upload Image")

    analysis_mode = st.radio(
        "Select Analysis Type",
        ["🌿 Crop Disease Analysis", "🌾 Seed Quality Analysis"]
    )

    country = st.text_input(
        "Country (for recommendations)",
        value="Global"
    )

    image = st.file_uploader(
        "Upload image (leaf / seed)",
        type=["jpg", "jpeg", "png"]
    )

    seed_type = None
    if analysis_mode.startswith("🌾"):
        seed_type = st.text_input("Seed Type (optional)", value="Unknown")

    analyze_btn = st.button("🔍 Analyze")
    st.markdown("</div>", unsafe_allow_html=True)

# -------- RIGHT PANEL --------
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 AI Result")

    if analyze_btn:
        if not image:
            st.warning("Please upload an image")
        else:
            with st.spinner("SmartFarm AI is analyzing..."):
                if analysis_mode.startswith("🌿"):
                    response = requests.post(
                        f"{BACKEND_URL}//analyze-disease",
                        files={"image": image}
                    )
                else:
                    response = requests.post(
                        f"{BACKEND_URL}/analyze-seed",
                        files={"image": image},
                        data={"seed_type": seed_type}
                    )

            if response.status_code != 200:
                st.error("Backend error occurred")
            else:
                data = response.json()
                st.image(image, use_column_width=True)

                # ---- CROP DISEASE OUTPUT ----
                if analysis_mode.startswith("🌿"):
                    st.markdown(f"**🌱 Crop:** {data['crop_name']}")
                    st.markdown(f"**🦠 Disease:** {data['disease_name']}")
                    st.markdown(f"**📊 Confidence:** {data['confidence']}")
                    st.markdown(f"**📝 Description:** {data['description']}")
                    st.markdown(f"**🧪 Pesticide:** {data['recommended_pesticide']}")
                    st.markdown(f"**🗣 Urdu Advice:** {data['urdu_message']}")
                    st.audio(f"{BACKEND_URL}/{data['audio_file']}")

                # ---- SEED QUALITY OUTPUT ----
                else:
                    st.markdown(f"**🌾 Seed Type:** {data['seed_type']}")
                    st.markdown(f"**⭐ Quality:** {data['quality']}")
                    st.markdown(f"**📊 Confidence:** {data['confidence']}")
                    st.markdown(f"**🔍 Observations:** {data['observations']}")
                    st.markdown(f"**🌱 Sowing Advice:** {data['sowing_recommendation']}")
                    st.markdown(f"**🗣 Farmer Message:** {data['message']}")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.divider()
f1, f2 = st.columns([6, 1])
with f1:
    st.markdown(
        "<p style='opacity:0.6;'>SmartFarm AI • Helping farmers worldwide 🌍</p>",
        unsafe_allow_html=True
    )
with f2:
    st.image(TEAM_LOGO_PATH, width=40)
    st.caption("Developed by Team IGOGs")
