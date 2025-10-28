import streamlit as st

st.set_page_config(page_title="Login")
with open("static/login.html", "r", encoding="utf-8") as f:
    html = f.read()
st.components.v1.html(html, height=500, scrolling=True)
