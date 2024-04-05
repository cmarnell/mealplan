import streamlit as st
import pandas as pd
import get_food
from st_pages import Page, show_pages, add_page_title
# import streamlit-authenticator as stauth
from datetime import date, timedelta
import datetime
import re

show_pages(
    [
        Page("streamlit_app.py", "Meal Plan", ":knife_fork_plate:"),
        Page("pages/manage_choices.py", "Dinner Options", ":pencil2:"),
    ]
)

# Get some session variables set
actual_password = "pass"
if 'loggedin' not in st.session_state:
	st.session_state['loggedin'] = False
if 'userrole' not in st.session_state:
	st.session_state['userrole'] = 'other'  

# If there is a logged in user, show who in the sidebar
with st.sidebar:
    if st.session_state['loggedin']:
        st.text(f'Welcome {st.session_state["email"]}')

# Do some work with dates
today = date.today()
dtMonday = today - timedelta(days = today.weekday())
dtTuesday = dtMonday + timedelta(1)
dtWednesday = dtMonday + timedelta(2)
dtThursday = dtMonday + timedelta(3)
dtFriday = dtMonday + timedelta(4)
dtSaturday = dtMonday + timedelta(5)
dtSunday = dtMonday + timedelta(6)

# Create an empty container
placeholder = st.empty()

# Create a login form
if not st.session_state['loggedin']:
    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit and password != actual_password:
        st.error("Login failed")
        
    elif submit and password == actual_password:
        users_df = get_food.getSheetasDataframe("users")
        new_email = re.sub(r"\.(?=.*?@gmail\.com)", "", email).lower()

        user_level = users_df[users_df['email'] == new_email]['role'].values[0]
        count = len(users_df[users_df['email'] == new_email])

        st.session_state['userrole'] = user_level

        if count == 0:
            st.error("Login failed")

        elif count > 0:
            # If the form is submitted and the email and password are correct,
            # clear the form/container and display a success message
            st.session_state['loggedin'] = True
            st.session_state['email'] = email

