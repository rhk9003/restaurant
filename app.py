import streamlit as st
import streamlit.components.v1 as components
import json

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
    """產生完整的 HTML/CSS/JS 輪盤元件（含首次同意彈窗）"""
    data_json = json.dumps(restaurants, ensure_ascii=False)
    colors_json = json.dumps(colors)

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

  /* ====== 同意彈窗 ====== */
  .overlay {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(8px);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.4s ease;
  }}
  .overlay.hidden {{ display: none; }}
  @keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
  }}
  .consent-card {{
    background: #fff;
    border-radius: 24px;
    padding: 2.5rem 2rem;
    max-width: 380px;
    width: 90%;
    text-align: center;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    animation: scaleIn 0.5s cubic-bezier(0.68,-0.55,0.265,1.55);
  }}
  @keyframes scaleIn {{
    from {{ transform: scale(0.5); opacity: 0; }}
    to {{ transform: scale(1); opacity: 1; }}
  }}
  .consent-card .icon {{ font-size: 3.5rem; margin-bottom: 0.8rem; }}
  .consent-card h2 {{
    font-size: 1.5rem;
    font-weight: 900;
    color: #333;
    margin-bottom: 0.6rem;
  }}
  .consent-card p {{
    font-size: 1.05rem;
    color: #555;
    line-height: 1.7;
    margin-bottom: 1.5rem;
  }}
  .consent-card .oath {{
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 1.1rem;
    font-weight: 700;
    color: #E74C3C;
    margin-bottom: 1.5rem;
    border: 2px dashed #E74C3C;
  }}
  .consent-btn {{
    background: linear-gradient(135deg, #E74C3C, #C0392B);
    color: #fff;
    border: none;
    padding: 0.9rem 3rem;
    font-size: 1.2rem;
    font-weight: 900;
    border-radius: 50px;
    cursor: pointer;
    font-family: 'Noto Sans TC', sans-serif;
    box-shadow: 0 6px 20px rgba(231,76,60,0.4);
    transition: all 0.2s;
  }}
  .consent-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(231,76,60,0.5);
  }}
  .consent-btn:active {{
    transform: translateY(0);
  }}

  /* ====== 違規確認彈窗 ====== */
  .violation-overlay {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.65);
    backdrop-filter: blur(6px);
    z-index: 9998;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.3s ease;
  }}
  .violation-overlay.hidden {{ display: none; }}
  .violation-card {{
    background: #fff;
    border-radius: 24px;
    padding: 2.2rem 2rem;
    max-width: 380px;
    width: 90%;
    text-align: center;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    animation: scaleIn 0.4s cubic-bezier(0.68,-0.55,0.265,1.55);
  }}
  .violation-card .icon {{ font-size: 3rem; margin-bottom: 0.6rem; }}
  .violation-card h2 {{
    font-size: 1.35rem;
    font-weight: 900;
    color: #E74C3C;
    margin-bottom: 0.5rem;
  }}
  .violation-card p {{
    font-size: 0.95rem;
    color: #555;
    line-height: 1.6;
    margin-bottom: 1.3rem;
  }}
  .violation-card .prev-choice {{
    background: #FFF3F3;
    border: 2px solid #E74C3C;
    border-radius: 12px;
    padding: 0.7rem 1rem;
    font-size: 1.1rem;
    font-weight: 900;
    color: #C0392B;
    margin-bottom: 1.2rem;
  }}
  .violation-btns {{
    display: flex;
    gap: 0.8rem;
    justify-content: center;
  }}
  .btn-obey {{
    background: linear-gradient(135deg, #2ECC71, #27AE60);
    color: #fff;
    border: none;
    padding: 0.7rem 1.5rem;
    font-size: 1rem;
    font-weight: 900;
    border-radius: 50px;
    cursor: pointer;
    font-family: 'Noto Sans TC', sans-serif;
    box-shadow: 0 4px 15px rgba(46,204,113,0.4);
    transition: all 0.2s;
  }}
  .btn-obey:hover {{ transform: translateY(-2px); }}
  .btn-violate {{
    background: linear-gradient(135deg, #E74C3C, #C0392B);
    color: #fff;
    border: none;
    padding: 0.7rem 1.5rem;
    font-size: 1rem;
    font-weight: 900;
    border-radius: 50px;
    cursor: pointer;
    font-family: 'Noto Sans TC', sans-serif;
    box-shadow: 0 4px 15px rgba(231,76,60,0.4);
    transition: all 0.2s;
  }}
  .btn-violate:hover {{ transform: translateY(-2px); }}

  /* ====== 主畫面（同意前模糊） ====== */
  .main-content {{
    filter: blur(12px);
    pointer-events: none;
    transition: all 0.6s ease;
  }}
  .main-content.unlocked {{
    filter: none;
    pointer-events: auto;
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

  .outer-ring {{
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    border-radius: 50%;
    background: repeating-conic-gradient(#555 0deg 5deg, #ddd 5deg 10deg);
    box-shadow: 0 8px 40px rgba(0,0,0,0.25);
  }}

  canvas#wheel {{
    position: absolute;
    top: 12px; left: 12px;
    width: 346px; height: 346px;
    border-radius: 50%;
    transition: transform 4.5s cubic-bezier(0.15, 0.60, 0.08, 1.00);
  }}

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
  .center-btn:hover {{ background: linear-gradient(135deg, #c0392b, #a93226); }}
  .center-btn:active {{ transform: translate(-50%, -50%) scale(0.95); }}
  .center-btn.disabled {{ opacity: 0.5; cursor: not-allowed; }}

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
    transition: background 0.2s;
  }}
  .result-card a:hover {{ background: rgba(255,255,255,0.35); }}

  /* confetti */
  .confetti-container {{
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 9999; overflow: hidden;
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

<!-- ===== 同意彈窗 ===== -->
<div class="overlay" id="consentOverlay">
  <div class="consent-card">
    <div class="icon">🎰</div>
    <h2>午餐輪盤使用條款</h2>
    <div class="oath">
      「我同意輪盤出現什麼<br>我就吃什麼」
    </div>
    <p>按下同意，即表示你願意<br>將午餐選擇權交給命運 🫡</p>
    <button class="consent-btn" onclick="acceptConsent()">✅ 同意</button>
  </div>
</div>

<!-- ===== 違規確認彈窗 ===== -->
<div class="violation-overlay hidden" id="violationOverlay">
  <div class="violation-card">
    <div class="icon">⚠️</div>
    <h2>違反使用條款警告</h2>
    <p>你已經同意「輪盤出現什麼就吃什麼」<br>命運已經為你選擇了：</p>
    <div class="prev-choice" id="prevChoiceText"></div>
    <p>確定要違反承諾，重新轉動嗎？ 🤨</p>
    <div class="violation-btns">
      <button class="btn-obey" onclick="obeyFate()">😇 乖乖去吃</button>
      <button class="btn-violate" onclick="violateAndSpin()">😈 我就要重轉</button>
    </div>
  </div>
</div>

<!-- ===== 主畫面 ===== -->
<div class="main-content" id="mainContent">
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
</div>

<script>
// ===== 同意邏輯 =====
function acceptConsent() {{
  document.getElementById('consentOverlay').classList.add('hidden');
  document.getElementById('mainContent').classList.add('unlocked');
}}

// ===== 資料 =====
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
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // 文字 — 逐字沿半徑從外到內排列（直書效果）
    const midAngle = (startAngle + endAngle) / 2;

    const name = restaurants[i].name;
    const chars = name.split('');
    const maxChars = 7;
    const displayChars = chars.length > maxChars ? chars.slice(0, maxChars) : chars;

    const fontSize = 20;

    // 從外到內，逐字放置
    const startR = R * 0.88;
    const charSpacing = fontSize * 1.2;

    for (let c = 0; c < displayChars.length; c++) {{
      const charR = startR - c * charSpacing;
      if (charR < R * 0.2) break;

      // 計算每個字的位置
      const charX = cx + Math.cos(midAngle) * charR;
      const charY = cy + Math.sin(midAngle) * charR;

      ctx.save();
      ctx.translate(charX, charY);
      // 不旋轉 — 每個字都保持正立
      ctx.fillStyle = '#fff';
      ctx.shadowColor = 'rgba(0,0,0,0.7)';
      ctx.shadowBlur = 5;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.font = '900 ' + fontSize + 'px "Noto Sans TC", sans-serif';
      ctx.fillText(displayChars[c], 0, 0);
      ctx.restore();
    }}
  }}

  // 內圈漸層
  const grd = ctx.createRadialGradient(cx, cy, R * 0.05, cx, cy, R);
  grd.addColorStop(0, 'rgba(0,0,0,0.10)');
  grd.addColorStop(0.3, 'rgba(0,0,0,0)');
  grd.addColorStop(1, 'rgba(0,0,0,0.06)');
  ctx.beginPath();
  ctx.arc(cx, cy, R, 0, Math.PI * 2);
  ctx.fillStyle = grd;
  ctx.fill();
}}
drawWheel();

// ===== 旋轉邏輯 =====
let currentRotation = 0;
let spinning = false;
let hasResult = false;       // 是否已經有結果
let currentWinner = null;    // 目前的結果
let violationCount = 0;      // 違規次數

function spin() {{
  if (spinning) return;

  // 如果已經有結果，跳出違規警告
  if (hasResult && currentWinner) {{
    document.getElementById('prevChoiceText').textContent = '🏆 ' + currentWinner.name;
    document.getElementById('violationOverlay').classList.remove('hidden');
    return;
  }}

  doSpin();
}}

// 乖乖去吃 — 關掉彈窗，打開地圖
function obeyFate() {{
  document.getElementById('violationOverlay').classList.add('hidden');
  if (currentWinner) {{
    window.open(currentWinner.url, '_blank');
  }}
}}

// 違規重轉
function violateAndSpin() {{
  violationCount++;
  document.getElementById('violationOverlay').classList.add('hidden');
  hasResult = false;
  currentWinner = null;
  doSpin();
}}

function doSpin() {{
  spinning = true;
  document.getElementById('spinBtn').classList.add('disabled');
  document.getElementById('resultCard').classList.remove('show');

  const winnerIdx = Math.floor(Math.random() * N);
  const winnerMidDeg = winnerIdx * sliceDeg + sliceDeg / 2;
  const targetStop = 360 - winnerMidDeg;
  const extraSpins = (5 + Math.floor(Math.random() * 4)) * 360;
  const totalRotation = currentRotation + extraSpins + (targetStop - (currentRotation % 360) + 360) % 360;

  canvas.style.transform = 'rotate(' + totalRotation + 'deg)';
  currentRotation = totalRotation;

  setTimeout(() => {{
    const winner = restaurants[winnerIdx];
    currentWinner = winner;
    hasResult = true;

    document.getElementById('winnerName').textContent = winner.name;
    document.getElementById('winnerLink').href = winner.url;

    // 如果有違規紀錄，加上恥辱標記
    if (violationCount > 0) {{
      document.getElementById('winnerName').textContent = winner.name + '（第 ' + (violationCount + 1) + ' 次轉）';
    }}

    document.getElementById('resultCard').classList.add('show');
    spinning = false;
    document.getElementById('spinBtn').classList.remove('disabled');
    launchConfetti();
  }}, 4800);
}}

// ===== Confetti =====
function launchConfetti() {{
  const container = document.createElement('div');
  container.className = 'confetti-container';
  document.body.appendChild(container);
  const cColors = ['#FF6B6B','#4ECDC4','#45B7D1','#FFA07A','#F7DC6F','#BB8FCE','#667eea','#E74C3C','#2ECC71'];
  for (let i = 0; i < 80; i++) {{
    const c = document.createElement('div');
    c.className = 'confetti';
    c.style.left = Math.random() * 100 + '%';
    c.style.background = cColors[Math.floor(Math.random() * cColors.length)];
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

    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {display: none;}
    [data-testid="stDecoration"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

    wheel_html = build_wheel_html(RESTAURANTS, COLORS)
    components.html(wheel_html, height=750, scrolling=False)


if __name__ == "__main__":
    main()
