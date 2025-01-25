import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_heatmap(excel_path, shapefile_path, output_path):
    # 检查文件是否存在
    if not os.path.exists(excel_path):
        print(f"错误：Excel 文件不存在 - {excel_path}")
        return
    if not os.path.exists(shapefile_path):
        print(f"错误：Shapefile 文件不存在 - {shapefile_path}")
        return

    # 读取攻击数据
    try:
        df_country_attacks = pd.read_excel(excel_path)
        print("成功读取 Excel 文件。")
    except Exception as e:
        print(f"读取 Excel 文件失败: {e}")
        return

    # 检查必要的列是否存在
    if 'Country' not in df_country_attacks.columns or 'Suspected Attacks' not in df_country_attacks.columns:
        print("错误：Excel 文件中缺少 'Country' 或 'Suspected Attacks' 列。")
        return

    # 读取世界地图数据
    try:
        world = gpd.read_file(shapefile_path)
        print("成功读取 shapefile 文件。")
    except Exception as e:
        print(f"读取 shapefile 文件失败: {e}")
        return

    # 检查 shapefile 是否包含 'NAME' 列
    if 'NAME' not in world.columns:
        print("错误：shapefile 中缺少 'NAME' 列。")
        return

    # 重命名 'NAME' 列为 'Country' 以匹配攻击数据
    world = world.rename(columns={'NAME': 'Country'})

    # 合并地图数据和攻击数据
    merged = world.set_index('Country').join(df_country_attacks.set_index('Country'))
    print("成功合并地图数据和攻击数据。")

    # 处理缺失值：将没有攻击数据的国家设为 0
    merged['Suspected Attacks'] = merged['Suspected Attacks'].fillna(0)

    # 使用对数刻度，以更好地展示数据分布，避免极值影响
    merged['log_attack_count'] = np.log1p(merged['Suspected Attacks'])  # log1p: log(1 + x)

    # 设置颜色范围
    vmin = merged['log_attack_count'].min()  # 最小值
    vmax = merged['log_attack_count'].max()  # 最大值

    # 创建绘图
    fig, ax = plt.subplots(figsize=(20, 12))

    # 绘制热力图
    merged.plot(
        column='log_attack_count',
        cmap='coolwarm',  # 使用与第二段代码相同的颜色映射
        linewidth=0.8,
        edgecolor='0.8',
        legend=False,
        vmin=vmin,
        vmax=vmax,
        ax=ax
    )

    # 设置图标题
    ax.set_title('Distribution of Suspected Attacks', fontname='Times New Roman', fontsize=16, pad=20)

    # 去除轴
    ax.set_axis_off()

    # 创建颜色条
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])  # 仅用于颜色条，不需要实际数据

    # 添加颜色条并调整其大小和位置
    cbar = fig.colorbar(sm, ax=ax, fraction=0.02, pad=0.04)  # 与第二段代码中的设置一致
    cbar.set_label('Log(Suspected Attacks + 1)', fontsize=12, fontname='Times New Roman')

    # 保存热力图
    try:
        plt.savefig(output_path, dpi=1200, bbox_inches='tight')  # dpi 设置为 1200
        print(f"热力图已保存到 {output_path}")
    except Exception as e:
        print(f"保存热力图失败: {e}")
        return

    # 显示图像
    plt.show()

if __name__ == '__main__':
    # 定义文件路径
    excel_file = "./result/excel/suspected_countries.xlsx"
    shapefile = "./ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
    output_image = "./result/image/Crime_Suspected_distribution.pdf"

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_image), exist_ok=True)

    # 生成热力图
    generate_heatmap(excel_file, shapefile, output_image)