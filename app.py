import streamlit as st
import random
import time
import requests
from bs4 import BeautifulSoup

# 目標網址清單
TARGET_URLS = [
    "https://maps.app.goo.gl/vFUdFkyY4Sfw8bKo7",
    "https://maps.app.goo.gl/baU5xQ847aw4F8hT9",
    "https://maps.app.goo.gl/7yiyyxB75gLKKHUS9",
    "https://maps.app.goo.gl/tBK6GrspDkrLdg1K8",
    "https://maps.app.goo.gl/kJzYjJ6ERxNQfzuS6",
    "https://maps.app.goo.gl/BLFwBtV82SqLifaj8",
    "https://maps.app.goo.gl/Xy9ZTiAKuk3dczQ47",
]

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_restaurant_data(urls):
    """
    爬取網址的 <title> 標籤作為餐廳名稱。
    使用 cache 確保每日 (86400秒) 最多只抓取一次，提升載入速度。
    """
    restaurants = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for idx, url in enumerate(urls):
        try:
            # 設定 timeout 避免單一網址卡死整個應用程式
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')
            
            if title_tag and title_tag.text:
                # 針對 Google Maps 常見的標題格式進行清理
                raw_title = title_tag.text
                clean_name = raw_title.replace(" - Google Maps", "").replace("Google Maps", "").strip()
                name = clean_name if clean_name else f"未命名地點 ({idx})"
            else:
                name = f"無法解析名稱 ({idx})"
                
        except requests.exceptions.RequestException:
            # 處理無效網址或連線失敗的狀況
            name = f"連線失效的餐廳 ({idx})"
            
        restaurants.append({"name": name, "url": url})
        
        # 建立請求間隔，避免觸發反爬蟲機制
        time.sleep(0.5)
        
    return restaurants

def main():
    st.set_page_config(page_title="午餐輪盤", page_icon="🎲")
    st.title("🎲 午餐輪盤：今天吃什麼？")
    
    # 載入資料區塊
    with st.spinner("正在自動連線並抓取餐廳資料，請稍候..."):
        restaurants = fetch_restaurant_data(TARGET_URLS)

    # 狀態管理
    if 'is_spinning' not in st.session_state:
        st.session_state.is_spinning = False

    # 輪盤UI與邏輯
    if st.button("開始轉動輪盤", type="primary", use_container_width=True, disabled=st.session_state.is_spinning):
        st.session_state.is_spinning = True
        
        animation_placeholder = st.empty()
        spin_duration = random.randint(15, 25)
        
        for _ in range(spin_duration):
            temp_choice = random.choice(restaurants)
            animation_placeholder.markdown(f"### 🔄 正在選擇... **{temp_choice['name']}**")
            time.sleep(0.1)

        winner = random.choice(restaurants)
        animation_placeholder.empty() 

        st.success("🎉 決定了！就是這家：")
        st.markdown(f"## 🏆 {winner['name']}")
        st.markdown(f"[📍 點擊此處查看導航]({winner['url']})")
        st.balloons()
        
        st.session_state.is_spinning = False

    # 顯示目前已抓取的餐廳清單供核對
    with st.expander("查看所有候選餐廳資料庫"):
        for r in restaurants:
            st.write(f"- [{r['name']}]({r['url']})")

if __name__ == "__main__":
    main()
