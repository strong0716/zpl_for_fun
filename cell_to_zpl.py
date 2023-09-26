import tkinter as tk
from tkinter import filedialog

def parse_custom_syntax(file_content):
    lines = file_content.split("\n")
    dimensions = lines[0].split("x")
    rows = int(dimensions[0])
    cols = int(dimensions[1])

    # 假設每個單元格的大小為100x100像素
    cell_width = 80
    cell_height = 80

    zpl_commands = []

    # 假設我們的標籤大小為4x6英寸，使用203 DPI的打印機
    zpl_commands.append("^XA")
    zpl_commands.append(f"^LL{rows * cell_height}")  # 標籤長度
    zpl_commands.append("^LH0,0")   # 標籤起始位置

    # 根據cell指令添加大格子和文字
    for line in lines[1:]:
        if "cell:" in line:
            parts = line.replace("cell:", "").strip().split("|")
            coordinates = parts[0].strip().split("-")
            start = coordinates[0].split(",")
            end = coordinates[1].split(",")
            start_row = int(start[0]) - 1
            start_col = int(start[1]) - 1
            end_row = int(end[0]) - 1
            end_col = int(end[1]) - 1
            
            # 畫上方邊框
            zpl_commands.append(f"^FO{start_col * cell_width},{start_row * cell_height}^GB{(end_col - start_col + 1) * cell_width},3,3^FS")
            # 畫左方邊框
            zpl_commands.append(f"^FO{start_col * cell_width},{start_row * cell_height}^GB3,{(end_row - start_row + 1) * cell_height},3^FS")
            # 畫下方邊框
            zpl_commands.append(f"^FO{start_col * cell_width},{(end_row + 1) * cell_height}^GB{(end_col - start_col + 1) * cell_width},3,3^FS")
            # 畫右方邊框
            zpl_commands.append(f"^FO{(end_col + 1) * cell_width},{start_row * cell_height}^GB3,{(end_row - start_row + 1) * cell_height},3^FS")

            # 如果有文字，則添加文字
            if len(parts) > 1 and "txt:" in parts[1]:
                text_parts = parts[1].split(" ")
                text = text_parts[1].strip().strip('"')
                xShift = 0
                yShift = 0
                if "xShift:" in line:
                    xShift = int(line.split("xShift:")[1].split()[0])
                if "yShift:" in line:
                    yShift = int(line.split("yShift:")[1].split()[0])
                
                text_x = start_col * cell_width + ((end_col - start_col + 1) * cell_width) // 2 + xShift
                text_y = start_row * cell_height + ((end_row - start_row + 1) * cell_height) // 2 + yShift
                zpl_commands.append(f"^FO{text_x},{text_y}^CI28^A0N,50,50^FD{text}^FS")  # ^CI28 是用於支持中文的指令

    zpl_commands.append("^XZ")
    
    return '\n'.join(zpl_commands)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隱藏主窗口
    input_file_path = filedialog.askopenfilename(title="選擇自定義語法檔案", filetypes=[("Text files", "*.txt")])
    
    if not input_file_path:
        print("未選擇檔案，程式結束。")
        exit()
    
    output_txt_path = input_file_path.replace(".txt", "_zpl.txt")
    
    with open(input_file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
    zpl_output = parse_custom_syntax(file_content)
    
    with open(output_txt_path, "w", encoding="utf-8") as file:
        file.write(zpl_output)
    
    print(f"ZPL output has been saved to {output_txt_path}")
