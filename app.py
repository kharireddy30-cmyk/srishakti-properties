import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Streamlit Secrets నుండి వివరాలను డిక్షనరీగా క్రియేట్ చేయడం
# ఇది ఫైల్ తో సంబంధం లేకుండా నేరుగా పనిచేస్తుంది
creds_dict = {
    "type": st.secrets["TYPE"],
    "project_id": st.secrets["PROJECT_ID"],
    "private_key_id": st.secrets["PRIVATE_KEY_ID"],
    "private_key": st.secrets["PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": st.secrets["CLIENT_EMAIL"],
    "client_id": st.secrets["CLIENT_ID"],
    "auth_uri": st.secrets["AUTH_URI"],
    "token_uri": st.secrets["TOKEN_URI"],
    "auth_provider_x509_cert_url": st.secrets["AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": st.secrets["CLIENT_X509_CERT_URL"]
}

# Google Sheets Setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet_id = '1h5sYj5zpUPZj62qaVrnQsjmeI1ozLXILenHwyihpakU'
sheet = client.open_by_key(sheet_id).sheet1

st.set_page_config(page_title="Sri Shakti Marketplace", layout="centered")

st.title("🕉️ Sri Shakti Consultancy")
st.markdown("---")

tab1, tab2 = st.tabs(["🏡 Buy Property", "➕ Post Property"])

# --- BUYER SECTION ---
with tab1:
    st.subheader("Available Properties")
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    if not df.empty:
        search_query = st.text_input("🔍 Search...")
        if search_query:
            mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
            df = df[mask]
        
        for index, row in df.iterrows():
            status_color = "🟢" if row.get('Status', 'Available') == 'Available' else "🔴"
            with st.container(border=True):
                st.write(f"### {row['Property Name']} {status_color}")
                st.write(f"💰 Price: {row['Price']} | 🧭 Facing: {row['Facing']}")
                st.write(f"📍 Location: {row['Location']}")
                
                col1, col2, col3 = st.columns(3)
                if row['Media Link']: col1.link_button("📸 Photos", row['Media Link'], use_container_width=True)
                if row['Map Link']: col2.link_button("📍 Map", row['Map Link'], use_container_width=True)
                if row['Phone Number']:
                    wa_link = f"https://wa.me/91{row['Phone Number']}"
                    col3.link_button("💬 WhatsApp", wa_link, use_container_width=True)
    else:
        st.info("No properties found.")

# --- SELLER SECTION ---
with tab2:
    st.subheader("Post Your Property")
    with st.form("sell_form", clear_on_submit=True):
        prop_title = st.text_input("Property Name")
        price = st.text_input("Price")
        facing = st.selectbox("Facing", ["East", "West", "North", "South"])
        location = st.text_input("Location")
        owner = st.text_input("Owner Name")
        phone = st.text_input("Phone Number")
        media_link = st.text_input("Google Drive Folder Link")
        map_link = st.text_input("Google Maps Link")
        status = st.selectbox("Status", ["Available", "Sold"])
        
        submit = st.form_submit_button("Submit Property", use_container_width=True)
        if submit:
            sheet.append_row([prop_title, price, facing, location, owner, phone, media_link, map_link, status])
            st.success("Property added successfully!")
