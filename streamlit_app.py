import streamlit as st
import pandas as pd
import get_food
from st_pages import Page, show_pages, add_page_title
# import streamlit-authenticator as stauth
from datetime import date, timedelta
import datetime

show_pages(
    [
        Page("streamlit_app.py", "Meal Plan", ":knife_fork_plate:"),
        Page("pages/manage_choices.py", "Dinner Options", ":pencil2:"),
    ]
)

sh = get_food.getAuth()

worksheet = sh.worksheet('history')

cell = worksheet.find("03/26/2024")

# st.text(f"cell: {cell}")

# Do some work with dates
today = date.today()
dtMonday = today - timedelta(days = today.weekday())
dtTuesday = dtMonday + timedelta(1)
dtWednesday = dtMonday + timedelta(2)
dtThursday = dtMonday + timedelta(3)
dtFriday = dtMonday + timedelta(4)
dtSaturday = dtMonday + timedelta(5)
dtSunday = dtMonday + timedelta(6)

# st.text(f"Monday {dtMonday.strftime('%m/%d/%Y')}")

this_week = [dtMonday.strftime('%m/%d/%Y'), dtTuesday.strftime('%m/%d/%Y'), dtWednesday.strftime('%m/%d/%Y'), dtThursday.strftime('%m/%d/%Y'), dtFriday.strftime('%m/%d/%Y'), dtSaturday.strftime('%m/%d/%Y'), dtSunday.strftime('%m/%d/%Y')]

history_df = get_food.getSheetasDataframe("history")
choices_df = get_food.getSheetasDataframe("options")

testing_email = 'test@email.com'

st.text(st.experimental_user["email"])

# TODO change this to st.experimental_user
# If this user is not me, just show them the meal plan
if testing_email != 'test@email.com':
    mask = history_df['date'].isin(this_week)
    this_week_df = history_df[mask]
    st.dataframe(this_week_df, hide_index=True)

# if the user is me, give meal plan selector
if testing_email == 'test@email.com':
# st.experimental_user["email"]
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

    with st.form("menu_form", clear_on_submit=True):
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
            worksheet.clear()
            for meal in meal_list:
                # mealplan_df = pd.DataFrame(columns=['Date', 'Meal'])
                # Only do this if a meal has been selected
                if meal[1]:
                    # mealplan_df.loc[len(mealplan_df.index)] = [meal[0], meal[1]]  
                      
                    df = history_df[history_df['date'] == meal[0].strftime('%m/%d/%Y')]
                    # only update the spreadsheet if there isn't already a value selected for that day
                    if len(df.index) < 1:
                        st.text(f"adding {meal[0].strftime('%m/%d/%Y')} {meal[1]}")
                        history_df.loc[len(history_df.index)+1] = [meal[0].strftime('%m/%d/%Y'), meal[1]]
                        st.dataframe(history_df)
                        # worksheet.append_row([meal[0].strftime('%m/%d/%Y'), meal[1]], table_range="A1:B1", value_input_option="USER_ENTERED")
                    else:
                        st.text(f"updating {meal[0].strftime('%m/%d/%Y')} {meal[1]}")
                        history_df.loc[history_df['date'] == meal[0].strftime('%m/%d/%Y'), 'meal'] = meal[1]
                        st.dataframe(history_df)
                    
                    history_df = history_df.sort_values(by='date')
                    worksheet.update([history_df.columns.values.tolist()] + history_df.values.tolist())

            # st.text(f'Monday: {sMonday}\nTuesday: {sTuesday}\nWednesday: {sWednesday}\nThursday: {sThursday}\nFriday: {sFriday}\nSaturday: {sSaturday}\nSunday: {sSunday}')

            # st.dataframe(mealplan_df)

            # st.dataframe(history_df)

           