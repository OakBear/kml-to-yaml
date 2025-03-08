import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import xml.etree.ElementTree as ET
import yaml

def extract_waypoints_from_kml(kml_file):
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    tree = ET.parse(kml_file)
    root = tree.getroot()
    waypoints = []
    
    for placemark in root.findall('.//kml:Placemark', ns):
        description = placemark.find('.//kml:description', ns)
        if description is None:
            continue
        if "Waypoint" in description.text:
            coords = placemark.find('.//kml:coordinates', ns)
            if coords is not None and coords.text:
                lon, lat, _ = coords.text.strip().split(',')
                waypoints.append([float(lon), float(lat)])
    
    return waypoints

def generate_yaml(waypoints, output_file):
    yaml_data = {"points": waypoints}
    with open(output_file, 'w') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True, indent=2)

def on_drop(event):
    kml_file = event.data.strip('{}')  # 去除拖入路径的额外符号
    if not os.path.exists(kml_file):
        status_label.config(text=f"错误：文件 {kml_file} 不存在！")
        return
    
    waypoints = extract_waypoints_from_kml(kml_file)
    output_yaml = os.path.splitext(kml_file)[0] + ".yaml"
    generate_yaml(waypoints, output_yaml)
    status_label.config(text=f"成功提取 {len(waypoints)} 个航点，已保存到 {output_yaml}")

# 创建 GUI 窗口
root = TkinterDnD.Tk()
root.title("KML 转 YAML")
root.geometry("800x600")

# 拖入文件区域
drop_label = tk.Label(root, text="将 KML 文件拖到此处", font=("Arial", 12))
drop_label.pack(pady=20)

# 状态标签
status_label = tk.Label(root, text="", fg="green")
status_label.pack()

# 绑定拖入事件
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# 运行主循环
root.mainloop()