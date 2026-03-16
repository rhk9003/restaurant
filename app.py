import streamlit as st
import streamlit.components.v1 as components
import json
import math

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

COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", "#F7DC6F", "#BB8FCE"]


def build_wheel_html(restaurants, colors):
    """產生完整的 HTML/CSS/JS 輪盤元件"""
    data_json = json.dumps(restaurants, ensure_ascii=False)
    colors_json = json.dumps(colors)
    n = len(restaurants)
    slice_deg = 360 / n

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Noto Sans TC', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: transparent;
    overflow-x: hidden;
  }}

  h1 {{
    font-size: 2.2rem;
    font-weight: 900;
    margin: 0.8rem 0 0.2rem;
    text-align: center;
  }}
  .subtitle {{
    color: #999;
    font-size: 0.95rem;
    margin-bottom: 1.2rem;
    text-align: center;
  }}

  /* ====== 輪盤主體 ====== */
  .wheel-wrapper {{
    position: relative;
    width: 370px;
    height: 370px;
    margin: 0 auto;
  }}

  /* 指針 (頂部朝下) */
  .pointer {{
    position: absolute;
    top: -8px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 30;
    width: 0; height: 0;
    border-left: 16px solid transparent;
    border-right: 16px solid transparent;
    border-top: 36px solid #E74C3C;
    filter: drop-shadow(0 3px 6px rgba(0,0,0,0.35));
  }}

  /* 外圈裝飾 */
  .outer-ring {{
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    border-radius: 50%;
    background: conic-gradient(
      from 0deg,
      #555 0deg 5deg, #ddd 5deg 10deg,
      #555 10deg 15deg, #ddd 15deg 20deg,
      #555 20deg 25deg, #ddd 25deg 30deg,
      #555 30deg 35deg, #ddd 35deg 40deg,
      #555 40deg 45deg, #ddd 45deg 50deg,
      #555 50deg 55deg, #ddd 55deg 60deg,
      #555 60deg 65deg, #ddd 65deg 70deg,
      #555 70deg 75deg, #ddd 75deg 80deg,
      #555 80deg 85deg, #ddd 85deg 90deg,
      #555 90deg 95deg, #ddd 95deg 100deg,
      #555 100deg 105deg, #ddd 105deg 110deg,
      #555 110deg 115deg, #ddd 115deg 120deg,
      #555 120deg 125deg, #ddd 125deg 130deg,
      #555 130deg 135deg, #ddd 135deg 140deg,
      #555 140deg 145deg, #ddd 145deg 150deg,
      #555 150deg 155deg, #ddd 155deg 160deg,
      #555 160deg 165deg, #ddd 165deg 170deg,
      #555 170deg 175deg, #ddd 175deg 180deg,
      #555 180deg 185deg, #ddd 185deg 190deg,
      #555 190deg 195deg, #ddd 195deg 200deg,
      #555 200deg 205deg, #ddd 205deg 210deg,
      #555 210deg 215deg, #ddd 215deg 220deg,
      #555 220deg 225deg, #ddd 225deg 230deg,
      #555 230deg 235deg, #ddd 235deg 240deg,
      #555 240deg 245deg, #ddd 245deg 250deg,
      #555 250deg 255deg, #ddd 255deg 260deg,
      #555 260deg 265deg, #ddd 265deg 270deg,
      #555 270deg 275deg, #ddd 275deg 280deg,
      #555 280deg 285deg, #ddd 285deg 290deg,
      #555 290deg 295deg, #ddd 295deg 300deg,
      #555 300deg 305deg, #ddd 305deg 310deg,
      #555 310deg 315deg, #ddd 315deg 320deg,
      #555 320deg 325deg, #ddd 325deg 330deg,
      #555 330deg 335deg, #ddd 335deg 340deg,
      #555 340deg 345deg, #ddd 345deg 350deg,
      #555 350deg 355deg, #ddd 355deg 360deg
    );
    box-shadow: 0 8px 40px rgba(0,0,0,0.25);
  }}

  /* Canvas 輪盤 */
  canvas#wheel {{
    position: absolute;
    top: 12px; left: 12px;
    width: 346px; height: 346px;
    border-radius: 50%;
    transition: transform 4.5s cubic-bezier(0.15, 0.60, 0.08, 1.00);
  }}

  /* 中心鈕 */
  .center-btn {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 72px; height: 72px;
    border-radius: 50%;
    background: linear-gradient(135deg, #E74C3C, #C0392B);
    border: 4px solid #fff;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    color: white;
    font-weight: 900;
    font-size: 0.85rem;
    cursor: pointer;
    z-index: 20;
    display: flex;
    align-items: center;
    justify-content: center;
    letter-spacing: 1px;
    user-select: none;
    font-family: 'Noto Sans TC', sans-serif;
  }}
  .center-btn:hover {{
    background: linear-gradient(135deg, #c0392b, #a93226);
  }}
  .center-btn:active {{
    transform: translate(-50%, -50%) scale(0.95);
  }}
  .center-btn.disabled {{
    opacity: 0.5;
    cursor: not-allowed;
  }}

  /* ====== 結果卡片 ====== */
  .result-card {{
    margin-top: 1.5rem;
    padding: 1.8rem 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    text-align: center;
    max-width: 400px;
    width: 90%;
    box-shadow: 0 12px 40px rgba(102,126,234,0.45);
    animation: popUp 0.6s cubic-bezier(0.68,-0.55,0.265,1.55);
    display: none;
  }}
  .result-card.show {{ display: block; }}
  @keyframes popUp {{
    0%   {{ transform: scale(0.4); opacity: 0; }}
    100% {{ transform: scale(1);   opacity: 1; }}
  }}
  .result-card .big-emoji {{ font-size: 2.8rem; }}
  .result-card .label {{ font-size: 0.95rem; opacity: 0.8; margin-top: 0.3rem; }}
  .result-card .winner-name {{ font-size: 1.8rem; font-weight: 900; margin: 0.4rem 0; }}
  .result-card a {{
    display: inline-block;
    margin-top: 0.8rem;
    padding: 0.55rem 1.6rem;
    background: rgba(255,255,255,0.2);
    color: #fff;
    text-decoration: none;
    border-radius: 30px;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.35);
    backdrop-filter: blur(4px);
    transition: background 0.2s;
  }}
  .result-card a:hover {{ background: rgba(255,255,255,0.35); }}

  /* 🎊 confetti */
  .confetti-container {{
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 9999;
    overflow: hidden;
  }}
  .confetti {{
    position: absolute;
    width: 10px; height: 10px;
    opacity: 0;
    animation: confettiFall 3s ease-out forwards;
  }}
  @keyframes confettiFall {{
    0%   {{ opacity: 1; transform: translateY(-10px) rotate(0deg); }}
    100% {{ opacity: 0; transform: translateY(105vh) rotate(720deg); }}
  }}
