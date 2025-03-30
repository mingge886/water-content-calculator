import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd  # 用于导出数据为 Excel

# 初始化序号
current_id = 1

def generate_data_and_calculate():
    # 随机生成 m3 (称量瓶空瓶重量)，范围 (40.0000, 60.0000)
    m3 = f"{random.uniform(40.0000, 60.0000):.4f}"
    
    # 随机生成 m0 (样品重量)，范围 (3.0001, 3.0089)
    m0 = f"{random.uniform(3.0001, 3.0089):.4f}"
    
    # 计算 m1 (称量瓶 + 样品重量)
    m1 = f"{(float(m3) + float(m0)):.4f}"
    
    # 确保 X ≤ 8%，计算 m2 的范围
    max_x = 8  # 最大水分百分比
    m2_min = float(m1) - (max_x / 100) * (float(m1) - float(m3))  # 根据公式反推 m2 的最小值
    m2 = f"{random.uniform(m2_min, float(m1)):.4f}"  # 随机生成 m2，范围 [m2_min, m1]
    
    # 计算水分 X(%)
    x = round(((float(m1) - float(m2)) / (float(m1) - float(m3))) * 100, 2)
    
    # 返回结果
    return {
        "编号": current_id,
        "m3 (空瓶重量)": m3,
        "m0 (样品重量)": m0,
        "m1 (空瓶+样品重量)": m1,
        "m2 (恒重后重量)": m2,
        "水分X(%)": x
    }

def on_generate(event=None):  # 支持按键绑定
    global current_id
    for _ in range(10):  # 一次生成 10 个数据
        result = generate_data_and_calculate()
        # 插入结果到表格，交替设置背景色
        tree.insert("", "end", values=(
            current_id,
            result["m3 (空瓶重量)"],
            result["m0 (样品重量)"],
            result["m1 (空瓶+样品重量)"],
            result["m2 (恒重后重量)"],
            result["水分X(%)"]
        ), tags=("evenrow" if current_id % 2 == 0 else "oddrow",))
        current_id += 1  # 序号递增

def calculate_average(event=None):  # 添加 event 参数以兼容按键事件
    try:
        # 获取输入框中的两个水分值
        value1 = float(entry1.get())
        value2 = float(entry2.get())
        # 计算平均值并保留一位小数
        average = round((value1 + value2) / 2, 1)
        # 显示结果
        average_label.config(text=f"平均修约值: {average}")
    except ValueError:
        average_label.config(text="请输入有效的数字！")

def on_tree_click(event):
    # 获取选中的行
    selected_item = tree.selection()
    if selected_item:
        # 获取水分X(%)列的值
        values = tree.item(selected_item, "values")
        if values:
            water_content = values[5]  # 水分X(%)在第6列
            # 将值粘贴到第一个输入框中
            entry1.delete(0, tk.END)
            entry1.insert(0, water_content)

def on_key_press(event):
    """监听键盘输入，将数字直接填入水分2的输入框"""
    char = event.char
    if char.isdigit() or char == ".":  # 允许输入数字和小数点
        entry2.insert(tk.END, char)
    elif event.keysym == "BackSpace":  # 支持退格键删除
        current_text = entry2.get()
        entry2.delete(0, tk.END)
        entry2.insert(0, current_text[:-1])

def export_to_excel():
    """将表格中的数据导出为 Excel 文件"""
    # 获取表格中的所有数据
    rows = tree.get_children()
    if not rows:
        messagebox.showwarning("警告", "表格中没有数据可导出！")
        return

    data = []
    for row in rows:
        data.append(tree.item(row)["values"])

    # 将数据转换为 DataFrame
    df = pd.DataFrame(data, columns=["编号", "m3 (空瓶重量)", "m0 (样品重量)", "m1 (空瓶+样品重量)", "m2 (恒重后重量)", "水分X(%)"])

    # 导出为 Excel 文件
    try:
        df.to_excel("导出数据.xlsx", index=False, engine="openpyxl")
        messagebox.showinfo("成功", "数据已成功导出为 '导出数据.xlsx'")
    except Exception as e:
        messagebox.showerror("错误", f"导出失败：{e}")

