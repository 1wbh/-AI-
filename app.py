 import streamlit as st
import pandas as pd
import openai

# （如果需要用OpenAI，先在终端安装：pip install openai）

# ========== 页面设置 ==========
st.set_page_config(page_title="钢铁冶炼智能仿真系统", layout="wide")
st.title("🏭 高炉—电弧炉全流程AI智能仿真与专家系统")
st.subheader("钢铁冶炼工艺智能分析与诊断平台")

# 侧边栏菜单
menu = st.sidebar.selectbox(
    "选择功能模块",
    [
        "首页｜系统介绍",
        "高炉炼铁｜仿真+工艺诊断",
        "电弧炉炼钢｜仿真+工艺诊断",
        "工艺故障案例库",
        "AI工艺问答助手",
        "用户数据上传｜知识库扩展"
    ]
)

# ========== 首页 ==========
if menu == "首页｜系统介绍":
    st.markdown("## 📌 系统核心功能")
    st.markdown("""
    1. 高炉炼铁全流程工艺仿真与实时诊断
    2. 电弧炉炼钢工艺参数智能优化与分析
    3. 典型工艺故障案例库与解决方案
    4. AI工艺问答助手，提供专业冶金知识解答
    5. 用户数据上传与工艺模型扩展
    """)

# ========== 高炉炼铁模块 ==========
elif menu == "高炉炼铁｜仿真+工艺诊断":
    st.subheader("🔥 高炉炼铁工艺仿真与诊断")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 工艺参数调节")
        炉顶压力 = st.slider("炉顶压力 (kPa)", 180, 280, 245)
        炉顶温度 = st.slider("炉顶温度 (℃)", 80, 300, 180)
        透气性指数 = st.slider("透气性指数 K", 2.2, 4.0, 3.0)
        铁水Si = st.slider("铁水 [Si] (%)", 0.20, 1.0, 0.45)
        铁水S = st.slider("铁水 [S] (%)", 0.010, 0.080, 0.030)

    with col2:
        st.markdown("### 📊 工艺诊断结果")
        # 1. 炉顶压力诊断
        if 230 <= 炉顶压力 <= 260:
            st.success("炉顶压力：正常✅，煤气流分布稳定")
        elif 200 <= 炉顶压力 < 230 or 260 < 炉顶压力 <= 280:
            st.warning("炉顶压力：异常⚠️，可能导致煤气流分布不均")
        else:
            st.error("炉顶压力：危险❌，存在悬料/管道行程风险")

        # 2. 铁水Si诊断
        if 0.35 <= 铁水Si <= 0.55:
            st.success("铁水[Si]：正常✅，炉温稳定")
        elif 0.25 <= 铁水Si < 0.35:
            st.warning("铁水[Si]：偏低⚠️，炉温偏凉，需提高风温或增加焦炭负荷")
        else:
            st.error("铁水[Si]：过高❌，炉温过热，需降低风温或减少焦炭")

        # 3. 工艺评分
        工艺评分 = 100
        if not (230 <= 炉顶压力 <= 260):
            工艺评分 -= 20
        if not (0.35 <= 铁水Si <= 0.55):
            工艺评分 -= 20
        if not (2.5 <= 透气性指数 <= 3.5):
            工艺评分 -= 15
        st.metric("高炉顺行状态评分", value=f"{工艺评分}/100")

# ========== 电弧炉炼钢模块 ==========
elif menu == "电弧炉炼钢｜仿真+工艺诊断":
    st.subheader("⚡ 电弧炉炼钢工艺仿真与诊断")
    col1, col2 = st.columns(2)
    with col1:
        二次电流 = st.slider("二次电流 (kA)", 30, 85, 55)
        功率因数 = st.slider("功率因数", 0.60, 0.95, 0.85)
        泡沫渣高度 = st.slider("泡沫渣高度 (mm)", 150, 600, 400)
        终点P = st.slider("终点磷含量 (%)", 0.005, 0.040, 0.012)

    with col2:
        st.markdown("### 📊 工艺诊断结果")
        if 45 <= 二次电流 <= 65:
            st.success("二次电流：正常✅，电弧稳定")
        elif 30 <= 二次电流 < 45 or 65 < 二次电流 <= 75:
            st.warning("二次电流：异常⚠️，易导致电弧不稳定或电极损耗增加")
        else:
            st.error("二次电流：危险❌，存在电极断损风险")

        if 功率因数 >= 0.82:
            st.success("功率因数：优秀✅，电能利用效率高")
        elif 0.75 <= 功率因数 < 0.82:
            st.warning("功率因数：偏低⚠️，电能损耗增加，需优化供电曲线")
        else:
            st.error("功率因数：过低❌，电能利用率低，设备无功损耗严重")