</style>
</head>
<body>

<h1>🎰 午餐輪盤</h1>
<p class="subtitle">選擇困難症救星 — 按下中間按鈕，讓命運決定！</p>

<div class="wheel-wrapper">
  <div class="pointer"></div>
  <div class="outer-ring"></div>
  <canvas id="wheel" width="692" height="692"></canvas>
  <div class="center-btn" id="spinBtn" onclick="spin()">SPIN</div>
</div>

<div class="result-card" id="resultCard">
  <div class="big-emoji">🎉</div>
  <div class="label">今天就決定吃</div>
  <div class="winner-name" id="winnerName"></div>
  <a id="winnerLink" href="#" target="_blank">📍 開啟 Google Maps 導航</a>
</div>

<script>
const restaurants = {data_json};
const colors = {colors_json};
const N = restaurants.length;
const sliceDeg = 360 / N;

// ===== 畫輪盤 =====
const canvas = document.getElementById('wheel');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;
const cx = W / 2, cy = H / 2, R = W / 2 - 2;

function drawWheel() {{
  for (let i = 0; i < N; i++) {{
    const startAngle = (i * sliceDeg - 90) * Math.PI / 180;
    const endAngle   = ((i + 1) * sliceDeg - 90) * Math.PI / 180;

    // 扇形
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, R, startAngle, endAngle);
    ctx.closePath();
    ctx.fillStyle = colors[i % colors.length];
    ctx.fill();

    // 分隔線
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // 文字
    const midAngle = (startAngle + endAngle) / 2;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(midAngle);
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#fff';
    ctx.shadowColor = 'rgba(0,0,0,0.5)';
    ctx.shadowBlur = 4;

    const name = restaurants[i].name;
    const fontSize = name.length > 6 ? 20 : 24;
    ctx.font = '900 ' + fontSize + 'px "Noto Sans TC", sans-serif';

    // 沿著半徑方向寫字（放在 60% 半徑處）
    ctx.fillText(name, R * 0.58, 0);
    ctx.restore();
  }}

  // 內圈陰影
  const grd = ctx.createRadialGradient(cx, cy, R * 0.05, cx, cy, R);
  grd.addColorStop(0, 'rgba(0,0,0,0.12)');
  grd.addColorStop(0.3, 'rgba(0,0,0,0)');
  grd.addColorStop(1, 'rgba(0,0,0,0.08)');
  ctx.beginPath();
  ctx.arc(cx, cy, R, 0, Math.PI * 2);
  ctx.fillStyle = grd;
  ctx.fill();
}}
drawWheel();

