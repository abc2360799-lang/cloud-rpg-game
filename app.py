import streamlit as st
import random

st.set_page_config(page_title="雲端 RPG 冒險遊戲 - 專屬版", page_icon="⚔️")

#### 個人署名區域 (防抄襲專用) ####
# 請在這裡填入你的名字和學號，這會顯示在遊戲頂部
YOUR_NAME = "林聖凱"
YOUR_STUDENT_ID = "3B261096"
#### ---------------------------- ####

# 顯示專屬署名標頭
st.markdown(f"""
<div style="background-color:#1e1e1e; padding:10px; border-radius:5px; border-bottom: 2px solid #f63366; margin-bottom:20px;">
    <p style="color:white; margin:0; font-size:14px;">🛠️ DEVELOPER: <b>{YOUR_NAME}</b> | 專屬學號: <b>{YOUR_STUDENT_ID}</b></p>
</div>
""", unsafe_allow_html=True)

st.title("⚔️ 雲端 RPG 冒險遊戲")
st.write(f"這是一個基於雲端部署的互動式網頁遊戲，點擊按鈕即可與怪物進行即時戰鬥！<br><span style='font-size:12px; color:gray;'>(本程式由 {YOUR_NAME} 開發並部署於 Railway)</span>", unsafe_allow_html=True)

# 初始化遊戲數據（使用 session_state 確保按按鈕時資料不會重置）
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
if "monster_hp" not in st.session_state:
    st.session_state.monster_hp = 120
if "logs" not in st.session_state:
    st.session_state.logs = ["🌲 你走進了神秘森林，遭遇 brand 惡魔！戰鬥開始！"]

# 側邊欄：難度調整與互動
st.sidebar.header("🎮 遊戲設定")
difficulty = st.sidebar.radio("選擇難度", ["普通", "困難（怪物攻擊力加倍）"])
if st.sidebar.button("🔄 重置遊戲 (Reset)"):
    st.session_state.player_hp = 100
    st.session_state.monster_hp = 120
    st.session_state.logs = ["🌲 遊戲已重置，新一輪戰鬥開始！"]

# 顯示目前的血量狀態
col1, col2 = st.columns(2)
with col1:
    st.subheader("🧙‍♂️ 玩家 (勇者)")
    st.progress(max(0, min(st.session_state.player_hp / 100, 1.0)))
    st.metric(label="你的 HP", value=f"{st.session_state.player_hp} / 100")

with col2:
    st.subheader("👹 怪物 (惡魔)")
    st.progress(max(0, min(st.session_state.monster_hp / 120, 1.0)))
    st.metric(label="怪物 HP", value=f"{st.session_state.monster_hp} / 120")

st.divider()

# 判斷遊戲是否結束
if st.session_state.player_hp <= 0:
    st.error("💀 你被怪物擊敗了！請點擊左側的重置按鈕重新挑戰。")
elif st.session_state.monster_hp <= 0:
    st.success("🎉 恭喜你！成功擊敗惡魔，拯救了雲端世界！")
else:
    # 戰鬥互動按鈕
    st.write("### 🗡️ 請選擇你的行動：")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    # 怪物反擊傷害計算邏輯
    monster_dmg_base = random.randint(8, 15)
    monster_dmg = monster_dmg_base * 2 if difficulty == "困難" else monster_dmg_base

    with btn_col1:
        if st.button("⚔️ 普通攻擊", use_container_width=True):
            dmg = random.randint(10, 20)
            st.session_state.monster_hp -= dmg
            st.session_state.player_hp -= monster_dmg
            st.session_state.logs.insert(0, f"💥 你使用普通攻擊，對怪物造成 {dmg} 點傷害！")
            st.session_state.logs.insert(0, f"🩸 怪物反擊，對你造成 {monster_dmg} 點傷害！")
            st.rerun()

    with btn_col2:
        if st.button("🔥 魔法大招", use_container_width=True):
            dmg = random.randint(25, 40)
            st.session_state.monster_hp -= dmg
            # 魔法消耗代價：怪物會強力反擊
            heavy_dmg = monster_dmg + 5
            st.session_state.player_hp -= heavy_dmg
            st.session_state.logs.insert(0, f"🔮 你詠唱吟滅火球！對怪物造成 {dmg} 點暴擊傷害！")
            st.session_state.logs.insert(0, f"🩸 怪物趁你施法反擊，對你造成 {heavy_dmg} 點傷害！")
            st.rerun()

    with btn_col3:
        if st.button("🧪 喝治療藥水", use_container_width=True):
            heal = random.randint(20, 35)
            st.session_state.player_hp = min(100, st.session_state.player_hp + heal)
            st.session_state.player_hp -= monster_dmg
            st.session_state.logs.insert(0, f"💚 你喝下甘露藥水，回復了 {heal} 點生命值。")
            st.session_state.logs.insert(0, f"🩸 怪物趁你喝藥水偷襲，對你造成 {monster_dmg} 點傷害！")
            st.rerun()

# 顯示戰鬥日誌
st.write("### 📜 戰鬥動態日誌 (Battle Logs)")
for log in st.session_state.logs[:6]:  # 只顯示最新的 6 條記錄
    st.write(log)
