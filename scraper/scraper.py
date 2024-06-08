import requests
from bs4 import BeautifulSoup

def fetch_score(so_bao_danh):
    # Kiểm tra nếu số báo danh là của thí sinh ảo
    if so_bao_danh == "038205022868":
        # Dữ liệu giả lập cho thí sinh ảo
        mock_data = [
            ["Toán", "8.5"],
            ["Văn", "7.0"],
            ["Anh", "8.0"],
            ["Lý", "7.5"],
            ["Hóa", "8.5"],
            ["Sinh", "6.6"]
        ]
        return mock_data
    
    # Nếu không phải thí sinh ảo, tiếp tục lấy dữ liệu từ trang web
    so_bao_danh = str(so_bao_danh).rjust(8, '0')
    URL = f"https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/2023/{so_bao_danh}.html"
    print(f"Fetching URL: {URL}")
    r = requests.get(URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        target = soup.find('div', class_='resultSearch__right')
        if target:
            table = target.find('tbody')
            if table:
                rows = table.find_all('tr')
                placeHolder = []
                for row in rows:
                    lst = row.find_all('td')
                    cols = [ele.text.strip() for ele in lst]
                    placeHolder.append([ele for ele in cols if ele])
                print(f"Fetched data: {placeHolder}")
                return placeHolder
    
    return "Không tìm thấy kết quả"
