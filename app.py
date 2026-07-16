import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. ప్రాపర్టీ ఆప్షన్స్
property_options = {
    "Agricultural Land": ["Dry Land", "Gardens (Mango/Coconut etc.)", "Wet Land", "Farm House Land"],
    "Residential Properties": ["Apartment / Flat", "Independent House / Villa", "Row House", "Residential Plot"],
    "Commercial Properties": ["Office Space", "Retail Shops", "Hotel / Restaurant Space", "Warehouse / Godown"],
    "Industrial & Mining": ["Factory / Manufacturing Plant", "Mining Lease Land", "Quarry (Stone/Gravel)", "Industrial Plot"],
    "Specialized Properties": ["Educational Institution Land", "Hospital Space", "Mixed-use (Commercial + Residential)"]
}

# 2. Google Sheets కనెక్షన్
creds_dict = {
    "type": st.secrets["TYPE"], "project_id": st.secrets["PROJECT_ID"],
    "private_key_id": st.secrets["PRIVATE_KEY_ID"],
    "private_key": st.secrets["PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": st.secrets["CLIENT_EMAIL"], "client_id": st.secrets["CLIENT_ID"],
    "auth_uri": st.secrets["AUTH_URI"], "token_uri": st.secrets["TOKEN_URI"],
    "auth_provider_x509_cert_url": st.secrets["AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": st.secrets["CLIENT_X509_CERT_URL"]
}
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1h5sYj5zpUPZj62qaVrnQsjmeI1ozLXILenHwyihpakU').sheet1

st.set_page_config(page_title="Sri Shakti Marketplace", layout="centered")
st.title("🕉️ Sri Shakti Consultancy")
tab1, tab2 = st.tabs(["🏡 Buy Property", "➕ Post Property"])

# --- BUYER SECTION ---
with tab1:
    st.subheader("Available Properties")
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        with st.container(border=True):
            st.write(f"### {row['Property Name']} ({row['Measurements']})")
            st.write(f"💰 Price: {row['Price']} | 🧭 Facing: {row['Facing']}")
            st.write(f"📍 Address: {row['Address']}")
            st.write(f"👤 Contact: {row['Contact Person']} ({row['Role']})")
            
            col1, col2, col3 = st.columns(3)
            if row.get('Media Link'): col1.link_button("📸 Photos", row['Media Link'], use_container_width=True)
            if row.get('Map Link'): col2.link_button("📍 Map", row['Map Link'], use_container_width=True)
            if row.get('Phone Number'): col3.link_button("💬 WhatsApp", f"https://wa.me/91{row['Phone Number']}", use_container_width=True)

# --- SELLER SECTION ---
with tab2:
    st.subheader("Post Your Property")
    with st.form("sell_form", clear_on_submit=True):
        cat = st.selectbox("Property Category", list(property_options.keys()))
        
        # అన్ని టైప్స్ ని ఒకే లిస్టులోకి మార్చడం
        all_types = []
        for types in property_options.values():
            all_types.extend(types)
            
        ptype = st.selectbox("Select Property Type (అన్ని ఆప్షన్లు ఇక్కడ ఉన్నాయి)", all_types)
        prop_title = st.text_input("Property Name")
        
        c1, c2 = st.columns(2)
        mval = c1.text_input("Measurement Value")
        munit = c2.selectbox("Unit", ["Acres", "Cents", "Square Yards", "Square Feet"])
        
        price = st.text_input("Price")
        facing = st.selectbox("Facing", ["East", "West", "North", "South"])
        addr = st.text_area("Address")
        cp = st.text_input("Contact Person")
        role = st.selectbox("Role", ["Property Owner (సొంతదారు)", "Staff / Representative (స్టాఫ్ / ప్రతినిధి)", "Mediator / Agent (మధ్యవర్తి)", "Family Member (కుటుంబ సభ్యుడు)"])
        phone = st.text_input("Phone Number")
        mlink = st.text_input("Media Link")
        maplink = st.text_input("Map Link")
        status = st.selectbox("Status", ["Available", "Sold"])
        
        if st.form_submit_button("Submit Property"):
            full_meas = f"{mval} {munit}"
            sheet.append_row([cat, ptype, prop_title, full_meas, price, facing, addr, cp, role, phone, mlink, maplink, status])
            st.success("Property added successfully!")