elif st.session_state['loggedin']:
    
    placeholder.empty()

    sh = get_food.getAuth()
    history_worksheet = sh.worksheet('history')

    this_week = [dtMonday.strftime('%m/%d/%Y'), dtTuesday.strftime('%m/%d/%Y'), dtWednesday.strftime('%m/%d/%Y'), dtThursday.strftime('%m/%d/%Y'), dtFriday.strftime('%m/%d/%Y'), dtSaturday.strftime('%m/%d/%Y'), dtSunday.strftime('%m/%d/%Y')]

    history_df = get_food.getSheetasDataframe("history")
    choices_df = get_food.getSheetasDataframe("options").sort_values(by=["meal"])
    requests_df = get_food.getSheetasDataframe("requests")

    if st.session_state['userrole'] == 'admin':
        # Show any meal requests
        if len(requests_df) > 0:
            st.markdown("Current Requests")
            st.dataframe(requests_df)

        # return values from history_df if they already exist
        vMonday = history_df[history_df['date'] == dtMonday.strftime('%m/%d/%Y')]['meal']
        vTuesday = history_df[history_df['date'] == dtTuesday.strftime('%m/%d/%Y')]['meal']
        vWednesday = history_df[history_df['date'] == dtWednesday.strftime('%m/%d/%Y')]['meal']
        vThursday = history_df[history_df['date'] == dtThursday.strftime('%m/%d/%Y')]['meal']
        vFriday = history_df[history_df['date'] == dtFriday.strftime('%m/%d/%Y')]['meal']
        vSaturday = history_df[history_df['date'] == dtSaturday.strftime('%m/%d/%Y')]['meal']
        vSunday = history_df[history_df['date'] == dtSunday.strftime('%m/%d/%Y')]['meal']

        # Use values from above to get the index from the choices dataframe. Will use this to set the default value in the selections if it already exists
        vMonday = choices_df.index.get_loc(choices_df[choices_df['meal'] == vMonday.values[0]].index[0]) if len(vMonday) > 0 else 0
        vTuesday = choices_df.index.get_loc(choices_df[choices_df['meal'] == vTuesday.values[0]].index[0]) if len(vTuesday) > 0 else 0
        vWednesday = choices_df.index.get_loc(choices_df[choices_df['meal'] == vWednesday.values[0]].index[0]) if len(vWednesday) > 0 else 0
        vThursday = choices_df.index.get_loc(choices_df[choices_df['meal'] == vThursday.values[0]].index[0]) if len(vThursday) > 0 else 0
        vFriday = choices_df.index.get_loc(choices_df[choices_df['meal'] == vFriday.values[0]].index[0]) if len(vFriday) > 0 else 7
        vSaturday = choices_df.index.get_loc(choices_df[choices_df['meal'] == vSaturday.values[0]].index[0]) if len(vSaturday) > 0 else 7
        vSunday = choices_df.index.get_loc(choices_df[choices_df['meal'] == vSunday.values[0]].index[0]) if len(vSunday) > 0 else 0

        with st.form("menu_form"): #, clear_on_submit=True):
            sMonday = st.selectbox(f"Monday {dtMonday}", choices_df.meal.unique(), index=vMonday)
            sTuesday = st.selectbox(f"Tuesday {dtTuesday}", choices_df.meal.unique(), index=vTuesday)
            sWednesday = st.selectbox(f"Wednesday {dtWednesday}", choices_df.meal.unique(), index=vWednesday)
            sThursday = st.selectbox(f"Thursday {dtThursday}", choices_df.meal.unique(), index=vThursday)
            sFriday = st.selectbox(f"Friday {dtFriday}", choices_df.meal.unique(), index=vFriday)
            sSaturday = st.selectbox(f"Saturday {dtSaturday}", choices_df.meal.unique(), index=vSaturday)
            sSunday = st.selectbox(f"Sunday {dtSunday}", choices_df.meal.unique(), index=vSunday)
            
            submitted = st.form_submit_button("Submit")

            if submitted:
                meal_list = [[dtMonday, sMonday], [dtTuesday, sTuesday], [dtWednesday, sWednesday], [dtThursday, sThursday], [dtFriday, sFriday], [dtSaturday, sSaturday], [dtSunday, sSunday]]
                history_worksheet.clear()
                for meal in meal_list:
                    # Only do this if a meal has been selected
                    if meal[1]:
                        # Check to see if there is already a meal planned for this day
                        df = history_df[history_df['date'] == meal[0].strftime('%m/%d/%Y')]
                        # only update the spreadsheet if there isn't already a value selected for that day
                        if len(df.index) < 1:
                            st.text(f"adding {meal[0].strftime('%m/%d/%Y')} {meal[1]}")
                            history_df.loc[len(history_df.index)+1] = [meal[0].strftime('%m/%d/%Y'), meal[1]]
                        else:
                            # update if there is already a meal for the day
                            st.text(f"updating {meal[0].strftime('%m/%d/%Y')} {meal[1]}")
                            history_df.loc[history_df['date'] == meal[0].strftime('%m/%d/%Y'), 'meal'] = meal[1]
                        
                        # rewrite the datasheet with a new version once we are done
                        history_df = history_df.sort_values(by='date')
                        history_worksheet.update([history_df.columns.values.tolist()] + history_df.values.tolist())

                st.text(f'Monday: {sMonday}\nTuesday: {sTuesday}\nWednesday: {sWednesday}\nThursday: {sThursday}\nFriday: {sFriday}\nSaturday: {sSaturday}\nSunday: {sSunday}')

#  Display the below if it isn't me logging in
    if st.session_state['userrole'] != 'admin':
        mask = history_df['date'].isin(this_week)
        this_week_df = history_df[mask]
        st.markdown("Planned meals for this week:")
        st.dataframe(this_week_df, hide_index=True)  

        request_worksheet = sh.worksheet('requests')

        with st.form("meal_requests", clear_on_submit=True):
            request_date = date.today()
            who = st.session_state["email"]
            meal = st.selectbox("Request dinner for this week", choices_df.meal.unique())

            submitted = st.form_submit_button("Submit")

            if submitted:
                request_worksheet.clear()
                requests_df.loc[len(requests_df.index)+1] = [who, meal, request_date] # .strftime('%m/%d/%Y')
                
                requests_df['request_date'] = pd.to_datetime(requests_df['request_date'], format='%Y-%m-%d') # format='%m/%d/%Y')
                requests_df = requests_df[requests_df['request_date'].dt.date > date.today() - timedelta(14)]
                requests_df['request_date'] = requests_df['request_date'].dt.strftime('%Y-%m-%d')

                requests_df = requests_df.sort_values(by='request_date')
                
                request_worksheet.update([requests_df.columns.values.tolist()] + requests_df.values.tolist())


            # requests_df['request_date'] = pd.to_datetime(requests_df['request_date'], format='%m/%d/%Y')

        st.markdown("Current Requests")
        st.dataframe(requests_df)