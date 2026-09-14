import random
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="多彩种历史经验推荐工具", layout="centered")

# 专属标题与寄语
st.title("🎰 多彩种历史经验推荐工具")
st.markdown("<h2 style='text-align: center; color: #E63946;'>✨ 陈伟，你就是下一个亿元富翁！ ✨</h2>", unsafe_allow_html=True)
st.caption("注：开奖事件均为独立随机事件。本工具基于历史常见概率形态（和值、奇偶比、连号/同尾号）进行筛选过滤，仅供日常娱乐参考。")
st.write("---")

# ----------------- 经验过滤校验逻辑 -----------------
def validate_numbers(reds, min_sum, max_sum):
    total_sum = sum(reds)
    if not (min_sum <= total_sum <= max_sum):
        return False
        
    odd_count = sum(1 for r in reds if r % 2 != 0)
    min_odd = max(1, len(reds) // 3)
    max_odd = len(reds) - min_odd
    if odd_count < min_odd or odd_count > max_odd:
        return False

    has_consecutive = any(reds[i+1] - reds[i] == 1 for i in range(len(reds)-1))
    has_same_tail = len(set(r % 10 for r in reds)) < len(reds)
    
    if not (has_consecutive or has_same_tail):
        return False
        
    return True

# ----------------- 算法生成核心逻辑 -----------------
def generate_game_numbers(game_type, strategy):
    if game_type == "双色球":
        total_reds, pick_reds = 33, 6
        total_blues, pick_blues = 16, 1
        min_sum, max_sum = 70, 130
    elif game_type == "大乐透":
        total_reds, pick_reds = 35, 5
        total_blues, pick_blues = 12, 2
        min_sum, max_sum = 65, 125
    elif game_type == "快乐8 (选十)":
        total_reds, pick_reds = 80, 10
        total_blues, pick_blues = 0, 0
        min_sum, max_sum = 330, 480
    elif game_type == "买马/赛马 (精选马匹组合)":
        # 模拟 1~14 号马匹中精选 2 匹连胜/位置组合 (Q/QP)
        total_reds, pick_reds = 14, 2
        total_blues, pick_blues = 0, 0
        min_sum, max_sum = 5, 25

    red_balls = list(range(1, total_reds + 1))
    
    if strategy == "偏向大号":
        red_weights = np.linspace(1.0, 2.0, total_reds)
    elif strategy == "冷热平衡":
        red_weights = np.array([1.5 if i % 2 == 0 else 1.0 for i in range(total_reds)])
    else:
        red_weights = np.ones(total_reds)
    red_weights /= red_weights.sum()

    attempts = 0
    while attempts < 1000:
        attempts += 1
        red_pick = sorted(np.random.choice(red_balls, size=pick_reds, replace=False, p=red_weights).tolist())
        
        # 赛马等特殊玩法跳过复杂校验，普通彩票进行形态校验
        if game_type in ["买马/赛马 (精选马匹组合)"] or validate_numbers(red_pick, min_sum, max_sum):
            blue_pick = sorted(random.sample(range(1, total_blues + 1), pick_blues)) if pick_blues > 0 else []
            return red_pick, blue_pick, sum(red_pick), sum(1 for r in red_pick if r % 2 != 0)
            
    # 保底生成
    red_pick = sorted(random.sample(red_balls, pick_reds))
    blue_pick = sorted(random.sample(range(1, total_blues + 1), pick_blues)) if pick_blues > 0 else []
    return red_pick, blue_pick, sum(red_pick), sum(1 for r in red_pick if r % 2 != 0)

# ----------------- UI 界面控制 -----------------
st.subheader("🎯 请选择彩种与策略")
col1, col2 = st.columns(2)

with col1:
    game_choice = st.selectbox("选择游戏类型：", ["双色球", "大乐透", "快乐8 (选十)", "买马/赛马 (精选马匹组合)"])

with col2:
    strategy_choice = st.selectbox("选择形态倾向：", ["标准历史均值形态", "偏向大号", "冷热平衡"])

if st.button(f"🎲 生成 2 组【{game_choice}】经验精选组合", type="primary"):
    st.write("### 推荐组合列表（固定 2 组）：")
    
    for i in range(2):
        reds, blues, total_sum, odd_cnt = generate_game_numbers(game_choice, strategy_choice)
        even_cnt = len(reds) - odd_cnt
        
        red_str = "  ".join([f"{r:02d}" for r in reds])
        blue_str = "  ".join([f"{b:02d}" for b in blues]) if blues else ""
        
        st.markdown(f"#### **第 {i+1} 组推荐：**")
        
        if game_choice == "买马/赛马 (精选马匹组合)":
            st.markdown(f"🏇 **精选马匹序号：** `<span style='font-size: 22px; color:darkgreen; font-weight:bold;'>{red_str} 号马</span>`", unsafe_allow_html=True)
            st.caption("📌 玩法建议：可用于参考投注 连赢 (Q) 或 位置 Q (QP) 组合")
        else:
            display_html = f"🔴 `<span style='font-size: 19px; color:red;'>{red_str}</span>`"
            if blue_str:
                display_html += f"  |  🔵 `<span style='font-size: 19px; color:blue;'>{blue_str}</span>`"
            st.markdown(display_html, unsafe_allow_html=True)
            st.caption(f"📌 形态分析：和值 **{total_sum}** | 奇偶比 **{odd_cnt}:{even_cnt}** | 符合历史经验黄金过滤标准")
            
        st.write("")

st.info("💡 祝陈伟早日中奖！彩票仅宜作为日常娱乐，请理性购彩，量力而行。")
