from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

app = Flask(__name__)

# 配置 Cloudinary
cloudinary.config(
    cloud_name='dpr0pl2tf',
    api_key='548549517251566',
    api_secret='9o-PlPBRQzQPfuVCQfaGrUV3_IE'
)

# 首页
@app.route('/')
def index():
    main_image_url = "https://res.cloudinary.com/dpr0pl2tf/image/upload/v1754343393/pexels-caio-69969_aq5kzz.jpg"
    return render_template('index.html', main_image_url=main_image_url)

@app.route('/about')
def about():
    about_image_url = "https://res.cloudinary.com/dpr0pl2tf/image/upload/v1754343392/pexels-samuel-walker-15032-569098_wm1kxg.jpg"
    return render_template('about.html', about_image_url=about_image_url)

# 存储所有故事
@app.route('/story', methods=['GET', 'POST'])
def story():
    if request.method == 'POST':
        image = request.files['image']
        caption = request.form.get('caption')
        result = cloudinary.uploader.upload(image, folder='story')
        image_url = result['secure_url']
        with open('story_data.txt', 'a') as f:
            f.write(f"{image_url}|{caption}\n")
    stories = []
    if os.path.exists('story_data.txt'):
        with open('story_data.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    stories.append({'url': parts[0], 'caption': parts[1]})
    return render_template('story.html', stories=stories)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    message = ''
    if request.method == 'POST':
        folder = request.form['folder']
        image = request.files['image']
        try:
            cloudinary.uploader.upload(image, folder=f'albums/{folder}')
            message = '上传成功！'
        except Exception as e:
            message = f'上传失败: {str(e)}'
    return render_template('upload.html', message=message)

@app.route('/album')
def album():
    try:
        # 获取 albums/ 下所有资源，获取所有文件夹名称
        result = cloudinary.api.resources(type='upload', prefix='albums/', resource_type='image')
        albums = set()
        for item in result['resources']:
            folder = item['public_id'].split('/')[1] if '/' in item['public_id'] else 'default'
            albums.add(folder)
        return render_template('albums.html', albums=sorted(list(albums)))
    except Exception as e:
        return f"Error fetching albums: {e}"

@app.route('/album/<album_name>')
def view_album(album_name):
    try:
        prefix = f"albums/{album_name}/"
        result = cloudinary.api.resources(type='upload', prefix=prefix, resource_type='image')
        image_urls = [item['secure_url'] for item in result['resources']]
        return render_template('view_album.html', album_name=album_name, image_urls=image_urls)
    except Exception as e:
        return f"Error fetching album images: {e}"

if __name__ == '__main__':
    app.run(debug=True)