// ===== 旋轉邏輯 =====
let currentRotation = 0;
let spinning = false;

function spin() {{
  if (spinning) return;
  spinning = true;
  document.getElementById('spinBtn').classList.add('disabled');
  document.getElementById('resultCard').classList.remove('show');

  // 隨機選一個 winner index
  const winnerIdx = Math.floor(Math.random() * N);

  // 計算目標角度：
  // 指針在 12 點鐘方向 (top)，輪盤順時針轉
  // 讓 winner 的扇形中心對準 12 點鐘
  const winnerMidDeg = winnerIdx * sliceDeg + sliceDeg / 2;
  // 需要旋轉到 360 - winnerMidDeg 才能對準頂部指針
  const targetStop = 360 - winnerMidDeg;
  // 加上多圈 (5~8 圈) 讓它轉得夠久
  const extraSpins = (5 + Math.floor(Math.random() * 4)) * 360;
  const totalRotation = currentRotation + extraSpins + (targetStop - (currentRotation % 360) + 360) % 360;

  canvas.style.transform = 'rotate(' + totalRotation + 'deg)';
  currentRotation = totalRotation;

  // 轉完後顯示結果
  setTimeout(() => {{
    const winner = restaurants[winnerIdx];
    document.getElementById('winnerName').textContent = winner.name;
    document.getElementById('winnerLink').href = winner.url;
    document.getElementById('resultCard').classList.add('show');
    spinning = false;
    document.getElementById('spinBtn').classList.remove('disabled');
    launchConfetti();
  }}, 4800);
}}

// ===== 🎊 Confetti =====
function launchConfetti() {{
  const container = document.createElement('div');
  container.className = 'confetti-container';
  document.body.appendChild(container);

  const confettiColors = ['#FF6B6B','#4ECDC4','#45B7D1','#FFA07A','#F7DC6F','#BB8FCE','#667eea','#E74C3C','#2ECC71'];
  for (let i = 0; i < 80; i++) {{
    const c = document.createElement('div');
    c.className = 'confetti';
    c.style.left = Math.random() * 100 + '%';
    c.style.background = confettiColors[Math.floor(Math.random() * confettiColors.length)];
    c.style.animationDelay = Math.random() * 1.5 + 's';
    c.style.width = (6 + Math.random() * 8) + 'px';
    c.style.height = (6 + Math.random() * 8) + 'px';
    c.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
    container.appendChild(c);
  }}
  setTimeout(() => container.remove(), 4500);
}}
</script>
</body>
</html>
"""


def main():
    st.set_page_config(page_title="午餐輪盤", page_icon="🎰", layout="centered")

    # 隱藏 Streamlit 預設元素，讓畫面更乾淨
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {display: none;}
    [data-testid="stDecoration"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

    # 嵌入完整的輪盤 HTML 元件
    wheel_html = build_wheel_html(RESTAURANTS, COLORS)
    components.html(wheel_html, height=750, scrolling=False)


if __name__ == "__main__":
    main()
