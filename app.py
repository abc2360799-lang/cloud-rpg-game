import streamlit as st
import random

st.set_page_config(page_title="雲端 RPG 冒險遊戲 - 豪華版", page_icon="⚔️", layout="wide")

#### 個人署名區域 (防抄襲專用) ####
YOUR_NAME = "林聖凱"
YOUR_STUDENT_ID = "國立勤益科技大學 - 智慧自動化工程系"
#### ---------------------------- ####

# 頂部開發者專屬簽名欄
st.markdown(f"""
<div style="background-color:#1e1e1e; padding:15px; border-radius:8px; border-left: 5px solid #ff4b4b; margin-bottom:25px;">
    <h4 style="color:white; margin:0; font-family:monospace;">🛠️ 雲端系統開發者認證</h4>
    <p style="color:#aaa; margin:5px 0 0 0; font-size:14px;">姓名：<b>{YOUR_NAME}</b> ｜ 班級單位：<b>{YOUR_STUDENT_ID}</b></p>
</div>
""", unsafe_allow_html=True)

st.title("⚔️ 雲端期末專案：RPG 勇者戰鬥模擬器")
st.write("這是一個部署在 Railway 雲端平台的動態網頁遊戲，具備完整的按鈕即時邏輯、狀態回傳與圖文動態互動功能。")

# 初始化遊戲數據
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
if "monster_hp" not in st.session_state:
    st.session_state.monster_hp = 120
if "logs" not in st.session_state:
    st.session_state.logs = ["🌲 你手持利刃走進了神祕森林，遭遇了 brand 惡魔！戰鬥一觸即發！"]

# 側邊欄控制面板
st.sidebar.header("🎮 遊戲核心設定")
difficulty = st.sidebar.radio("設定關卡難度：", ["普通模式", "困難模式（怪物傷害加倍）"])
st.sidebar.divider()
if st.sidebar.button("🔄 重置戰鬥 (Reset)", use_container_width=True):
    st.session_state.player_hp = 100
    st.session_state.monster_hp = 120
    st.session_state.logs = ["🌲 戰鬥已重置！勇者滿血回歸，新一輪挑戰開始！"]

# 顯示遊戲精美圖片與血量 (分成左右兩邊)
col_game1, col_game2 = st.columns(2)

with col_game1:
    st.markdown("### 🧙‍♂️ 勇者 (You)")
    # 嵌入勇者精美圖片
    st.image("https://images.unsplash.com/photo-1534447677768-be436bb09401?w=500&auto=format&fit=crop&q=60", caption="手握聖光之力的雲端勇者", use_container_width=True)
    st.progress(max(0, min(st.session_state.player_hp / 100, 1.0)))
    st.metric(label="勇者 HP 生命值", value=f"{st.session_state.player_hp} / 100")

with col_game2:
    st.markdown("### 👹 惡魔 (Boss)")
    # 嵌入怪物精美圖片
    st.image("https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=500&auto=format&fit=crop&q=60", caption="來自深淵的終極 brand 惡魔", use_container_width=True)
    st.progress(max(0, min(st.session_state.monster_hp / 120, 1.0)))
    st.metric(label="惡魔 HP 生命值", value=f"{st.session_state.monster_hp} / 120")

st.divider()

# 戰鬥邏輯與互動按鈕
if st.session_state.player_hp <= 0:
    st.error(f"💀 勇者 {YOUR_NAME} 戰死了！請點擊左側的「重置戰鬥」重新挑戰。")
elif st.session_state.monster_hp <= 0:
    st.success(f"🎉 恭喜！勇者 {YOUR_NAME} 成功擊敗惡魔！順利完成雲端期末專案！")
else:
    st.write("### 🗡️ 請下達你的戰鬥指令：")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    monster_dmg_base = random.randint(8, 15)
    monster_dmg = monster_dmg_base * 2 if difficulty == "困難模式" else monster_dmg_base

    with btn_col1:
        if st.button("⚔️ 揮劍普通攻擊", use_container_width=True):
            dmg = random.randint(12, 22)
            st.session_state.monster_hp -= dmg
            st.session_state.player_hp -= monster_dmg
            st.session_state.logs.insert(0, f"💥 你使出雙劍橫斬！對怪物造成 {dmg} 點傷害！")
            st.session_state.logs.insert(0, f"🩸 惡魔發動利爪反擊，對你造成 {monster_dmg} 點傷害！")
            st.rerun()

    with btn_col2:
        if st.button("🔥 吟滅魔能大招", use_container_width=True):
            dmg = random.randint(28, 45)
            st.session_state.monster_hp -= dmg
            heavy_dmg = monster_dmg + 6
            st.session_state.player_hp -= heavy_dmg
            st.session_state.logs.insert(0, f"🔮 你詠唱終極魔法！烈焰在惡魔身上爆裂，砍下 {dmg} 點暴擊傷害！")
            st.session_state.logs.insert(0, f"🩸 惡魔陷入暴怒，頂著魔法瘋狂反撲，對你造成 {heavy_dmg} 點重傷！")
            st.rerun()

    with btn_col3:
        if st.button("🧪 喝下治癒神水", use_container_width=True):
            heal = random.randint(22, 38)
            st.session_state.player_hp = min(100, st.session_state.player_hp + heal)
            st.session_state.player_hp -= monster_dmg
            st.session_state.logs.insert(0, f"💚 你喝下煉金治癒神水，體力回復了 {heal} 點。")
            st.session_state.logs.insert(0, f"🩸 惡魔趁你喝藥水時無情偷襲，對你造成 {monster_dmg} 點傷害！")
            st.rerun()

# 顯示動態戰鬥日誌
st.write("### 📜 戰鬥動態即時日誌 (Battle Logs)")
for log in st.session_state.logs[:6]:
    st.write(log)
