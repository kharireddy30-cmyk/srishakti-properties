import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. ప్రాపర్టీ ఆప్షన్స్ డిక్షనరీ
property_options = {
    "Agricultural Land": ["Dry Land", "Gardens (Mango/Coconut etc.)", "Wet Land", "Farm House Land"],
    "Residential Properties": ["Apartment / Flat", "Independent House / Villa", "Row House", "Residential Plot"],
    "Commercial Properties": ["Office Space", "Retail Shops", "Hotel / Restaurant Space", "Warehouse / Godown"],
    "Industrial & Mining": ["Factory / Manufacturing Plant", "Mining Lease Land", "Quarry (Stone/Gravel)", "Industrial Plot"],
    "Specialized Properties": ["Educational Institution Land", "Hospital Space", "Mixed-use (Commercial + Residential)"]
}

# 2. Google Sheets కనెక్షన్
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

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet_id = '1h5sYj5zpUPZj62qaVrnQsjmeI1ozLXILenHwyihpakU'
sheet = client.open_by_key(sheet_id).sheet1

st.set_page_config(page_title="Sri Shakti Marketplace", layout="centered")
st.title("🕉️ Sri Shakti Consultancy")

tab1, tab2 = st.tabs(["🏡 Buy Property", "➕ Post Property"])

# --- BUYER SECTION ---
with tab1:
    st.subheader("Available Properties")
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if not df.empty:
        for index, row in df.iterrows():
            with st.container(border=True):
                st.write(f"### {row['Property Name']} ({row['Measurements']})")
                st.write(f"💰 Price: {row['Price']} | 🧭 Facing: {row['Facing']}")
                st.write(f"📍 Address: {row['Address']}")
                st.write(f"👤 Contact: {row['Contact Person']} ({row['Role']})")
                # మరిన్ని వివరాల బటన్లు...
    else:
        st.info("No properties found.")

# --- SELLER SECTION ---
with tab2:
    st.subheader("Post Your Property")
    with st.form("sell_form", clear_on_submit=True):
        cat = st.selectbox("Property Category", list(property_options.keys()))
        prop_type = st.selectbox("Property Type", property_options[cat])
        prop_title = st.text_input("Property Name")
        
        col1, col2 = st.columns(2)
        dim_val = col1.text_input("Measurement Value")
        dim_unit = col2.selectbox("Unit", ["Acres", "Cents", "Square Yards", "Square Feet"])
        
        price = st.text_input("Price")
        facing = st.selectbox("Facing", ["East", "West", "North", "South"])
        address = st.text_area("Address")
        
        c_name = st.text_input("Name of the Contact Person")
        role = st.selectbox("Role / Relationship", ["Property Owner (సొంతదారు)", "Staff / Representative (స్టాఫ్ / ప్రతినిధి)", "Mediator / Agent (మధ్యవర్తి)", "Family Member (కుటుంబ సభ్యుడు)"])
        phone = st.text_input("Phone Number")
        
        m_link = st.text_input("Google Drive Folder Link")
        map_link = st.text_input("Google Maps Link")
        status = st.selectbox("Status", ["Available", "Sold"])
        
        if st.form_submit_button("Submit Property"):
            full_meas = f"{dim_val} {dim_unit}"
            # కాలమ్స్ ఆర్డర్: Cat, Type, Name, Meas, Price, Facing, Addr, Contact, Role, Phone, Media, Map, Status
            sheet.append_row([cat, prop_type, prop_title, full_meas, price, facing, address, c_name, role, phone, m_link, map_link, status])
            st.success("Property added successfully!")
