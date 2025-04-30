import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
st.set_page_config(layout="wide")


# === Auto-refresh every 5 minutes (300 seconds) ===
st_autorefresh(interval=300_000, key="auto_refresh")

# === Google Sheet settings ===
creds_path = "lcy3-plc-data.json"
sheet_name = "Data Monitor"
# worksheet_name = "plc_1_min"

# === Load data from Google Sheets ===
@st.cache_data(ttl=300)  # cache for 5 minutes to match auto-refresh
def load_data_min(sheet):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Directly access Streamlit secrets and parse them as JSON
    credentials_dict = st.secrets["gcp"] 
    
    # Authenticate using the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(sheet)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    # Ensure 'Value' is numeric
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df.dropna(subset=["Serialization", "Value"], inplace=True)
    
    return df

# === Load data from Google Sheets ===
@st.cache_data(ttl=60*30)  # cache for 5 minutes to match auto-refresh
def load_data_hour(sheet):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Directly access Streamlit secrets and parse them as JSON
    credentials_dict = st.secrets["gcp"] 
    
    # Authenticate using the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(sheet)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    # Ensure 'Value' is numeric
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df.dropna(subset=["Serialization", "Value"], inplace=True)
    
    return df

# === Load data from Google Sheets ===
@st.cache_data(ttl=60*60)  # cache for 5 minutes to match auto-refresh
def load_data_day(sheet):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Directly access Streamlit secrets and parse them as JSON
    credentials_dict = st.secrets["gcp"] 
    
    # Authenticate using the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(sheet)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    # Ensure 'Value' is numeric
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df.dropna(subset=["Serialization", "Value"], inplace=True)
    
    return df

# === Streamlit layout ===
st.title("🔧 Induct Data Monitor 🚀")
st.caption("Auto-refreshes every 5 minutes. You can also trigger a manual refresh below.")

# === Manual Refresh Button ===
if st.button("🔄 Manual Refresh"):
    st.cache_data.clear()
    st.rerun()

# === Load and display data ===
df_min_plc_1 = load_data_min("plc_1_min")
df_hour_plc_1 = load_data_hour("plc_1_hour")
df_day_plc_1 = load_data_day("plc_1_day")
# === Load and display data ===
df_min_plc_2 = load_data_min("plc_2_min")
df_hour_plc_2 = load_data_hour("plc_2_hour")
df_day_plc_2 = load_data_day("plc_2_day")

tabs_1, tabs_2 = st.tabs(['Induct 105','Induct 106'])

# Inject CSS for styling the tabs
st.markdown(
    """
    <style>
    div[data-baseweb="tab-list"] button {
        flex: 1 !important;
        font-size: 80px !important;
        justify-content: center !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with tabs_1:
    # Show numbers at each point and use color to differentiate (optional: based on category or series name)
    fig_1 = px.line(df_min_plc_2, x="Serialization", y="Value", markers=True, title="Minute View",
                    text="Value")  # shows value on hover and on the chart

    fig_2 = px.line(df_hour_plc_2, x="Serialization", y="Value", markers=True, title="Hourly View",
                    text="Value")

    fig_3 = px.line(df_day_plc_2, x="Serialization", y="Value", markers=True, title="Daily View",
                    text="Value")

    # Optionally adjust appearance of the text
    fig_1.update_traces(textposition="top center", line=dict(color="royalblue"))
    fig_2.update_traces(textposition="top center", line=dict(color="seagreen"))
    fig_3.update_traces(textposition="top center", line=dict(color="indianred"))

    # Display in Streamlit
    st.plotly_chart(fig_1, use_container_width=True, key='11')
    st.plotly_chart(fig_2, use_container_width=True, key='21')
    st.plotly_chart(fig_3, use_container_width=True, key='31')
    
with tabs_2:
    
    # Show numbers at each point and use color to differentiate (optional: based on category or series name)
    fig_1 = px.line(df_min_plc_1, x="Serialization", y="Value", markers=True, title="Minute View",
                    text="Value")  # shows value on hover and on the chart

    fig_2 = px.line(df_hour_plc_1, x="Serialization", y="Value", markers=True, title="Hourly View",
                    text="Value")

    fig_3 = px.line(df_day_plc_1, x="Serialization", y="Value", markers=True, title="Daily View",
                    text="Value")

    # Optionally adjust appearance of the text
    fig_1.update_traces(textposition="top center", line=dict(color="royalblue"))
    fig_2.update_traces(textposition="top center", line=dict(color="seagreen"))
    fig_3.update_traces(textposition="top center", line=dict(color="indianred"))

    # Display in Streamlit
    st.plotly_chart(fig_1, use_container_width=True, key='1')
    st.plotly_chart(fig_2, use_container_width=True, key='2')
    st.plotly_chart(fig_3, use_container_width=True, key='3')
    
    
