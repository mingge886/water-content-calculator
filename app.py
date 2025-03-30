import random
import pandas as pd
import streamlit as st

# 初始化数据存储
data = []

# 随机生成数据的函数
def generate_data_and_calculate():
    # 随机生成 m3 (称量瓶空瓶重量)，范围 (40.0000, 60.0000)
    m3 = round(random.uniform(40.0000, 60.0000), 4)
    
    # 随机生成 m0 (样品重量)，范围 (3.0001, 3.0089)
    m0 = round(random.uniform(3.0001, 3.0089), 4)
    
    # 计算 m1 (称量瓶 + 样品重量)
    m1 = round(m3 + m0, 4)
    
    # 确保 X ≤ 8%，计算 m2 的范围
    max_x = 8  # 最大水分百分比
    m2_min = m1 - (max_x / 100) * (m1 - m3)  # 根据公式反推 m2 的最小值
    m2 = round(random.uniform(m2_min, m1), 4)  # 随机生成 m2，范围 [m2_min, m1]
    
    # 计算水分 X(%)
    x = round(((m1 - m2) / (m1 - m3)) * 100, 2)
    
    # 返回结果
    return {
        "m3 (空瓶重量)": m3,
        "m0 (样品重量)": m0,
        "m1 (空瓶+样品重量)": m1,
        "m2 (恒重后重量)": m2,
        "水分X(%)": x
    }

# Streamlit 页面标题
st.title("水分计算器")

# 生成数据按钮
if st.button("生成数据"):
    for _ in range(10):  # 一次生成 10 个数据
        data.append(generate_data_and_calculate())

# 显示数据表格
if data:
    df = pd.DataFrame(data)
    st.dataframe(df)

    # 导出数据为 Excel
    st.download_button(
        label="导出数据为 Excel",
        data=df.to_excel(index=False, engine="openpyxl"),
        file_name="导出数据.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# 计算平均值
st.subheader("计算水分平均值")
value1 = st.number_input("输入水分值1", min_value=0.0, format="%.2f")
value2 = st.number_input("输入水分值2", min_value=0.0, format="%.2f")

if st.button("计算平均值"):
    average = round((value1 + value2) / 2, 1)
    st.success(f"平均修约值: {average}")