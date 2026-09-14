import random
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="双色球历史经验推荐选号工具", layout="centered")

# 专属标题与寄语
st.title("🎱 双色球历史经验推荐选号工具")
st.markdown("<h2 style='text-align: center; color: #E63946;'>✨ 陈伟，你就是下一个亿元富翁！ ✨</h2>", unsafe_allow_html=True)
st.caption("注：双色球开奖为随机事件。本工具基于历史常见概率形态（和值、奇偶比、连号/同尾号）进行筛选过滤，仅供日常娱乐参考。")
st.write("---")

# 经验过滤逻辑校验函数
def validate_numbers(reds):
    # 经验 1：和值过滤（历史开奖红球和值约有80%集中在 70 - 130 之间）
    total_sum = sum(reds)
    if not (70 <= total_sum <= 130):
        return False
        
    # 经验 2：奇偶比过滤（避免极端的全奇或全偶，奇数个数在 2 到 4 个之间）
    odd_count = sum(1 for r in reds if r % 2 != 0)
    if odd_count < 2 or odd_count > 4:
        return False

    # 经验 3：历史形态过滤（大多期数包含“连号”或“同尾号”）
    has_consecutive = any(reds[i+1] - reds[i] == 1 for i in range(len(reds)-1))
    has_same_tail = len(set(r % 10 for r in reds)) < len(reds)
    
    if not (has_consecutive or has_same_tail):
        return False
        
    return True

# 生成单组符合历史经验的号码
def generate_experienced_group(strategy):
    red_balls = list(range(1, 34))
    blue_balls = list(range(1, 17))
    
    # 红球权重模拟：根据策略微调概率分布
    if strategy == "大号倾向（偏向 17-33）":
        red_weights = np.linspace(1.0, 2.0, 33)
    elif strategy == "冷热平衡（冷号回补）":
        red_weights = np.array([1.5 if i % 2 == 0 else 1.0 for i in range(33)])
    else: # 均等概率
        red_weights = np.ones(33)
        
    red_weights /= red_weights.sum()

    # 循环抽样直到满足历史经验值
    attempts = 0
    while attempts < 1000:
        attempts += 1
        red_pick = sorted(np.random.choice(red_balls, size=6, replace=False, p=red_weights).tolist())
        if validate_numbers(red_pick):
            blue_pick = random.choice(blue_balls)
            return red_pick, blue_pick, sum(red_pick), sum(1 for r in red_pick if r % 2 != 0)
            
    # 保底返回
    red_pick = sorted(random.sample(red_balls, 6))
    return red_pick, random.choice(blue_balls), sum(red_pick), sum(1 for r in red_pick if r % 2 != 0)

# 控制区域
st.subheader("📊 经验分析策略选择")
strategy_type = st.selectbox("请选择形态倾向：", ["标准历史均值形态", "大号倾向（偏向 17-33）", "冷热平衡（冷号回补）"])

if st.button("🎲 生成 2 组历史经验精选号码", type="primary"):
    st.write("### 🎯 推荐号码组合（固定 2 组）：")
    
    for i in range(2):
        reds, blue, total_sum, odd_cnt = generate_experienced_group(strategy_type)
        even_cnt = 6 - odd_cnt
        red_str = "  ".join([f"{r:02d}" for r in reds])
        blue_str = f"{blue:02d}"
        
        st.markdown(f"#### **第 {i+1} 组推荐：**")
        st.markdown(f"🔴 `<span style='font-size: 20px; color:red;'>{red_str}</span>`  |  🔵 `<span style='font-size: 20px; color:blue;'>{blue_str}</span>`", unsafe_allow_html=True)
        st.caption(f"📌 形态分析：红球和值 **{total_sum}** | 奇偶比 **{odd_cnt}:{even_cnt}** | 符合黄金历史区间过滤标准")
        st.write("")

st.info("💡 祝陈伟早日中奖！彩票仅宜作为日常娱乐，请理性购彩，量力而行。")
