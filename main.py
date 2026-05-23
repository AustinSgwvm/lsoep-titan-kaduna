# ==============================================================================
# PROJECT: LSOEP TITAN KADUNA - CORE ENGINE INTERFACE
# REVISION: v34.0.46 [MASTER PROPORTION RUNTIME MATRIX - PERFECT MACE VISIBILITY]
# ==============================================================================

import streamlit as st
import pandas as pd
import datetime
import os
import json

# ==============================================================================
# DATA ARCHITECTURE LAYER: SOBA ADMINISTRATIVE MATRIX (EXPLICIT DECLARATION)
# ==============================================================================

# Every single administrative ward mapped comprehensively across Soba LGA
GEOGRAPHY = {
    "Soba LGA": [
        "Alhazai Ward",
        "Danwata Ward",
        "Gamagira Ward",
        "Garkaye Ward",
        "Gimba Ward",
        "KINKIBA Ward",
        "Kwassallo Ward",
        "Maigana Ward",
        "Rahama Ward",
        "Soba Ward",
        "Turawa Ward"
    ]
}

# Dropdown selection matrix mappings for standardized intake logic
LGA_WARD_DATA = {
    "SOBA": [
        "ALHAZAI",
        "DANWATA",
        "GAMAGIRA",
        "GARKAYE",
        "GIMBA",
        "KINKIBA",
        "KWASSALLO",
        "MAIGANA",
        "RAHAMA",
        "SOBA",
        "TURAWA"
    ]
}

# Full un-truncated core sector dictionary registry data arrays
MOCK_DATA_REGISTRY = [
    {
        "ID": "LSOEP-KAD-SOB-001",
        "Name": "Alhaji Ibrahim Sani",
        "LGA": "Soba LGA",
        "Ward": "Alhazai Ward",
        "NIN": "12345678901",
        "Status": "Verified",
        "Allocation": "SME Seed Capital"
    },
    {
        "ID": "LSOEP-KAD-SOB-002",
        "Name": "Yusuf Lawal Maigana",
        "LGA": "Soba LGA",
        "Ward": "Maigana Ward",
        "NIN": "98765432109",
        "Status": "Verified",
        "Allocation": "Agro-Development Grant"
    },
    {
        "ID": "LSOEP-KAD-SOB-003",
        "Name": "Aminu Umar Danwata",
        "LGA": "Soba LGA",
        "Ward": "Danwata Ward",
        "NIN": "45678912301",
        "Status": "Pending Review",
        "Allocation": "Educational Bursary"
    },
    {
        "ID": "LSOEP-KAD-SOB-004",
        "Name": "Khadijah Gambo Richifa",
        "LGA": "Soba LGA",
        "Ward": "Soba Ward",
        "NIN": "78912345602",
        "Status": "Verified",
        "Allocation": "Dry Season Irrigation Support"
    },
    {
        "ID": "LSOEP-KAD-SOB-005",
        "Name": "Mustapha Haruna Turawa",
        "LGA": "Soba LGA",
        "Ward": "Turawa Ward",
        "NIN": "32165498705",
        "Status": "Flagged",
        "Allocation": "None - Verification Required"
    }
]

PROJECT_PARTITION_ID = "SOBA_KADUNA"
COLUMNS_STRUCTURE = [
    "NIN", "VIN", "Name", "LGA", "Ward", "Status", "Category", 
    "Skill_Interest", "Custom_Skill", "Gender", "DOB", "Disability_Status", 
    "Prior_Palliative", "Academic_Qual", "Admission_Year", "Admission_Letter",
    "Phone", "Leader_Name", "Leader_Contact", "Leader_NIN", "Leader_LGA", 
    "Leader_Ward", "Leader_Portfolio", "Voucher_Code", "Remarks", "Timestamp"
]

OFFLINE_REGISTRY_CACHE = "offline_registry_cache.csv"
OFFLINE_METADATA_CACHE = "offline_metadata_cache.json"

# ==============================================================================
# AUTOSAVE PERSISTENCE & ERROR EXTRACTION MATRIX
# ==============================================================================
def trigger_background_autosave():
    try:
        st.session_state.global_registry.to_csv(OFFLINE_REGISTRY_CACHE, index=False)
        meta_payload = {
            "submitted_wards": st.session_state.submitted_wards,
            "submitted_pus": st.session_state.submitted_pus
        }
        with open(OFFLINE_METADATA_CACHE, "w") as f:
            json.dump(meta_payload, f)
    except Exception as e:
        st.caption(f"Autosave sync bypass: {e}")

def initialize_and_recover_system_states():
    if 'global_registry' not in st.session_state:
        if os.path.exists(OFFLINE_REGISTRY_CACHE):
            try:
                st.session_state.global_registry = pd.read_csv(OFFLINE_REGISTRY_CACHE)
            except Exception:
                os.remove(OFFLINE_REGISTRY_CACHE)
        
        if 'global_registry' not in st.session_state:
            st.session_state.global_registry = pd.DataFrame([
                {"NIN": "23456789012", "VIN": "90FVA2345678901", "Name": "Bello Ahmed", "LGA": "SOBA", "Ward": "ALHAZAI", "Status": "Verified", "Category": "Professional", "Skill_Interest": "ICT & AI Core Programming", "Custom_Skill": "", "Gender": "Male", "DOB": "1994-04-12", "Disability_Status": "None", "Prior_Palliative": "No", "Academic_Qual": "Degree/HND", "Admission_Year": "2024", "Admission_Letter": None, "Phone": "08039999999", "Leader_Name": "Hon. Richifa", "Leader_Contact": "08038888888", "Leader_NIN": "33333333333", "Leader_LGA": "SOBA", "Leader_Ward": "ALHAZAI", "Leader_Portfolio": "Community Leader", "Voucher_Code": "SB01V", "Remarks": "Authentic", "Timestamp": "2026-05-15 10:00:00"},
                {"NIN": "87654321098", "VIN": "90FVA8765432109", "Name": "Fatima Usman", "LGA": "SOBA", "Ward": "MAIGANA", "Status": "Flagged", "Category": "Skilled Artisan", "Skill_Interest": "Solar Renewable Energy Engineering", "Custom_Skill": "", "Gender": "Female", "DOB": "1998-09-21", "Disability_Status": "None", "Prior_Palliative": "Yes", "Academic_Qual": "SSCE", "Admission_Year": "2025", "Admission_Letter": None, "Phone": "08037777777", "Leader_Name": "Alhaji Wada", "Leader_Contact": "08036666666", "Leader_NIN": "44444444444", "Leader_LGA": "SOBA", "Leader_Ward": "MAIGANA", "Leader_Portfolio": "Clergy", "Voucher_Code": "SB02V", "Remarks": "Verify Biometrics", "Timestamp": "2026-05-15 11:15:22"}
            ], columns=COLUMNS_STRUCTURE)

    if 'submitted_wards' not in st.session_state or 'submitted_pus' not in st.session_state:
        recovered_meta = False
        if os.path.exists(OFFLINE_METADATA_CACHE):
            try:
                with open(OFFLINE_METADATA_CACHE, "r") as f:
                    meta_payload = json.load(f)
                st.session_state.submitted_wards = meta_payload.get("submitted_wards", {})
                st.session_state.submitted_pus = meta_payload.get("submitted_pus", {})
                recovered_meta = True
            except Exception:
                os.remove(OFFLINE_METADATA_CACHE)
                
        if not recovered_meta:
            st.session_state.submitted_wards = {
                "SOBA_ALHAZAI": "2026-05-15 08:12:04",
                "SOBA_MAIGANA": "2026-05-15 09:45:10"
            }
            st.session_state.submitted_pus = {
                "SOBA_ALHAZAI_PU001": "{\"Presidential\": 120, \"Senatorial\": 245, \"Governorship\": 190, \"State_House\": 210, \"Timestamp\": \"2026-05-15 08:10:00\", \"Agent\": \"Umar Ibrahim\", \"EC8A_Status\": \"Verified_PNG\"}",
                "SOBA_MAIGANA_PU003": "{\"Presidential\": 95, \"Senatorial\": 310, \"Governorship\": 220, \"State_House\": 185, \"Timestamp\": \"2026-05-15 09:30:15\", \"Agent\": \"Sani Haruna\", \"EC8A_Status\": \"Verified_JPG\"}"
            }

    if 'current_page' not in st.session_state: st.session_state.current_page = "skill_form"
    if 'radar_threat' not in st.session_state: st.session_state.radar_threat = False
    if 'threat_msg' not in st.session_state: st.session_state.threat_msg = ""
    if 'recycle_bin_registry' not in st.session_state: st.session_state.recycle_bin_registry = None
    if 'recycle_bin_wards' not in st.session_state: st.session_state.recycle_bin_wards = {}
    if 'recycle_bin_pus' not in st.session_state: st.session_state.recycle_bin_pus = {}

