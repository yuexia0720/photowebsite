import cloudinary
import cloudinary.api
import cloudinary.uploader

cloudinary.config(
  cloud_name='dpr0pl2tf',
  api_key='548549517251566',
  api_secret='9o-PlPBRQzQPfuVCQfaGrUV3_IE'
)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    image_urls = [
        "https://res.cloudinary.com/dpr0pl2tf/image/upload/v1753816843/WechatIMG2_mzsnw2.jpg",
    ]
    return render_template('index.html', image_urls=image_urls)



@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

if __name__ == "__main__":
    app.run()







