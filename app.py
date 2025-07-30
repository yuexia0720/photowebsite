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
    # 获取 Cloudinary 中 "photowebsite/" 文件夹下的所有图片
    resources = cloudinary.api.resources(type="upload", prefix="photowebsite/", max_results=30)
    image_urls = [img['secure_url'] for img in resources['resources']]
    return render_template('index.html', image_urls=image_urls)


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

if __name__ == "__main__":
    app.run()







