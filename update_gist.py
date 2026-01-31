import requests
from bs4 import BeautifulSoup
import re
import base64
import os

# تنظیمات از طریق محیط گیت‌هاب
GIST_ID = os.getenv('GIST_ID')
GIST_TOKEN = os.getenv('GIST_TOKEN')

def get_telegram_configs():
    url = "https://t.me/s/prrofile_purple"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    messages = soup.find_all('div', class_='tgme_widget_message_text')
    
    all_configs = []
    for msg in messages[-5:]:
        text = msg.get_text()
        found = re.findall(r'(vless|vmess|trojan|ss|shadowsocks)://[^\s]+', text)
        all_configs.extend(found)
    
    if not all_configs:
        return None
    return base64.b64encode("\n".join(list(set(all_configs))).encode('utf-8')).decode('utf-8')

def update_gist(content):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    data = {"files": {"sub.txt": {"content": content}}}
    r = requests.patch(url, headers=headers, json=data)
    if r.status_code == 200:
        print("Gist updated successfully!")
    else:
        print(f"Error: {r.status_code}")

new_configs = get_telegram_configs()
if new_configs:
    update_gist(new_configs)
