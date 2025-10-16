import json, os, requests
from bs4 import BeautifulSoup
from google import genai

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
    soup = BeautifulSoup(r.text, "html.parser")  ############
    if selector:
        # el= soup.select(selector)
        el = soup.find_all(class_=selector)
        return el
    #     return el.get_text( " ", strip=True) if el else " "
    # return el.get_text(" " , strip= True)


def call_ai(new_txt):
    prompt = f"""
Formatting requirements:
- Keep line breaks, spacing, and indentation similar to how the text would visually appear.
- For <table>, <tr>, <td>, <th> tags:
  - Remove the tags but keep the table structure aligned in a readable text format.
  - Each table row should be on a new line.
  - Separate table columns using tabs or consistent spaces.
- For lists (<ul>, <ol>, <li>), preserve the bullet/numbering structure.
- Preserve headings and their spacing.
- Do NOT include any HTML tags, attributes, or inline styles.
- Do NOT summarize or rewrite—only clean and format the text as described.
- Below is the raw HTML content to be formatted:
 "{new_txt}"

"""
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    print(response)


def watch_page(name, url, selector, recipient, use_playwright):
    state = load_state()
    new_txt = fetch_text(url, selector)
    call_ai(new_txt)
    state[name] = new_txt
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
