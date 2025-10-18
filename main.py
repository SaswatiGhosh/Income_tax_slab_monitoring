import json, os, requests
from bs4 import BeautifulSoup
from google import genai
import pandas as pd


STATE_FILE = "state.json"


def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}


def save_state(state):
    json.dump(state, open(STATE_FILE, "w"), indent=2)


def fetch_text(url, selector):
    r = requests.get(url, timeout=20, headers={"User_Agent": "AI_watcher/1.0"})
    r.raise_for_status()
    # soup = BeautifulSoup(r.text, "html.parser")  ############
    # if selector:
    #     # el= soup.select(selector)
    #     el = soup.find_all(class_=selector)
    #     if selector:
    #     # el= soup.select(selector)
    #         el = soup.find_all(class_=selector)
    #     return el
    soup= BeautifulSoup(r.text, "lxml")
    tables= soup.find_all(class_= selector)
    for i,table in  enumerate(tables, start=1):
        html_table=str(table)
        with open(f"table_{i}.html",'w', encoding="utf-8") as f:
            f.write(html_table)


   




def call_ai(new_txt):
    prompt = f"""
You will be given HTML content. Your job is to remove ALL HTML tags and return ONLY the visible text content.

Very important instructions:
- DO NOT return any code (no Python, no pseudocode, no regex, no explanations).
- DO NOT describe how to do it.
- DO NOT wrap the output in code blocks.
- Only return the cleaned text.

Formatting requirements:
1. Preserve indentation and visual structure of the text.
2. For tables (<table>, <tr>, <td>, <th>):
   - Remove all tags but keep the text in a readable table layout.
   - Each row on a new line.
   - Separate columns with tabs or consistent spaces.
3. For lists (<ul>, <ol>, <li>):
   - Keep bullets or numbering.
4. Preserve headings and line breaks.
5. Don't summarize, rephrase, or add commentary.

Your output must be ONLY the cleaned text with correct indentation. Do not include HTML, code, or explanations.
 "{new_txt}"

"""
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    print(response.text)
    return response.text


def watch_page(name, url, selector, recipient, use_playwright):
    state = load_state()
    new_txt = fetch_text(url, selector)
    # updated_txt = call_ai(new_txt)
    # state[name] = updated_txt
    # print(new_txt)
    save_state(state)


if __name__ == "__main__":
    watch_page(
        name="ITR Monitoring",
        url="https://www.incometax.gov.in/iec/foportal/help/individual/return-applicable-1",
        selector="Table",
        recipient=["saswatititli99@gmail.com"],
        use_playwright=True,
    )
