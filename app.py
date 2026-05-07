import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="冶金工艺智能系统", layout="wide", page_icon="🔥")
st.title("🔥 冶金工艺智能仿真与专家系统")
st.subheader("高炉·电弧炉全流程工艺计算、故障诊断、AI问答")

# 侧边栏
menu = st.sidebar.selectbox("功能菜单", [
    "系统介绍",
    "高炉工艺计算",
    "电弧炉工艺计算",
    "故障案例库",
    "AI冶金问答"
])

# ----------------------
# 1. 系统介绍
# ----------------------
if menu == "系统介绍":
    st.markdown("""
## 系统功能
- 高炉：炉温判断、透气性、顺行状态、热状态评估
- 电弧炉：供电、泡沫渣、脱磷、脱硫、电耗计算
- 故障库：12种现场故障 + 标准处理方案
- AI问答：专业冶金知识在线解答
""")

# ----------------------
# 2. 高炉工艺计算（内行版）
# ----------------------
elif menu == "高炉工艺计算":
    st.subheader("高炉工艺计算系统")
    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("### 输入参数")
        P = st.number_input("炉顶压力 (kPa)", 200.0, 280.0, 245.0)
        T_top = st.number_input("炉顶温度 (℃)", 80.0, 300.0, 180.0)
        K = st.number_input("焦比 (kg/t)", 300.0, 450.0, 370.0)
        Si = st.number_input("[Si] %", 0.20, 1.0, 0.45)
        S = st.number_input("[S] %", 0.010, 0.080, 0.030)
        eta_CO = st.number_input("煤气利用率 ηCO %", 40.0, 55.0, 49.0)

    with col2:
        st.markdown("### 工艺计算结果")

        # 炉温判断
        if Si >= 0.55:
            st.error("炉温：过热 → 建议减焦、降风温")
        elif Si <= 0.30:
            st.error("炉温：凉炉 → 建议加焦、提风温")
        else:
            st.success("炉温：正常稳定")

        # 顺行判断
        dP = 170  # 固定压差参考
        perme = (P / dP) * 10
        st.metric("料柱透气性指数", round(perme,2))
        if perme < 2.5:
            st.warning("透气性差 → 易悬料")
        elif perme > 3.5:
            st.warning("气流过强 → 易崩料")
        else:
            success = st.success("透气性正常")

        # 热状态
        heat = 1500 + (Si - 0.4) * 100
        st.metric("铁水温度估算 (℃)", round(heat))

        # 脱硫
        eta_S = 90 if (1.15 < 1.25 and heat>1480) else 75
        st.metric("脱硫效率 %", eta_S)

        st.info("内行看：炉温→Si→铁水温度→透气性→顺行→脱硫，全链路闭环计算")

# ----------------------
# 3. 电弧炉工艺计算（内行版）
# ----------------------
elif menu == "电弧炉工艺计算":
    st.subheader("电弧炉工艺计算系统")
    col1, col2 = st.columns([1,1])

    with col1:
        I = st.number_input("二次电流 kA", 30.0, 85.0, 55.0)
        cosφ = st.number_input("功率因数", 0.60, 0.95, 0.85)
        foam_h = st.number_input("泡沫渣高度 mm", 150, 600, 400)
        P_content = st.number_input("磷含量 %", 0.005, 0.040, 0.012)

    with col2:
        st.markdown("### 工艺判断")
        if cosφ < 0.80:
            st.warning("功率因数低 → 电耗高")
        else:
            st.success("功率正常")

        if foam_h < 250:
            st.error("泡沫渣不足 → 热效率低")
        else:
            st.success("埋弧良好")

        if P_content > 0.015:
            st.error("磷超标 → 需强化脱磷")
        else:
            st.success("磷合格")

        elec_consume = 430 - (cosφ - 0.8) * 200 - (foam_h - 300) * 0.1
        st.metric("估算电耗 kWh/t", round(elec_consume))

# ----------------------
# 4. 故障案例库
# ----------------------
elif menu == "故障案例库":
    st.subheader("冶金故障案例库")
    data = {
        "编号":["BF01","BF02","BF03","BF04","BF05","BF06","EAF01","EAF02","EAF03","EAF04","EAF05","EAF06"],
        "故障":["炉缸堆积","悬料","崩料","结瘤","炉温反跳","脱硫差","熔化慢","断电极","泡沫渣差","回磷","温低","耐材侵蚀"],
        "原因":["中心不活跃","软熔带过高","边缘过强","碱金属富集","布料突变","碱度低","废钢差","冲击/电流不均","碳不足","下渣","功率低","FeO高"],
        "处理":["提风温、中心加焦","减风坐料","压边、控气流","洗炉、降碱负荷","稳布料、调焦比","提碱度、提炉温","优化供电、预热","稳电流、防冲击","补碳、调渣","挡渣、控渣","加功率","MgO调渣"],
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

# ----------------------
# 5. AI冶金问答（核心！）
# ----------------------
elif menu == "AI冶金问答":
    st.subheader("🤖 AI冶金专家问答")
    st.info("可提问：高炉、电弧炉、造渣、脱硫、脱磷、故障处理、工艺参数")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_msg = st.chat_input("请输入你的问题")

    if user_msg:
        st.session_state.chat.append({"role":"user","content":user_msg})
        with st.chat_message("user"):
            st.write(user_msg)

        with st.chat_message("assistant"):
            res = ""

            # 高炉
            if "悬料" in user_msg:
                res = "悬料处理：减风→坐料→优化布料→提高边缘气流→检查粉末含量"
            elif "炉缸" in user_msg:
                res = "炉缸堆积：提高风温、加中心焦、洗炉、强化冷却"
            elif "脱硫" in user_msg:
                res = "脱硫三要素：炉温足够、炉渣碱度1.15-1.25、渣量充足"
            elif "焦比" in user_msg:
                res = "焦比优化：提高风温、提高喷煤、优化布料、提高煤气利用率"

            # 电弧炉
            elif "泡沫渣" in user_msg:
                res = "泡沫渣：喷碳、控制FeO、合适粘度、高度300-500mm"
            elif "脱磷" in user_msg:
                res = "脱磷：高碱度、高FeO、低温、充分搅拌"
            elif "电极" in user_msg:
                res = "断电极：电流稳定、防废钢冲击、合理阻抗、调节器灵敏"
            elif "电耗" in user_msg:
                res = "降低电耗：高功率因数、良好泡沫渣、氧煤强化、预热废钢"

            # 通用
            else:
                res = "我是冶金AI专家，可回答高炉、电弧炉、造渣、故障、参数优化等问题。"

            st.write(res)
        st.session_state.chat.append({"role":"assistant","content":res})

st.sidebar.info("冶金工艺智能系统 V2.0")