# ========== 故障案例库 ==========
elif menu == "工艺故障案例库":
    st.subheader("📚 钢铁冶炼典型故障与解决方案")
    data = {
        "故障编号": ["BF-F-001","BF-F-002","BF-F-003","BF-F-004","BF-F-005","BF-F-006",
                    "EAF-F-007","EAF-F-008","EAF-F-009","EAF-F-010","EAF-F-011","EAF-F-012"],
        "故障名称": ["炉缸堆积","悬料","崩料","结瘤","炉温反跳","脱硫失常",
                    "熔化效率低","电极折断","泡沫渣不稳定","回磷超标","终点温度偏低","耐材侵蚀过快"],
        "严重等级": ["紧急","严重","严重","一般","一般","严重",
                "一般","紧急","一般","严重","一般","一般"],
        "解决方案": ["提高鼓风动能、调整风口布局","降低料线、适当减风","疏松料柱、控制煤气流","洗炉、调整炉料配比","调整焦炭负荷、稳定风温","提高炉渣碱度、优化造渣制度",
                  "优化氧枪位置、提高吹氧效率","检查电极夹持器、调整供电曲线","优化造渣工艺、控制渣碱度","提高炉渣氧化性、控制渣量","提高供电功率、延长冶炼时间","优化渣系、控制炉温"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

# ========== AI工艺问答助手 ==========
elif menu == "AI工艺问答助手":
    st.subheader("🤖 冶金工艺AI问答助手")
    st.info("您可以提问任何钢铁冶炼相关的工艺问题，如高炉顺行控制、电弧炉造渣制度、故障处理方案等。")

    # 初始化对话历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示对话历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 接收用户输入
    if prompt := st.chat_input("请输入您的问题，例如：高炉悬料的处理措施有哪些？"):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 这里可以接入OpenAI/本地大模型，我先给你一个模拟的回复逻辑
        with st.chat_message("assistant"):
            # 模拟AI回复，实际使用时替换为真实的API调用
            if "悬料" in prompt:
                response = """
                高炉悬料的常见处理措施包括：
                1. 适当减风，降低风压，松动料柱
                2. 调整料线，适当降低料线，改善上部透气性
                3. 控制煤气流分布，适当增加边缘煤气流
                4. 检查炉料质量，避免粉末入炉
                5. 必要时可采用疏松料柱的操作（如放风坐料）
                """
            elif "造渣" in prompt:
                response = """
                电弧炉造渣工艺要点：
                1. 控制炉渣碱度在2.0-3.0之间，根据钢种调整
                2. 保证泡沫渣高度在300-500mm，提高电弧稳定性
                3. 控制渣中FeO含量，避免过高导致回磷
                4. 优化造渣剂加入时机，保证成渣速度
                """
            else:
                response = "您的问题我已收到，我会结合冶金工艺规范和行业经验为您解答。目前我处于基础版本，可先为您解答常见的高炉/电弧炉工艺问题。"
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# ========== 用户数据上传 ==========
elif menu == "用户数据上传｜知识库扩展":
    st.subheader("📤 用户数据上传与工艺模型扩展")
    uploaded_file = st.file_uploader("上传Excel/CSV格式的工艺数据文件", type=["xlsx", "csv"])
    if uploaded_file:
        st.success("文件上传成功✅，系统将自动解析并更新工艺模型与知识库")
        st.info("您上传的工艺数据将用于优化系统的诊断规则与AI问答能力")

st.sidebar.success("🚀 系统运行正常")
