# For register page and add it to navigation
import streamlit as st
import os
import pandas as pd

CSV_FILE = "registration.csv"


def load_users():
    try:
        users_df = pd.read_csv(CSV_FILE)
        return users_df
    except FileNotFoundError:
        st.error("User data file not found. Please create 'users.csv'.")


def save_user_data(username, email, password):
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Username", "Email", "Password"])
        df.to_csv(CSV_FILE)

    dataframe = pd.read_csv(CSV_FILE)
    data = [[username, email, password]]
    new_user_data = pd.DataFrame(data, columns=["Username", "Email", "Password"])
    df = pd.concat([dataframe, new_user_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)


st.title("User Registration")
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")
# submit_button = st.form_submit_button("Register")

if st.button("Register"):
    data_sheet = load_users()
    if username in data_sheet["Username"].values:
        st.error("Username already exists. Please choose a different username.")
    elif email in data_sheet["Email"].values:
        st.error("Email already exists. Please choose a different Email.")
    elif password == confirm_password:
        if username and email and password:
            save_user_data(username, email, password)
            st.switch_page("pages/login.py")
            st.success("Registration successful.Please login")
        else:
            st.error("Please fill in all fields.")
    else:
        st.error("Passwords do not match.")
