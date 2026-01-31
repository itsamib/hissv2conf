import requests
from bs4 import BeautifulSoup
import re
import base64
import os

GIST_ID = os.getenv('GIST_ID')
GIST_TOKEN = os.getenv('GIST_TOKEN')

def get_telegram_configs():
    # استفاده از نسخه Preview تلگرام
    url = "https://t.me/s/prrofile_purple"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج تمام پیام‌ها
        messages = soup.find_all('div', class_='tgme_widget_message_text')
        
        raw_text = ""
        # بررسی ۵ پیام آخر برای جمع‌آوری متن
        for msg in messages[-5:]:
            # حذف اینترهای اضافی که لینک را خراب می‌کنند
            raw_text += msg.get_text(separator=' ').replace('\n', '') + " "

        # Regex هوشمند برای استخراج لینک‌های کامل (حتی با کاراکترهای خاص در هشتگ)
        pattern = r'(?:vless|vmess|trojan|ss)://[^\s<>"]+'
        configs = re.findall(pattern, raw_text)
        
        if not configs:
            print("No configs found!")
            return None
            
        # حذف تکراری‌ها
        unique_configs = []
        for c in configs:
            if c not in unique_configs:
                unique_configs.append(c)
        
        print(f"Found {len(unique_configs)} configs.")
        
        # ترکیب و تبدیل به Base64
        combined_configs = "\n".join(unique_configs)
        encoded_sub = base64.b64encode(combined_configs.encode('utf-8')).decode('utf-8')
        return encoded_sub

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def update_gist(content):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    data = {"files": {"sub.txt": {"content": content}}}
    r = requests.patch(url, headers=headers, json=data)
    if r.status_code == 200:
        print("Gist updated successfully on GitHub!")
    else:
        print(f"Failed to update Gist: {r.status_code}")

# اجرا
encoded_data = get_telegram_configs()
if encoded_data:
    update_gist(encoded_data)