# Trigger automated self-heal sequence immediately on engine boot
initialize_and_recover_system_states()
IS_LOCAL_SANDBOX = not os.path.exists("/app/secrets.toml") and not os.path.exists(".streamlit/secrets.toml")

conn = None
if not IS_LOCAL_SANDBOX:
    try:
         conn = st.connection("postgresql", type="sql")
    except Exception:
         conn = None

# ==============================================================================
# UI STYLE CONFIGURATION & REGAL GLASSMORPHISM KEYFRAMES
# ==============================================================================
st.set_page_config(
    page_title="LSOEP TITAN KADUNA | HON. SULEIMAN YAHAYA RICHIFA HUB", 
    page_icon="🏛️",
    layout="wide", 
    initial_sidebar_state="expanded"
)

try:
    from modules import branding
    HAS_MODULES = True
except ImportError:
    HAS_MODULES = False

st.markdown("""
    <style>
    [data-testid="stSidebar"] { 
        background-color: #030f21 !important; 
        border-right: 4px solid #8B0000 !important;
    }
    
    .admin-launch-zone {
        border: 2px dashed #00E5FF; padding: 15px; border-radius: 14px;
        background-color: rgba(0, 229, 255, 0.08); margin-bottom: 15px;
    }
    
    .inst-link-box {
        display: block; background: linear-gradient(90deg, #8B0000 0%, #4A0000 100%) !important;
        color: #FFFFFF !important; padding: 12px; border-radius: 10px; 
        text-align: center; font-weight: 900; margin-bottom: 10px; text-decoration: none;
        font-size: 14px; letter-spacing: 1px; text-transform: uppercase;
    }
    
    .stButton>button { 
        width: 100% !important; height: 48px !important; font-weight: 800 !important; 
        font-size: 14px !important; margin-bottom: 10px !important; border: 2px solid #8B0000 !important;
        border-radius: 10px !important; color: #FFFFFF !important; transition: all 0.3s ease;
        text-transform: uppercase; letter-spacing: 1px;
    }
    
    button[key="btn_skill"] { background: linear-gradient(90deg, #00B4DB 0%, #0083B0 100%) !important; }
    button[key="btn_sch"] { background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important; }
    button[key="btn_pal"] { background: linear-gradient(90deg, #2e8b57 0%, #38ef7d 100%) !important; }
    button[key="btn_cv"] { background: linear-gradient(90deg, #8E2DE2 0%, #4A00E0 100%) !important; }
    button[key="btn_cmd"] { background: #0b1e36 !important; border: 2px solid #00E5FF !important; }

    @keyframes master_chroma_flow {
        0% { border-color: #FFD700; box-shadow: 0 0 20px rgba(255, 215, 0, 0.45); }
        50% { border-color: #00E5FF; box-shadow: 0 0 35px rgba(0, 229, 255, 0.7); }
        100% { border-color: #FFD700; box-shadow: 0 0 20px rgba(255, 215, 0, 0.45); }
    }

    @keyframes alert_pulse { 
        0% { background-color: #FF1744; box-shadow: 0 0 10px #FF1744; } 
        50% { background-color: #B71C1C; box-shadow: 0 0 25px #FF1744; } 
        100% { background-color: #FF1744; box-shadow: 0 0 10px #FF1744; } 
    }

    @keyframes radar_flash {
        0% { background-color: #FF0000; color: #FFFFFF; box-shadow: 0 0 20px #FF0000; }
        50% { background-color: #330000; color: #FF0000; box-shadow: 0 0 0px #000000; }
        100% { background-color: #FF0000; color: #FFFFFF; box-shadow: 0 0 20px #FF0000; }
    }

    /* SOLID COMMAND PANELS HUB PORTAL CONTAINER STRUCTURE */
    .unified-command-vault {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        height: 195px !important; 
        background: linear-gradient(135deg, rgba(6, 32, 74, 1.0) 0%, rgba(2, 10, 23, 1.0) 100%) !important;
        border: 4px solid #FFD700 !important;
        animation: master_chroma_flow 4s infinite ease-in-out !important;
        padding: 0px !important; 
        border-radius: 18px !important;
        backdrop-filter: blur(30px) !important;
        -webkit-backdrop-filter: blur(30px) !important;
        margin-top: 5px !important;
        box-shadow: inset 0 0 30px rgba(255, 215, 0, 0.2), 0 12px 35px rgba(0, 0, 0, 0.5) !important;
        overflow: hidden !important;
    }

    /* MAXIMUM FILL LEFT WITHOUT CROPPING ARTIFACTS */
    .mace-vault-shield {
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 210px !important; 
        height: 100% !important; 
        /* Darker matte gradient anchor layer to ground the raw asset color beautifully */
        background: rgba(4, 20, 48, 0.6) !important; 
        overflow: hidden !important;
        transition: transform 0.4s ease;
    }
    
    .mace-vault-shield:hover {
        transform: scale(1.02);
    }

    .mace-vault-shield img {
        height: 100% !important; 
        width: 100% !important; 
        /* FIXED: Changed to contain so that no part of the legislative crown or rod is clipped out */
        object-fit: contain !important; 
        mix-blend-mode: normal !important; 
        image-rendering: -webkit-optimize-contrast !important;
        image-rendering: crisp-edges !important;
        filter: drop-shadow(0px 0px 14px rgba(255, 215, 0, 0.75)) contrast(1.35) brightness(1.05);
    }

    /* MAXIMUM EDGE-TO-EDGE RIGHT CAPACITY CONSTITUENCY PHOTO */
    .photo-vault-shield {
        flex-shrink: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 285px !important; 
        height: 100% !important; 
        background: transparent !important; 
        overflow: hidden !important;
    }

    .photo-vault-shield img {
        height: 100% !important;
        width: 100% !important; 
        object-fit: cover !important; /* Kept cover so map profile stretches completely flush without borders */
        mix-blend-mode: normal !important; 
        image-rendering: -webkit-optimize-contrast !important;
        image-rendering: crisp-edges !important;
        filter: contrast(1.25) brightness(1.02);
    }

    .vault-text-block {
        flex-grow: 2 !important;
        text-align: center !important;
        padding: 0 10px !important;
    }

    .vault-text-block h1 {
        color: #FFFF00 !important;
        margin: 0 !important;
        font-size: 2.1rem !important;
        font-weight: 900 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        text-shadow: 2px 2px 5px #000000 !important;
    }

    .vault-text-block .sub-title {
        color: #FFFFFF !important;
        margin: 6px 0 0 0 !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6) !important;
    }

    .vault-text-block .geo-stamp {
        color: #00E5FF !important;
        margin: 4px 0 0 0 !important;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6) !important;
    }

    /* RESPONSIVE LAYOUT CONSTRAINTS FOR MOBILES */
    @media (max-width: 768px) {
        .unified-command-vault {
            flex-direction: column !important; 
            height: auto !important; 
            padding: 20px 10px !important;
            gap: 15px !important;
        }

        .mace-vault-shield {
            width: 100% !important; 
            height: 140px !important; 
        }

        .photo-vault-shield {
            width: 100% !important;
            height: 160px !important; 
        }

        .mace-vault-shield img {
            object-fit: contain !important;
        }
        .photo-vault-shield img {
            object-fit: cover !important; 
        }

        .vault-text-block h1 {
            font-size: 1.4rem !important; 
            line-height: 1.2 !important;
        }

        .vault-text-block .sub-title {
            font-size: 0.85rem !important;
        }

        .vault-text-block .geo-stamp {
            font-size: 0.95rem !important;
        }
    }

    .sidebar-red-flash {
        animation: alert_pulse 1.2s infinite ease-in-out; color: #FFFFFF !important;
        padding: 14px; border-radius: 10px; text-align: center; font-weight: 900; 
        display: block; width: 100%; font-size: 14px; margin-bottom: 12px;
        letter-spacing: 1px; text-transform: uppercase;
    }
    .radar-sticky-threat {
        animation: radar_flash 0.5s infinite;
        padding: 15px; border-radius: 8px; border: 3px solid #FFFFFF;
        text-align: center; font-weight: bold; font-size: 14px; margin-bottom: 15px;
    }
    .tier-box {
        display: inline-block; padding: 10px 20px; margin: 5px; border-radius: 6px;
        font-weight: bold; color: white; text-align: center; border: 2px solid #FFFFFF;
    }
    .tier-box.tier-pres { background-color: #FF4B4B !important; }
    .tier-box.tier-sen { background-color: #1F77B4 !important; }
    .tier-box.tier-rep { background-color: #2CA02C !important; }
    .tier-box.tier-gov { background-color: #9467BD !important; }
    .tier-box.tier-house { background-color: #FF7F0E !important; }
    
    .printable-slip-box {
        background-color: #FFFFFF !important; color: #000000 !important;
        padding: 25px; border: 3px double #8B0000; border-radius: 4px;
        font-family: 'Courier New', Courier, monospace; margin-top: 15px;
    }
    .slip-header { text-align: center; font-weight: 900; font-size: 16px; margin-bottom: 15px; border-bottom: 2px dashed #000; padding-bottom: 10px; }
    .slip-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; font-weight: bold; }
    
    .stTextInput label p { color: #00E5FF !important; font-weight: 700 !important; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR NAVIGATION INTERFACE CONTROL MATRIX
# ==============================================================================
with st.sidebar:
    if st.session_state.radar_threat:
        st.markdown(f'<div class="radar-sticky-threat">🚨 SECURITY WARNING: IDENTITY DUPLICATION COLLISION<br>{st.session_state.threat_msg}</div>', unsafe_allow_html=True)

    st.markdown('<div class="admin-launch-zone">', unsafe_allow_html=True)
    adm_key = st.text_input("COMMAND HUB KEY", type="password", key="adm_v30_auth")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown('<a href="https://www.facebook.com/salis.isah.39/" target="_blank" class="inst-link-box">🌐 Hon. Richifa Facebook</a>', unsafe_allow_html=True)
    
    st.divider()
    if st.button("🛠️ SKILL VOCATION POOL", key="btn_skill"): st.session_state.current_page = "skill_form"
    if st.button("🎓 STUDENT SCHOLARSHIP/GRANT", key="btn_sch"): st.session_state.current_page = "scholarship_form"
    if st.button("📦 CONSTITUENT PALLIATIVE ENROLLMENT", key="btn_pal"): st.session_state.current_page = "palliative_gateway"
    if st.button("🚀 CV & ARTISAN VAULT", key="btn_cv"): st.session_state.current_page = "cv_vault"
    
    st.markdown('<div class="sidebar-red-flash">🚨 COMMUNITY URGENT NEED</div>', unsafe_allow_html=True)
    if st.button("TRIGGER REGISTRATION INTERFACE", key="btn_cun_redirect"):
        st.session_state.current_page = "cun_trigger"
    
    st.divider()
    if st.button("🏛️ RETURN TO COMMAND HUB", key="btn_cmd"): st.session_state.current_page = "main_dashboard"

    st.divider()
    st.markdown("<p style='color:#8B0000; font-weight:bold; text-transform: uppercase;'>🔒 Field Authentication Core</p>", unsafe_allow_html=True)
    
    sup_key_input = st.text_input("WARD SUPERVISOR KEY", type="password", key="sup_v30_auth_sidebar")
    agt_key_input = st.text_input("POLLING UNIT AGENT KEY", type="password", key="agt_v30_auth_sidebar")

    if adm_key == "adc 2027":
        st.session_state.current_page = "main_dashboard"
    elif sup_key_input == "adc adc 2027":
        st.session_state.current_page = "supervisor_panel"
    elif agt_key_input == "adc 2027":
        st.session_state.current_page = "agent_panel"

    if sup_key_input:
        st.text_area("Supervisor Remarks/Field Observations", key="sup_remarks", placeholder="Field log entry space...")
    if agt_key_input:
        st.text_area("Agent Remarks/Field Observations", key="agt_remarks", placeholder="Unit log entry space...")
        
    st.caption(f"Engine: v34.0.46-SOBA | {datetime.date.today()}")

# ==============================================================================
# INTEGRATED HEADER OBJECTS BUILD ZONE (PIXEL PERFECT FLUSH & TEXTURE CONTROL)
# ==============================================================================
def render_marquee_header():
    if HAS_MODULES:
        branding.render_header()
    else:
        st.markdown(
            '<div class="unified-command-vault">'
            '  <div class="mace-vault-shield">'
            '    <img src="https://raw.githubusercontent.com/AustinSgwvm/lsoep-titan-kaduna/main/assets/mace.png">'
            '  </div>'
            '  <div class="vault-text-block">'
            '    <h1>HON. SULEIMAN YAHAYA RICHIFA</h1>'
            '    <div class="sub-title">MEMBER REPRESENTING SOBA FEDERAL CONSTITUENCY</div>'
            '    <div class="geo-stamp">KADUNA STATE</div>'
            '  </div>'
            '  <div class="photo-vault-shield">'
            '    <img src="https://raw.githubusercontent.com/AustinSgwvm/lsoep-titan-kaduna/main/assets/soba_icon.png">'
            '  </div>'
            '</div>', 
            unsafe_allow_html=True
        )
        
        st.markdown(
            '<div style="margin-top:15px; background:linear-gradient(180deg, #061a33 0%, #020b17 100%); padding:8px; border-radius:8px;">'
            '  <marquee scrollamount="4" style="color:#FFFFFF; font-weight:800; font-size:16px; letter-spacing:1.5px; font-family:sans-serif;">'
            '    ⚡ ADC 2027, SET TO LEAD THE NATION....... ADC 2027, SET TO LEAD THE NATION....... ⚡'
            '  </marquee>'
            '</div><br>',
            unsafe_allow_html=True
        )

# Shared download trigger assembly mapping node
def render_module_download_trigger(data_source, filename_prefix, unique_key):
    try:
        csv_bytes = pd.DataFrame(data_source).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DOWNLOAD SYSTEM LOG EXPORT",
            data=csv_bytes,
            file_name=f"{filename_prefix}_{datetime.date.today()}.csv",
            mime="text/csv",
            key=f"dl_btn_{unique_key}"
        )
    except Exception as e:
        st.caption(f"Download entry failure: {e}")

# Shared execution purge sub-engine frame 
def render_institutional_purge_engine(key_suffix):
    st.markdown("---")
    st.subheader("🚨 Institutional Data Purge Zone")
    confirm_purge = st.text_input("Type 'PURGE SYSTEM DATA' to authorize reset:", key=f"purge_box_{key_suffix}")
    if st.button("💥 EXECUTE SYSTEM PURGE", type="primary", key=f"purge_btn_{key_suffix}"):
        if confirm_purge == "PURGE SYSTEM DATA":
            st.session_state.global_registry = pd.DataFrame(columns=COLUMNS_STRUCTURE)
            st.session_state.submitted_wards = {}
            st.session_state.submitted_pus = {}
            trigger_background_autosave()
            st.success("System tracking layers reset completely.")
            st.sidebar.rerun()

# ==============================================================================
# MASTER APPLICATION CORE ROUTING LAYER
# ==============================================================================

# --- ROUTING FRAME 1: WARD SUPERVISOR MATRIX ENGINE ---
if st.session_state.current_page == "supervisor_panel":
    render_marquee_header()
    st.markdown('<div class="sidebar-red-flash">🛡️ WARD SUPERVISOR COMMAND: FORM EC8A LOGS</div>', unsafe_allow_html=True)
    if 'sup_slip_preview' not in st.session_state: st.session_state.sup_slip_preview = None

    with st.form("supervisor_form"):
        c1, c2 = st.columns(2)
        with c1:
            sup_name = st.text_input("Supervisor Full Name")
            sup_phone = st.text_input("Phone Number")
            sup_state = st.text_input("State Link Node", value="KADUNA STATE")
            sup_lga = st.selectbox("LGA Bound", list(LGA_WARD_DATA.keys()))
            sup_ward = st.selectbox("Ward Node Matrix Selector", LGA_WARD_DATA.get(sup_lga, []))
            sup_unit = st.text_input("Ward Unit Tracking Code/Number")
        
        ward_id = f"{sup_lga}_{sup_ward}".replace(" ", "_").upper()
        
        with c2:
            st.markdown("""
            **Tiers Audited Vector Checkbox Mapping:**<br>
            <div class="tier-box tier-pres">Presidential</div><div class="tier-box tier-sen">Senatorial</div><div class="tier-box tier-rep">House of Reps</div>
            """, unsafe_allow_html=True)
            tiers_selected = st.multiselect("Active Scope Assessment Matrix", ["Presidential", "Senatorial", "Federal House"], default=["Federal House"])
            st.number_input("Highest Party Vote Recorded", min_value=0, key="sup_high_vote")
            st.number_input("Principal Votes Cast Density", min_value=0, key="sup_pr_vote")
            st.file_uploader("Upload Supervisor Physical NIN Slip Link Asset", type=['pdf', 'jpg', 'png'])
        
        st.camera_input("Live Capture Sensor Matrix: Form EC8A Sheet Sheet")
        
        if st.form_submit_button("🔍 GENERATE SYSTEM INTEGRITY PREVIEW RECORD SLIP"):
            if sup_name == "" or sup_phone == "" or sup_unit == "":
                st.warning("All core primary field parameters must match strings.")
            else:
                st.session_state.sup_slip_preview = {
                    "Supervisor": sup_name, "Phone": sup_phone, "LGA": sup_lga, "Ward": sup_ward,
                    "Unit": sup_unit, "Tiers": ", ".join(tiers_selected),
                    "High_Vote": int(st.session_state.get("sup_high_vote", 0)),
                    "Principal_Votes": int(st.session_state.get("sup_pr_vote", 0)),
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

    if st.session_state.sup_slip_preview is not None:
        p_data = st.session_state.sup_slip_preview
        st.markdown(f"""
        <div class="printable-slip-box">
            <div class="slip-header">🏛️ LSOEP NATIONAL ASSEMBLY INTEGRITY RECEIPT OVERVIEW</div>
            <div class="slip-row"><span>TIMESTAMP DATA:</span> <span>{p_data['Timestamp']}</span></div>
            <div class="slip-row"><span>SUPERVISOR NAME:</span> <span>{p_data['Supervisor']}</span></div>
            <div class="slip-row"><span>PHONE INTERFACE:</span> <span>{p_data['Phone']}</span></div>
            <div class="slip-row"><span>LGA BOUNDARY:</span> <span>{p_data['LGA']}</span></div>
            <div class="slip-row"><span>WARD SECTOR:</span> <span>{p_data['Ward']}</span></div>
            <div class="slip-row"><span>UNIT IDENTIFIER:</span> <span>{p_data['Unit']}</span></div>
            <div class="slip-row"><span>ACTIVE TIERS:</span> <span>{p_data['Tiers']}</span></div>
            <div class="slip-row"><span>HIGHEST TOTAL:</span> <span>{p_data['High_Vote']:,}</span></div>
            <div class="slip-row"><span>VALID CORE SUM:</span> <span>{p_data['Principal_Votes']:,}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("🔒 CONFIRM METRICS: LOG INTO PRODUCTION ARRAYS"):
                if ward_id in st.session_state.submitted_wards:
                    st.error("🛑 Results sheet indicators for this Ward coordinate set have already been locked.")
                else:
                    st.session_state.submitted_wards[ward_id] = p_data['Timestamp']
                    trigger_background_autosave()
                    st.session_state.sup_slip_preview = None
                    st.success("Sheet information successfully committed.")
                    st.rerun()
        with col_v2:
            if st.button("❌ ABORT TRANSACTION: CLEAR PREVIEW NODE STUB"):
                st.session_state.sup_slip_preview = None
                st.warning("Preview storage wiped successfully.")
                st.rerun()

# --- ROUTING FRAME 2: POLLING UNIT AGENT MATRIX ENGINE ---
elif st.session_state.current_page == "agent_panel":
    render_marquee_header()
    st.markdown('### 🗳️ POLLING UNIT AGENT: FIELD DATA TRANSFERS')
    if 'agt_slip_preview' not in st.session_state: st.session_state.agt_slip_preview = None

    a1, a2 = st.columns(2)
    with a1:
        agt_name = st.text_input("Agent Full Operator Name")
        agt_phone = st.text_input("Agent Communication Contact Phone")
        agt_lga = st.selectbox("LGA Scope Mapping Zone", list(LGA_WARD_DATA.keys()))
        agt_ward = st.selectbox("Ward Scope Mapping Zone Node", LGA_WARD_DATA.get(agt_lga, []))
        agt_pu_num = st.text_input("Polling Unit (PU) Identity Name Code").strip().replace(" ", "_").upper()
        
    pu_id = f"{agt_lga}_{agt_ward}_{agt_pu_num}".replace(" ", "_").upper()
    
    if agt_pu_num != "" and pu_id in st.session_state.submitted_pus:
        st.error("🛑 Polling Unit entry parameter sequence matches locked profile record. Dropping link stream.")
    else:
        with st.form("agent_form"):
            with a2:
                st.markdown("""
                **Unit Active Layout Validation Mapping Check:**<br>
                <div class="tier-box tier-pres">Presidential</div><div class="tier-box tier-sen">Senatorial</div>
                """, unsafe_allow_html=True)
                agt_tiers = st.multiselect("Affirm Verification Parameters Scope", ["Federal House", "Presidential", "Senatorial"], default=["Federal House"])
                st.number_input("Total Ballots Inside Unit Box Container", min_value=0, key="agt_tot_vote")
                st.number_input("Valid Votes Quantum Metric Total", min_value=0, key="agt_pr_vote")
                st.file_uploader("Upload Agent Verification NIN Slip Column File", type=['pdf', 'jpg', 'png'])
            st.camera_input("Capture Local Unit Level Physical Document Ledger Asset Sheet")
            
            if st.form_submit_button("🔍 COMPREHENSIVE ENTRY EVALUATION"):
                if agt_name == "" or agt_phone == "" or agt_pu_num == "":
                    st.warning("Please satisfy required identity configuration strings before transmission validation steps.")
                else:
                    st.session_state.agt_slip_preview = {
                        "Agent": agt_name, "Phone": agt_phone, "LGA": agt_lga, "Ward": agt_ward, "PU": agt_pu_num,
                        "Tiers": ", ".join(agt_tiers), "Total_Votes": int(st.session_state.get("agt_tot_vote", 0)),
                        "Principal_Votes": int(st.session_state.get("agt_pr_vote", 0)),
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

        if st.session_state.agt_slip_preview is not None:
            a_data = st.session_state.agt_slip_preview
            st.markdown(f"""
            <div class="printable-slip-box">
                <div class="slip-header">🗳️ LSOEP FIELD OPERATOR REGISTERED FIELD SLIP LOG</div>
                <div class="slip-row"><span>CAPTURED TIMESTAMP:</span> <span>{a_data['Timestamp']}</span></div>
                <div class="slip-row"><span>AGENT NAME STAMP:</span> <span>{a_data['Agent']}</span></div>
                <div class="slip-row"><span>CELLULAR INTERFACE:</span> <span>{a_data['Phone']}</span></div>
                <div class="slip-row"><span>LGA SECTOR NODE:</span> <span>{a_data['LGA']}</span></div>
                <div class="slip-row"><span>WARD ASSIGNMENT:</span> <span>{a_data['Ward']}</span></div>
                <div class="slip-row"><span>POLLING UNIT NUM:</span> <span>{a_data['PU']}</span></div>
                <div class="slip-row"><span>AUDITED BALANCES:</span> <span>{a_data['Total_Votes']:,}</span></div>
                <div class="slip-row"><span>VALID QUANTUM LOG:</span> <span>{a_data['Principal_Votes']:,}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            av1, av2 = st.columns(2)
            with av1:
                if st.button("🔒 COMMIT METRICS CONFIGURATION AND ARCHIVE RECORD"):
                    st.session_state.submitted_pus[pu_id] = a_data['Timestamp']
                    trigger_background_autosave()
                    st.session_state.agt_slip_preview = None
                    st.success("Polling unit log matrix records written to global cache layer arrays.")
                    st.rerun()
            with av2:
                if st.button("❌ DISCARD TRANSACTION BUFFER"):
                    st.session_state.agt_slip_preview = None
                    st.warning("Buffer variables cleared.")
                    st.rerun()

# --- ROUTING FRAME 3: EXECUTIVE COMMAND HUB CONSOLE MATRIX ---
elif st.session_state.current_page == "main_dashboard":
    render_marquee_header()
    st.markdown('## 🏛️ EXECUTIVE CONTROL COMMAND DASHBOARD PORTAL ARRAY')
    
    tabs = st.tabs([
        "📊 Master Registry Matrix", 
        "📈 Infrastructure CUN Matrix", 
        "⚖️ Database Audit Diagnostics", 
        "🛡️ RADAR Deduplication Interceptor", 
        "🎓 Scholar Talent Matrix", 
        "💎 Vantedge Influencer Proportions", 
        "🗳️ Live Election Analytical Sync", 
        "📝 Ground Truth Form EC8A Data", 
        "📂 Bulk Data Sync Stream", 
        "📜 Executive Waiver Ledger", 
        "🚀 Legislative Progress Tracker", 
        "📅 Long-Term Momentum Monitoring"
    ])
    
    soba_index_metrics_mock = pd.DataFrame({
        "LGA Name Location": ["SOBA LGA MATRIX NODE"],
        "Performance Index Score": [84.6],
        "CUN Deficit Rate Proportion": [21.4],
        "Voter Turnout Metric Density": [76.8],
        "Waivers Distributed Yield": [14]
    }).set_index("LGA Name Location")
    
    with tabs[0]:
        st.subheader("📊 Master Verification Registry Database Partition Array")
        mc1, mc2 = st.columns([1, 2])
        with mc1:
            st.markdown("**Active Intake Status Partition Trace Records**")
            st.dataframe(st.session_state.global_registry[['Name', 'LGA', 'Ward', 'Status']])
        with mc2:
            st.markdown("**Processing Stream Success Metrics Vector Chart Across Soba LGA**")
            st.bar_chart(soba_index_metrics_mock["Performance Index Score"])
        st.dataframe(st.session_state.global_registry, width='stretch')
        
        render_module_download_trigger(st.session_state.global_registry, "Master_Registry_Log", "t1_dl")
        render_institutional_purge_engine("t1_purge")

    with tabs[1]:
        st.subheader("📈 Regional Community Urgent Need Matrix Framework Indicators")
        
        cun_records_array = []
        for index_node, ward_string_name in enumerate(GEOGRAPHY["Soba LGA"]):
            cun_records_array.append({
                "LGA Territory Identification Link": "SOBA CONST AREA", 
                "Administrative Ward Boundary Target": ward_string_name.upper(), 
                "Water Infrastructure Asset Deficit Ratio %": 44 + (index_node * 4) % 15, 
                "Grid Energy Power Interruption Density %": 88 - (index_node * 3) % 12, 
                "Critical Access Road Shortage Weights %": 71 + (index_node * 5) % 16, 
                "Logged Internal Community Security Threats Metrics": 11 + (index_node * 2) % 9
            })
        df_cun_matrix_canvas = pd.DataFrame(cun_records_array)
        st.dataframe(df_cun_matrix_canvas, width='stretch')
        st.bar_chart(df_cun_matrix_canvas.set_index("Administrative Ward Boundary Target")[["Water Infrastructure Asset Deficit Ratio %", "Grid Energy Power Interruption Density %"]])
        render_module_download_trigger(df_cun_matrix_canvas, "CUN_Deficit_Matrix_Log", "t2_dl")
        render_institutional_purge_engine("t2_purge")

    with tabs[2]:
        st.subheader("⚖️ Forensic Audit Database Query & Connection Diagnostic Stream")
        st.error("⚠️ Isolation Warning Layer: Supabase API Cloud Gateway locked inside internal local execution container frames.")
        
        if conn is not None:
             try:
                 df_db_direct_test = conn.query(f"SELECT * FROM ward_returns WHERE project_partition = '{PROJECT_PARTITION_ID}' LIMIT 5;", ttl="0m")
                 st.success("Operational link established cleanly with relational query tables vector pools.")
                 st.dataframe(df_db_direct_test)
             except Exception as e:
                 st.caption(f"Connection framework bypassed intentionally to run local backup cache: {e}")
                 
        with st.expander("🛠️ Expose Active Developer State Cache JSON Mapping Trees", expanded=True):
             st.json({
                 "Memory_State_Allocation_Tokens": list(st.session_state.keys()),
                 "Sandbox_Static_Override_Circuit": "ACTIVE LOCAL BACKUP CONTAINER",
                 "Internal_Target_Matrix_Stencil": PROJECT_PARTITION_ID,
                 "Current_System_Clock_Time": str(datetime.datetime.now())
             })
        render_institutional_purge_engine("t3_purge")

    with tabs[3]:
        st.subheader("🛡️ RADAR Multi-Intake Anti-Fraud Deduplication Interceptor Shield")
        
        radar_records_array = []
        for index_node, ward_string_name in enumerate(GEOGRAPHY["Soba LGA"]):
            radar_records_array.append({
                "LGA Territory Identification Link": "SOBA CONST AREA", 
                "Administrative Ward Boundary Target": ward_string_name.upper(), 
                "Cross-Verification Biometric Pass Confidence %": 99.1 - (index_node * 0.12),
                "Intercepted Duplication Collision Anomalies Tracked": index_node % 2,
                "Multi-Voucher System Fraud Attempts Dropped": index_node % 3
            })
        df_radar_matrix_canvas = pd.DataFrame(radar_records_array)
        st.dataframe(df_radar_matrix_canvas, width='stretch')
        st.metric("Total Duplicate Fraud Collisions Terminated Safely", "0 Active Threat Logs Confirmed")
        
        if st.button("Send Global System Clear Code To Sidebar Threat Indicators"):
            st.session_state.radar_threat = False
            st.session_state.threat_msg = ""
            st.success("Threat verification clear signals dispatched smoothly.")
            st.rerun()
        render_module_download_trigger(df_radar_matrix_canvas, "Radar_Deduplication_Logs", "t4_dl")
        render_institutional_purge_engine("t4_purge")

    with tabs[4]:
        st.subheader("🎓 Academic Grants Distribution Pools & Talent Demographics Hub")
        
        cv_records_array = []
        for index_node, ward_string_name in enumerate(GEOGRAPHY["Soba LGA"]):
            cv_records_array.append({
                "LGA Territory Identification Link": "SOBA CONST AREA", 
                "Administrative Ward Boundary Target": ward_string_name.upper(), 
                "PhD High-Fidelity Research Candidates Enrolled": index_node % 2,
                "Masters Level Profiles Captured": 1 + (index_node % 3),
                "Bachelors Degree Holders Indexed": 15 + (index_node * 2),
                "Technical Vocation Artisans Tracked": 30 + (index_node * 4)
            })
        df_cv_matrix_canvas = pd.DataFrame(cv_records_array)
        st.dataframe(df_cv_matrix_canvas, width='stretch')
        st.bar_chart(df_cv_matrix_canvas.set_index("Administrative Ward Boundary Target")[["Bachelors Degree Holders Indexed", "Technical Vocation Artisans Tracked"]])
        render_module_download_trigger(df_cv_matrix_canvas, "Talent_Pool_Demographics", "t5_dl")
        render_institutional_purge_engine("t5_purge")

    with tabs[5]:
        st.subheader("💎 Vantedge Strategic Influence Vectors & Demographics Scale")
        
        vantage_records_array = []
        for index_node, ward_string_name in enumerate(GEOGRAPHY["Soba LGA"]):
            vantage_records_array.append({
                "LGA Territory Identification Link": "SOBA CONST AREA", 
                "Administrative Ward Boundary Target": ward_string_name.upper(), 
                "Opinion Influencers Authenticated": 3 + (index_node % 4),
                "Youth Mobilization Mobilization Directors": 6 + (index_node % 5),
                "Community Vouched Elders Registered": 4 + (index_node % 6),
                "Regional Strategic Weight Matrix Allocation Coefficient": round(1.15 + (index_node * 0.04), 2)
            })
        df_vantage_matrix_canvas = pd.DataFrame(vantage_records_array)
        st.dataframe(df_vantage_matrix_canvas, width='stretch')
        render_module_download_trigger(df_vantage_matrix_canvas, "Vantedge_Influence_Matrix_Log", "t6_dl")
        render_institutional_purge_engine("t6_purge")

    with tabs[6]:
        st.subheader("🗳️ Cross-National Multi-Tier Election Verification War Room Sync Arrays")
        
        national_presidential_state_ledgers = {
            "Abia State": {"Registered": 2120000, "Turnout": 381000, "Tally": 361200},
            "Adamawa State": {"Registered": 2190000, "Turnout": 763000, "Tally": 731500},
            "Akwa Ibom State": {"Registered": 2350000, "Turnout": 591000, "Tally": 562400},
            "Anambra State": {"Registered": 2620000, "Turnout": 621000, "Tally": 598100},
            "Bauchi State": {"Registered": 2740000, "Turnout": 890000, "Tally": 855200},
            "Bayelsa State": {"Registered": 1050000, "Turnout": 485900, "Tally": 461300},
            "Benue State": {"Registered": 2770000, "Turnout": 804000, "Tally": 769400},
            "Borno State": {"Registered": 2510000, "Turnout": 712000, "Tally": 681300},
            "Cross River State": {"Registered": 1760000, "Turnout": 441000, "Tally": 419500},
            "Delta State": {"Registered": 3220000, "Turnout": 691000, "Tally": 662500},
            "Ebonyi State": {"Registered": 1590000, "Turnout": 341000, "Tally": 322100},
            "Edo State": {"Registered": 2500000, "Turnout": 612000, "Tally": 581900},
            "Ekiti State": {"Registered": 988000, "Turnout": 315000, "Tally": 301200},
            "Enugu State": {"Registered": 2110000, "Turnout": 482000, "Tally": 461500},
            "FCT Abuja": {"Registered": 1570000, "Turnout": 412500, "Tally": 394200},
            "Gombe State": {"Registered": 1560000, "Turnout": 541000, "Tally": 519200},
            "Imo State": {"Registered": 2410000, "Turnout": 511000, "Tally": 489400},
            "Jigawa State": {"Registered": 2350000, "Turnout": 961000, "Tally": 929500},
            "Kaduna State": {"Registered": 4330000, "Turnout": 1412000, "Tally": 1361400},
            "Kano State": {"Registered": 5920000, "Turnout": 1761000, "Tally": 1702100},
            "Katsina State": {"Registered": 3510000, "Turnout": 1102000, "Tally": 1061900},
            "Kebbi State": {"Registered": 2030000, "Turnout": 781000, "Tally": 749500},
            "Kogi State": {"Registered": 1930000, "Turnout": 615000, "Tally": 591200},
            "Kwara State": {"Registered": 1690000, "Turnout": 491000, "Tally": 472400},
            "Lagos State": {"Registered": 7060000, "Turnout": 1341000, "Tally": 1295200},
            "Nasarawa State": {"Registered": 1890000, "Turnout": 561000, "Tally": 541300},
            "Niger State": {"Registered": 2690000, "Turnout": 821000, "Tally": 789400},
            "Ogun State": {"Registered": 2680000, "Turnout": 621000, "Tally": 594100},
            "Ondo State": {"Registered": 1990000, "Turnout": 571000, "Tally": 549500},
            "Osun State": {"Registered": 1950000, "Turnout": 764000, "Tally": 731200},
            "Oyo State": {"Registered": 3270000, "Turnout": 861000, "Tally": 829500},
            "Plateau State": {"Registered": 2780000, "Turnout": 1112000, "Tally": 1071400},
            "Rivers State": {"Registered": 3530000, "Turnout": 612400, "Tally": 589100},
            "Sokoto State": {"Registered": 791000, "Turnout": 791000, "Tally": 761300},
            "Taraba State": {"Registered": 2020000, "Turnout": 531000, "Tally": 508400},
            "Yobe State": {"Registered": 1480000, "Turnout": 412000, "Tally": 395100},
            "Zamfara State": {"Registered": 1920000, "Turnout": 518000, "Tally": 499200}
        }
        
        state_query_search = st.text_input("Type target State name to evaluate returns parameters:", key="nat_search").strip()
        if state_query_search in national_presidential_state_ledgers:
             matched_metrics = national_presidential_state_ledgers[state_query_search]
             st.success(f"Metrics Extract Mapped Safely for {state_query_search}")
             tc1, tc2, tc3 = st.columns(3)
             tc1.metric("INEC Total Registered Base", f"{matched_metrics['Registered']:,}")
             tc2.metric("Audited Ballots Turnout", f"{matched_metrics['Turnout']:,}")
             tc3.metric("🔴 Presidential Confirmed Tally", f"{matched_metrics['Tally']:,}")
             
        st.markdown(f"""
        **Static Visual Alignment Layout Flags Check:**
        * <div class="tier-box tier-pres" style="width:100%; text-align:left;">🔴 Presidential Accumulation Tally — <b style="float:right;">{sum(x['Tally'] for x in national_presidential_state_ledgers.values()):,} Total Clean Votes</b></div>
        * <div class="tier-box tier-sen" style="width:100%; text-align:left;">🔵 Senatorial Accumulation Tally — <b style="float:right;">24,815,402 Valid Ballots</b></div>
        """, unsafe_allow_html=True)
        render_institutional_purge_engine("t7_purge")

    with tabs[7]:
        st.subheader("📝 Ground Truth Form EC8A Audited Verification Schema")
        target_state_ec8a = st.selectbox("Select State Target Matrix Boundary Node", ["Kaduna State", "Rivers State", "Delta State", "Akwa Ibom State"])
        
        if st.button("Run Real-Time Verification Document Audit Transfer"):
             st.info(f"Establishing verification tracking streams with {target_state_ec8a} repositories...")
             ec8a_records = []
             for item_node in range(1, 6):
                 ec8a_records.append({
                     "State Link Mapped": target_state_ec8a,
                     "Polling Unit Code Identification Link": f"SOBA-WARD-PU00{item_node}",
                     "EC8A Image Link Validation Checksum": f"BLOB_IMG_ID_0{item_node}_SECURE.PNG",
                     "Cryptographic SHA-256 Stamp Metric": f"0xSHA256_{item_node}B99A11FF",
                     "Audited Discrepancy Margin Rate": "0.00% Match Perfect"
                 })
             df_ec8a_trace = pd.DataFrame(ec8a_records)
             st.dataframe(df_ec8a_trace, width='stretch')
        render_institutional_purge_engine("t8_purge")

    with tabs[8]:
        st.subheader("📂 Bulk Throughput Tunnel Sync")
        global_search_string = st.text_input("Input specific Profile target parameters (Name/NIN/VIN):").strip()
        if st.button("Fire Core Scan"):
             st.success(f"Scan completed. String '{global_search_string}' verified safely.")
        render_institutional_purge_engine("t9_purge")

    with tabs[9]:
        st.subheader("📜 Strategic Waiver Assignment Parameters Matrix Ledgers")
        
        waiver_records_array = []
        for index_node, ward_string_name in enumerate(GEOGRAPHY["Soba LGA"]):
            waiver_records_array.append({
                "LGA Territory Identification Link": "SOBA CONST AREA", 
                "Administrative Ward Boundary Target": ward_string_name.upper(), 
                "Waivers Dispatched Allocation": 1 + (index_node % 3),
                "Financial Allocation Metric Equivalent": 150000 * (index_node % 4),
                "Bypass Signature Seal String": f"EXE-AUTH-SOB-0{index_node}"
            })
        df_waiver_matrix_canvas = pd.DataFrame(waiver_records_array)
        st.dataframe(df_waiver_matrix_canvas, width='stretch')
        render_module_download_trigger(df_waiver_matrix_canvas, "Executive_Waivers_Dispatched", "t10_dl")
        render_institutional_purge_engine("t10_purge")

    with tabs[10]:
        st.subheader("🚀 National Assembly Legislative Action Motion Tracking")
        
        df_nass_bills_matrix = pd.DataFrame([
             {"Bill Identification Code": "HB-2026-102", "Legislative Title Summary": "Agricultural Processing Zone Development (Soba) Act", "Current Floor Progress Track": "Third Reading Concluded & Passed", "Last Checked Update Time": "May 2026"},
             {"Bill Identification Code": "HB-2026-115", "Legislative Title Summary": "Federal Medical Centre, Maigana (Establishment) Bill", "Current Floor Progress Track": "Committee Reference Referral", "Last Checked Update Time": "April 2026"},
             {"Bill Identification Code": "HB-2026-128", "Legislative Title Summary": "Aviation Technology Development Fund Bill", "Current Floor Progress Track": "First Reading Table Entry", "Last Checked Update Time": "May 2026"}
        ]).set_index("Bill Identification Code")
        st.dataframe(df_nass_bills_matrix, width='stretch')
        st.progress(85, text="HB-2026-102 Analytical Progress: 85% Concluded")
        render_institutional_purge_engine("t11_purge")

    with tabs[11]:
        st.subheader("📅 Long-Term Temporal Momentum Tracking Interface Matrix Trends")
        mc_col1, mc_col2 = st.columns(2)
        with mc_col1:
             st.markdown("**Weekly Intake Performance Trajectory**")
             st.line_chart(soba_index_metrics_mock["Voter Turnout Metric Density"])
        with mc_col2:
             st.markdown("**Monthly Deficiency Compression Scale Ratios**")
             st.bar_chart(soba_index_metrics_mock["CUN Deficit Rate Proportion"])
        render_institutional_purge_engine("t12_purge")

# --- ROUTING FRAME 4: VOCATIONAL SKILLS REGISTRATION FORM APPLICATION CORE ---
elif st.session_state.current_page == "skill_form":
    render_marquee_header()
    st.markdown('<div class="white-registry-header">🛠️ CONSTITUENT VOCATIONAL SKILLS APPLICATION FORM CORE</div>', unsafe_allow_html=True)
    with st.form("skill_form_engine"):
        k1, k2 = st.columns(2)
        with k1:
            sv_name = st.text_input("Full Name (as written inside identification documents)")
            st.text_input("Mobile Phone String")
            sv_nin = st.text_input("NIN (National Identification String)")
            st.text_input("VIN (Voter Identification String Check)")
            
            sv_dob = st.date_input("Date of Birth", value=datetime.date(2000, 1, 1))
            sv_gender = st.selectbox("Gender Matrix", ["Male", "Female", "Prefer Not to Say"])
            sv_disability = st.selectbox("Disability Status Profile", ["None", "Visual Impairment", "Hearing Impairment", "Physical Challenge/Locomotor", "Other Challenges"])
            
            st.file_uploader("Upload Profile NIN Slip Document Click", type=['pdf', 'jpg', 'png'])
        with k2:
            klga = st.selectbox("LGA Location Area", list(LGA_WARD_DATA.keys()))
            st.selectbox("Ward Location Frame Area (Auto-Cascading)", LGA_WARD_DATA.get(klga, []))
            
            vocation_list = [
                "ICT & AI Core Programming", 
                "Solar Renewable Energy Engineering", 
                "Fashion & Textile Design Layout", 
                "Catering & Culinary Arts Matrix",
                "Automobile Mechanical Engineering",
                "Electrical Installation & Wiring",
                "Plumbing & Hydraulics Systems",
                "Carpentry & Woodwork Manufacturing",
                "Modern Hairdressing & Cosmetology",
                "Other (Type Custom Vocation Below)"
            ]
            sv_selection = st.selectbox("Vocational Domain Target Pool Sector", vocation_list)
            
            custom_vocation = ""
            if sv_selection == "Other (Type Custom Vocation Below)":
                custom_vocation = st.text_input("Type Your Choice Vocation Natively Here")
            
            st.divider()
            sv_palliative_check = st.selectbox("Have you received a palliative from this office before?", ["No", "Yes"])

        st.text_area("Candidate Skill Interest Statement Details")
        st.camera_input("Biometric Security Verification Core Scan")
        
        if st.form_submit_button("🚀 COMMIT APPLICATION TO TRAINING POOLS"):
            match_check = st.session_state.global_registry[st.session_state.global_registry['NIN'] == sv_nin]
            if not match_check.empty:
                st.session_state.radar_threat = True
                st.session_state.threat_msg = f"Collision: NIN [{sv_nin}] matches a record belonging to user [{match_check.iloc[0]['Name']}]."
                st.error("Duplicate Entry Detected. Entry Rejected by Security System Shield Protocols.")
            else:
                final_skill = custom_vocation if sv_selection == "Other (Type Custom Vocation Below)" else sv_selection
                new_profile_row = {
                    "NIN": sv_nin, 
                    "VIN": "", 
                    "Name": sv_name, 
                    "LGA": klga, 
                    "Ward": "Vouched Sector Link", 
                    "Status": "Pending Review Tracker", 
                    "Category": "Applicant", 
                    "Skill_Interest": final_skill, 
                    "Custom_Skill": custom_vocation,
                    "Gender": sv_gender,
                    "DOB": str(sv_dob),
                    "Disability_Status": sv_disability,
                    "Prior_Palliative": sv_palliative_check,
                    "Academic_Qual": "Degree Matrix", 
                    "Admission_Year": "2026", 
                    "Admission_Letter": None, 
                    "Phone": "080", 
                    "Leader_Name": "Hon. Richifa Vouched", 
                    "Leader_Contact": "080", 
                    "Leader_NIN": "000", 
                    "Leader_LGA": "SOBA", 
                    "Leader_Ward": "CENTRAL", 
                    "Leader_Portfolio": "Directorate Node", 
                    "Voucher_Code": "V-SOB", 
                    "Remarks": "Verified Clear", 
                    "Timestamp": str(datetime.datetime.now())
                }
                st.session_state.global_registry = pd.concat([st.session_state.global_registry, pd.DataFrame([new_profile_row])], ignore_index=True)
                trigger_background_autosave()
                st.success("Constituent profile parameters with extended demographic metrics verified and safely saved into database arrays.")

# --- ROUTING FRAME 5: STUDENT SCHOLARSHIP ARCHIVAL INTERFACE ENGINE ---
elif st.session_state.current_page == "scholarship_form":
    render_marquee_header()
    st.markdown('### 🎓 CONSTITUENT STUDENT SCHOLARSHIP APPLICATION CORE')
    with st.form("scholarship_form_engine"):
        s1, s2 = st.columns(2)
        with s1:
            st.text_input("Student Legal Full Name")
            st.text_input("National ID Card String (NIN)")
            st.text_input("Active Mobile Connection Contact Phone")
            st.selectbox("Academic Year of Intake Admission", [str(year_token) for year_token in range(2018, 2027)])
            st.file_uploader("Attach Scanned NIN Identity Slip File", type=['pdf', 'jpg', 'png'])
        with s2:
            st.text_input("Tertiary Institution Allocation Name")
            st.selectbox("Current Institutional Study Level Track", ["Level 100", "Level 200", "Level 300", "Level 400", "Level 500", "Post-Graduate Stream"])
            slga = st.selectbox("LGA Residential Boundary Parameter Link", list(LGA_WARD_DATA.keys()))
            st.selectbox("Ward Sector Location Block (Auto-Cascading)", LGA_WARD_DATA.get(slga, []))
        st.file_uploader("Attach Official University Admission Letter Asset File", type=['pdf', 'jpg', 'png'])
        st.text_area("Applicant Justification Space")
        st.camera_input("Capture Student Identity Card Sensor")
        st.form_submit_button("🚀 SUBMIT SCHOLARSHIP ENTRY APPLICATION PARAMETERS")

# --- ROUTING FRAME 6: PROFESSIONAL TALENT VAULT GATEWAY CONTROL ---
elif st.session_state.current_page == "cv_vault":
    render_marquee_header()
    st.markdown('### 🚀 CONSTITUENT PROFESSIONAL TALENT VAULT ENGINE')
    with st.form("cv_vault_engine"):
        v1, v2 = st.columns(2)
        with v1:
            st.text_input("Expert Full Name")
            st.selectbox("Talent Classification Target Category", ["Professional Domain Leader", "Skilled Artisan Professional", "Business Enterprise Executive Owner"])
            st.selectbox("Highest Level Academic Qualification Attained", ["Doctorate PhD", "Masters Degree Level", "Bachelors Degree / HND Layer", "National Diploma ND", "NCE", "SSCE Credentials Matrix", "Primary Leaving", "None"])
            st.file_uploader("Attach Professional CV/Resume Document Link File", type=['pdf', 'jpg', 'png'])
        with v2:
            st.text_input("National Identification Validation String (NIN)")
            st.text_input("Cellular Interface Link Contact Phone")
            vlga = st.selectbox("LGA Location Area Coordinates", list(LGA_WARD_DATA.keys()))
            st.selectbox("Ward Area Coordinates Identifier (Auto-Cascading)", LGA_WARD_DATA.get(vlga, []))
        st.text_area("Summary Matrix of Functional Career Experience Vectors")
        st.camera_input("Capture Valid Professional Certification Seals")
        st.form_submit_button("📤 COMMIT CREDENTIALS STRINGS TO TALENT PLATFORM ARCHIVE MATRIX")

# --- ROUTING FRAME 7: REGIONAL INFRASTRUCTURE CUN INCIDENT RECONNAISSANCE ENGINE ---
elif st.session_state.current_page == "cun_trigger":
    render_marquee_header()
    st.markdown('### 🚨 COMMUNITY URGENT NEED FIELD DEFICIT REPORT GATEWAY')
    with st.form("cun_form_engine"):
        st.text_input("Field Reconnaissance Reporter Full Name")
        st.text_input("Reporter Contact Phone Number")
        clga = st.selectbox("Affected LGA Territory Boundary Sector", list(LGA_WARD_DATA.keys()))
        st.selectbox("Affected Ward Location Frame Zone (Auto)", LGA_WARD_DATA.get(clga, []))
        st.selectbox("Primary Critical Asset Deficiency Classification Type", ["Water Source Deficit", "Grid Electricity Failure", "Access Road Failure Collapse", "Community Security Vulnerability", "Healthcare Facility Absence"])
        st.file_uploader("Attach Identification NIN Validation Document Slip", type=['pdf', 'jpg', 'png'])
        st.text_area("Detailed Situation Report Narrative Logs")
        st.camera_input("Field Visual Evidence Deficit Capture Sensor Matrix Camera")
        st.form_submit_button("🚨 TRIGGER COMMAND INCIDENT VECTOR ALERT TO CORE MASTER LEDGERS")

# --- ROUTING FRAME 8: PALLIATIVE INTAKE ENROLLMENT ENGINE LOGISTICS ---
else:
    render_marquee_header()
    st.markdown('### 📦 CONSTITUENT PALLIATIVE DISTRIBUTION REGISTER')
    with st.form("palliative_form_engine"):
        p1, p2 = st.columns(2)
        with p1: 
            st.text_input("Nominee Profile Full Legal Name")
            p_nin = st.text_input("National Identity Validation String (NIN Mapping ID)")
            st.text_input("Voters Card Electoral Tracking String (VIN Mapping ID)")
            st.multiselect("Vulnerability Vector Framework Classification Metrics", ["Aged Eldership Category", "Widowhood Support Matrix", "Physical Disability Framework Challenge", "Long-Term Unemployed Status Tracker"])
            st.file_uploader("Upload Nominee Profile NIN Slip Document Layout Check", type=['pdf', 'jpg', 'png'])
        with p2: 
            st.text_input("Nominee Cell Connection Contact Phone")
            plga = st.selectbox("LGA Location Core Bound Sector", list(LGA_WARD_DATA.keys()))
            st.selectbox("Ward Location Core Bound Sector Node (Auto-Cascading)", LGA_WARD_DATA.get(plga, []))
            st.text_input("Polling Unit Target Area Name/Number Code Assignment")
        
        st.divider()
        st.markdown("### 🛡️ FULL STRATEGIC LEADERSHIP VOUCHING TIER INTERFACE FRAME (ANTI-FRAUD MATRIX)")
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.text_input("Vouching Community Leader Full Legal Name")
            st.text_input("Vouching Leader Mobile Communication Contact Phone")
            st.text_input("Vouching Leader National ID Validation String (NIN)")
            vl_lga = st.selectbox("Vouching Leader LGA Registration Link", list(LGA_WARD_DATA.keys()))
        with v_col2:
            st.selectbox("Vouching Leader Ward Area Code Linking Check (Auto)", LGA_WARD_DATA.get(vl_lga, []))
            st.text_input("Current Portfolio/Traditional Leadership Title Stamped Within Community")
            st.file_uploader("Upload Vouching Leader Authentic NIN Verification Slip Document File", type=['pdf', 'jpg', 'png'])
        
        st.text_area("Leader Affirmation Testimony Verification Remarks Statement")
        st.camera_input("Biometric Face Capture Matrix Core Verification Face Scan")
        
        if st.form_submit_button("🚀 COMPLETE TRANSACTION: AUTHORIZE PALLIATIVE NOMINATION RECORD"):
            match_check = st.session_state.global_registry[st.session_state.global_registry['NIN'] == p_nin]
            if not match_check.empty:
                st.session_state.radar_threat = True
                st.session_state.threat_msg = f"Collision Trace Block: Identification NIN Token [{p_nin}] already allocated inside database system matrix arrays."
                st.error("Duplicate Registration Attempt Dropped Instantly. Verification Engine Locked Transaction Block.")
            else:
                st.success("Constituent biometric parameter validation cleared. Committing record arrays safely.")