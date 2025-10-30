import pdfkit
import pdfplumber
import requests
import hashlib, os, json, re
from google import genai
from email.message import EmailMessage
import smtplib
import streamlit as st

SUBSCRIBE_FILE = "subscribe.csv"

STATE_FILE = "state.json"


def load_subscribers():
    try:
        subscribers_df = pd.read_csv(SUBSCRIBE_FILE)
        return subscribers_df
    except FileNotFoundError:
        st.error("User data file not found. Please create 'users.csv'.")


def generate_256sha(res):
    encoded_data = res.encode("utf-8")
    sha256_hash_object = hashlib.sha256()
    sha256_hash_object.update(encoded_data)
    return sha256_hash_object.hexdigest()


def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}


def save_state(hashed_value):
    with open(STATE_FILE, "w") as f:
        json.dump(hashed_value, f, indent=2)


def analyze_change(old_text, new_text):
    # print("Analyze changes")
    prompt = f"""You are monitoring a website for meaningful updates.

    Old version:
    {old_text}

    New version:
    {new_text}
    Mainly focus on the tables below the text span:
    1. Tax rates for Individual (resident or non-resident) less than 60 years of age anytime during the previous year are as under:
    2.Tax rates for Individual (resident or non-resident), 60 years or more but less than 80 years of age anytime during the previous year are as under:
    3.Tax rates for Individual (resident or non-resident) 80 years of age or more anytime during the previous year are as under:

    Compare the two texts and describe:
    1. What changed (in one short sentence)
    2. Whether this change seems important (rate 1–5, where 5 is very important)

    Reply in JSON like this:
    {{"summary": "...", "importance": 4}}

    """
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    res = response.text
    clean = re.sub(r"(?s).*?(\{.*?\}).*", r"\1", res)
    print(clean)
    x = json.loads(clean)
    print(x)

    return x["summary"], x["importance"]


def html_to_pdf(url):

    path_wkthmltopdf = r"C:\Program Files\wkhtmltox\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    res = requests.get(url).text

    filename = "income_tax_page.html"

    # 1. Remove tags that load or execute external resources
    res = re.sub(r"<script[^>]*>.*?</script>", "", res, flags=re.IGNORECASE | re.DOTALL)
    res = re.sub(r"<iframe[^>]*>.*?</iframe>", "", res, flags=re.IGNORECASE | re.DOTALL)
    res = re.sub(
        r"<noscript[^>]*>.*?</noscript>", "", res, flags=re.IGNORECASE | re.DOTALL
    )
    res = re.sub(r"<object[^>]*>.*?</object>", "", res, flags=re.IGNORECASE | re.DOTALL)
    res = re.sub(r"<embed[^>]*>.*?</embed>", "", res, flags=re.IGNORECASE | re.DOTALL)
    res = re.sub(r"<source[^>]*>.*?</source>", "", res, flags=re.IGNORECASE | re.DOTALL)
    res = re.sub(r"<video[^>]*>.*?</video>", "", res, flags=re.IGNORECASE | re.DOTALL)
    res = re.sub(r"<audio[^>]*>.*?</audio>", "", res, flags=re.IGNORECASE | re.DOTALL)

    # 2. Remove self-closing resource tags
    res = re.sub(r"<link[^>]*?>", "", res, flags=re.IGNORECASE)
    res = re.sub(r"<meta[^>]*?>", "", res, flags=re.IGNORECASE)
    res = re.sub(r"<img[^>]*?>", "", res, flags=re.IGNORECASE)

    # 3. Remove problematic attributes (href, src, JS events, etc.)
    res = re.sub(
        r'\s+(href|src|srcset|data-src|prefix)\s*=\s*["\'][^"\']*["\']',
        "",
        res,
        flags=re.IGNORECASE,
    )
    res = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', "", res, flags=re.IGNORECASE)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(res)
    print(f"res file '{filename}' created successfully.")

    # print(res)
    options = {"load-error-handling": "ignore", "load-media-error-handling": "ignore"}
    # url = "http://127.0.0.1:5000/"
    output_pdf = "income_tax_page.pdf"
    # pdfkit.from_url(url, output_pdf, configuration=config, options=options)
    pdfkit.from_file(filename, output_pdf, configuration=config)

    with pdfplumber.open(output_pdf) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        print(text)

        tables = first_page.extract_tables()
        l = []
        for table in tables:
            for row in table:
                print(row)
    return res


def send_email(subject, body, recipients):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("FROM_EMAIL")
    msg["To"] = recipients
    msg.set_content(body)

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as smtp:
        smtp.starttls()
        smtp.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        smtp.send_message(msg)


if __name__ == "__main__":
    url = "http://127.0.0.1:5000/"
    res = html_to_pdf(url)
    # print("Done")
    hashed_value = generate_256sha(res)
    x = load_state()
    subs = load_subscribers()
    if x == {}:
        store_hash = {"hash_val": hashed_value, "content": res}
        save_state(store_hash)
    else:
        if x["hash_val"] != hashed_value:
            summary, importance = analyze_change(x["content"], res)
            if importance >= 4:
                for index, sub in subs.iterrows():
                    name = "Income tax Department"
                    recipients = sub["Email"]
                    body = (
                        f"Change detected for {sub["Username"]}\n\n"
                        f"URL : url \n\n"
                        f"AI Analysis: \n {summary}"
                    )
                    send_email(f"[Alert] {sub["Username"]}", body, recipients)
                    print(f"[{sub["Username"]}] Notification sent with AI summary.")
                store_hash = {"hash_val": hashed_value, "content": res}
                save_state(store_hash)
            else:
                print("No changes . We are good!!!")
