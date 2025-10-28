# For register page and add it to navigation
import streamlit as st
import os,pandas

CSV_FILE="registration.csv"
def save_user_data(username, email,password):
    if not os.path.exists(CSV_FILE):
        df=pandas.DataFrame(columns=['Username', 'Email','Password'])
        df.to_csv(CSV_FILE)
    
    pd=pandas.read_csv(CSV_FILE)
    data=[[username ,email, password]]
    new_user_data=pandas.DataFrame(data,columns=['Username','Email','Password'])
    df=pandas.concat([new_user_data], ignore_index=True)
    df.to_csv(CSV_FILE,index=False)



st.title("User Registration")
username= st.text_input("Username")
email=st.text_input("Email")
password=st.text_input("Password",type='password')
confirm_password = st.text_input("Confirm Password", type='password')
# submit_button = st.form_submit_button("Register")

if st.button("Register"):
    if password == confirm_password:
        if username and email and password:
            save_user_data(username, email, password)
            st.success("Registration successful.Please login")
        else:
            st.error("Please fill in all fields.")
    else:
        st.error("Passwords do not match.")
