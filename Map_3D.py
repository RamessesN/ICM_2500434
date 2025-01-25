import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate

# 数据预处理（保持不变）
data = {
    "Group": ["T1", "T2", "T3", "T4", "T5"],
    "2000": [0, 0, 0.120697917, 0, 0],
    "2001": [0.159507008, 0, 0, 0, 0],
    "2002": [0.12642716, 0, 0.941951584, 0, 0],
    "2003": [0.313362996, 0.035589772, 0.117048535, 0.035965791, 0],
    "2004": [0.644615276, 0, 0.115962494, 0, 0],
    "2005": [0.522967086, 0, 1.062607599, 0, 0],
    "2006": [0.548416154, 0.035551915, 0.494887275, 0, 0],
    "2007": [3.428544177, 1.064771371, 1.683906586, 0.876865312, 0],
    "2008": [3.351853657, 1.93932045, 0.445594551, 0.439896234, 0],
    "2009": [5.355474442, 0.039207315, 0.391004707, 1.721611911, 0],
    "2010": [17.38581184, 0.869858191, 2.758802117, 0, 0.356522116],
    "2011": [18.76544601, 0.557625729, 2.610603378, 3.537230029, 0],
    "2012": [59.94710853, 27.33386331, 29.77140348, 27.9659637, 22.48535458],
    "2013": [74.37465094, 49.9415854, 44.20840943, 39.06114736, 86.77309334],
    "2014": [39.80707911, 4.478437906, 18.71267909, 9.632312906, 2.637024726],
    "2015": [39.79380865, 2.902315595, 15.69309786, 19.10725081, 0],
    "2016": [37.71189188, 5.478667813, 19.19998226, 12.81697862, 54.48612141],
    "2017": [25.59824321, 4.77584506, 18.94799, 6.348182758, 12.30236599],
    "2018": [18.09635724, 0.326384641, 8.132209924, 4.911298215, 0.857757535],
    "2019": [16.29880573, 2.435899072, 12.98675595, 3.220256474, 0.278412044],
    "2020": [15.57610523, 9.905240931, 15.26117815, 3.859736243, 0.517428861],
    "2021": [5.610295779, 2.274530682, 8.551070492, 2.443728751, 0],
    "2022": [2.800464975, 1.083298965, 2.389171609, 0.909276148, 0.104869513],
    "2023": [25.72137524, 0.112675182, 4.942695489, 0.89749961, 0]
}

df = pd.DataFrame(data).set_index("Group")
df = df.T.reset_index().rename(columns={"index": "Year"})
df["Year"] = df["Year"].astype(int)
long_df = df.melt(id_vars="Year", var_name="Tier", value_name="Value").fillna(0)
pivot_df = long_df.pivot(index="Year", columns="Tier", values="Value")

# 插值处理
years = pivot_df.index.values
tiers = np.arange(1, 6)
interp_years = np.linspace(2000, 2023, 100)
Y_new, X_new = np.meshgrid(tiers, interp_years)

Z_interp = np.zeros_like(X_new)
for i, tier in enumerate(tiers):
    f = interpolate.interp1d(years, pivot_df.values[:,i], kind='cubic', fill_value="extrapolate")
    Z_interp[:,i] = f(interp_years)

# 创建图形
fig = plt.figure(figsize=(20, 14))
ax = fig.add_subplot(111, projection='3d')

plt.subplots_adjust(
    left=0.55,    # 左边距从5%增加到8%
    right=0.82,   # 右边距减少到82%（为颜色条留出18%空间）
    bottom=0.3,  # 底边距增加到12%
    top=0.92      # 顶边距减少到92%
)

# 关键参数：间距设置
data_max = np.nanmax(Z_interp)
spacing = data_max * 0.9  # 间距为数据最大值的15%

# 主曲面参数
cmap = cm.coolwarm
norm = plt.Normalize(0, data_max)

# 绘制3D曲面
surf = ax.plot_surface(
    X_new, Y_new, Z_interp,
    cmap=cmap,
    norm=norm,
    rstride=2,
    cstride=1,
    edgecolor='none',
    alpha=0.9,
    shade=True
)

# 关键修改：下移投影层
projection = ax.contourf(
    X_new, Y_new, Z_interp,
    zdir='z',
    offset=-spacing,  # 下移间距
    cmap=cmap,
    norm=norm,
    levels=50,
    alpha=0.8
)

# 坐标轴设置（扩展z轴范围）
year_ticks = list(range(2000, 2024, 4))
ax.set(
    xlabel='Year',
    ylabel='Tier',
    zlabel='Value',
    xlim=(2000, 2023),
    ylim=(1, 5),
    zlim=(-spacing, data_max*1.2),  # 扩展z轴下限
    yticks=range(1, 6),
    yticklabels=['T1', 'T2', 'T3', 'T4', 'T5'],
    xticks=year_ticks,
    xticklabels=[str(y) for y in year_ticks]
)

# 颜色条设置
cbar = fig.colorbar(surf, ax=ax, pad=0.15, shrink=0.3)
cbar.set_ticks(np.linspace(0, data_max, 6))

# 视角与标注优化
ax.view_init(elev=15, azim=-65)  # 增加俯视角

# 添加投影平面网格
ax.plot_wireframe(X_new, Y_new, np.full_like(Z_interp, -spacing), color='gray', linewidth=0.3, alpha=0.3)

# 导出设置
plt.savefig("./result/image/3D_heatmap.pdf", format='pdf', dpi=1200, bbox_inches='tight', facecolor='white')
plt.close()