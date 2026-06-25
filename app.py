import streamlit as st
import random
import time

# 設定網頁標題與排版
st.set_page_config(page_title="雲端 RPG 冒險遊戲 - 動態打鬥版", page_icon="⚔️", layout="wide")

#### 個人署名區域 (防抄襲專用) ####
# 請在這裡填入你的名字和學號，這會顯示在遊戲頂部
YOUR_NAME = "林聖凱"
YOUR_STUDENT_ID = "國立勤益科技大學 - 智慧自動化工程系"
#### ---------------------------- ####

# 自訂 CSS 風格 (讓畫面更像遊戲)
st.markdown("""
<style>
    .reportview-container {
        background: #121212;
    }
    .stMetric label {
        color: #aaa !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-family: monospace;
    }
    .battle-log {
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 5px;
        color: #ddd;
        font-size: 14px;
        border: 1px solid #333;
    }
    div[data-testid="stImageCaption"] {
        color: #888;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 頂部開發者專屬簽名欄
st.markdown(f"""
<div style="background-color:#1e1e1e; padding:15px; border-radius:8px; border-left: 5px solid #ff4b4b; margin-bottom:25px;">
    <h4 style="color:white; margin:0; font-family:monospace;">🛠️ 雲端系統開發者認證</h4>
    <p style="color:#aaa; margin:5px 0 0 0; font-size:14px;">姓名：<b>{YOUR_NAME}</b> ｜ 班級單位：<b>{YOUR_STUDENT_ID}</b></p>
</div>
""", unsafe_allow_html=True)

st.title("⚔️ 雲端 RPG 冒險遊戲：動態戰鬥版")
st.write(f"這是一個部署於 Railway 的雲端互動遊戲，具備即時按鈕邏輯、動態打鬥畫面切換與狀態回傳功能。<br><span style='font-size:12px; color:gray;'>(本程式由 {YOUR_NAME} 開發)</span>", unsafe_allow_html=True)

# 初始化遊戲數據 (使用 session_state 確保按按鈕時資料不會重置)
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
if "monster_hp" not in st.session_state:
    st.session_state.monster_hp = 120
if "logs" not in st.session_state:
    st.session_state.logs = ["🌲 你走進了神秘森林，遭遇了 brand 惡魔！戰鬥開始！"]
# [新增] 初始化戰鬥狀態：'idle' (平常), 'attack' (普通攻擊), 'magic' (魔法)
if "battle_status" not in st.session_state:
    st.session_state.battle_status = 'idle'

# 定義遊戲中的圖片網址
IMAGES = {
    'player_idle': "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400&auto=format&fit=crop&q=60", # 勇者靜態圖
    'monster_idle': "https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=400&auto=format&fit=crop&q=60", # 惡魔靜態圖
    'player_attack': "https://images.unsplash.com/photo-1555616635-be36a6e5b4b7?w=400&auto=format&fit=crop&q=60", # 普通攻擊打鬥圖 (劍氣/揮砍)
    'player_magic': "https://images.unsplash.com/photo-1628104634281-2a6d713bd427?w=400&auto=format&fit=crop&q=60", # 魔法大招打鬥圖 (爆炸/能量波)
    'game_over': "https://images.unsplash.com/photo-1583151978297-c6b7bd4d6f60?w=800&auto=format&fit=crop&q=60" # 遊戲結束圖 (💀)
}

# 側邊欄控制面板
st.sidebar.header("🎮 遊戲控制")
difficulty = st.sidebar.radio("選擇難度", ["普通", "困難（怪物攻擊力加倍）"])
if st.sidebar.button("🔄 重置遊戲 (Reset)", use_container_width=True):
    st.session_state.player_hp = 100
    st.session_state.monster_hp = 120
    st.session_state.battle_status = 'idle' # 重置戰鬥狀態
    st.session_state.logs = ["🌲 戰鬥已重置！新一輪挑戰開始！"]

st.divider()

# 顯示遊戲精美圖片與血量 (分成左右兩邊)
col_game1, col_game2 = st.columns(2)

# 根據目前的戰鬥狀態，動態切換顯示的圖片
current_player_img = IMAGES['player_idle']
current_monster_img = IMAGES['monster_idle']

if st.session_state.battle_status == 'attack':
    current_player_img = IMAGES['player_attack'] # 切換為攻擊圖
    # 一段時間後切換回平常狀態 (利用 st.rerun 在下一次渲染時恢復)
    st.session_state.battle_status = 'idle'
elif st.session_state.battle_status == 'magic':
    current_monster_img = IMAGES['player_magic'] # 切換為魔法圖 (在怪物那邊爆炸)
    st.session_state.battle_status = 'idle'

with col_game1:
    st.markdown("### 🧙‍♂️ 勇者 (Player)")
    # 嵌入勇者圖片 (平常或普通攻擊時會換圖)
    st.image(current_player_img, caption="手握聖光之力的雲端勇者", use_container_width=True)
    st.progress(max(0, min(st.session_state.player_hp / 100, 1.0)))
    st.metric(label="勇者 HP", value=f"{st.session_state.player_hp} / 100")

with col_game2:
    st.markdown("### 👹 惡魔 (Boss)")
    # 嵌入怪物圖片 (平常或魔法攻擊時會換成爆炸圖)
    st.image(current_monster_img, caption="來自深淵的終極 brand 惡魔", use_container_width=True)
    st.progress(max(0, min(st.session_state.monster_hp / 120, 1.0)))
    st.metric(label="怪物 HP", value=f"{st.session_state.monster_hp} / 120")

st.divider()

# 判斷遊戲是否結束
if st.session_state.player_hp <= 0:
    st.markdown(f'<div class="battle-log">💀 勇者 {YOUR_NAME} 被怪物擊敗了！請點擊側邊欄的重置按鈕重新挑戰。</div>', unsafe_allow_html=True)
    st.image(IMAGES['game_over'], use_container_width=True)
elif st.session_state.monster_hp <= 0:
    st.markdown(f'<div class="battle-log">🎉 恭喜！勇者 {YOUR_NAME} 成功擊敗惡魔！雲端期末專案大獲全勝！</div>', unsafe_allow_html=True)
    st.balloons() # 顯示氣球慶祝特效
else:
    # 戰鬥互動按鈕
    st.write("### 🗡️ 請選擇你的行動：")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    # 怪物反擊傷害計算邏輯
    monster_dmg_base = random.randint(8, 15)
    monster_dmg = monster_dmg_base * 2 if difficulty == "困難" else monster_dmg_base

    with btn_col1:
        if st.button("⚔️ 揮劍普通攻擊", use_container_width=True):
            # [新增] 切換狀態為普通攻擊
            st.session_state.battle_status = 'attack'
            dmg = random.randint(12, 22)
            st.session_state.monster_hp -= dmg
            st.session_state.player_hp -= monster_dmg
            st.session_state.logs.insert(0, f"💥 你使出雙劍橫斬！對怪物造成 {dmg} 點傷害！")
            st.session_state.logs.insert(0, f"🩸 怪物反擊，對你造成 {monster_dmg} 點傷害！")
            # [修改] 這裡不要立即 st.rerun()，讓狀態機先渲染一次攻擊圖，下一次渲染會 st.rerun 回復

    with btn_col2:
        if st.button("🔥 吟滅魔能大招", use_container_width=True):
            # [新增] 切換狀態為魔法攻擊
            st.session_state.battle_status = 'magic'
            dmg = random.randint(28, 45)
            st.session_state.monster_hp -= dmg
            heavy_dmg = monster_dmg + 6
            st.session_state.player_hp -= heavy_dmg
            st.session_state.logs.insert(0, f"🔮 你詠唱終極魔法！烈焰在惡魔身上爆裂，砍下 {dmg} 點暴擊傷害！")
            st.session_state.logs.insert(0, f"🩸 惡魔暴怒反撲，對你造成 {heavy_dmg} 點傷害！")

    with btn_col3:
        if st.button("🧪 喝下治癒神水", use_container_width=True):
            heal = random.randint(22, 38)
            st.session_state.player_hp = min(100, st.session_state.player_hp + heal)
            st.session_state.player_hp -= monster_dmg
            st.session_state.logs.insert(0, f"💚 你喝下煉金治癒神水，體力回復了 {heal} 點。")
            st.session_state.logs.insert(0, f"🩸 惡魔偷襲，對你造成 {monster_dmg} 點傷害！")

# 顯示戰鬥日誌 (只顯示最新的 6 條記錄)
st.write("### 📜 戰鬥日誌 (Battle Logs)")
for log in st.session_state.logs[:6]:
    st.markdown(f'<div class="battle-log">{log}</div>', unsafe_allow_html=True)
