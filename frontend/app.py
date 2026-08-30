# frontend/app.py
import streamlit as st
import requests

st.set_page_config(page_title="DocuMind AI", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body {
        background: radial-gradient(circle at 30% 30%, #1a1a2e, #16213e, #0f3460);
        background-attachment: fixed;
        color: #e2e8f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        overflow: hidden;
        height: 100vh;
        width: 100vw;
    }
    
    .main {
        background: transparent !important;
        padding: 0 !important;
        height: 100vh;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: rgba(168, 85, 247, 0.3) transparent;
    }
    
    .main::-webkit-scrollbar {
        width: 6px;
    }
    
    .main::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .main::-webkit-scrollbar-thumb {
        background: rgba(168, 85, 247, 0.3);
        border-radius: 10px;
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Header */
    .header-section {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.9), rgba(48, 43, 99, 0.5));
        border-bottom: 1px solid rgba(168, 85, 247, 0.2);
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .header-icon {
        font-size: 2rem;
        margin-bottom: 0.3rem;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #a855f7, #ec4899, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Tab buttons */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 1rem;
        border-bottom: 1px solid rgba(168, 85, 247, 0.2);
        padding: 0.8rem;
        margin: 0 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 0.95rem;
        font-weight: 600;
        color: #94a3b8;
        padding: 10px 24px !important;
        border-radius: 50px !important;
        border: 2px solid rgba(168, 85, 247, 0.3) !important;
        background: transparent !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #a855f7, #ec4899) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.4) !important;
    }
    
    /* Content wrapper */
    .content-wrapper {
        padding: 1.5rem;
        height: calc(100vh - 200px);
        overflow-y: auto;
    }
    
    /* Card styling */
    .upload-card {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid transparent;
        border-image: linear-gradient(135deg, #a855f7, #06b6d4) 1;
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(168, 85, 247, 0.25);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .upload-card:hover {
        box-shadow: 0 12px 40px rgba(168, 85, 247, 0.4);
        transform: translateY(-2px);
    }
    
    .upload-card h2 {
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }
    
    .upload-card p {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 1rem;
    }
    
    /* Upload area */
    .stFileUploader {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.05), rgba(59, 130, 246, 0.05)) !important;
        border: 3px dashed rgba(168, 85, 247, 0.4) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
    }
    
    /* Button container - CENTER BUTTON */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 1rem 0 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #a855f7, #ec4899, #06b6d4) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        padding: 12px 32px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.4) !important;
        width: auto !important;
        min-width: 150px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(168, 85, 247, 0.6) !important;
    }
    
    /* Text area */
    .stTextArea textarea {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 2px solid rgba(168, 85, 247, 0.2) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
    }
    
    /* Metrics */
    .metric-container {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(59, 130, 246, 0.1));
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        border-color: rgba(168, 85, 247, 0.5);
        transform: translateY(-4px);
    }
    
    /* Messages */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 12px !important;
    }
    
    h1, h2, h3 {
        color: #f1f5f9 !important;
        font-weight: 700;
    }
    
    .stDivider {
        border-color: rgba(168, 85, 247, 0.2) !important;
        margin: 1rem 0 !important;
    }
    
    .streamlit-expanderHeader {
        background: rgba(168, 85, 247, 0.1);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 10px;
    }
    
    /* Footer */
    .footer-section {
        text-align: center;
        padding: 1.5rem;
        color: #64748b;
        font-size: 0.85rem;
        border-top: 1px solid rgba(168, 85, 247, 0.1);
        margin-top: 1rem;
        background: rgba(15, 12, 41, 0.5);
    }
    
    /* Slider styling */
    .stSlider {
        padding: 0.5rem 0 !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.8rem;
        }
        
        .content-wrapper {
            height: calc(100vh - 180px);
        }
        
        .metric-container {
            padding: 0.8rem;
            font-size: 0.85rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

API_URL = "http://localhost:8000"

# Header
st.markdown("""
    <div class="header-section">
        <div class="header-icon">✨</div>
        <div class="header-title">DocuMind AI</div>
        <div class="header-subtitle">Enterprise Document Intelligence • Powered by AI Agents</div>
    </div>
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["📤 Upload", "🔍 Query"])

# ============================================================================
# TAB 1: UPLOAD
# ============================================================================
with tab1:
    st.markdown("""
        <div class="upload-card">
            <h2>Upload & Process Documents</h2>
            <p>Drag files or click to upload. Supports PDF, DOCX, TXT</p>
        </div>
        """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["pdf", "docx", "txt"], label_visibility="collapsed")
    
    if uploaded_file:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"📄 {uploaded_file.name}")
        with col2:
            st.write(f"💾 {uploaded_file.size / 1024:.1f} KB")
        with col3:
            st.write(f"🏷️ {uploaded_file.type}")
        
        st.markdown("")
        
        col_btn = st.columns([1, 2, 1])
        with col_btn[0]:
            st.write("")
        with col_btn[1]:
            if st.button("🚀 Process", use_container_width=True):
                with st.spinner("🔄 Processing..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                        response = requests.post(f"{API_URL}/upload", files=files, timeout=30)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✨ Processed!")
                            
                            st.markdown("### Results")
                            
                            m1, m2 = st.columns(2)
                            m3, m4 = st.columns(2)
                            
                            metrics = [
                                (m1, "🏷️", "Classification", result['classification'], "#a855f7"),
                                (m2, "🔒", "Compliance", "✓" if result['compliance_passed'] else "✗", "#22c55e" if result['compliance_passed'] else "#ef4444"),
                                (m3, "⚠️", "Risk", f"{result['risk_score']:.2f}", "#22c55e" if result["risk_score"] < 0.5 else "#eab308" if result["risk_score"] < 0.8 else "#ef4444"),
                                (m4, "📝", "Words", result['word_count'], "#06b6d4")
                            ]
                            
                            for col, emoji, label, value, color in metrics:
                                with col:
                                    st.markdown(f"""
                                    <div class="metric-container">
                                        <div style="font-size: 1.5rem;">{emoji}</div>
                                        <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 0.3rem;">{label}</div>
                                        <div style="font-size: 1.1rem; font-weight: bold; color: {color}; margin-top: 0.3rem;">{value}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            st.divider()
                            st.write("**Summary:** " + result["summary"][:200] + "...")
                            st.caption(f"ID: {result['document_id']}")
                        else:
                            st.error(f"❌ {response.json().get('detail')}")
                    except Exception as e:
                        st.error(f"❌ {str(e)}")
        with col_btn[2]:
            st.write("")

# ============================================================================
# TAB 2: QUERY
# ============================================================================
with tab2:
    st.markdown("""
        <div class="upload-card">
            <h2>Ask Questions</h2>
            <p>Query your documents using natural language</p>
        </div>
        """, unsafe_allow_html=True)
    
    question = st.text_area("Your question:", placeholder="What is the total amount?", height=80, label_visibility="collapsed")
    top_k = st.slider("Results:", 1, 10, 5)
    
    st.markdown("")
    
    col_btn = st.columns([1, 2, 1])
    with col_btn[0]:
        st.write("")
    with col_btn[1]:
        if st.button("🔍 Search", use_container_width=True):
            if question.strip():
                with st.spinner("🤖 Searching..."):
                    try:
                        query_data = {"question": question, "top_k": top_k, "document_ids": None}
                        response = requests.post(f"{API_URL}/query", json=query_data, timeout=30)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✨ Answer generated!")
                            
                            st.write("**Answer:** " + result["answer"][:300] + "...")
                            
                            conf_pct = result["confidence"] * 100
                            conf_color = "#22c55e" if result["confidence"] > 0.7 else "#eab308" if result["confidence"] > 0.5 else "#ef4444"
                            st.markdown(f"""
                            <div style="background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 10px; padding: 0.8rem; text-align: center;">
                                <div style="color: #94a3b8; font-size: 0.85rem;">Confidence</div>
                                <div style="font-size: 1.2rem; font-weight: bold; color: {conf_color};">{conf_pct:.1f}%</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if result["sources"]:
                                st.write("**Sources:** " + result["sources"][0]["filename"])
                        else:
                            st.error(f"❌ {response.json().get('detail')}")
                    except Exception as e:
                        st.error(f"❌ {str(e)}")
            else:
                st.warning("Please enter a question")
    with col_btn[2]:
        st.write("")

# Footer
st.markdown("""
    <div class="footer-section">
        <div>✨ Powered by LangGraph • Groq • Qdrant</div>
        <div style="font-size: 0.75rem;">v1.0</div>
    </div>
    """, unsafe_allow_html=True)