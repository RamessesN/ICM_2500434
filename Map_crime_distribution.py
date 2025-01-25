import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_country_attacks = pd.read_excel("./result/excel/country_attack_statistics.xlsx")

# Load the world map data
world = gpd.read_file("./ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")

# Merge the number of attacks data with the world map data
world = world.rename(columns={'NAME': 'Country'})  # Make sure the name column matches the column name of your attack count data
merged = world.set_index('Country').join(df_country_attacks.set_index('Country'))

# Use logarithmic scaling
merged['log_attack_count'] = np.log1p(merged['Attack Count'])  # log1p: handle zero values

# Setting the color range
vmin = merged['log_attack_count'].min()  # Min
vmax = merged['log_attack_count'].max()  # Max

# Draw
fig, ax = plt.subplots(figsize=(20, 12))
merged.plot(column='log_attack_count', cmap='coolwarm', linewidth=0.8, edgecolor='0.8', legend=False, vmin=vmin, vmax=vmax, ax=ax)

# Name
ax.set_title('Distribution Diagram', font='Times New Roman',fontsize=16)

# Adjust the size and position of color bar
sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm.set_array([])

# Add color bar and decrease its size
cbar = fig.colorbar(sm, ax=ax, fraction=0.02, pad=0.04)  # fraction: bar width; pad: regular

# Adjust the resolution
plt.savefig('./result/image/Crime_distribution.pdf', dpi=1200)  # increase the dpi
plt.show()