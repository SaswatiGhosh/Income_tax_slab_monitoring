import streamlit as st

pg = st.navigation(
    [
        st.Page("pages/home.py", title="Home", default=True),
        st.Page("pages/login.py", title="Login"),
        # st.page_link("register.html", label="Register", icon="ℹ️"),
    ],
    position="top",
    expanded=False,
)
st.set_page_config(page_title="Income Tax Calcuator")
pg.run()
