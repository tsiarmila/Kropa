from flask import Flask, render_template, request
import requests
import smtplib
import datetime as dt
from secret_words import my_mail, password

app = Flask(__name__)
response = requests.get("https://api.npoint.io/fc07c0359fcc06022050")
response.raise_for_status()
all_posts = response.json()

# now = dt.datetime.now()
# print(now)

@app.route("/")
def home():
    return render_template("index.html", posts=all_posts, name='Tsiar Mila')


@app.route("/gallery")
def about():
    return render_template("gallery.html")


def send_msg(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com:587") as connection:
        connection.starttls()
        connection.login(user=my_mail, password=password)
        connection.sendmail(
            from_addr=my_mail,
            to_addrs=my_mail,
            msg=f"Success!\n\nNew contact:\n{name}\n{email}\n{phone}\n{message}"
        )


@app.route("/contact", methods=['POST', "GET"])
def contact():
    text = "Contact Me"
    if request.method == 'POST':
        data = request.form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        text = "Successfully sent your message"
        send_msg(name, email, phone, message)
        return render_template("contact.html", text=text) # or msg_sent=True
    else:
        return render_template("contact.html", text=text) # or msg_sent=False

# in contact.html
# {% if msg_sent: %}
# <h1>Successfully ...</h1>
# {% else: %}
# <h1>Contact me</h1>
# {% endif %}

# @app.route("/contact", methods=['POST'])
# def receive_data():
#     data = request.form
#     name = request.form['name']
#     email = request.form['email']
#     phone = request.form['phone']
#     message = request.form['message']
#     return "<h1>Successfully sent your message</h1>"


@app.route("/post/<int:index>")
def show_post(index):
    title_post = all_posts[index-1]["title"]
    subtitle = all_posts[index-1]["subtitle"]
    text = all_posts[index-1]["body"]
    date = all_posts[index-1]["date"]
    img_url = all_posts[index-1]["img_url"]
    return render_template("post.html", index=index, title=title_post, subtitle=subtitle, text=text, date=date,
                           name='Tsiar Mila', img_url=img_url)


if __name__ == "__main__":
    app.run(debug=True, port=3000) #, host='0.0.0.0' to view on mobile right now

# <p>Top 15 Things to do When You are in Kropa. Are you in Kropa? Don't know what to do? Try these top 15 activities.
# </p>  "subtitle": "Who knew that Kropa lives such interesting life."the country takes an active part in order to preserve primitiveness