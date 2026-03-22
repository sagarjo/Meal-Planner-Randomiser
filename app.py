import streamlit as st
import random

st.set_page_config(page_title="Weekly Meal Randomizer", page_icon="🥗")

st.title("🥗 Weekly Meal Planner")
st.write("Input your meal options below, separated by commas.")

# 1. User Inputs
with st.sidebar:
    st.header("Meal Database")
    b_input = st.text_area("Breakfast Options", "Oats, Eggs, Poha, Smoothie")
    l_input = st.text_area("Lunch Options", "Chicken Salad, Dal Rice, Paneer Wrap")
    d_input = st.text_area("Dinner Options", "Soup, Stir Fry, Grilled Fish, Pasta")

# Convert strings to lists
breakfasts = [i.strip() for i in b_input.split(',')]
lunches = [i.strip() for i in l_input.split(',')]
dinners = [i.strip() for i in d_input.split(',')]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# 2. Randomizer Button
if st.button("🎲 Generate New Weekly Plan"):
    plan = {}
    for day in days:
        plan[day] = {
            "B": random.choice(breakfasts),
            "L": random.choice(lunches),
            "D": random.choice(dinners)
        }
    # Save to session state so it stays visible until we click again
    st.session_state['weekly_plan'] = plan

# 3. Display the Plan
if 'weekly_plan' in st.session_state:
    cols = st.columns(7) # Create 7 columns for the 7 days
    
    plan = st.session_state['weekly_plan']
    
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"**{day}**")
            st.caption(f"🍳 {plan[day]['B']}")
            st.caption(f"🍱 {plan[day]['L']}")
            st.caption(f"🍽️ {plan[day]['D']}")