# 创建主窗口
root = tk.Tk()
root.title("水分计算器")
root.geometry("1000x700")  # 调整窗口大小，确保表格和输入框完全显示

# 创建顶部备注区域
top_frame = tk.Frame(root)
top_frame.pack(fill="x", pady=5)

# 添加左上角备注信息
left_remark = tk.Label(top_frame, text="本软件仅供内部测试使用，如若侵权请于24小时内删除", font=("Arial", 9), anchor="w")
left_remark.grid(row=0, column=0, sticky="w", padx=10)

left_remark2 = tk.Label(top_frame, text="本软件仅供内部测试使用，请勿用于商业用途", font=("Arial", 9), anchor="w")
left_remark2.grid(row=1, column=0, sticky="w", padx=10)

# 添加右上角备注信息
right_remark = tk.Label(top_frame, text="左键点击水分一栏可直接填入水分1框中", font=("Arial", 9), anchor="e")
right_remark.grid(row=0, column=1, sticky="e", padx=10)

right_remark2 = tk.Label(top_frame, text="本窗口中直接输入数字可填入水分2框中", font=("Arial", 9), anchor="e")
right_remark2.grid(row=1, column=1, sticky="e", padx=10)

# 配置列的动态扩展
top_frame.columnconfigure(0, weight=1)  # 左侧备注动态扩展
top_frame.columnconfigure(1, weight=1)  # 右侧备注动态扩展

# 创建按钮
generate_button = tk.Button(root, text="开始计算（Enter）", command=on_generate, font=("Arial", 14), width=20, height=2)
generate_button.pack(pady=5)

# 创建表格
columns = ("编号", "m3 (空瓶重量)", "m0 (样品重量)", "m1 (空瓶+样品重量)", "m2 (恒重后重量)", "水分X(%)")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

# 添加滚动条
scrollbar = tk.Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")

# 将滚动条绑定到表格
tree.configure(yscrollcommand=scrollbar.set)

# 设置表头
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)

# 添加条纹背景色
style = ttk.Style()
style.configure("Treeview", rowheight=25)  # 设置行高
style.map("Treeview", background=[("selected", "#ececec")])  # 选中行的背景色
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  # 表头字体
style.configure("Treeview", font=("Arial", 10))  # 表格字体
style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])  # 表格布局

# 插入表格到窗口
tree.pack(pady=5, fill="both", expand=True)

# 设置行的背景色（交替颜色）
tree.tag_configure("evenrow", background="#f0f0f0")  # 偶数行背景色
tree.tag_configure("oddrow", background="#ffffff")   # 奇数行背景色

# 绑定点击事件到表格
tree.bind("<ButtonRelease-1>", on_tree_click)

# 创建输入框和计算按钮
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="水分1:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry1 = tk.Entry(frame, font=("Arial", 12), width=10)
entry1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="水分2:", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)
entry2 = tk.Entry(frame, font=("Arial", 12), width=10)
entry2.grid(row=0, column=3, padx=5, pady=5)

calculate_button = tk.Button(frame, text="计算平均修约值（空格）", command=calculate_average, font=("Arial", 14), width=20, height=2)
calculate_button.grid(row=0, column=4, padx=10, pady=5)

# 添加导出按钮
export_button = tk.Button(root, text="导出数据为Excel", command=export_to_excel, font=("Arial", 14), width=20, height=2)
export_button.pack(pady=10)

# 显示平均值结果
average_label = tk.Label(root, text="平均修约值: ", font=("Arial", 14), fg="blue")
average_label.pack(pady=10)

# 添加右下角水印
watermark = tk.Label(root, text="Github@mingge886", font=("Arial", 8), fg="gray", anchor="se")
watermark.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

# 绑定 Enter 键到生成函数
root.bind("<Return>", on_generate)

# 绑定空格键到计算平均值函数
root.bind("<space>", calculate_average)

# 绑定键盘输入到水分2输入框
root.bind("<Key>", on_key_press)

if __name__ == "__main__":
    # 运行主循环
    root.mainloop()
