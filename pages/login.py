import streamlit as st
import pandas as pd
import hashlib

# st.set_page_config(page_title="Login")
# with open("static/login.html", "r", encoding="utf-8") as f:
#     html = f.read()
# st.components.v1.html(html, height=500, scrolling=True)


def load_users():
    try:
        users_df = pd.read_csv("registration.csv")
        return users_df
    except FileNotFoundError:
        st.error("User data file not found. Please create 'users.csv'.")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest


def authenticate_users(username, password, user_df):
    # hashed_input_password=hash_password(password)

    # user_found=pd.Series([user_df["Username"]==username , user_df["Password"]==password])
    # print(user_df)
    flag = False
    for i, user in user_df.iterrows():
        if (user["Username"] == username) and (user["Password"] == password):
            flag = True
    return flag

    # result = (user_df["Username"] == username) & (user_df["Password"] == password)
    # print(result)
    # if result.bool():
    #     return True
    # else:
    #     return False

    # if user_found.all():
    #     return True
    # else:
    #     return False


st.title("Login")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_df = load_users()
        if authenticate_users(username, password, user_df):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.switch_page("pages/home.py")
        else:
            st.error("Invalid username or password")
            st.switch_page("pages/register.py")
else:
    st.write("You are logged in")
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()
