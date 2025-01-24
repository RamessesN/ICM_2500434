import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_country_attacks = pd.read_excel("./result/country_attack_statistics.xlsx")

# 加载世界地图数据
world = gpd.read_file("./ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")

# 合并攻击次数数据与世界地图数据
world = world.rename(columns={'NAME': 'Country'})  # 确保名称列与你的攻击次数数据的列名一致
merged = world.set_index('Country').join(df_country_attacks.set_index('Country'))

# 使用对数缩放
merged['log_attack_count'] = np.log1p(merged['Attack Count'])  # log1p 是为了处理零值

# 设定颜色范围
vmin = merged['log_attack_count'].min()  # 数据的最小值
vmax = merged['log_attack_count'].max()  # 数据的最大值

# 绘制世界热力图
fig, ax = plt.subplots(figsize=(20, 12))
merged.plot(column='log_attack_count', cmap='coolwarm', linewidth=0.8, edgecolor='0.8', legend=False, vmin=vmin, vmax=vmax, ax=ax)

# 调整标题
ax.set_title('Distribution Diagram', font='Times New Roman',fontsize=16)

# 调整颜色条的尺寸和位置
sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm.set_array([])

# 添加颜色条，并缩小尺寸
cbar = fig.colorbar(sm, ax=ax, fraction=0.02, pad=0.04)  # fraction 控制颜色条宽度，pad 控制间距

# 保存图像为高分辨率 PNG 文件
plt.savefig('./result/distribution_diagram.png', dpi=600)  # 提高 dpi 以增加分辨率

# 显示图像
plt.show()
