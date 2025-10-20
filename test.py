from flask import Flask, render_template_string
import requests


def fetch_webpage(target_url):
    try:
        res=requests.get(target_url)
        res.raise_for_status()
        new_text= res.text.replace(r"<p><span><span><span>5% above ₹ 3,00,000</span></span></span></p>", r"<p><span><span><span>25% above ₹ 3,00,000</span></span></span></p>")
        return new_text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
app= Flask(__name__)

@app.route('/')
def index():
    """Renders the main page with a form to create a new Flask app."""
    target_url="https://www.incometax.gov.in/iec/foportal/help/individual/return-applicable-1"
    html_content=fetch_webpage(target_url)
    return render_template_string(html_content)


if __name__ == '__main__':
    app.run(debug=True)