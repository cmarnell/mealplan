import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

skey = st.secrets["sheets_account"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=scopes,
)

def getAuth():
    # gc = gspread.service_account(credentials)
    gc = gspread.authorize(credentials)

    return gc.open_by_key("1XlngATA9zcyEpi7bZMVSL7tyQliGlj0rgfDfvRI5cfc")

def getSheetasDataframe(worksheetName="history"):
    sh = getAuth()
    worksheet = sh.worksheet(worksheetName)
    
    df = pd.DataFrame(worksheet.get_values('A:C', value_render_option='FORMATTED_VALUE'))
    # set first row as headers
    df.columns = df.iloc[0]
    #remove first row from DataFrame
    df = df[1:]
    
    return df
