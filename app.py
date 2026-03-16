import streamlit as st
import random
import time

# 餐廳資料（名稱 + Google Maps 連結）
RESTAURANTS = [
    {"name": "好厝邊精緻早午餐", "url": "https://maps.app.goo.gl/vFUdFkyY4Sfw8bKo7"},
    {"name": "食超飽", "url": "https://maps.app.goo.gl/baU5xQ847aw4F8hT9"},
    {"name": "阿木當歸鴨麵線", "url": "https://maps.app.goo.gl/7yiyyxB75gLKKHUS9"},
    {"name": "早喚 Morning Call", "url": "https://maps.app.goo.gl/tBK6GrspDkrLdg1K8"},
    {"name": "三分鐘熱度", "url": "https://maps.app.goo.gl/kJzYjJ6ERxNQfzuS6"},
    {"name": "萬佳鄉板橋店", "url": "https://maps.app.goo.gl/BLFwBtV82SqLifaj8"},
    {"name": "厚呷樂咖喱", "url": "https://maps.app.goo.gl/Xy9ZTiAKuk3dczQ47"},
]

# 每家店一個顏色
COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", "#F7DC6F", "#BB8FCE"]


def main():
    st.set_page_config(page_title="午餐輪盤", page_icon="🎰", layout="centered")

    # 注入 CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap');

    .roulette-title {
        text-align: center;
        font-family: 'Noto Sans TC', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
    }
    .roulette-subtitle {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* 輪盤外框 */
    .wheel-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem auto;
        position: relative;
        width: 320px;
        height: 320px;
    }
    .wheel {
        width: 300px;
        height: 300px;
        border-radius: 50%;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 0 8px #333, 0 0 0 11px #fff, 0 0 30px rgba(0,0,0,0.3);
        transition: transform 4s cubic-bezier(0.17, 0.67, 0.12, 0.99);
    }
    .wheel-center {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 40px;
        height: 40px;
        background: #333;
        border-radius: 50%;
        z-index: 10;
        box-shadow: 0 0 0 4px #fff;
    }

    /* 指針 */
    .pointer {
        position: absolute;
        top: -18px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 0;
        border-left: 15px solid transparent;
        border-right: 15px solid transparent;
        border-top: 30px solid #FF4444;
        z-index: 20;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }

    /* 跑馬燈式的選擇動畫 */
    .slot-machine {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        margin: 1rem auto;
        max-width: 400px;
    }
    .slot-item {
        width: 100%;
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        text-align: center;
        font-family: 'Noto Sans TC', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: white;
        transition: all 0.15s;
    }
    .slot-active {
        transform: scale(1.08);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .slot-dim {
        opacity: 0.3;
        transform: scale(0.95);
    }

    /* 結果卡片 */
    .winner-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin: 1.5rem auto;
        max-width: 420px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        animation: popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    @keyframes popIn {
        0% { transform: scale(0.5); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    .winner-card h1 {
        font-family: 'Noto Sans TC', sans-serif;
        font-size: 2rem;
        margin: 0.5rem 0;
    }
    .winner-card .emoji {
        font-size: 3rem;
    }
    .winner-card a {
        display: inline-block;
        margin-top: 1rem;
        padding: 0.6rem 1.5rem;
        background: rgba(255,255,255,0.2);
        color: white;
        text-decoration: none;
        border-radius: 30px;
        font-weight: 700;
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    .winner-card a:hover {
        background: rgba(255,255,255,0.35);
    }

    /* 候選清單 */
    .restaurant-list {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    .restaurant-chip {
        padding: 0.5rem 0.8rem;
        border-radius: 8px;
        text-align: center;
        font-family: 'Noto Sans TC', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # 標題
    st.markdown('<div class="roulette-title">🎰 午餐輪盤</div>', unsafe_allow_html=True)
    st.markdown('<div class="roulette-subtitle">選擇困難症救星 — 讓命運決定今天吃什麼</div>', unsafe_allow_html=True)

    # 顯示所有候選餐廳（彩色方塊）
    cols_html = ""
    for i, r in enumerate(RESTAURANTS):
        color = COLORS[i % len(COLORS)]
        cols_html += f'<div class="restaurant-chip" style="background:{color};">{r["name"]}</div>'

    st.markdown(f'<div class="restaurant-list">{cols_html}</div>', unsafe_allow_html=True)
    st.markdown("")

    # 狀態初始化
    if "winner" not in st.session_state:
        st.session_state.winner = None

    # 轉盤按鈕
    if st.button("🎰 轉動輪盤！", type="primary", use_container_width=True):
        st.session_state.winner = None
        placeholder = st.empty()
        n = len(RESTAURANTS)

        # 動畫：逐格高亮，速度由快到慢
        total_steps = random.randint(20, 35)
        current = random.randint(0, n - 1)

        for step in range(total_steps):
            current = (current + 1) % n
            # 漸慢效果
            delay = 0.05 + (step / total_steps) * 0.25

            items_html = ""
            for i, r in enumerate(RESTAURANTS):
                color = COLORS[i % len(COLORS)]
                if i == current:
                    items_html += f'<div class="slot-item slot-active" style="background:{color};">▶ {r["name"]}</div>'
                else:
                    items_html += f'<div class="slot-item slot-dim" style="background:{color};">{r["name"]}</div>'

            placeholder.markdown(
                f'<div class="slot-machine">{items_html}</div>',
                unsafe_allow_html=True
            )
            time.sleep(delay)

        # 最終結果
        winner = RESTAURANTS[current]
        st.session_state.winner = winner

        placeholder.markdown(
            f"""
            <div class="winner-card">
                <div class="emoji">🎉</div>
                <div style="font-size:1rem; opacity:0.8;">今天就決定吃</div>
                <h1>{winner['name']}</h1>
                <a href="{winner['url']}" target="_blank">📍 開啟 Google Maps 導航</a>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.balloons()

    # 如果已經有結果但頁面 rerun，顯示上次結果
    elif st.session_state.winner:
        winner = st.session_state.winner
        st.markdown(
            f"""
            <div class="winner-card">
                <div class="emoji">🎉</div>
                <div style="font-size:1rem; opacity:0.8;">今天就決定吃</div>
                <h1>{winner['name']}</h1>
                <a href="{winner['url']}" target="_blank">📍 開啟 Google Maps 導航</a>
            </div>
            """,
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
