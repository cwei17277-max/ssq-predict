import random
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="双色球数据分析与随机选号", layout="centered")

st.title("🎱 双色球选号与概率辅助工具")
st.caption("注：双色球为独立随机事件，本工具仅供娱乐与统计分析参考。")

# 1. 模拟或导入历史统计权重（实际使用中可从网络爬取历史数据）
st.subheader("📊 历史冷热度偏好设置")
strategy = st.radio("选择选号策略：", ["完全随机（机选）", "热号优先（加权抽取）", "冷号防漏（逆向抽取）"])

def generate_numbers(strategy_type):
    red_balls = list(range(1, 34))
    blue_balls = list(range(1, 17))
    
    if strategy_type == "完全随机（机选）":
        red_pick = sorted(random.sample(red_balls, 6))
        blue_pick = random.choice(blue_balls)
    else:
        # 为不同策略赋予简易权重数组
        if strategy_type == "热号优先（加权抽取）":
            red_weights = np.linspace(1, 2, 33) # 模拟热号权重高
        else:
            red_weights = np.linspace(2, 1, 33) # 模拟冷号权重高
            
        red_weights /= red_weights.sum()
        
        # 无放回加权抽样
        red_pick = sorted(np.random.choice(red_balls, size=6, replace=False, p=red_weights).tolist())
        blue_pick = random.choice(blue_balls)
        
    return red_pick, blue_pick

# 2. 交互控制区域
num_groups = st.slider("生成注数：", min_value=1, max_value=10, value=5)

if st.button("🎲 立即生成下一期预测号码", type="primary"):
    st.write("### 推荐号码组合：")
    for i in range(num_groups):
        reds, blue = generate_numbers(strategy)
        red_str = "  ".join([f"{r:02d}" for r in reds])
        blue_str = f"{blue:02d}"
        
        st.markdown(f"**第 {i+1} 注：** 🔴 `<span style='color:red;'>{red_str}</span>`  |  🔵 `<span style='color:blue;'>{blue_str}</span>`", unsafe_allow_html=True)

st.info("💡 建议：彩票仅宜作为日常娱乐，请理性购彩，量力而行。")
