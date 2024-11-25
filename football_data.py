import requests
from lxml import etree
import pandas as pd
import matplotlib.pyplot as plt

url = f'https://www.transfermarkt.com/manchester-city/leistungsdaten/verein/281/plus/1?reldata=%262023'
myheader = {'user-agent': 'Chrome'}
response = requests.get(url, headers=myheader)
# response.encoding = 'utf-8'
html = response.content
tree = etree.HTML(html)

players = tree.xpath('//tbody/tr')

# 提取数据
player_data = []
for player in players:
    # 提取球员名字
    name = player.xpath('.//img/@title')
    name = name[0] if name else None

    # 提取 PPG
    ppg = player.xpath('.//td[contains(@class, "cp")]/text()')
    ppg = ppg[0] if ppg else None
    ppg = eval(str(ppg))
    # 去掉未出场的球员
    if ppg == 0:
        continue

    # 提取出场时间
    playing_time = player.xpath('.//td[contains(@class, "rechts")]/text()')
    playing_time = playing_time[0].replace('.', '').strip("'") if playing_time else None
    playing_time = eval(str(playing_time))

    # 如果 PPG 或出场时间缺失，跳过该球员
    if name and ppg and playing_time:
        player_data.append({
            "name": name,
            "PPG": ppg,
            "playing_time": playing_time
        })

# 将数据存储到 DataFrame
df = pd.DataFrame(player_data)

# 添加 "Matches" 列，出场时间除以 90，保留两位小数
df['Matches'] = (df['playing_time'] / 90).round(2)

# 输出结果
print(df)

# 绘制散点图
plt.figure(figsize=(8, 6))
plt.scatter(df['Matches'], df['PPG'], color='blue', label='Player Data')

# 添加球员名字标注
for i, row in df.iterrows():
    plt.text(row['Matches'], row['PPG'], row['name'], fontsize=9, ha='right', va='bottom')

# 添加分割线
split_x = 30
split_y = 2.37
plt.axhline(y=split_y, color='red', linestyle='--', linewidth=1.5, label='PPG Split (2.13)')
plt.axvline(x=split_x, color='green', linestyle='--', linewidth=1.5, label='Matches Split (30)')

# 设置标题和标签
plt.title("Scatter Plot with Player Names and Splitting Lines", fontsize=14)
plt.xlabel("Matches (Games Played)", fontsize=12)
plt.ylabel("PPG (Points Per Game)", fontsize=12)

# 添加网格
plt.grid(alpha=0.3)

# 添加图例
plt.legend()

# 显示图形
plt.show()
