from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)

# Cấu hình session với Retry để khắc phục hiện tượng chặn truy cập
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

def Crawl_THPTQG(so_bao_danh):
    so_bao_danh = str(so_bao_danh).rjust(8, '0')
    URL = f"https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/2023/{so_bao_danh}.html"
    r = session.get(URL)
    if r.status_code != 404:
        soup = BeautifulSoup(r.content, 'html.parser')
        target = soup.find('div', attrs={'class': 'resultSearch__right'})
        table = target.find('tbody')
        rows = table.find_all('tr')
        placeHolder = []
        for row in rows:
            lst = row.find_all('td')
            cols = [ele.text.strip() for ele in lst]
            placeHolder.append([ele for ele in cols if ele])
        content = [so_bao_danh, placeHolder]
    else:
        return None
    return content

@app.route('/search', methods=['GET'])
def search():
    so_bao_danh = request.args.get('soBaoDanh')
    province = request.args.get('province')

    if not so_bao_danh or not province:
        return jsonify({"error": "Vui lòng nhập số báo danh và chọn tỉnh/thành phố"}), 400

    result = Crawl_THPTQG(so_bao_danh)
    if result:
        return jsonify({"result": result[1]})
    else:
        return jsonify({"error": "Không tìm thấy điểm thi cho số báo danh này"}), 404

if __name__ == "__main__":
    app.run(debug=True)
