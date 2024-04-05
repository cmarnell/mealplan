import streamlit as st
import get_food
from datetime import date, timedelta
import pandas as pd

requests_df = get_food.getSheetasDataframe("requests")
choices_df = get_food.getSheetasDataframe("options")
choices_df = choices_df[choices_df['meal'] != ''].sort_values("meal")

sh = get_food.getAuth()

worksheet = sh.worksheet('requests')

with st.form("meal_requests", clear_on_submit=True):
    request_date = date.today()
    who = st.session_state["email"]
    meal = st.selectbox("Meal", choices_df.meal.unique())

    submitted = st.form_submit_button("Submit")

    if submitted:
        requests_df.loc[len(requests_df.index)+1] = [who, meal, request_date] # .strftime('%m/%d/%Y')
        
        requests_df['request_date'] = pd.to_datetime(requests_df['request_date'], format='%Y-%m-%d') # format='%m/%d/%Y')
        requests_df = requests_df[requests_df['request_date'].dt.date > date.today() - timedelta(14)]
        requests_df['request_date'] = requests_df['request_date'].dt.strftime('%Y-%m-%d')

        requests_df = requests_df.sort_values(by='request_date')
        
        worksheet.update([requests_df.columns.values.tolist()] + requests_df.values.tolist())


    # requests_df['request_date'] = pd.to_datetime(requests_df['request_date'], format='%m/%d/%Y')

st.markdown("Current Requests")
st.dataframe(requests_df)
