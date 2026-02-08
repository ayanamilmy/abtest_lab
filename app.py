import streamlit as st
import sys
import os
import matplotlib.pyplot as plt

# --- 1. 还是那个路径黑魔法 (为了能找到 src) ---
current_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_path, 'src')
sys.path.insert(0, src_path)

# --- 2. 引入你的“后厨团队” ---
from abtest_lab.validators import check_srm
from abtest_lab.bayesian import calculate_bayesian_prob
from abtest_lab.visuals import plot_bayesian_distribution

# --- 3. 开始画网页 (前端) ---
st.set_page_config(page_title="A/B 测试实验室", layout="wide") # 设置网页标题

st.title("🧪 A/B 测试实验室 (Bayesian Edition)")
st.markdown("这是你的第一个 **AI 数据分析工具**。输入数据，立马出结果！")

# --- 4. 侧边栏：输入数据 ---
with st.sidebar:
    st.header("📊 输入实验数据")
    
    st.subheader("A组 (对照组)")
    n_a = st.sidebar.slider("A组总人数", value=5000, step=10)
    conv_a = st.sidebar.slider("A组转化数", value=100, step=1)
    
    st.subheader("B组 (实验组)")
    n_b = st.sidebar.slider("B组总人数", value=5000, step=10)
    conv_b = st.sidebar.slider("B组转化数", value=500, step=1)
    
    run_btn = st.button("🚀 开始分析", type="primary") # primary 让按钮变色

# --- 5. 主区域：点击按钮后执行逻辑 ---
if run_btn:
    # A. 先做安检 (SRM)
    is_valid, srm_p = check_srm(n_a, n_b)
    
    if not is_valid:
        st.error(f"🚨 SRM 检测失败！样本比例严重失调 (P={srm_p:.4f})。请检查分流系统！")
    else:
        st.success("✅ SRM 检测通过，数据健康。")
        
        # B. 贝叶斯计算
        with st.spinner('正在进行 10 万次蒙特卡洛模拟...'): # 加个加载动画
            prob, uplift = calculate_bayesian_prob(conv_a, n_a, conv_b, n_b)
        
        # C. 展示关键指标 (用大字体)
        col1, col2 = st.columns(2) # 分两列显示
        col1.metric("B组获胜概率", f"{prob:.2%}")
        col2.metric("预期提升幅度", f"{uplift:.2%}")
        
        # D. 给出 AI 风格的结论
        if prob > 0.95:
            st.balloons() # 🎉 放个气球动画！
            st.info("💡 **决策建议**：胜算很大！建议全量上线！")
        elif prob > 0.90:
            st.warning("💡 **决策建议**：看起来不错，但建议再观察两天。")
        elif 0.85<=prob<0.90:
            st.error("💡 **决策建议**：没啥区别，别折腾了。")
        elif 0.70<=prob<0.85:
            st.error("💡 **决策建议**：你好像开倒车了")
        elif prob<0.7:
            st.error("💡 **决策建议**：你故意乱编数据？如果你是认真的，那么你的新方案跟美国的星球大战计划一样性价比极高")
        # E. 画图
        st.subheader("📈 贝叶斯后验分布图")
        # 注意：这里我们要稍微改一下 visual.py 或者直接在这里调用
        # 因为 Streamlit 画图需要显式调用 st.pyplot(fig)
        # 我们先试试直接调用，如果不显示，我再教你改 visual.py
        
        # 临时技巧：创建一个 figure 对象传给 st.pyplot
        plot_bayesian_distribution(conv_a, n_a, conv_b, n_b)
        st.pyplot(plt) # 把 matplotlib 的图贴到网页上
        # 在展示完结论后，加一个“想学更多吗？”的折叠块
        with st.expander("🤓 点击查看背后的数学原理 (Beta分布公式)"):
            st.markdown("""
            我们使用了 **贝叶斯推断** 来计算概率。核心公式如下：
            """)
            # Streamlit 支持 LaTeX 公式渲染！哪怕你不会写，看着也高大上
            st.latex(r'''
            P(\theta | Data) \propto P(Data | \theta) \times P(\theta)
            ''')
            st.write(f"""
            - **A组** 被模拟为一个 Beta 分布：$\\alpha={conv_a+1}, \\beta={n_a-conv_a+1}$
            - **B组** 被模拟为一个 Beta 分布：$\\alpha={conv_b+1}, \\beta={n_b-conv_b+1}$
            - 我们让这两个分布在后台“打架”了 10 万次，B组赢了 {prob:.1%} 的次数。
            """)