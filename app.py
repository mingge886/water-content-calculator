import random
import pandas as pd
import streamlit as st
import io  # 用于创建字节流对象

# 初始化 Streamlit 页面标题
st.title("水分计算器")

# 初始化数据存储和序号
if "data" not in st.session_state:
    st.session_state.data = []  # 用于存储生成的数据
if "current_id" not in st.session_state:
    st.session_state.current_id = 1  # 序号从 1 开始

# 随机生成数据的函数
def generate_data_and_calculate(current_id):
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
        "编号": current_id,
        "m3 (空瓶重量)": m3,
        "m0 (样品重量)": m0,
        "m1 (空瓶+样品重量)": m1,
        "m2 (恒重后重量)": m2,
        "水分X(%)": x
    }

# 生成数据的函数
def generate_data():
    for _ in range(10):  # 一次生成 10 个数据
        st.session_state.data.append(generate_data_and_calculate(st.session_state.current_id))
        st.session_state.current_id += 1  # 序号递增

# 计算平均值的函数
def calculate_average(value1, value2):
    return round((value1 + value2) / 2, 1)

# 嵌入 JavaScript 监听快捷键
st.markdown("""
    <script>
    document.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            // 模拟点击生成数据按钮
            const generateButton = window.parent.document.querySelector('button[aria-label="生成数据"]');
            if (generateButton) generateButton.click();
        } else if (event.key === " ") {
            // 模拟点击计算平均值按钮
            const calculateButton = window.parent.document.querySelector('button[aria-label="计算平均值"]');
            if (calculateButton) calculateButton.click();
        }
    });
    </script>
""", unsafe_allow_html=True)

# 生成数据按钮
if st.button("生成数据", key="generate"):
    generate_data()

# 显示数据表格
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df, use_container_width=True)

    # 创建字节流对象
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    # 使用字节流对象作为下载数据
    st.download_button(
        label="导出数据为 Excel",
        data=output,
        file_name="导出数据.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# 输入框和计算平均值
st.subheader("计算平均值")
value1 = st.number_input("水分值1", min_value=0.0, format="%.2f")
value2 = st.number_input("水分值2", min_value=0.0, format="%.2f")

if st.button("计算平均值", key="calculate"):
    average = calculate_average(value1, value2)
    st.success(f"平均修约值: {average}")
