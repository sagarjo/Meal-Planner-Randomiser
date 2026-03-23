import streamlit as st
from streamlit_gsheets import GSheetsConnection
import random
import pandas as pd

st.set_page_config(page_title="Cloud Meal Planner", layout="wide")

# --- 1. CONNECTION ---
# In your .streamlit/secrets.toml, you'll put your Google Sheet URL
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60) # Refreshes every minute
# Temporary modification to debug the connection
def get_data():
    try:
        # Setting ttl=0 forces a fresh read every time
        options_df = conn.read(worksheet="Options", ttl=0)
        plan_df = conn.read(worksheet="CurrentPlan", ttl=0)
        return options_df, plan_df
    except Exception as e:
        st.error(f"Spreadsheet Error: {e}")
        return pd.DataFrame(), pd.DataFrame()

options_df, plan_df = get_data()

st.title("☁️ Cloud-Synced Meal Planner")

# --- 3. SIDEBAR: EDIT MASTER LIST ---
with st.sidebar:
    st.header("Master Meal List")
    st.write("Edit your options here:")
    # This creates an editable table inside your app!
    edited_options = st.data_editor(options_df, num_rows="dynamic", key="opt_editor")
    
    if st.button("Update Cloud Options"):
        conn.update(worksheet="Options", data=edited_options)
        st.success("Synced to Google Sheets!")

# --- 4. MAIN: RANDOMIZER ---
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

if st.button("🎲 Generate & Sync New Weekly Plan"):
    new_rows = []
    for day in days:
        # Filter options by category from the dataframe
        b_pool = edited_options[edited_options['Category'] == 'Breakfast']['Item'].tolist()
        l_pool = edited_options[edited_options['Category'] == 'Lunch']['Item'].tolist()
        d_pool = edited_options[edited_options['Category'] == 'Dinner']['Item'].tolist()
        
        new_rows.append({
            "Day": day,
            "Breakfast": random.choice(b_pool) if b_pool else "N/A",
            "Lunch": random.choice(l_pool) if l_pool else "N/A",
            "Dinner": random.choice(d_pool) if d_pool else "N/A"
        })
    
    new_plan_df = pd.DataFrame(new_rows)
    conn.update(worksheet="CurrentPlan", data=new_plan_df)
    st.cache_data.clear() # Force reload from the sheet
    st.rerun()

# --- 5. DISPLAY CURRENT PLAN ---
st.subheader("This Week's Schedule")
latest_plan = conn.read(worksheet="CurrentPlan")

# Display as interactive cards using columns
cols = st.columns(7)
for i, row in latest_plan.iterrows():
    with cols[i]:
        st.markdown(f"**{row['Day']}**")
        st.info(f"🍳 {row['Breakfast']}\n\n🍱 {row['Lunch']}\n\n🍽️ {row['Dinner']}")
      
