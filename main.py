import streamlit as st
import os
from sow_backend import process_file_and_generate_sow

st.set_page_config(page_title="SoW Generator", layout="centered")

# --- Styles ---
st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    .stButton>button {
        background-color: #004080;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stSelectbox>div {
        border-radius: 8px;
    }
    .stFileUploader {margin-bottom: 20px;}
    .stMarkdown h1 {
        font-size: 2.2rem;
        color: #003366;
    }
    .stMarkdown h4 {
        color: #004080;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("📄 Statement of Work (SoW) Generator")
st.markdown("Generate professional, client-ready SoWs automatically from your proposal documents in minutes.")

# --- Upload Section ---
st.markdown("#### 1. Upload Proposal File")
uploaded_file = st.file_uploader(
    "Supported formats: PDF, PPTX, DOCX, TXT",
    type=["pdf", "pptx", "docx", "txt"]
)

# --- Format Selection ---
st.markdown("#### 2. Choose Output Format")
format_option = st.selectbox("Select format:", ["pdf", "docx", "txt", "pptx"])

# --- Generate Button ---
st.markdown("#### 3. Generate SoW")
if st.button("🚀 Generate Statement of Work"):
    if not uploaded_file:
        st.error("❗ Please upload a proposal file first.")
    else:
        try:
            # Save uploaded file to disk temporarily
            temp_file_path = f"temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("⚙️ Processing... Generating your SoW..."):
                sow_text, download_url = process_file_and_generate_sow(temp_file_path, output_format=format_option)

            st.success("✅ SoW generated successfully!")
            st.markdown("#### 📥 Download Your SoW")
            st.markdown(f"[Click here to download]({download_url})", unsafe_allow_html=True)

            st.markdown("#### 🔍 Preview of Generated SoW")
            st.text(sow_text[:5000] + ("..." if len(sow_text) > 5000 else ""))

        except Exception as e:
            st.error(f"🚨 Error while generating SoW: {e}")

        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)