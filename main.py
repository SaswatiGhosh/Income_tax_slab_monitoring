import json, os , requests 
from bs4 import BeautifulSoup
from google import genai

STATE_FILE="state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}



def save_state(state):
    json.dump(state, open(STATE_FILE, 'w'), indent=2)

def fetch_text(url, selector):
    r= requests.get(url, timeout=20, headers={"User_Agent" : "AI_watcher/1.0"})
    r.raise_for_status()
    soup=BeautifulSoup(r.text , "html.parser") ############
    if selector:
        # el= soup.select(selector)
        el= soup.find_all(class_=selector)
        return el
    #     return el.get_text( " ", strip=True) if el else " "
    # return el.get_text(" " , strip= True)

def call_ai(new_txt):
    prompt=f"""
You are given raw HTML scraped from a website.
Your task is to remove all HTML tags and metadata, except tables.
For each table, extract and convert it into clean plain text, keeping:

The same number of rows and columns

Proper spacing or alignment so that each row and column is distinguishable

The original numerical and textual values as they appear

All other elements (scripts, styles, divs, links, headers, paragraphs, etc.) should be completely removed.
Output only the plain text, with tables formatted clearly and neatly for further data analysis. "":
 "{new_txt}"

"""
    client = genai.Client()
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    )
    print(response)

def watch_page( name, url, selector , recipient , use_playwright):
    state=load_state()
    new_txt= fetch_text(url, selector)
    call_ai(new_txt)
    # print(new_txt)
    save_state(state)











if __name__ == "__main__":
    watch_page(
        name="ITR Monitoring",
        url="https://www.incometax.gov.in/iec/foportal/help/individual/return-applicable-1",
        selector ="Table",
        recipient=["saswatititli99@gmail.com"],
        use_playwright= True,
    )
