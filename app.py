from datetime import date, datetime, timedelta
import streamlit as st
import pandas as pd


st.set_page_config(
   page_title="AIO 22 Schedule",
   page_icon="🗓️",
#    layout="wide",
#    initial_sidebar_state="expanded",
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

today = date.today()
sheet_id = "1n3Iz8aYFgurnZf_Z8rhNEbXmtotgrBGRiSJP_FJHFNA"
sheet_name = "LOG"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url).iloc[:,3:]
df["THỜI GIAN"] = pd.to_datetime(df["THỜI GIAN"], format="%d/%m/%Y %H:%M:%S")
df.sort_values(by="THỜI GIAN", inplace=True, ascending=True)

def render_task(row):
    _date = row["THỜI GIAN"].strftime("%a, %d/%m/%y")
    _task = row["CÔNG VIỆC"]
    _person = row["ĐẢM NHẬN"]
    _url = row["LINK"]
    return f"[{_date}] **{_task}** - *{_person}* → [Link Classroom]({_url})"


st.title("LOG AIO 2022")
st.write(f'Today: {today.strftime("%a, %d/%m/%y")}')

st.header("Trong 14 ngày nữa:")
with st.expander("Show/hide", expanded=True):

    from_date = today
    to_date  = today +  timedelta(days=14)

    df_14d = df[(df["THỜI GIAN"].dt.date >= today) & (df["THỜI GIAN"].dt.date <= to_date)]
    for idx, row in df_14d.iterrows():
        text = render_task(row)
        st.markdown(text)

st.header("Đã qua:")
with st.expander("Show/hide", expanded=False):
    df_past = df[(df["THỜI GIAN"].dt.date < today)][::-1]
    for idx, row in df_past.iterrows():
        text = render_task(row)
        st.markdown(text)