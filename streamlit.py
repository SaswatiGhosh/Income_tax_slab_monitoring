import streamlit as st

pg = st.navigation(
    [
        st.Page("pages/home.py", title="Home", default=True),
        st.Page("pages/login.py", title="Login"),
        st.Page("pages/register.py", title="Register"),
    ],
    position="top",
    expanded=False,
)
st.set_page_config(page_title="Income Tax Calcuator")
pg.run()
