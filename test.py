from flask import Flask, render_template_string, redirect, url_for
import requests,csv


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

@app.route('/login', methods=['GET','POST'])
def login():
    """Login """
    if requests.method == "POST":
        username= requests.form['username']
        password= requests.form['password']
        
        if validate_credentials(username=username, password=password):
            return redirect(url_for('index'))
def validate_credentials(username, password):
    with open('registration.csv' , 'r') as f:
            reader=csv.reader(f)
            for row in reader:
                if row[0] == username and row[1] == password:
                    return True
            return False



@app.route('/login', methods=['POST'])
def register():
    if register.method =="POST":
        username= requests.form['username']
        email= requests.form['email']
        password= requests.form['password']
        with open("registration.csv" , "w") as f:
            fieldnames=["Name", "Email" , "Password"]
            writer= csv.DictWriter(f, fieldnames)

            if f.tell() ==0:
                writer.writeheader()
            writer.writerow({'Name': username, 'Email': email, 'Password': password})
        return redirect(url_for(login))



if __name__ == '__main__':
    app.run(debug=True)