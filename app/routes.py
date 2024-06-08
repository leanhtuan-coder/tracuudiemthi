from flask import render_template, request, jsonify, send_from_directory
from app import app
from scraper.scraper import fetch_score
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    so_bao_danh = request.args.get('soBaoDanh')
    result = fetch_score(so_bao_danh)
    return jsonify({'result': result})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
