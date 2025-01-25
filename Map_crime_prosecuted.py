import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df_country_attacks = pd.read_excel("./result/excel/country_attack_statistics.xlsx")

# Load the world map data
world = gpd.read_file("./ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")

# Merge the number of attacks data with the world map data
world = world.rename(columns={'NAME': 'Country'})  # Ensure the 'Country' column matches the one in your attack data
merged = world.set_index('Country').join(df_country_attacks.set_index('Country'))

# Use logarithmic scaling
merged['log_prosecuted'] = np.log1p(merged['prosecuted'])  # log1p to handle zero values

# Setting the color range
vmin = merged['log_prosecuted'].min()
vmax = merged['log_prosecuted'].max()

# Create the plot
fig, ax = plt.subplots(figsize=(20, 12))
merged.plot(column='log_prosecuted', cmap='coolwarm', linewidth=0.8, edgecolor='0.8', legend=False, vmin=vmin, vmax=vmax, ax=ax)

# Add title
ax.set_title('Where are Cybercrimes Prosecuted?', font='Times New Roman', fontsize=16)

# Adjust the size and position of color bar
sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm.set_array([])

# Add color bar
cbar = fig.colorbar(sm, ax=ax, fraction=0.02, pad=0.04)  # fraction: bar width; pad: regular

# Save the image with high resolution
plt.savefig('./result/image/Crime_prosecuted_distribution.png', dpi=600)  # increase the dpi
plt.show()