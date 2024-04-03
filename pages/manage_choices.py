import streamlit as st
import get_food

choices_df = get_food.getSheetasDataframe("options")

sh = get_food.getAuth()

worksheet = sh.worksheet('options')

with st.form("my_form", clear_on_submit=True):
    sMeal = st.text_input("Enter Meal", value='')
    sTags = st.text_input("Tags", value='')
    sSource = st.text_input("Enter Source", value='')

    submitted = st.form_submit_button("Submit")

    if submitted:
        worksheet.append_row([sMeal, sTags, sSource], table_range="A1:C1", value_input_option="USER_ENTERED")
        st.text(f"{sMeal} added")

st.dataframe(choices_df)        


# # Get updated dividend df
# update_dividends = st.button("Update Dividend Data", type="primary")
# if update_dividends:
#     with st.spinner('Getting updated dividend data...'):
#         st.session_state['dividends_df'] = get_food.getDividendsDF(st.session_state['dividend_val'])