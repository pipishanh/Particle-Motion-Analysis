# Particle-Motion-Analysis
This repository work for a paper about micromotors.

使用前仔细阅读“#”后面的注释。

瞬时速度计算.py
通过每一时刻的坐标信息，计算每一时刻粒子们的平均速度。坐标信息由fiji获得，获得的坐标文件包含四列，分别是area，x，y，slice，注意删除文件中的第一行“area，x，y，slice”。

轨迹绘制.py
使用了海龟绘图体系。输入值为粒子显微图片与粒子坐标数据，fiji坐标与海龟坐标存在差异，注意坐标转换，你或许可以直接将坐标转换修改在代码里。输入的坐标信息包含三列，分别为number，x，y。

聚合分析粒子数无需处理原文件.py
通过坐标数据计算每一时刻聚集情况，坐标文件包含四列，分别是area，x，y，slice，注意不要删除文件中的第一行“area，x，y，slice”。
