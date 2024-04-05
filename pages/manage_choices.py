import streamlit as st
import get_food

if not st.session_state['loggedin']:
    st.error("Please return to the meal plan page and log in")

elif st.session_state['loggedin']:
    choices_df = get_food.getSheetasDataframe("options")
    choices_df = choices_df[choices_df['meal'] != ''].sort_values("meal")

    sh = get_food.getAuth()

    worksheet = sh.worksheet('options')

    if st.session_state["userrole"] == 'admin':
        with st.form("my_form", clear_on_submit=True):
            sMeal = st.text_input("Enter Meal", value='')
            sTags = st.text_input("Tags", value='')
            sSource = st.text_input("Enter Source", value='')

            submitted = st.form_submit_button("Submit")

            if submitted:
                worksheet.append_row([sMeal, sTags, sSource], table_range="A1:C1", value_input_option="USER_ENTERED")
                st.text(f"{sMeal} added")

        st.dataframe(choices_df, 
            column_config={"meal": "Dinner Option", 
                "source": st.column_config.LinkColumn("Source")
            },
            use_container_width=True,
            hide_index=True)

    else:

        entered_tags = st.text_input("What kind of meal are you looking for? (only enter one search term at a time)").lower()

        if len(entered_tags) > 0:
            choices_filtered_df = choices_df[choices_df['tags'].str.contains(entered_tags)]
        else:
            choices_filtered_df = choices_df

        st.dataframe(choices_filtered_df[['meal', 'source']], 
            column_config={
                "meal": st.column_config.TextColumn("Dinner Option", width = "small"), 
                "source": st.column_config.LinkColumn("Source", width = "Large")
            },
            use_container_width=True,
            hide_index=True)