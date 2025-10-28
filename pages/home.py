import streamlit as st
from google import genai
import json, re
from google.genai.types import GenerateContentConfig

# from streamlit_extras.switch_page_button import switch_page


def calculate_incometax(user_income, user_age, user_regime):
    # print("Analyze changes")
    prompt = f"""
    You are given an HTML page that contains all the information about income tax slabs for different age groups. Give only the computed income tax answer in the below JSON format that calculates the income tax based on the user’s age {user_age} and annual income {user_income} and for Regime {user_regime}.
    DONT HAVE TO WRITE ANY CODE OR GIVE ANY EXPLANATION, JUST THE CALCULATED INCOME TAX AMOUNT.
    The HTML page already includes tables or data defining tax slabs for various age categories (e.g., below 60, 60–80, above 80).

    The variables age and income are provided as inputs.

    Your task is to extract the correct tax slab information from the HTML page and compute the total tax payable for the given age and income.

    Display the computed tax amount clearly as output.

    Reply in JSON like this:
    {{"income_tax": ....}}

    """
    client = genai.Client()
    gemini_config = GenerateContentConfig(temperature=0.2)
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt, config=gemini_config
    )
    return response.text


st.title("Income Tax Calcuator")
user_income = st.text_input("Enter your annual income")
user_age = st.text_input("Enter your age")
user_regime = st.text_input(
    "Enter your preferred regime: Old Tax Regime or New Tax Regime"
)
if st.button("Calculate the income tax"):
    tax = calculate_incometax(
        user_income=user_income, user_age=user_age, user_regime=user_regime
    )
    clean = re.sub(r"(?s).*?(\{.*?\}).*", r"\1", tax)
    i_tax = json.loads(clean)
    st.write(f"The calculated income tax is :{i_tax["income_tax"]}")
